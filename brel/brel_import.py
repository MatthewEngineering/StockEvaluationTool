from brel import Filing, utils

from sec_edgar_api import EdgarClient
import pandas as pd
import json

import requests

def search_cik(companySearchName):
    response = requests.get(f"https://financialmodelingprep.com/api/v3/cik-search/{companySearchName}?apikey=fefd111730a97a24b6caeaea4c8fac8a")
    search_results = response.json()
    return search_results


class Company(object): 
    def __init__(self,cik_or_searchterm,num_filings,search=True) -> None:
        if search:
            self.search_results = search_cik(cik_or_searchterm)
            if len(self.search_results) == 0: 
                raise Exception("No search results")
            print(self.search_results[0])
            self.cik = self.search_results[0]['cik']
        else:        
            self.cik = cik_or_searchterm

        self.num_filings = num_filings

        self._store_all_filings() # this stores it in self.df_filings


    def __str__(self):
        return "<Company>"+json.dumps(self.company_information, indent=4)
        # return self.company_information


    # this function gets all the options for the filings from the SEC
    def _sec_filing_cursory_info(self):
        edgar = EdgarClient(user_agent="SampleCompany bear.grills@gmail.com")
        submissions = edgar.get_submissions(cik=self.cik)

        # pull company information
        keys_to_include = ["name","tickers","sic","sicDescription","description","exchanges"]
        # print(submissions.keys())
        self.company_information = {key: submissions[key] for key in keys_to_include if key in submissions}
        

        # create information for 
        df = pd.DataFrame(submissions['filings']['recent'])
        df = df[df['form'].isin(["10-K","10-Q"])] # filters to important forms 
        df = df[df['isXBRL']==1] # filters to just xbrl 
        # dates = df['reportDate']
        # print(dates)

        df = df[["reportDate","form"]]
        df["cik"] = self.cik
        
        return df

        #       reportDate  form     cik
        # 6     2024-03-30  10-Q  320193
        # 51    2023-12-30  10-Q  320193
        # 64    2023-09-30  10-K  320193
        # 84    2023-07-01  10-Q  320193
        # 93    2023-04-01  10-Q  320193
        # 132   2022-12-31  10-Q  320193

    # this function gets the filing options and creates the Filing object from brel 
    def _store_all_filings(self,K10=True,Q10=True):        
        ### Changed to make this work   C:\Users\matth\AppData\Local\Programs\Python\Python312\Lib\site-packages\brel\utils\edgar.py
        ### Changed to make this work   C:\Users\matth\AppData\Local\Programs\Python\Python312\Lib\site-packages\brel\parsers\dts\xml_file_manager.py
        ### get request headers to: headers={"User-Agent": "bear.grills@gmail.com"}

        df = self._sec_filing_cursory_info()
        print(df)

        # filtering operations
        if not Q10:
            df = df[df["form"] != "10-Q"]
        if not K10:
            df = df[df["form"] != "10-K"]
        df = df.head(self.num_filings)

        print(df)

        if df.empty:
            raise KeyError("df is empty, check filtering maybe? ")


        # instantiate the filing object
        df['Filing'] = df.apply(lambda row: utils.open_edgar(row['cik'], row['form'], row['reportDate']), axis=1)
        
        # save the form, cik, reportDate in the Filing object
        # df = df.apply(lambda row: row["Filing"])

        self.df_filings = df
        # filing = utils.open_edgar(cik="320193", filing_type="10-Q", date="2023-12-30") # date is date of submission 
        # print(filing)


if __name__ == "__main__":

    a = Company("MasterCard", 1)

    print(a.df_filings.iloc[0]["Filing"].path)
