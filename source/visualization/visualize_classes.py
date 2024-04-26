from datetime import timedelta
import pandas as pd
import json
import data_preprocessing.preproccess_classes as pre
import matplotlib.pyplot as plt
from plotly.offline import iplot
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
import data_business_logic.bussiness_logic_classes as bl


import cufflinks
cufflinks.go_offline()

class visualize_fmp():

    def __init__(self, pre_fmp: pre.preproccessing_fmp_data) -> None:
    
            self.preproccessed_data = pre_fmp.normalized_data_dividend
            self.preproccessed_data_stock = pre_fmp.normalized_stock_data

            

    def visualize_dividenden_data(self, stock_symbol:str):
        import matplotlib.pyplot as plt
        import seaborn as sns

        print(self.preproccessed_data.columns)

        df_to_plot = self.preproccessed_data[(self.preproccessed_data["variable"] == "adjDividend") & (self.preproccessed_data["symbol"] == stock_symbol) ][["date", "value"]]
        # df_to_plot["date"] = pd.to_datetime(df_to_plot["date"])
        
        # df_to_plot = df_to_plot.set_index("date")

        # plt.plot(df_to_plot)

        df_to_plot.iplot(kind="bar", x="date", y="value", title=f"Datetime plot '{stock_symbol}' from financal modeling prep", xTitle="date", yTitle="dividend", asFigure=True).write_html(f"../data/vis/{stock_symbol}_fmp_dividende.html")
        # df_to_plot.iplot(kind="line", x="date", y="value", title=f"Datetime plot '{stock_symbol}' from financal modeling prep", xTitle="x", yTitle="x", asFigure=True).write_html(f"../data/vis/{stock_symbol}_fmp_stock.html")

    pass

    def visualize_stock_as_candlestick(self, stock_symbol:str):

        # only get where column stock_symbol is filled
        temp_df = self.preproccessed_data_stock[(self.preproccessed_data_stock["symbol"] == stock_symbol)]

        
        temp_df = self.preproccessed_data_stock[(self.preproccessed_data_stock["variable"].isin(["open", "high", "low", "close"]))]



        fig = go.Figure(
             data=[go.Candlestick( x=temp_df["date"].dt.to_timestamp(),
                                    open=temp_df[temp_df["variable"].isin(["open"])]["value"],
                                    high=temp_df[temp_df["variable"].isin(["high"])]["value"],
                                    low=temp_df[temp_df["variable"].isin(["low"])]["value"],
                                    close=temp_df[temp_df["variable"].isin(["close"])]["value"]
                                    )]) 
        fig.write_html(f"../data/vis/{stock_symbol}_fmp_stock_candlestick.html")
         

    def visualize_stock_data(self, stock_symbol:str):
        
        import matplotlib.pyplot as plt
        import seaborn as sns



        df_to_plot = self.preproccessed_data_stock[(self.preproccessed_data_stock["variable"] == "low") 
                                             & (self.preproccessed_data_stock["symbol"] == stock_symbol) ][["date", "value"]]

        # df_to_plot["date"] = pd.to_datetime(df_to_plot["date"])
        # df_to_plot = df_to_plot.set_index("date")

        # plt.plot(df_to_plot)

        df_to_plot.iplot(kind="line", x="date", y="value", title=f"Datetime plot '{stock_symbol}' from financal modeling prep", xTitle="x", yTitle="x", asFigure=True).write_html(f"../data/vis/{stock_symbol}_fmp_stock.html")
        
        pass

class visualize_alphavantage():

    def __init__(self, pre_alpha: pre.preproccessing_alphavantage_data) -> None:
        
        self.preproccessed_data = pre_alpha.normalized_data

    
    def visualize_stock_as_candlestick(self, stock_symbol:str = "AAPL"):

        df_with_selected_information = self.preproccessed_data[(self.preproccessed_data["information"].str.strip() == "close") 
                                                               | (self.preproccessed_data["information"].str.strip() == "open") 
                                                               | (self.preproccessed_data["information"].str.strip() == "high") 
                                                               | (self.preproccessed_data["information"].str.strip() == "low")]

        
        # df_with_selected_information = df_with_selected_information.groupby(by="date").first().reset_index()

        stock_symbol_list_with_date = [stock_symbol] + ["date"] + ["information"]

        df_to_plot = df_with_selected_information[stock_symbol_list_with_date].copy()
        # df_to_plot = df_to_plot[df_to_plot["date"] > datetime.datetime.fromisoformat("2011-12-31T00:00:00")]
        # df_to_plot = df_to_plot[df_to_plot["date"] < datetime.datetime.fromisoformat("2016-12-31T00:00:00")]
        df_to_plot = df_to_plot.dropna(subset=[stock_symbol])
        print("hi")
        print(df_to_plot[df_to_plot["information"].str.strip() == "high"][stock_symbol])
        print(df_to_plot[df_to_plot["information"].str.strip() == "low"][stock_symbol])
        print(df_to_plot[df_to_plot["information"].str.strip() == "close"][stock_symbol])

        fig = go.Figure(
             data=[go.Candlestick( x=df_to_plot["date"].dt.to_timestamp(),
                                    open=df_to_plot[df_to_plot["information"].str.strip() == "open"][stock_symbol],
                                    high=df_to_plot[df_to_plot["information"].str.strip() == "high"][stock_symbol],
                                    low=df_to_plot[df_to_plot["information"].str.strip() == "low"][stock_symbol],
                                    close=df_to_plot[df_to_plot["information"].str.strip() == "close"][stock_symbol]
                                    )]) 
        
        fig.update_layout(title=f"{stock_symbol} candlestick chart")
        # add x axis label
        fig.update_xaxes(title_text="Date")
        # add y axis label
        fig.update_yaxes(title_text="Price")
        fig.write_html(f"../data/vis/{stock_symbol}_alpha_stock_candlestick.html")

    def visualize_stock_data(self, stock_symbol_list:list = ["AAPL","ADBE", "MSFT"]):
        

        # only take values where "closed" in column information stands
        df_with_selected_information = self.preproccessed_data[self.preproccessed_data["information"].str.strip() == "adjusted close"]

        # for x in df_with_selected_information.columns:
        #     if(x != "date" and x != "random_counter" and x != "information" and x != "index_extracted" and x != "index"):
        #        df_with_selected_information[x] = df_with_selected_information[df_with_selected_information[x] != 0][x]

        # grouping the data by month so there is no varriance occuring when plotting more than one column 
        # for example 
        # 2020-01-01 | 2020-01-02 --|transferd to|--> 2020-01-01 | 2020-01-01
        # ----------------------^-------------------------------------------^

        df_with_selected_information = df_with_selected_information.groupby(by="date").first().reset_index()

        # print(df_with_selected_information.columns)
        
        # careful attempts with .append() will not work as expected
        stock_symbol_list_with_date = stock_symbol_list + ["date"]

        print(df_with_selected_information)
        print(stock_symbol_list_with_date)

        # .copy() is only to remove the warning from pandas
        df_to_plot = df_with_selected_information[stock_symbol_list_with_date].copy()
        # df_to_plot = df_to_plot[df_to_plot["date"] > datetime.datetime.fromisoformat("2011-12-31T00:00:00")]
        # df_to_plot = df_to_plot[df_to_plot["date"] < datetime.datetime.fromisoformat("2022-12-31T00:00:00")]

        df_to_plot.iplot(kind="bar", x="date", y=stock_symbol_list, title=f"Datetime plot '{stock_symbol_list}' from alphavantage", xTitle="date", yTitle="stock price", asFigure=True).write_html(f"../data/vis/{stock_symbol_list}_alpha_stock.html")


        # df_to_plot["date"] = df_to_plot["date"].dt.to_timestamp()
        # df_to_plot.set_index("date", inplace=True)
        # # make a line plot
        # # make the line plot wider
        # plt.figure(figsize=(10,5))
        # # title
        # plt.title(f"{' '.join(stock_symbol_list)} Stock Price")
        # # ylabel
        # plt.ylabel("Price")
        # # xlabel
        # plt.xlabel("Date")
        # # reference line at 50 100 and 200
        # plt.axhline(50, color="gray", linestyle="--")
        # plt.axhline(100, color="gray", linestyle="--")
        # plt.axhline(200, color="gray", linestyle="--")

        # add xticks every 2 years



        # plot the data
        # plt.plot(df_to_plot)
        # plt.show()
    
    def visualize_dividenden_data(self, stock_symbol_list:list = ["COST","AAPL", "T"]):

        df_with_selected_information = self.preproccessed_data[self.preproccessed_data["information"].str.strip() == "dividend amount"]

        df_with_selected_information = df_with_selected_information.groupby(by="date").mean(numeric_only=True).reset_index()

        stock_symbol_list_with_date = stock_symbol_list + ["date"]
        
        # .copy() is only to remove the warning from pandas
        df_to_plot = df_with_selected_information[stock_symbol_list_with_date].copy()
        # df_to_plot = df_to_plot[df_to_plot["date"] > datetime.datetime.fromisoformat("2011-12-31")]
        # df_to_plot = df_to_plot[df_to_plot["date"] < datetime.datetime.fromisoformat("2016-12-31")]
        
        # df_to_plot["date"] = df_to_plot["date"].dt.to_timestamp()
        # print(stock_symbol_list)
        # df_to_plot = df_to_plot.set_index("date")[stock_symbol_list]
        # df_to_plot.plot()

        # plt.show()
        df_to_plot.iplot(kind="bar", x="date", y=stock_symbol_list, title=f"Datetime plot '{stock_symbol_list}' from alphavantage", xTitle="date", yTitle="dividenden", asFigure=True).write_html(f"../data/vis/dividend_data/{stock_symbol_list}_alpha_dividenden.html")
    
        pass

    def visualize_all_dividend_data(self):
        for x in self.preproccessed_data.columns:
            if(x == "information" or x == "index" or x == "index_extracted" or x == "random_counter" or x == "date" or x == "variable" or x == "value" or x == "symbol"):
                continue
            self.visualize_dividenden_data([x])

class visualize_combined_data():
     
    def __init__(self, pre_combine: pre.preproccessing_combined_data) -> None:
        self.pre_combine = pre_combine
        self.combined_data = pre_combine.combined_data
          

    def fmp_vs_alpha(self, stock_symbol:str = "ADBE"):

        # Filter for 'adjusted close' and 'close' rows
        filtered_df = self.combined_data[self.combined_data["information"].isin(['alpha_close', 'fmp_close'])]
        
        filtered_df = filtered_df[[stock_symbol, 'date', 'information']]
        
        # Pivot the DataFrame to have 'adbe' as columns
        pivot_df = filtered_df.pivot_table(index='date', columns='information', values=stock_symbol, aggfunc='mean').rename(columns={'alpha_close': 'alphavantage', 'fmp_close': 'fmp'})
        print(pivot_df)

        # group by information and date
        
        pivot_df.reset_index().iplot(kind="bar", x="date", y=['alphavantage', 'fmp'], title=f"Datetime plot '{stock_symbol}'", xTitle="date", yTitle="dividenden", asFigure=True).write_html(f"../data/vis/{stock_symbol}_alpha_vs_fmp.html")
        # plt.show()

        pass

    def fmp_stock_vs_fmp_dividend(self, stock_symbol:str = "ADBE"):

        # Filter for 'adjusted close' and 'close' rows
        print(self.combined_data["information"].unique())
        filtered_df = self.combined_data[self.combined_data["information"].isin(['alpha_close', 'alpha_dividend'])]
        
        filtered_df = filtered_df[[stock_symbol, 'date', 'information']]
        

        # Pivot the DataFrame to have 'adbe' as columns
        pivot_df = filtered_df.pivot_table(index='date', columns='information', values=stock_symbol, aggfunc='mean').rename(columns={'alpha_close': 'alpha_close', 'alpha_dividend': 'alpha_dividend'})
        print(pivot_df)

        pivot_df = pivot_df.reset_index()

        fig = make_subplots(specs=[[{"secondary_y": True}]])#this a one cell subplot

        close_plot = go.Scatter(mode="lines", x=pivot_df["date"].dt.to_timestamp(), y=pivot_df["alpha_close"], name=f"close {stock_symbol}")
        dividend_plot = go.Scatter(mode="lines", x=pivot_df["date"].dt.to_timestamp(), y=pivot_df["alpha_dividend"], name=f"dividend {stock_symbol}")

        fig.add_trace(close_plot, secondary_y=True)
        fig.add_trace(dividend_plot, secondary_y=False)
        # add title to fig
        fig.update_layout(title=f"{stock_symbol} dividends vs stocks")
        
        fig.write_html(f"../data/vis/{stock_symbol}_stock_vs_dividend.html")


        
        # pivot_df.reset_index().iplot(kind="line", x="date", y=['alpha_close', 'alpha_dividend'], title=f"Datetime plot '{stock_symbol}'", xTitle="date", yTitle="dividenden", asFigure=True).write_html(f"../data/vis/{stock_symbol}_stock_vs_dividend.html")
        # plt.show()

        pass

class visualize_single_stock_checker_results():
    def __init__(self) -> None:
        # data here is very different for every method so i dont think its good to have a general init
        pass

    
class visualize_result_data():
     
    def __init__(self, result_data: pd.DataFrame) -> None:
        
        self.result_data = result_data

    def visualize_scatter_plots(self):
        self.result_data.iplot(kind="bar", x="symbol", y="money_made", title="Top 30 symbols", xTitle="Symbol", yTitle="Money made (AVG)", asFigure=True).write_html(f"../data/vis/results_symbol_vs_money_made.html")
        self.result_data.iplot(kind="scatter", x="time_span", y="money_made", mode="markers", xTitle="Time span", yTitle="Money made", title="Money made vs time span", asFigure=True).write_html(f"../data/vis/results_time_span_vs_money_made.html")
        self.result_data.iplot(kind="scatter", x="look_forward_years", y="money_made", mode="markers", xTitle="Look forward years", yTitle="Money made", title="Money made vs look forward years", asFigure=True).write_html(f"../data/vis/results_look_forward_years_vs_money_made.html")
        self.result_data.iplot(kind="scatter", x="look_backward_years", y="money_made", mode="markers", xTitle="Look backward years", yTitle="Money made", title="Money made vs look backward years", asFigure=True).write_html(f"../data/vis/results_look_backward_years_vs_money_made.html")
        self.result_data.iplot(kind="scatter", x="all", y="money_made", mode="markers", xTitle="All", yTitle="Money made", title="Money made vs all", asFigure=True).write_html(f"../data/vis/results_all_vs_money_made.html")
        self.result_data.drop_duplicates(subset=["symbol","money_made"]).iplot(kind="scatter", x="all", y="money_made", mode="markers", xTitle="All", yTitle="Money made", title="Money made vs all", asFigure=True).write_html(f"../data/vis/results_all_vs_money_made_no_dup.html")

        self.result_data.iplot(kind="scatter", x="rank_growth", y="money_made", mode="markers", xTitle="Rank growth", yTitle="Money made", title="Money made vs rank growth", asFigure=True).write_html(f"../data/vis/results_rank_growth_vs_money_made.html")
        self.result_data.iplot(kind="scatter", x="rank_stability", y="money_made", mode="markers", xTitle="Rank stability", yTitle="Money made", title="Money made vs rank stability", asFigure=True).write_html(f"../data/vis/results_rank_stability_vs_money_made.html")
        self.result_data.iplot(kind="scatter", x="rank_yield", y="money_made", mode="markers", xTitle="Rank yield", yTitle="Money made", title="Money made vs rank yield", asFigure=True).write_html(f"../data/vis/results_rank_yield_vs_money_made.html")
        self.result_data.iplot(kind="scatter", x="yield", y="money_made", mode="markers", xTitle="Yield", yTitle="Money made", title="Money made vs yield", asFigure=True).write_html(f"../data/vis/results_yield_vs_money_made.html")
        self.result_data.iplot(kind="scatter", x="growth", y="money_made", mode="markers", xTitle="Growth", yTitle="Money made", title="Money made vs growth", asFigure=True).write_html(f"../data/vis/results_growth_vs_money_made.html")
        self.result_data.iplot(kind="scatter", x="stability", y="money_made", mode="markers", xTitle="Stability", yTitle="Money made", title="Money made vs stability", asFigure=True).write_html(f"../data/vis/results_stability_vs_money_made.html")


    def visualize_vs_msiw(self, combined_data: pd.DataFrame):
        """
        This function is used to compare all the data from the result data with the msci world stock.
        """

        # thats a little bit anyoing because, you need to know if the data is there on the time
        # whats the time you ask?
        # well its 1990 + 10 + 7 + x = 2007
        # so we look at the portfolio from 2007 to x years in the future
        # but important is that i dont show what happens if we sell after 1 year but after 4 years the first time
        # so the first future date is 2011
        # that is only an example and i want to try more than this
        # and obviously i want to compare data from the msi world with the same data as the portfolio
        # so the missing point is add the future date to the msci world stock

        year_selection = 11
        look_backward_years = 6

        local_single_stock_checker = bl.single_stock_check()

        # so the future date is calculated by
        # 1990 + year_selection + look_backward_years + look_forward_years
        # lookforward years variy between 3 and 10
        # for example 1990 + 15 + 6 + 3 = 2014 is the first year

        # msic_world_stock = msciw_data[msciw_data["information"].isin(["alpha_close"])]
        start_date = self.result_data[(self.result_data["time_span"] == year_selection)& (self.result_data["look_backward_years"] == look_backward_years)].groupby("future_date").first()["start_date"].iloc[0]
        # print(start_date, msciw_data.reset_index().columns)
        # print(msic_world_stock.reset_index().head(50))
        print(start_date)
        # print(start_date)
        # print(local_single_stock_checker.check_money_made_by_div(start_date=pd.to_datetime(start_date), look_foward_years=10, symbol="MSCI", df_combined=combined_data, money_invested=100))

        middle_date = pd.to_datetime(start_date) + timedelta(days = 365 * look_backward_years)
        start_investment = 100

        # works but adds 10 years idk why
        # print("hi", start_date, pd.to_datetime(start_date) + timedelta(days = 365 * 10))
        # print(pd.to_datetime(start_date) + timedelta(days = 365 * 4))
        list_msciworld = [{"money_made": local_single_stock_checker.check_money_made_by_div(start_date=pd.to_datetime(start_date) + timedelta(days = 365 * (look_backward_years)), look_foward_years=x, symbol="MSCI", df_combined=combined_data, money_invested=100).iloc[-1]["money"], "date": pd.to_datetime(start_date)+ timedelta(days = 365 * look_backward_years) + timedelta(days = 365 * x)} for x in range(3, 11)]
        list_msciworld = list_msciworld + [{"money_made":start_investment, "date": middle_date}]

        msic_money_made = pd.DataFrame(list_msciworld).sort_values(by="date")
        

        # print(msic_money_made)

        portfolio_progression = self.result_data[(self.result_data["time_span"] == year_selection)& (self.result_data["look_backward_years"] == look_backward_years)].groupby("future_date").mean(numeric_only=True).reset_index()[["future_date", "money_made"]]
        portfolio_progression["future_date"] = pd.to_datetime(portfolio_progression["future_date"])

        portfolio_progression = pd.concat([portfolio_progression, pd.DataFrame([{"money_made":start_investment, "future_date": middle_date}])]).sort_values(by="future_date")
        
        



        # print(portfolio_progression.columns)
        # print(portfolio_progression)

        # print(msic_money_made.head(10))
        fig = make_subplots(specs=[[{"secondary_y": True}]])#this a one cell subplot

        close_plot = go.Scatter(mode="lines", x=portfolio_progression["future_date"], y=portfolio_progression["money_made"], name=f"close from portfolio {year_selection+1990} to {year_selection+ 1990 + look_backward_years} years", line=dict(color='blue'))
        msci_plot = go.Scatter(mode="lines", x=msic_money_made["date"], y=msic_money_made["money_made"], name=f"msci world stock", line=dict(color='red'))

        fig.add_trace(close_plot, secondary_y=False)
        fig.add_trace(msci_plot, secondary_y=False)
        # add title to fig
        # its from (1990 + 10 + 7 + 3) = 2010 to (1990 + 10 + 7 + 3 + 7) = 2010
        fig.update_layout(title=f"msci world vs portfolio from {year_selection+look_backward_years+1990 + 3} to {year_selection+ 1990 + 3 + 7 + look_backward_years} years")
        
        fig.write_html(f"../data/vis/msci_world_vs_portfolio_{year_selection+ look_backward_years+ 1990 + 3}_{year_selection+ 1990 + look_backward_years + 3 + 7}.html")

    def visualize_histogram_plots(self):
        self.result_data[["money_made"]].iplot(kind="histogram", x="money_made", xTitle="Money made", yTitle="Frequency", title="Money made histogram", asFigure=True).write_html(f"../data/vis/histogram_money_made.html")
        # histogram symbols sort by frequency
        self.result_data["symbol"].value_counts().iplot(kind="bar", xTitle="Symbol", yTitle="Frequency", title="Symbol frequency", asFigure=True).write_html(f"../data/vis/histogram_.html")

        # histogram all sort by frequency
        self.result_data["all"].value_counts().iplot(kind="bar", xTitle="All", yTitle="Frequency", title="All frequency", asFigure=True).write_html(f"../data/vis/histogram_.html")



        # histogram but with timespan selected before
        
        for x in range(1, 30):
            if self.result_data[(self.result_data["time_span"] == x)].empty:
                        continue
            
            self.result_data[(self.result_data["time_span"] == x)]["money_made"].iplot(kind="histogram", x="money_made", xTitle="Money made", yTitle="Frequency", title="Money made histogram", asFigure=True).write_html(f"../data/vis/iteration_stuff/histogram_money_made_timespan_{1990+x}_combined.html")


            for y in range(3, 11):
                if self.result_data[(self.result_data["time_span"] == x)
                                        & (self.result_data["look_backward_years"] == y)].empty:
                        continue
                
                self.result_data[(self.result_data["time_span"] == x)
                                        & (self.result_data["look_backward_years"] == y)][["money_made"]].iplot(kind="histogram", x="money_made", xTitle="Money made", yTitle="Frequency", title="Money made histogram", asFigure=True).write_html(f"../data/vis/iteration_stuff/histogram_money_made_timespan_{1990+x}_look_forward{y}_combined.html")
                
                
                for z in range(3, 11):
                    if self.result_data[(self.result_data["time_span"] == x)
                                        & (self.result_data["look_backward_years"] == y)
                                        & (self.result_data["look_forward_years"] == z) ].empty:
                        continue

                    # self.result_data[(self.result_data["time_span"] == x)
                    #                     & (self.result_data["look_backward_years"] == y)
                    #                     & (self.result_data["look_forward_years"] == z) ][["money_made"]].iplot(kind="histogram", x="money_made", xTitle="Money made", yTitle="Frequency", title="Money made histogram", asFigure=True).write_html(f"../data/vis/iteration_stuff/histogram_money_made_timespan_{1990+x}_look_forward{y}_look_backwards{z}.html")
        





    def visualize_symbol_vs_money_made(self):
        """
        Actually it is really bad because of variable middle dates!
        """
        # histogram but with timespan selected before
        
        for x in range(1, 30):
            if self.result_data[(self.result_data["time_span"] == x)].empty:
                        continue
            
            self.result_data[(self.result_data["time_span"] == x)][["money_made", "symbol"]].groupby("symbol").mean().reset_index().iplot(kind="bar", y="money_made",x="symbol", xTitle="Money made", yTitle="Frequency", title="Money made histogram", asFigure=True).write_html(f"../data/vis/iteration_stuff/symbol_vs_money_made_timespan_{1990+x}_combined.html")


            for y in range(3, 11):
                if self.result_data[(self.result_data["time_span"] == x)
                                        & (self.result_data["look_backward_years"] == y)].empty:
                        continue
                
                to_plot = self.result_data[(self.result_data["time_span"] == x)
                                        & (self.result_data["look_backward_years"] == y)][["money_made", "symbol", "all"]].groupby("symbol").mean().reset_index().sort_values(by="all", ascending=False)
                
                fig = go.Figure()

                fig.add_trace(go.Bar(x=to_plot["symbol"], y=to_plot["money_made"], hovertext=to_plot["all"] ))
                
                fig.update_layout(title=f"Money made vs symbol timespan  Start_date: {1990+x}, Middle_date {1990+x+y} Future_date combined from {1990+x+y + 3} to {1990+x+y+10} years")
                fig.write_html(f"../data/vis/iteration_stuff/symbol_vs_money_made_timespan_{1990+x}_look_forward{y}_combined.html")

                # self.result_data[(self.result_data["time_span"] == x)
                #                         & (self.result_data["look_backward_years"] == y)].iplot(kind="bar", y="money_made",x="symbol",xTitle="Money made", yTitle="Frequency", title="Money made histogram", asFigure=True).write_html(f"../data/vis/iteration_stuff/symbol_vs_money_made_timespan_{1990+x}_look_forward{y}_combined.html")
                
                
                for z in range(3, 11):
                    if self.result_data[(self.result_data["time_span"] == x)
                                        & (self.result_data["look_backward_years"] == y)
                                        & (self.result_data["look_forward_years"] == z) ].empty:
                        continue

                    # self.result_data[(self.result_data["time_span"] == x)
                    #                     & (self.result_data["look_backward_years"] == y)
                    #                     & (self.result_data["look_forward_years"] == z) ][["money_made"]].iplot(kind="histogram", x="money_made", xTitle="Money made", yTitle="Frequency", title="Money made histogram", asFigure=True).write_html(f"../data/vis/iteration_stuff/histogram_money_made_timespan_{1990+x}_look_forward{y}_look_backwards{z}.html")
        

    def visualize_symbol_vs_money_made_same_middle_date(self):


        for y in range(11, 30):
            middle_year = y
            
            for x in range(3,11):
                
                temp_year_selection = middle_year-x
                temp_look_backward_years = x

                start_date = self.result_data[(self.result_data["time_span"] == temp_year_selection)& (self.result_data["look_backward_years"] == temp_look_backward_years)].groupby("future_date").first()["start_date"]
                if(start_date.empty):
                    continue
                start_date = start_date.iloc[0]

                # middle_date = pd.to_datetime(start_date) + timedelta(days = 365 * temp_look_backward_years)
                # start_investment = 100

                portfolio_progression = self.result_data[(self.result_data["time_span"] == temp_year_selection)& (self.result_data["look_backward_years"] == temp_look_backward_years)][["future_date", "money_made", "all", "symbol", "look_forward_years", "middle_date", "start_date"]]
                portfolio_progression["future_date"] = pd.to_datetime(portfolio_progression["future_date"])
                portfolio_progression["temp_look_backward_years"] = temp_look_backward_years

                # color_code the portfolio_progression["future_date"]
                
                print(portfolio_progression.sort_values(by="future_date"))
                input()
                

                fig = make_subplots(specs=[[{"secondary_y": True}]])
                fig.update_layout(title=f"Money made vs symbol, Year the Investment started: {1990+temp_year_selection + temp_look_backward_years}")
                for z in range(3,11):
                    
                    to_plot = portfolio_progression[portfolio_progression["look_forward_years"] == z]

                    
                    
                    bar_chart = go.Bar(x=to_plot["symbol"], y=to_plot["money_made"], hovertext=to_plot["future_date"], name=f"Sold end of year:{1990+temp_year_selection + temp_look_backward_years + z}")
                    fig.add_trace(bar_chart, secondary_y=False)
                    
                    
                fig.write_html(f"../data/vis/iteration_stuff/symbol_vs_money_made_middle_date{1990 + middle_year}.html")

                # portfolio_progression = pd.concat([portfolio_progression, pd.DataFrame([{"money_made":start_investment, "future_date": middle_date, "temp_look_backward_years": temp_look_backward_years}])]).sort_values(by="future_date")

    def visualize_symbol_vs_money_made_same_future_date(self):
         
         # save all portfolios which got sold on the same year 

        some_df = self.result_data.copy()


        some_df["together"] = (some_df["time_span"] + some_df["look_backward_years"] + some_df["look_forward_years"])
        
        for x in range(some_df["together"].min(), some_df["together"].max()):
            
            
            temp_df = some_df[(some_df["together"] == x)].sort_values(by="time_span", ascending=False)

            # if the time invested and the time sold are the same the result is the same so its no need to clutter the plot with the same data
            temp_df = temp_df.drop_duplicates(subset=["symbol", "money_made"])
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.update_layout(title=f"Money made vs symbol, Year the Investment ended: {1990+x}")

            # combine temp_df[["look_backward_years","look_forward_years", "time_span"] ] with \n
            temp_df["info"] = "past years: " +  temp_df["look_backward_years"].astype(str) + "\n years invested:" + temp_df["look_forward_years"].astype(str) + "\n start year" + (1990+ temp_df["time_span"]).astype(str)
                
            bar_chart = go.Bar(x=temp_df["symbol"], y=temp_df["money_made"], hovertext=temp_df["info"], name=f"Sold end of year:{1990 + x}")
            fig.add_trace(bar_chart, secondary_y=False)
            
                
            fig.write_html(f"../data/vis/iteration_stuff/symbol_vs_money_made_sold_on{1990 + x}.html")

    def visualize_portfolio_vs_money_made_same_future_date(self):
         
         # save all portfolios which got sold on the same year 

        some_df = self.result_data.copy()


        some_df["together"] = (some_df["time_span"] + some_df["look_backward_years"] + some_df["look_forward_years"])
        
        for x in range(some_df["together"].min(), some_df["together"].max()):
            
            
            temp_df = some_df[(some_df["together"] == x)].sort_values(by="time_span", ascending=False)

            # if the time invested and the time sold are the same the result is the same so its no need to clutter the plot with the same data
            temp_df = temp_df.groupby(by=["time_span", "look_backward_years", "look_forward_years"])["money_made"].mean().reset_index()
            
            # fig = make_subplots(specs=[[{"secondary_y": True}]])
            # fig.update_layout(title=f"Money made vs symbol, Year the Investment ended: {1990+x}")

            # combine temp_df[["look_backward_years","look_forward_years", "time_span"] ] with \n
            temp_df["info"] = "past years: " +  temp_df["look_backward_years"].astype(str) + "\n years invested:" + temp_df["look_forward_years"].astype(str) + "\n start year" + (1990+ temp_df["time_span"]).astype(str)
            
            temp_df["time_span_to_show"] = (temp_df["time_span"] + 1990).astype(str)
            

            fig = px.bar(temp_df, x="time_span_to_show", y="money_made",color="look_backward_years", hover_name="info", title=f"Sold end of year:{1990 + x}", color_continuous_scale=px.colors.sequential.Viridis, barmode="group")
            
            
                
            fig.write_html(f"../data/vis/iteration_stuff/portfolio_vs_money_made_sold_on{1990 + x}.html")
    
    def visualize_portfolios_with_same_middledate(self):
            """
            
            """

            
            for y in range(11, 30):
                middle_year = y
                
                to_plot = pd.DataFrame()
                for x in range(3,11):
                    
                    temp_year_selection = middle_year-x
                    temp_look_backward_years = x

                    start_date = self.result_data[(self.result_data["time_span"] == temp_year_selection)& (self.result_data["look_backward_years"] == temp_look_backward_years)].groupby("future_date").first()["start_date"]
                    if(start_date.empty):
                        continue
                    start_date = start_date.iloc[0]

                    # middle_date = pd.to_datetime(start_date) + timedelta(days = 365 * temp_look_backward_years)
                    # start_investment = 100


                    portfolio_progression = self.result_data[(self.result_data["time_span"] == temp_year_selection)& (self.result_data["look_backward_years"] == temp_look_backward_years)].groupby("future_date").mean(numeric_only=True).reset_index()[["future_date", "money_made"]]
                    portfolio_progression["future_date"] = pd.to_datetime(portfolio_progression["future_date"])
                    portfolio_progression["temp_look_backward_years"] = temp_look_backward_years
                    # portfolio_progression = pd.concat([portfolio_progression, pd.DataFrame([{"money_made":start_investment, "future_date": middle_date, "temp_look_backward_years": temp_look_backward_years}])]).sort_values(by="future_date")

                    to_plot = pd.concat([to_plot, portfolio_progression])

                to_plot = to_plot.pivot_table(index="future_date", columns="temp_look_backward_years", values="money_made", aggfunc="mean").reset_index()
                


                fig = make_subplots(specs=[[{"secondary_y": True}]])#this a one cell subplot
                fig.update_layout(title=f"all portfolios with same middle date")
                for x in to_plot.columns:
                    if x == "future_date":
                        continue
                    fig.add_trace(go.Scatter(mode="lines", x=to_plot["future_date"], y=to_plot[x], name=f"portfolio with {x} years looked back, date in the middle is {1990 + middle_year}"), secondary_y=False)
                fig.write_html(f"../data/vis/portfolios_with_same_middle_date{1990+middle_year}.html")