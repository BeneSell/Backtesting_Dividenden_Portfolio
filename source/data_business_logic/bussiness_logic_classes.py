import pandas as pd
import datetime

from datetime import timedelta

class single_stock_check():
    def __init__(self) -> None:
        pass

    def invest_on_date(self, date: datetime, stock_name, df_combined: pd.DataFrame):
        # get the row with the date
        row = df_combined[df_combined["information"].str.contains("adjusted close")]
        
        # TODO change it because this is kinda slow and confusing ATM i dont really kown how to do it better
        row = row[row["date"] == pd.Series(date).dt.to_period("M").iloc[0]]
        
        # get the column with the stock_name
        return row[stock_name]

    def check_single_stock(self, stock_symbol:str):
        pass

    # filtering data to get symbols wich have dividend over 5

    def check_for_min_dividend(self, df_combined: pd.DataFrame, min_dividend: float = 0.05, x: datetime.date = datetime.date(2020, 1, 1), look_back_years: int = 5):
        """
        Checks if a symbol has a dividend for every year in the look_back_years until the given date x
        
        Args:
            df_combined (pd.DataFrame): dataframe with dividend values
            min_dividend (float, optional): minimum dividend. Defaults to 5.
        """

        # TODO think about the amout of times a dividend is paid in a year
        df_temp = df_combined.loc[(df_combined["information"].str.contains("adjDividend")) & (pd.to_datetime(df_combined["date"]) <= pd.to_datetime(x))]
        df_temp["year_period"] = pd.to_datetime(df_combined["date"]).dt.to_period("Y")
        
        df_temp["value"] = df_temp["value"].astype(float)
        df_temp = df_temp.groupby("year_period").sum().reset_index()
        
        # subtract year of x with look_back_years
        first_year = x.year - look_back_years

        # df_temp["year_period"] = df_temp["year_period"].astype(str).astype(int)
        print(df_temp["value"])
        df_temp = df_temp[df_temp["year_period"].astype(str).astype(int) > first_year]

        result = df_temp.loc[df_temp["value"].astype(float) >= min_dividend]["value"].all()

        return result

# check_for_min_dividend(df[df["symbol"] == "MSFT"], 0.05, datetime.date(2020, 1, 1), 15)

    def get_dividends(self, df_combined: pd.DataFrame,x: datetime.date,look_back_years, symbol: str):
        
        # print(df_combined["date"].dt.to_timestamp().sort_values(ascending=False) <= x)
        df_temp = df_combined.loc[(df_combined["information"].str.contains("dividend amount|close", regex=True)) 
                                  & (df_combined["date"].dt.to_timestamp() <= x) 
                                  & (df_combined["date"].dt.to_timestamp() >= x - datetime.timedelta(days=365 * look_back_years))][["ADBE", "date", "information"]]
        
        df_temp = df_temp.pivot(index="date", columns="information", values="ADBE").reset_index()
        
        
        
        # strip column names whitespace 
        df_temp.columns = df_temp.columns.str.strip()
        
        # print(df_temp[df_temp["dividend amount"] > 0.0])

        return df_temp[df_temp["dividend amount"] > 0.0]

    def check_money_made_by_div(self):
        # get dividends
        # get stock price at the beginning of the check
        # calculate money earned until next dividend
        # add those money to the stock price
        # repeat until the end of the check
        
        pass

# filtering data to get symbols wich have consistent increased there dividends


# show the stock price of a symbol on a specific date
    def check_for_increased_stock(self, df_combined: pd.DataFrame, money_invested: int = 1, start_date: datetime.datetime = datetime.datetime(2012, 12, 31), look_forward_years: int = 4):
        # start_date = datetime.datetime.fromisoformat("2012-12-31")
        end_date = start_date + datetime.timedelta(days=365 * look_forward_years)

        start_money = self.invest_on_date(start_date, "ADBE", df_combined).iloc[0]
        end_money = self.invest_on_date(end_date, "ADBE", df_combined).iloc[0]


        print(f"invested money:\t\t {money_invested}$")
        print("stock:\t\t\t ADBE")
        print(f"start date:\t\t{start_date:%d.%m.%Y}")
        print(f"stock start:\t\t{start_money : .2f}")
        print(f"end date:\t\t{end_date:%d.%m.%Y}")
        print(f"stock end:\t\t{end_money : .2f}")
    
        # how much money would you have if you invested 1$ in adobe on 2012-12-31 and sold it on 2013-12-31
#         print(f"idk  :\t\t{((1/start_money)*end_money) : .2f}$ ")
        print(f"stock changed by:\t{end_money-start_money : .2f}$ ")
        # how much procents is the difference
        print(f"percentage growth:\t{(((end_money/start_money)*100)) : .2f}%")

        print(f"money earned: \t\t {money_invested *(end_money/start_money) }")

    def compound_interest_calc_recursive(self, r_money, r_months, s_months, s_anual_interest_rate=0.04):
        """
        Calculate compound interest with a recursive function
        r_ = recursive
        s_ = static 

        """
        monthly = s_anual_interest_rate / 12
        print(f"interest after month {(s_months+1) - r_months}:{monthly * r_money : 0.2f},\t total money:{r_money * (1 + monthly): 0.2f}")
        r_money = r_money * (1 + monthly)
        if r_months == 1:
            return r_money
        return self.compound_interest_calc_recursive(r_money, r_months-1, s_months)