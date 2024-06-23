from brel import Filing, utils

from sec_edgar_api import EdgarClient
import pandas as pd
import json

import requests
from io import BytesIO

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# this gets the statements within the filing, for each filing url
def get_df_statements(url):
    # Headers for authorization
    headers = {
        'User-Agent': 'bear.grills@gmail.com'  # Replace with your actual authorization header
    }

    # Fetch the content using requests
    response = requests.get(url, headers=headers)
    # Check if the request was successful
    # try:
    if True:
        if response.status_code == 200:
            # Read the content into a BytesIO object
            file_content = response.content
            
            # Create an ExcelFile object
            xls = pd.ExcelFile(file_content)
            
            # Get the list of sheet names
            sheet_names = xls.sheet_names
            # print(f"Sheet names: {sheet_names}")
            
            # Read each sheet into a DataFrame, combining row 1 and row 2 for header
            listofdicts = []
 
            for sheet_name in sheet_names:
                # Read the first two rows to get the header
                df = pd.read_excel(xls, sheet_name, header=None, nrows=2)
                
                # remove columns with Null headers 
                columns_to_drop = []
                for column in df.columns:
                    dropme_huh = pd.isna(df[column].iloc[1]) and pd.isna(df[column].iloc[0])
                    columns_to_drop.append(dropme_huh)

                # Combine row 1 and row 2 to create the header
                new_columns = [str(df.iloc[0, col]) + ' ' + str(df.iloc[1, col]) for col in range(len(df.columns))]
                
                # Read the rest of the data skipping the first two rows
                df = pd.read_excel(xls, sheet_name, header=2)
                
                # Assign the combined header to the DataFrame
                df.columns = new_columns

                # now remove the null column
                filtered_columns = df.columns[columns_to_drop]
                df = df.drop(columns=filtered_columns)
                            

                # postprocessing
                if True: 
                    save_A1 = df.columns[0] 
                    save_A2 = df.columns[1]
                    df = df[[save_A1, save_A2]] # just this column

                    # rename this column
                    new_column_name = str(save_A1)+" "+str(save_A2)
                    # df[new_column_name] = df[save_A2] 
                    # df = df.drop(columns=[save_A2])
                    df = df.rename(columns={save_A2:new_column_name})
                    df = df.rename(columns={save_A1:"Concept"})
                    

                # Store the DataFrame in the dictionary
                adict = {"Name":sheet_name,"Internal Name":save_A1,"df_table":df}
                listofdicts.append(adict)

                # print(f"DataFrame for {sheet_name}:")
                # display(dfs[sheet_name])

            df_statements = pd.DataFrame(listofdicts)
            return df_statements
                    
        else:
            print(f"Failed to fetch the file. Status code: {response.status_code}")
    # except Exception as e:
    #     return e




# this section defines a company and pulls the information needed from the sec
def search_cik(companySearchName):
    response = requests.get(f"https://financialmodelingprep.com/api/v3/cik-search/{companySearchName}?apikey=fefd111730a97a24b6caeaea4c8fac8a")
    search_results = response.json()
    return search_results


class Company(object): 
    def __init__(self,cik_or_searchterm,num_filings,isin=["10-K","10-Q"],search=True) -> None:
        if search:
            self.search_results = search_cik(cik_or_searchterm)
            if len(self.search_results) == 0: 
                raise Exception("No search results")
            print(self.search_results[0])
            self.cik = self.search_results[0]['cik']
        else: 
            self.cik = cik_or_searchterm
        
        self.isin = isin
        self.num_filings = num_filings

        self._store_all_filings() # this stores it in self.df_filings


    def __str__(self):
        return "<Company>"+json.dumps(self.company_information, indent=4)

    # this function gets all the options for the filings from the SEC
    def _store_all_filings(self):

        K10=True
        Q10=True

        edgar = EdgarClient(user_agent="SampleCompany bear.grills@gmail.com")
        submissions = edgar.get_submissions(cik=self.cik)

        # pull company information
        keys_to_include = ["name","tickers","sic","sicDescription","description","exchanges"]
        # print(submissions.keys())
        self.company_information = {key: submissions[key] for key in keys_to_include if key in submissions}

        # create information for 
        df = pd.DataFrame(submissions['filings']['recent'])
        df = df[df['form'].isin(self.isin)] # filters to important forms 
        df = df[df['isXBRL']==1] # filters to just xbrl 

        # df = df[["reportDate","form"]]
        df["cik"] = self.cik
        
        # create urls 
        df['InteractiveURL'] = df['accessionNumber'].apply(lambda report_id: f"https://www.sec.gov/Archives/edgar/data/{self.cik}/{report_id.replace('-', '')}/{report_id}-index.htm")
        df['ExcelURL'] = df['accessionNumber'].apply(lambda report_id: f"https://www.sec.gov/Archives/edgar/data/{self.cik}/{report_id.replace('-', '')}/Financial_Report.xlsx")
        
        # filtering operations
        if not Q10:
            df = df[df["form"] != "10-Q"]
        if not K10:
            df = df[df["form"] != "10-K"]
        df = df.head(self.num_filings)

        if df.empty:
            raise KeyError("df is empty, check filtering maybe? ")

        # tODO: only get the excel sheets for the top 3 statements
        # limit = 3
        df['df_statements'] = df['ExcelURL'].apply(lambda url: get_df_statements(url))
        # df.loc[:limit-1, 'Statements'] = df.loc[:limit-1, 'ExcelURL'].apply(lambda url: get_statements(url))

        # save the form, cik, reportDate in the Filing object
        # df = df.apply(lambda row: row["Filing"])

        self.df_filings = df

if __name__ == "__main__":

    COMPANY = Company("Costco", 5)

    COMPANY.df_filings.to_csv("output.csv")

    print(COMPANY.df_filings)

    print(COMPANY.df_filings.iloc[0]["df_statements"])

    print(COMPANY.df_filings.iloc[0]["df_statements"].iloc[1]["df"])
