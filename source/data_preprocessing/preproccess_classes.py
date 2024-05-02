"""
This package is used to preprocess the data. 
It is used to normalize the data and to combine the data from different sources.
"""

import pandas as pd

# import json
# from datetime import datetime, timedelta


class PreproccsesingTickerSymbol:
    """
    This class is used to preprocess the ticker symbols
    from the wikidata_ticker_symbol_data.csv and the wikilist_1.csv and wikilist_2.csv

    it will create an array with all the ticker symbols
    """

    def get_ticker_symbol(self):
        """
        This function is used to get all the ticker symbols from the
        wikidata_ticker_symbol_data.csv and the wikilist_1.csv and wikilist_2.csv
        """
        symbol_df = pd.read_csv("../data/companies/wikidata_ticker_symbol_data.csv")
        list_df_1 = pd.read_csv("../data/companies/wikilist_1.csv", encoding="latin-1")
        list_df_2 = pd.read_csv("../data/companies/wikilist_2.csv", encoding="latin-1")

        len(symbol_df["tickerSymbol"].unique())
        # check which companies are missing in the wikidata_ticker_symbol_data.csv
        result_list = []
        result_list.extend(symbol_df["tickerSymbol"].to_list())

        list_of_ticker_symbols_1 = list_df_1["Symbol"].unique()

        missing_ticker_symbols = []
        for symbol in list_of_ticker_symbols_1:
            if symbol not in symbol_df["tickerSymbol"].unique():
                missing_ticker_symbols.append({"symbol": symbol, "list": "first"})
                result_list.append(symbol)

        list_of_ticker_symbols_2 = list_df_2["Removed"].unique()
        for symbol in list_of_ticker_symbols_2:
            if symbol not in symbol_df["tickerSymbol"].unique():
                missing_ticker_symbols.append({"symbol": symbol, "list": "second"})
                result_list.append(symbol)

        print(missing_ticker_symbols)

        print(len(set(result_list)))

        return result_list


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

        # same as above but for stock value

        # for testing it once before doing it in for loop
        # print(self.raw_data_stock[1].keys())

        # df_stock = pd.DataFrame(pd.json_normalize(self.raw_data_stock[0]["data"]))
        # df_stock["date"] = pd.to_datetime(df_stock["date"]).dt.to_period('M')

        # df_stock

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
                "dividend": "fmp_dividend",
                " dividend amount": "alpha_dividend",
                " adjusted close": "alpha_close",
            }
        )

        return df_concat
