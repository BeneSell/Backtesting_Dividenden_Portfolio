import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import os
import sys
import time
import json
import requests
from pandas.io.json import json_normalize
import csv
import requests


class download_fmp():

    def __init__(self, secret_key_fmp):
        self.secret_key_fmp = secret_key_fmp
        self.base_url = "https://financialmodelingprep.com/api/v3/"
        self.headers = {'Content-Type': 'application/json'}
        self.is_valid = False

    
        
    def validate_api_key(self):
        # validate api key
        url = f"https://financialmodelingprep.com/api/v3/historical/sp500_constituent?apikey={self.secret_key_fmp}"
        response = requests.get(url)
        if(response.status_code == 200):
            print("API key is valid")
            self.is_valid = True
        else:
            self.is_valid = False
            print("API key has not the right privileges and is invalid")
        
        return self.is_valid

    def get_company_ticker_symbols_by_choice(self):
        # Prompt the user for their choice
        print("ATM only read_csv is working")
        choice = input("Choose a solution (fmprep/read_csv/already_done): ")

        result_list = []

        if choice == "fmprep" and self.is_valid:
            
            # not sure if its working at the moment
            # fmprep solution

            fmprep_sp500 = f"https://financialmodelingprep.com/api/v3/historical/sp500_constituent?apikey={self.secret_key_fmp}"
            r = requests.get(fmprep_sp500)
            data = r.json()
            result_list = data["symbol"]
            if(len(result_list) > 505):
                print("successfully read csv file")
            

        elif choice == "read_csv":
            # read_csv solution
            sp500 = pd.read_csv('../data/companies/s&p_companies_ticker_name.csv')
            
            result_list = sp500
            result_list = result_list["0"].to_list()
            if(len(result_list) > 505):
                print("successfully read csv file")
            

        elif choice == "already_done":
            # data generate from code above
            result_list = result_list
            if(len(result_list) > 505):
                print("successfully from code above")

        else:
            print("Invalid choice. Please choose either 'fmprep', 'already_done' or 'read_csv'. \nIMPORTANT NOTE: If you choose 'fmprep' you need to have a valid API key.")
            

        return result_list

    def download_fmp_dividend_data(self):

        result_list = self.get_company_ticker_symbols_by_choice()



        raw_data_dividend = []
        for index, x in enumerate(result_list):
            url = f'https://financialmodelingprep.com/api/v3/historical-price-full/stock_dividend/{ x }?apikey={self.secret_key_fmp}'
            # !!!!!!carefull don't print url and commit!!!!!!!!
            if(index % 50 == 0):
                print(index)
            r = requests.get(url)
            data = r.json()
            raw_data_dividend.append(data)
            # save to file every time because i dont want to lose data
            with open('../data/stock_infos/raw_data_fmp.json', 'w') as outfile:
                json.dump(raw_data_dividend, outfile)
            time.sleep(1)

    def download_fmp_stock_data(self):

        result_list = self.get_company_ticker_symbols_by_choice()

        raw_data_stocks= []
        for index, x in enumerate(result_list):
            url = f'https://financialmodelingprep.com/api/v3/historical-pricel-full/1month/{ x }?apikey={self.secret_key_fmp}'
            # !!!!!!carefull don't print url and commit!!!!!!!!
            if(index % 50 == 0):
                print(index)
            r = requests.get(url)
            data = r.json()
            raw_data_stocks.append({"data":data, "symbol":x})
            # save to file every time because i dont want to lose data
            with open('../data/stock_infos/raw_data_fmp_stock_value.json', 'w') as outfile:
                json.dump(raw_data_stocks, outfile)
            
            if(type(data) != list):
                # if data is not a list then it is an error
                print(data)
                break
            time.sleep(1)


    def download_fmp_dividend_from_local(self):
        # read from file

        result_list = self.get_company_ticker_symbols_by_choice()

        data_result_list = []

        for index, x in enumerate(result_list):
            # if in local folder there is a file called StockDividend_x.json then read it
            if os.path.isfile(f'../data/stock_infos/from_prof/StockDividend_{x}.json'):
                with open(f'../data/stock_infos/from_prof/StockDividend_{x}.json') as json_file:
                    data = json.load(json_file)
                    data_result_list.append(data)
        
        with open('../data/stock_infos/raw_data_fmp_from_local_div.json', 'w') as outfile:
                json.dump(data_result_list, outfile)

        return data_result_list

class download_alphavantage_data():

    def __init__(self):
        
        with open("../secret_file.json") as json_file:
            data = json.load(json_file)
            secret_key_alphavantage = data["secret_key_alphavantage"]

        self.secret_key_alphavantage = secret_key_alphavantage
        self.base_url = "https://www.alphavantage.co/query?"
        self.headers = {'Content-Type': 'application/json'}
        self.is_valid = False

    def validate_api_key(self):
        # get secret key from secret_file.json

        # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=IBM&apikey={ self.secret_key_alphavantage}'
        r = requests.get(url)
        data = r.json()

        print(data["Meta Data"])

        return True
    
    def get_company_ticker_symbols_by_choice(self):
        # Prompt the user for their choice
        print("ATM only read_csv is working")
        choice = input("Choose a solution (fmprep/read_csv/already_done): ")

        result_list = []

        if choice == "fmprep" and self.is_valid:
            
            # not sure if its working at the moment
            # fmprep solution

            fmprep_sp500 = f"https://financialmodelingprep.com/api/v3/historical/sp500_constituent?apikey={self.secret_key_fmp}"
            r = requests.get(fmprep_sp500)
            data = r.json()
            result_list = data["symbol"]
            if(len(result_list) > 505):
                print("successfully read csv file")
            

        elif choice == "read_csv":
            # read_csv solution
            sp500 = pd.read_csv('../data/companies/s&p_companies_ticker_name.csv')
            
            result_list = sp500
            result_list = result_list["0"].to_list()
            if(len(result_list) > 505):
                print("successfully read csv file")
            

        elif choice == "already_done":
            # data generate from code above
            result_list = result_list
            if(len(result_list) > 505):
                print("successfully from code above")

        else:
            print("Invalid choice. Please choose either 'fmprep', 'already_done' or 'read_csv'. \nIMPORTANT NOTE: If you choose 'fmprep' you need to have a valid API key.")
            

        return result_list


    def download_alphavantage_stock_and_dividend_data(self):

        result_list = self.get_company_ticker_symbols_by_choice()


        raw_data = []
        for index, x in enumerate(result_list):
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={ x }&apikey={self.secret_key_alphavantage}'
            # !!!!!!carefull don't print url and commit!!!!!!!!
            if(index % 50 == 0):
                print(index)
            r = requests.get(url)
            data = r.json()
            raw_data.append(data)
            time.sleep(1.5)

        with open('../data/stock_infos/result.json', 'w') as fp:
            json.dump(raw_data, fp)