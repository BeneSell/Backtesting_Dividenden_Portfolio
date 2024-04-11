import pandas as pd
import datetime

from datetime import timedelta
import numpy as np

class single_stock_check():
    def __init__(self) -> None:
        pass

    def invest_on_date(self, date: datetime, stock_name, df_combined: pd.DataFrame):
        # get the row with the date
        row = df_combined[df_combined["information"].str.contains("adjusted close")]
        
        row = row[row["date"] == pd.to_datetime(date).to_period("M")]
        
        # get the column with the stock_name
        return row[stock_name]


    # TODO: Check if commiting this effect something
    # filtering data to get symbols wich have dividend over 5

    # def check_for_min_dividend(self, df_combined: pd.DataFrame, min_dividend: float = 0.05, x: datetime.date = datetime.date(2020, 1, 1), look_back_years: int = 5):
    #     """
    #     Checks if a symbol has a dividend for every year in the look_back_years until the given date x
        
    #     Args:
    #         df_combined (pd.DataFrame): dataframe with dividend values
    #         min_dividend (float, optional): minimum dividend. Defaults to 5.
    #     """

    #     # TODO think about the amout of times a dividend is paid in a year
    #     df_temp = df_combined.loc[(df_combined["information"].str.contains("adjDividend")) & (pd.to_datetime(df_combined["date"]) <= pd.to_datetime(x))]
    #     df_temp["year_period"] = pd.to_datetime(df_combined["date"]).dt.to_period("Y")
        
    #     df_temp["value"] = df_temp["value"].astype(float)
    #     df_temp = df_temp.groupby("year_period").sum().reset_index()
        
    #     # subtract year of x with look_back_years
    #     first_year = x.year - look_back_years

    #     # df_temp["year_period"] = df_temp["year_period"].astype(str).astype(int)
    #     print(df_temp["value"])
    #     df_temp = df_temp[df_temp["year_period"].astype(str).astype(int) > first_year]

    #     result = df_temp.loc[df_temp["value"].astype(float) >= min_dividend]["value"].all()

    #     return result

# check_for_min_dividend(df[df["symbol"] == "MSFT"], 0.05, datetime.date(2020, 1, 1), 15)

    def get_dividends(self, df_combined: pd.DataFrame, x: datetime.date, look_forward_years, symbol: str):
        # TODO check for errors for example no data available
        
        df_combined = df_combined[[symbol, "date", "information"]]

        # print(df_combined["date"].dt.to_timestamp().sort_values(ascending=False) <= x)
        df_temp = df_combined.loc[(df_combined["information"].str.contains("dividend amount|close", regex=True)) 
                                  & (df_combined["date"].dt.to_timestamp() >= pd.to_datetime(x)) 
                                  & (df_combined["date"].dt.to_timestamp() <= pd.to_datetime(x + datetime.timedelta(days=365 * look_forward_years)))][[symbol, "date", "information"]]
        
        # print duplicates on date 
        # print(df_temp[df_temp.duplicated(subset=["date"], keep=False)])

        # remove duplicates on date
        df_temp = df_temp.drop_duplicates(subset=["date", "information"], keep="first")

        
        df_temp = df_temp.pivot(index="date", columns="information", values=symbol).reset_index()
        
        
        # strip column names whitespace 
        df_temp.columns = df_temp.columns.str.strip()
          
        

        

        return df_temp[df_temp["dividend amount"] > 0.0]

    def check_money_made_by_div(self, start_date: datetime.datetime, look_foward_years: int, symbol: str, df_combined: pd.DataFrame, money_invested: int = 1):
        # check_moeny_made_by_stock 

        # get stock price at the beginning of the check
        start_stock_price_in_a_list = self.invest_on_date(start_date, symbol, df_combined)

        if(start_stock_price_in_a_list.empty):
            return pd.DataFrame()

        start_stock_price = start_stock_price_in_a_list.iloc[0]
        # print(start_stock_price)
        
        
        # get dividends
        dividends = self.get_dividends(df_combined, start_date, look_foward_years, symbol)

        # print(dividends)


        if(dividends.empty):
            return pd.DataFrame()

        output = []
        self.compound_interest_calc_recursive_with_extras(money_invested, dividends["adjusted close"].count(), dividends["adjusted close"].count(), start_stock_price, dividends["dividend amount"], dividends["adjusted close"], output)

        # last stock price
        end_stock_price_in_a_list = self.invest_on_date(start_date + timedelta(365 * look_foward_years), symbol, df_combined)
        
        if(end_stock_price_in_a_list.empty):
            return pd.DataFrame(output)
        
        end_stock_price = end_stock_price_in_a_list.iloc[0]

        # last dividend stock price
        last_dividend_stock_price = dividends["adjusted close"].iloc[-1] 

        last_money_made = output[-1]["money"]

        last_money = float(last_money_made) * (end_stock_price/last_dividend_stock_price)

        output.append({
            "r-anual_interest_rate": str(np.nan),
            "money": str(last_money),
            "growth_from_stock": str(end_stock_price/last_dividend_stock_price),
            "last stock price": end_stock_price,
            "current stock price": end_stock_price,
            "money from growth" : str(last_money * (end_stock_price/last_dividend_stock_price)),
            "dividend": np.nan,
            "dividend_money": np.nan,
            "date": np.nan
        })


        # money_invested *(end_money/start_money)

        # calculate money earned until next dividend

        # add those money to the stock price
        # repeat until the end of the check
        return pd.DataFrame(output)
        pass

# filtering data to get symbols wich have consistent increased there dividends


# show the stock price of a symbol on a specific date
    def check_for_increased_stock(self, df_combined: pd.DataFrame,symbol="ADBE", money_invested: int = 1, start_date: datetime.datetime = datetime.datetime(2012, 12, 31), look_forward_years: int = 4):
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
        print(f"interest after month {(s_months+1) - r_months}:{s_anual_interest_rate * r_money : 0.2f},\t total money:{r_money * (1 + s_anual_interest_rate): 0.2f}")
        r_money = r_money * (1 + s_anual_interest_rate)
        if r_months == 1:
            return r_money
        return self.compound_interest_calc_recursive(r_money, r_months-1, s_months)
    
    # TODO rename this function
    def compound_interest_calc_recursive_with_extras(self, r_money, r_months, s_months, s_first_stock_price, s_anual_interest_rate_list: pd.Series, s_anual_stock_price_change_list: pd.Series, output: list = []):
        """
        Calculate compound interest with a recursive function but a lookup table for the anual_interest_rate
        r_ = recursive
        s_ = static 

        """
        r_anual_interest_rate = s_anual_interest_rate_list.iloc[s_months - r_months] * 0.01

        r_anual_stock_price_change = s_anual_stock_price_change_list.iloc[s_months - r_months]

        if(s_months - r_months == 0):
            # first entry
            last_stock_price = s_first_stock_price
        else:
            # every other entry
            last_stock_price = s_anual_stock_price_change_list.iloc[s_months - r_months - 1]
            pass
        

        # a lot of print statements for debugging
        # print("r-anual interest rate:" + str(r_anual_interest_rate))
        # print("money:" + str(r_money))
        # print("growth from stock: "+ str( r_anual_stock_price_change/last_stock_price))
        # print(f"last stock price: {last_stock_price}")
        # print(f"current stock price: {r_anual_stock_price_change}")
        # print("money from growth: "+ str(r_money * (r_anual_stock_price_change/last_stock_price)))
        # print("dividend: "+ str(1 + r_anual_interest_rate))
        # print("dividend money: "+ str(r_money * (r_anual_interest_rate)))
        
        # calculate the anual interest rate
        
        
        # adding the growth of the stock to the money
        r_money = r_money * (r_anual_stock_price_change/last_stock_price)
        
        # print(f"interest after year {(s_months+1) - r_months}:{r_anual_interest_rate * r_money : 0.2f},\t total money:{r_money * (1 + r_anual_interest_rate): 0.2f}")
        
        # print("dividend after money: "+ str(r_money * (r_anual_interest_rate)))

        # adding the interest to the money
        r_money = r_money + (r_money * r_anual_interest_rate)

        
        # print("new money: "+str(r_money))
        # print("")


        output.append({
            "r-anual_interest_rate": str(r_anual_interest_rate),
            "money": str(r_money),
            "growth_from_stock": str( r_anual_stock_price_change/last_stock_price),
            "last stock price": last_stock_price,
            "current stock price": r_anual_stock_price_change,
            "money from growth" : str(r_money * (r_anual_stock_price_change/last_stock_price)),
            "dividend": str(1 + r_anual_interest_rate),
            "dividend_money": str(r_money * (r_anual_interest_rate)),
            "date": s_months - r_months
        })

        if r_months == 1:
            return r_money
        return self.compound_interest_calc_recursive_with_extras(r_money, r_months-1, s_months,s_first_stock_price, s_anual_interest_rate_list, s_anual_stock_price_change_list, output)
    
    def calculate_dividend_yield(self, dividends_of_stock: pd.DataFrame):
        # print("mean of dividend yield: " + str(dividends_of_stock["dividend amount"].mean()))
        return dividends_of_stock["dividend amount"].mean()
        pass
    
    def calculate_dividend_growth(self, dividends_of_stock):

        dividend_growth = dividends_of_stock["dividend amount"].pct_change()
        # print(dividend_growth)
        # print("mean of dividend growth: "+str(dividend_growth.mean()))
        return dividend_growth.mean()
        pass

    def calculate_dividend_stability(self, dividends_of_stock):
        # Calculate the interval between consecutive dividend dates
        dividend_intervals = dividends_of_stock["date"].dt.to_timestamp().diff().dt.days
        # print("varianz of stability: " + str(dividend_intervals.var()))

        return dividend_intervals.var()
    



class bruteforce_checks():
    def __init__(self, combined_data) -> None:
        self.single_stock_checker = single_stock_check()
        self.combined_data = combined_data
        pass

    def check_all_stocks(self, start_date: datetime.datetime = datetime.date(2015, 12, 31)):

        result = []
        for x in self.combined_data.columns:
            
            # stop when the column is not a stock symbol
            # TODO rework this
            if(x == "date" or x == "information" or x == "index" or x == "index_extracted" or x == "random_counter"):
                continue

            temp_dividends = self.single_stock_checker.get_dividends(self.combined_data, start_date, 5, x)


            temp_growth = self.single_stock_checker.calculate_dividend_growth(temp_dividends)
            temp_stability = self.single_stock_checker.calculate_dividend_stability(temp_dividends)
            temp_yield = self.single_stock_checker.calculate_dividend_yield(temp_dividends)
            
            result.append({
                "symbol": x,
                "growth": temp_growth,
                "stability": temp_stability,
                "yield": temp_yield
            })
        	
        result_df = pd.DataFrame(result)
        
        
        result_df["rank_growth"] = result_df["growth"].rank(ascending=False) 
        result_df["rank_stability"] = result_df["stability"].rank(ascending=False) 
        result_df["rank_yield"] = result_df["yield"].rank(ascending=False)
        result_df["all"] = result_df["rank_growth"] + result_df["rank_stability"] + result_df["rank_yield"]

        # print(result_df.sort_values(by="yield", ascending=False).head(5))
        # print(result_df.sort_values(by="growth", ascending=False).head(5))
        # print(result_df.sort_values(by="stability", ascending=False).head(5))
        # print(result_df.sort_values(by="all", ascending=True).head(5))
        return result_df
    
    def test_a_portfolio(self, list_of_stocks: list, start_date: datetime.datetime = datetime.date(2015, 12, 31)):
        result = []
        for x in list_of_stocks:

            temp = self.single_stock_checker.check_money_made_by_div(start_date, 5, x, self.combined_data, 100)
 
            if(temp.empty):
                continue
 
            temp_money_made = temp["money"].iloc[-1]
            result.append({
                "symbol": x,
                "money_made": temp_money_made
            })

        
        return pd.DataFrame(result)

    def check_along_time_axis(self):

        result = pd.DataFrame()
        for x in range(0, 20):

            temp_list_of_stocks = self.check_all_stocks(datetime.datetime(2000, 12, 31) + timedelta(days=365 * x))
            if(temp_list_of_stocks.empty):
                continue
            temp_df = self.test_a_portfolio(temp_list_of_stocks.sort_values(by="all", ascending=True)["symbol"][0:30].to_list(),
                                            datetime.datetime(2005, 12, 31) + timedelta(days=365 * x))
            
            temp_df["time_span"] = x


            if(x == 0):
                result = temp_df
            else:
                result = pd.concat([result, temp_df], ignore_index=True)
            pass
        # TODO change the path
        result.to_csv("test_along_time.csv")
        # result.to_csv("../../data/results/test_along_time.csv")
        pass