"""
This module is used to define the business logic classes for the data analysis.
"""

import datetime

from datetime import timedelta

import pandas as pd
import numpy as np


class StrategieDataInterface:
    """
    Get the data needed to calculate the strategies
    """

    def __init__(self) -> None:
        pass

    def invest_on_date(self, date: datetime, stock_name, df_combined: pd.DataFrame):
        """
        Returns the stock price of a stock on a specific date
        """
        # get the row with the date
        row = df_combined[df_combined["information"].str.contains("alpha_close")]

        row = row[row["date"] == pd.to_datetime(date).to_period("M")]

        # get the column with the stock_name
        return row[stock_name]

    def get_dividends(
        self,
        df_combined: pd.DataFrame,
        x: datetime.date,
        look_forward_years,
        symbol: str,
    ):
        """
        get all dividends with there stock price for a specific symbol in a specific time span

        args:
            df_combined (pd.DataFrame): dataframe with dividend values
            x (datetime.date): start date
            look_forward_years (int): how many years to look forward
            symbol (str): the symbol to look for
        """
        # TODO check for errors for example no data available

        df_combined = df_combined[[symbol, "date", "information"]]

        # print(df_combined["date"].dt.to_timestamp().sort_values(ascending=False) <= x)
        df_temp = df_combined.loc[
            (
                df_combined["information"].str.contains(
                    "alpha_dividend|alpha_close", regex=True
                )
            )
            & (df_combined["date"].dt.to_timestamp() >= pd.to_datetime(x))
            & (
                df_combined["date"].dt.to_timestamp()
                <= pd.to_datetime(x + datetime.timedelta(days=365 * look_forward_years))
            )
        ][[symbol, "date", "information"]]

        # print duplicates on date
        # print(df_temp[df_temp.duplicated(subset=["date"], keep=False)])

        # remove duplicates on date
        df_temp = df_temp.drop_duplicates(subset=["date", "information"], keep="first")

        df_temp = df_temp.pivot(
            index="date", columns="information", values=symbol
        ).reset_index()

        # strip column names whitespace
        df_temp.columns = df_temp.columns.str.strip()

        if df_temp.empty or "alpha_dividend" not in df_temp.columns:
            return pd.DataFrame()

        return df_temp[df_temp["alpha_dividend"] > 0.0]

    def check_money_made_by_div(
        self,
        start_date: datetime.datetime,
        look_foward_years: int,
        symbol: str,
        df_combined: pd.DataFrame,
        money_invested: int = 1,
    ):
        """
        this checks how much money you would have made by investing in a stock,
        on a specific date and selling it on a specific date.
        it also calculates if you have reinvested the money from the dividends

        args:
            start_date (datetime.datetime): the start date
            look_foward_years (int): how many years to look forward
            symbol (str): the symbol you want to check
            df_combined (pd.DataFrame): dataframe with dividend values
            money_invested (int, optional): the amount of money you have invested. Defaults to 1.
        """

        # check_moeny_made_by_stock

        # get stock price at the beginning of the check
        start_stock_price_in_a_list = self.invest_on_date(
            start_date, symbol, df_combined
        )

        if start_stock_price_in_a_list.empty:
            return pd.DataFrame()

        start_stock_price = start_stock_price_in_a_list.iloc[0]
        # print(start_stock_price)

        # get dividends
        dividends = self.get_dividends(
            df_combined, start_date, look_foward_years, symbol
        )

        # print(dividends)

        output = []

        # check if there are dividends
        # if alpha close is zero my index calculation will fail

        if not dividends.empty and dividends["alpha_close"].count() > 0:

            # check if stock price on start date is not there but there are dividends to check
            if np.isnan(start_stock_price):
                start_stock_price = dividends["alpha_close"].iloc[0]

            self.compound_interest_calc_recursive_with_extras(
                money_invested,
                dividends["alpha_close"].count(),
                dividends["alpha_close"].count(),
                start_stock_price,
                dividends["alpha_dividend"],
                dividends["alpha_close"],
                output,
            )

            # last dividend stock price
            last_dividend_stock_price = dividends["alpha_close"].iloc[-1]
            last_money_made = output[-1]["money"]
            current_stock_price = output[-1]["current stock price"]
            summed_dividend_money = output[-1]["summed_dividend_money"]
        else:
            last_dividend_stock_price = start_stock_price
            last_money_made = money_invested
            current_stock_price = start_stock_price
            summed_dividend_money = 0
        # last stock price
        end_stock_price_in_a_list = self.invest_on_date(
            start_date + timedelta(365 * look_foward_years), symbol, df_combined
        )

        # TODO: probably change this behavior
        if end_stock_price_in_a_list.empty:
            # we have to assume if no end_stock_price is found the company is bankrupt
            # the other case is that the data is not available (because of its a future date)
            end_stock_price = 0
        else:
            end_stock_price = end_stock_price_in_a_list.iloc[0]

        last_money = float(last_money_made) * (
            end_stock_price / last_dividend_stock_price
        )

        output.append(
            {
                "r-anual_interest_rate": str(np.nan),
                "money": str(last_money),
                "growth_from_stock": str(end_stock_price / last_dividend_stock_price),
                "last stock price": current_stock_price,
                "current stock price": end_stock_price,
                "money from growth": str(
                    last_money * (end_stock_price / last_dividend_stock_price)
                ),
                "dividend": np.nan,
                "dividend_money": np.nan,
                "summed_dividend_money": str(summed_dividend_money),
                "date": np.nan,
            }
        )

        # money_invested *(end_money/start_money)

        # calculate money earned until next dividend

        # add those money to the stock price
        # repeat until the end of the check
        return pd.DataFrame(output)

    # filtering data to get symbols wich have consistent increased there dividends

    # show the stock price of a symbol on a specific date
    def check_for_increased_stock(
        self,
        df_combined: pd.DataFrame,
        symbol="ADBE",
        money_invested: int = 1,
        start_date: datetime.datetime = datetime.datetime(2012, 12, 31),
        look_forward_years: int = 4,
    ):
        """
        Show the stock price of a symbol on a specific date.
        Calculate the growth of the stock price and the percentage growth of the stock price.
        No return value only print statments.

        args:
            df_combined (pd.DataFrame): dataframe with dividend values
            symbol (str, optional): the symbol you want to check. Defaults to "ADBE".
            money_invested (int, optional): the amount of money you have invested. Defaults to 1.
            start_date (datetime.datetime, optional): the start date.
            look_forward_years (int, optional): how many years to look forward. Defaults to 4.
        """
        # start_date = datetime.datetime.fromisoformat("2012-12-31")
        end_date = start_date + datetime.timedelta(days=365 * look_forward_years)

        start_money = self.invest_on_date(start_date, symbol, df_combined).iloc[0]
        end_money = self.invest_on_date(end_date, symbol, df_combined).iloc[0]

        print(f"invested money:\t\t {money_invested}$")
        print(f"stock:\t\t\t {symbol}")
        print(f"start date:\t\t{start_date:%d.%m.%Y}")
        print(f"stock start:\t\t{start_money : .2f}")
        print(f"end date:\t\t{end_date:%d.%m.%Y}")
        print(f"stock end:\t\t{end_money : .2f}")

        print(f"stock changed by:\t{end_money-start_money : .2f}$ ")
        # how much procents is the difference
        print(f"percentage growth:\t{(((end_money/start_money)*100)) : .2f}%")

        print(f"money earned: \t\t {money_invested *(end_money/start_money) }")

    def compound_interest_calc_recursive(
        self, r_money, r_months, s_months, s_anual_interest_rate=0.04
    ):
        """
        Calculate compound interest with a recursive function
        r_ = recursive
        s_ = static

        """

        print(
            "interest after month"
            f"{(s_months+1) - r_months}:{s_anual_interest_rate * r_money : 0.2f},"
            f"\t total money:{r_money * (1 + s_anual_interest_rate): 0.2f}"
        )
        r_money = r_money * (1 + s_anual_interest_rate)
        if r_months == 1:
            return r_money
        return self.compound_interest_calc_recursive(r_money, r_months - 1, s_months)

    # TODO rename this function
    def compound_interest_calc_recursive_with_extras(
        self,
        r_money,
        r_months,
        s_months,
        s_first_stock_price,
        s_anual_interest_rate_list: pd.Series,
        s_anual_stock_price_change_list: pd.Series,
        output: list,
    ):
        """
        Calculate compound interest with a recursive function,
        but a lookup table for the anual_interest_rate and
        anual_stock_price_change
        you need the first stock price to see the worth of the stock
        when you start investing, dividend often starts later
        r_ = recursive
        s_ = static

        args:
            r_money (float): the amount of money
            r_months (int): the amount of months to calculate
            s_months (int): the amount of months to look back
            s_first_stock_price (float): the first stock price
            s_anual_interest_rate_list (pd.Series): the list of anual interest rates
            s_anual_stock_price_change_list (pd.Series): the list of anual stock price changes
            output (list): the output list
        """
        r_anual_interest_rate = (
            s_anual_interest_rate_list.iloc[s_months - r_months] * 0.01
        )

        r_anual_stock_price_change = s_anual_stock_price_change_list.iloc[
            s_months - r_months
        ]

        if s_months - r_months == 0:
            # first entry
            last_stock_price = s_first_stock_price
        else:
            # every other entry
            last_stock_price = s_anual_stock_price_change_list.iloc[
                s_months - r_months - 1
            ]

        # adding the growth of the stock to the money
        r_money = r_money * (r_anual_stock_price_change / last_stock_price)

        # adding the interest to the money
        # if the next line is uncommented the dividenden will be added to the money
        # r_money = r_money + (r_money * r_anual_interest_rate)

        # print("new money: "+str(r_money))
        # print("")

        last_dividend_money = 0
        if len(output) > 0:
            # print(output[-1])
            last_dividend_money = float(output[-1]["dividend_money"])
        # print(r_money)
        output.append(
            {
                "r-anual_interest_rate": str(r_anual_interest_rate),
                "money": str(r_money),
                "growth_from_stock": str(r_anual_stock_price_change / last_stock_price),
                "last stock price": last_stock_price,
                "current stock price": r_anual_stock_price_change,
                "money from growth": str(
                    r_money * (r_anual_stock_price_change / last_stock_price)
                ),
                "dividend": str(1 + r_anual_interest_rate),
                "dividend_money": str(r_money * (r_anual_interest_rate)),
                "summed_dividend_money": str((r_money * r_anual_interest_rate) + last_dividend_money),
                "date": s_months - r_months,
                # "date_time":
            }
        )

        if r_months == 1:
            return r_money
        return self.compound_interest_calc_recursive_with_extras(
            r_money,
            r_months - 1,
            s_months,
            s_first_stock_price,
            s_anual_interest_rate_list,
            s_anual_stock_price_change_list,
            output,
        )
