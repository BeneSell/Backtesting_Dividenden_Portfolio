"""
This package is used to preprocess the data. 
It is used to normalize the data and to combine the data from different sources.
"""

import json
import pandas as pd



# from datetime import datetime, timedelta

with open("../config.json", "r", encoding="utf-8") as file_data:
    config_file = json.load(file_data)


class PreproccsesingTickerSymbol:
    """
    This class is used to preprocess the ticker symbols
    from the wikidata_ticker_symbol_data.csv and the wikilist_1.csv and wikilist_2.csv

    it will create an array with all the ticker symbols
    """

    def get_ticker_symbol_for_specific_year(self, year=pd.to_datetime("2022-01-01")):
        """
        This function returns the sp500 at a specific year.
        heavly based on the wikilist
        https://en.wikipedia.org/wiki/List_of_S%26P_500_companies

        sadly the second wikilist needs some adjustments
        1. Delete the first header row
        2. change the first column name "Ticker" to "Ticker_Added"
        3. change the second column name "Ticker" to "Ticker_Removed"

        args:
            sp500_current (list): the current newest sp500
            changes_to_sp500 (pd.DataFrame): the changes to the sp500
            year (pd.Timestamp): the year to get the sp500 at
        """

        sp500_current = pd.read_csv(
            config_file["file_names"]["company_names_from_wiki_1"],
            encoding="latin-1",
        )

        changes_to_sp500 = pd.read_csv(
            config_file["file_names"]["company_names_from_wiki_2"],
            encoding="latin-1",
        )

        current_sp500 = sp500_current["Symbol"].to_list()

        changes_to_sp500["Date"] = pd.to_datetime(changes_to_sp500["Date"])
        changes_to_sp500 = changes_to_sp500.sort_values(by="Date", ascending=False)

        for x in changes_to_sp500.iterrows():

            # we have the current sp500
            # we need the sp500 at x date
            # so we iterate until x date and do the opposite changes
            # if something got removed we add it to the current_sp500
            # if something got added we remove it from the current_sp500
            # if we reach the date x we stop

            # after that we have the sp500 at date x
            if not pd.isna(x[1]["Ticker_Added"]):

                # remove the ticker from the current_sp500
                # check if the ticker is in the current_sp500
                if x[1]["Ticker_Added"] in current_sp500:
                    current_sp500.remove(x[1]["Ticker_Added"])

            if not pd.isna(x[1]["Ticker_Removed"]):
                # add the ticker to the current_sp500
                current_sp500.append(x[1]["Ticker_Removed"])

            if x[1]["Date"] < year:
                break

        return current_sp500

    def setup_unique_ticker_symbols(self):
        """
        This function is used to setup the unique ticker symbols
        from alle the ticker symbols we have
        """
        sp500_current = pd.read_csv(
            config_file["file_names"]["company_names_from_wiki_1"],
            encoding="latin-1",
        )

        changes_to_sp500 = pd.read_csv(
            config_file["file_names"]["company_names_from_wiki_2"],
            encoding="latin-1",
        )
        combined_series = pd.concat([sp500_current["Symbol"], changes_to_sp500["Ticker_Added"], changes_to_sp500["Ticker_Removed"]], axis=0)
        

        pd.Series(combined_series.unique()).to_csv(
            config_file["file_names"]["company_names"]
            , index=False
        )

class PreproccessingAlphavantageData:
    """
    This class is used to preprocess the data from the alphavantage api
    Mainly the structure of the data is changed and the data is normalized
    """

    def __init__(self, data_from_csv: list) -> None:

        self.normalized_data = self.normalize_data(data_from_csv)

    def normalize_data(self, data_from_csv: list):
        """
        This function is used to normalize the data from the alphavantage api

        Args:
            data_from_csv: list -> list of json objects
        """

        # normalize data
        normalized_json_df = pd.json_normalize(data_from_csv)

        # Meta Data.2. Symbol is the company ticker and needs only once per
        # new row thats why we drop duplicates here

        normalized_json_df = normalized_json_df.drop_duplicates("Meta Data.2. Symbol")
        normalized_json_df = normalized_json_df.dropna(
            axis=0, subset=["Meta Data.2. Symbol"]
        )

        normalized_json_df = normalized_json_df.set_index("Meta Data.2. Symbol")

        transposed_df = normalized_json_df.transpose()
        transposed_df = transposed_df.reset_index()

        # Monthly Adjusted Time Series.2024-02-01.2. high
        # regex explained
        # .* = match any character (except for line terminators) -> "Monthly Adjusted Time Series"
        # (\d\d\d\d-\d\d-\d\d) = match a date -> "2024-02-01"
        # .* = match any character (except for line terminators) -> ".2. high"
        # r"\1 \2" = replace with the first and second group -> "2024-02-01 .2. high"
        # index_extraced will be = "2024-02-01 .2. high"
        # which then can be split by the dot and the date can be extracted

        transposed_df["index_extracted"] = transposed_df["index"].replace(
            {r".*(\d\d\d\d-\d\d-\d\d)(.*)": r"\1 \2"}, regex=True
        )
        transposed_df[["date", "random_counter", "information"]] = transposed_df[
            "index_extracted"
        ].str.split(".", expand=True)

        transposed_df["date"] = pd.to_datetime(transposed_df["date"], errors="coerce")
        transposed_df.dropna(subset=["date"], inplace=True)

        # set every column to numeric except date,
        # random_counter and information and index_extracted
        for x in transposed_df.columns:
            if x not in (
                "date",
                "random_counter",
                "information",
                "index_extracted",
                "index",
            ):
                transposed_df[x] = transposed_df[x].astype(float)

        return transposed_df


class PreproccessingFMPData:
    """
    This class is used to preprocess the data from the financialmodelingprep api
    Mainly the structure of the data is changed and the data is normalized
    For Combining the structure can actually change a lot
    """

    def __init__(self, raw_data_dividend: list, raw_data_stock: list) -> None:
        self.normalized_data_dividend = self.normalize_dividenden_data(
            raw_data_dividend
        )
        self.normalized_stock_data = self.normalize_stock_data(raw_data_stock)

    def normalize_stock_data(self, raw_data_stock: list):
        """
        This function is used to normalize the stock data from the financialmodelingprep api
        """

        result_df = pd.DataFrame()

        # result_df["date"] = pd.to_datetime(months).to_period('M')

        for i, x in enumerate(raw_data_stock):

            try:
                # unpivot json
                df = pd.json_normalize(x["data"])

            # after a while the data gets a limit error
            # so you have to break the loop in order
            # to prevent the error from crashig the programm
            # TODO: use the right Exception

            except Exception as e:
                if e:
                    pass
                # print(x)
                # input()
                continue

            if df.empty:
                continue
            # show me df if column date does not exist
            if "date" not in df.columns:
                continue

            df["date"] = pd.to_datetime(df["date"], errors="coerce").dropna()
            # df['date'] = pd.to_datetime(df['date']).dt.to_period('M')

            df["date"] = df["date"].dt.to_period("M")

            df_melted = df.melt(
                id_vars=["date"],
                value_vars=["date", "open", "low", "high", "close", "volume"],
            )

            # rename value column to json_response_2['symbol']
            # df_melted = df_melted.rename(columns={"value": x['symbol']})
            # join result df with df_melted on date
            df_melted["symbol"] = x["symbol"]

            if i == 0:
                result_df = df_melted
                continue

            result_df = pd.concat([result_df, df_melted])

            # result_df = result_df.merge(df_melted, how='left', on='date')

        # result_df[(result_df["variable"] == "close") & (result_df["symbol"] == "PFE") ]
        # result_df.to_csv("./data/stock_infos/stock_values_per_symbol.csv", index=False)

        return result_df

    def normalize_dividenden_data(self, raw_data_dividend: list):
        """
        This function is used to normalize the dividend data from the financialmodelingprep api
        """
        result_df = pd.DataFrame()

        # result_df["date"] = pd.to_datetime(months).to_period('M')

        for i, x in enumerate(raw_data_dividend):

            try:

                # unpivot json
                df = pd.json_normalize(x["historical"])
            except Exception as e:
                if e:
                    pass
                # shows which company ticker is not working
                # print(x)
                continue

            if df.empty:
                continue

            df["orignal_date"] = pd.to_datetime(df["date"])
            # df['date'] = pd.to_datetime(df['date']).dt.to_period('M')

            df["date"] = df["orignal_date"].dt.to_period("M")

            df_melted = df.melt(
                id_vars=["date"],
                value_vars=[
                    "adjDividend",
                    "dividend",
                    "recordDate",
                    "paymentDate",
                    "declarationDate",
                ],
            )
            # print(x['symbol'])
            # rename value column to json_response_2['symbol']
            # df_melted = df_melted.rename(columns={"value": x['symbol']})
            # join result df with df_melted on date
            df_melted["symbol"] = x["symbol"]

            if i == 0:
                result_df = df_melted
                continue

            result_df = pd.concat([result_df, df_melted])

            # result_df = result_df.merge(df_melted, how='left', on='date')

        # result_df[(result_df["variable"] == "adjDividend") & (result_df["symbol"] == "MSFT") ]
        # result_df.to_csv("../data/stock_infos/dividend_values_per_symbol.csv", index=False)

        return result_df

    def pivot_dividenden_data(self, df_normalized: pd.DataFrame):
        """
        This function is used to pivot the dividend data
        Its used to get the data in the right format for the combined data
        """

        df_pivot = df_normalized.pivot_table(
            index=["date", "variable"],
            columns="symbol",
            values="value",
            aggfunc="first",
        ).reset_index()
        return df_pivot

    def pivot_stock_data(self, df_normalized: pd.DataFrame):
        """
        This function is used to pivot the stock data
        Its used to get the data in the right format for the combined data
        """

        df_pivot = df_normalized.pivot_table(
            index=["date", "variable"],
            columns="symbol",
            values="value",
            aggfunc="first",
        ).reset_index()
        return df_pivot


class PreproccessingCombinedData:
    """
    This class is used to preprocess the combined data from the
    financialmodelingprep api and the alphavantage api
    """

    def __init__(
        self, pre_fmp: PreproccessingFMPData, pre_alpha: PreproccessingAlphavantageData
    ) -> None:
        self.pre_fmp = pre_fmp
        self.pre_alpha = pre_alpha
        self.combined_data = self.basic_combined_data()

    def basic_combined_data(self):
        """
        This function is used to combine the data from the
        financialmodelingprep api and the alphavantage api

        The data is combined by the date and the information
        """

        fmp_div_df = self.pre_fmp.pivot_dividenden_data(
            self.pre_fmp.normalized_data_dividend
        ).rename(columns={"variable": "information"})
        fmp_stock_df = self.pre_fmp.pivot_stock_data(
            self.pre_fmp.normalized_stock_data
        ).rename(columns={"variable": "information"})

        alpha_df = self.pre_alpha.normalized_data
        alpha_df["date"] = alpha_df["date"].dt.to_period("M")

        alpha_div = alpha_df[alpha_df["information"].str.contains("dividend")]
        fmp_div = fmp_div_df[fmp_div_df["information"].str.contains("dividend")]

        alpha_stock = alpha_df[alpha_df["information"].str.contains("adjusted close")]
        fmp_stock = fmp_stock_df[fmp_stock_df["information"].str.contains("close")]

        # combine alpha_div, fmp_div and alpha_stock, fmp_stock concat

        df_concat = pd.concat([alpha_div, fmp_div, alpha_stock, fmp_stock], axis=0)

        df_concat["information"] = df_concat["information"].replace(
            {
                "close": "fmp_close",
                "dividend": "alpha_dividend",
                " dividend amount": "fmp_dividend",
                " adjusted close": "alpha_close",
            }
        )
        

        # df_concat["information"] = df_concat["information"].replace(
        #     {
        #         "close": "alpha_close",
        #         "dividend": "alpha_dividend",
        #         " dividend amount": "fmp_dividend",
        #         " adjusted close": "fmp_close",
        #     }
        # )

        return df_concat
