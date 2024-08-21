"""
This file contains the classes for downloading data from the APIs. 
The classes are used in the main.py file to download data from the APIs and save it to a file. 
"""

import os
import time
import json
from datetime import datetime, timedelta


import pandas as pd
import requests

with open("../config.json", "r", encoding="utf-8") as file_data:
    config_file = json.load(file_data)


class DownloadFMP:
    """
    This class is used to download data from the Financial Modeling Prep API.
    """

    def __init__(self):

        with open(
            config_file["file_names"]["secret_file"], encoding="utf-8"
        ) as json_file:
            data = json.load(json_file)
            secret_key_fmp = data["secret_key_fmp"]

        self.secret_key_fmp = secret_key_fmp
        self.base_url = "https://financialmodelingprep.com/api/v3/"
        self.headers = {"Content-Type": "application/json"}
        self.is_valid = False

    def validate_api_key(self):
        """
        This function is used to validate the API key.
        """
        # validate api key
        url = (
            "https://financialmodelingprep.com/api/v3/historical/"
            f"sp500_constituent?apikey={self.secret_key_fmp}"
        )

        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print("API key is valid")
            self.is_valid = True
        else:
            self.is_valid = False
            print("API key has not the right privileges and is invalid")

        return self.is_valid

    def get_company_ticker_symbols(self):
        """
        This function is used to get the company ticker symbols.
        """
        result_list = []

        # read_csv solution
        sp500 = pd.read_csv(
            config_file["file_names"]["company_names"]
        )

        result_list = sp500["0"].to_list()
        if len(result_list) > 505:
            print("successfully read csv file")
        

        return result_list

    def downloadFMP_dividend_data(self):
        """
        This function is used to download dividend data from the Financial Modeling Prep API.
        """

        result_list = self.get_company_ticker_symbols()

        for index, x in enumerate(result_list):
            url = f"https://financialmodelingprep.com/api/v3/historical-price-full/stock_dividend/{ x }?apikey={self.secret_key_fmp}"

            # small progression logic
            if index % 50 == 0:
                print(index)

            r = requests.get(url, timeout=10)
            data = r.json()

            # create a file for each stock
            with open(
                config_file["file_names"]["temp_dividend_fmp"].replace("REPLACEDBYCODE", str(x)),
                "w",
                encoding="utf-8",
            ) as outfile:
                json.dump(data, outfile)

            time.sleep(1)

    def downloadFMP_stock_data(self):
        """
        this function is used to download stock data from the Financial Modeling Prep API.
        """

        result_list = self.get_company_ticker_symbols()

        raw_data_stocks = []
        for index, x in enumerate(result_list):
            url = f"https://financialmodelingprep.com/api/v3/historical-pricel-full/1month/{ x }?apikey={self.secret_key_fmp}"
            # !!!!!!carefull don't print url and commit!!!!!!!!
            if index % 50 == 0:
                print(index)
            r = requests.get(url, timeout=10)
            data = r.json()
            raw_data_stocks.append({"data": data, "symbol": x})
            # save to file every time because i dont want to lose data
            with open(
                config_file["file_names"]["fmp_stocks"],
                "w",
                encoding="utf-8",
            ) as outfile:
                json.dump(raw_data_stocks, outfile)

            
            # if data has key "Error Message" then the limit is reached
            if "Error Message" in data:
                print("limit reached")
                break
            time.sleep(1)

    def downloadFMP_dividend_from_local(self):
        """
        This function is used to download dividend data from the local folder.
        """
        # read from file

        result_list = self.get_company_ticker_symbols()

        data_result_list = []

        for x in result_list:
            # if in local folder there is a file called x_dividend-historical.json then read it
            if os.path.isfile(
                config_file["file_names"]["temp_dividend_fmp"].replace("REPLACEDBYCODE", str(x))
            ):
                with open(
                    config_file["file_names"]["temp_dividend_fmp"].replace("REPLACEDBYCODE", str(x)),
                    encoding="utf-8",
                ) as json_file:
                    data = json.load(json_file)
                    data_result_list.append(data)

        with open(
            config_file["file_names"]["fmp_dividends"],
            "w",
            encoding="utf-8",
        ) as outfile:
            json.dump(data_result_list, outfile)

        return data_result_list


class DownloadAlphavantageData:
    """
    This class is used to download data from the Alpha Vantage API.
    """

    def __init__(self):

        with open(
            config_file["file_names"]["secret_file"], encoding="utf-8"
        ) as json_file:
            data = json.load(json_file)
            secret_key_alphavantage = data["secret_key_alphavantage"]

        self.secret_key_alphavantage = secret_key_alphavantage
        self.base_url = "https://www.alphavantage.co/query?"
        self.headers = {"Content-Type": "application/json"}
        self.is_valid = False

    def validate_api_key(self):
        """
        This function is used to validate the API key.
        """
        # get secret key from secret_file.json

        # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol=IBM&apikey={ self.secret_key_alphavantage}"
        r = requests.get(url, timeout=10)
        data = r.json()

        print(data["Meta Data"])

        return True

    def get_company_ticker_symbols(self):
        """
        This function is used to get the company ticker symbols.
        """
        

        result_list = []

        
        sp500 = pd.read_csv(
            config_file["file_names"]["company_names"]
        )

        result_list = sp500
        result_list = result_list["0"].to_list()
        if len(result_list) > 505:
            print("successfully read csv file")

        return result_list

    def download_alphavantage_stock_and_dividend_data(self):
        """
        This function is used to download stock and dividend data from the Alpha Vantage API.
        """

        result_list = self.get_company_ticker_symbols()
        result_list.append("URTH")

        raw_data = []
        for index, x in enumerate(result_list):
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={ x }&apikey={self.secret_key_alphavantage}"
            # !!!!!!carefull don't print url and commit!!!!!!!!
            if index % 50 == 0:
                print(index)
            r = requests.get(url, timeout=10)
            data = r.json()
            raw_data.append(data)
            time.sleep(1.5)

        with open(
            config_file["file_names"]["alpha_vantage_data"],
            "w",
            encoding="utf-8",
        ) as fp:
            json.dump(raw_data, fp)

    def add_newest_alphavantage_stock_and_dividend_data(self):
        """
        This function is used to add the newest stock and dividend data to the existing data.
        """
        # read from file
        with open(
            config_file["file_names"]["alpha_vantage_data"],
            encoding="utf-8",
        ) as json_file:
            data = json.load(json_file)

        # get newest entry from data
        newest_date = pd.to_datetime(data[-1]["Meta Data"]["3. Last Refreshed"])
        print(newest_date)

        result_list = self.get_company_ticker_symbols()
        result_list.append("URTH")

        raw_data = []
        for index, x in enumerate(result_list):
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={ x }&apikey={self.secret_key_alphavantage}"
            # !!!!!!carefull don't print url and commit!!!!!!!!
            if index % 50 == 0:
                print(index)
            r = requests.get(url, timeout=10)
            data = r.json()

            raw_data.append(data)
            time.sleep(1.5)

        with open(
            config_file["file_names"]["alpha_vantage_data"].replace(".json","") + newest_date.strftime("%Y-%m-%d") + ".json",
            "w",
            encoding="utf-8",
        ) as fp:
            json.dump(raw_data, fp)