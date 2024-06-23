import brel
from brel.utils import pprint
from random import sample 
import pandas as pd

import brel_import
company = brel_import.Company("MasterCard", 1)
filing = company.df_filings["Filing"].iloc[0]

#### --------- 

# filing = Filing.open(r"C:/Workspace/MyRepositories/StockEvaluationTool/v/v-20230930_htm.xml")
# import sys
# sys.exit()

#### --------- 

def get_dei_info(): 

    networks = filing.get_all_physical_networks()
    some_networks = sample(networks, 3)

    for network in some_networks:
        pprint(network)

get_dei_info()


# if __name__ == "__main__":
#     df = get_presentation()

#     print(df)
#     # print(filing.get_all_facts()[0])