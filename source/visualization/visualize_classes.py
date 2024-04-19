import pandas as pd
import json
import data_preprocessing.preproccess_classes as pre
import matplotlib.pyplot as plt
from plotly.offline import iplot

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

        df_to_plot.iplot(kind="line", x="date", y="value", title=f"Datetime plot '{stock_symbol}' from financal modeling prep", xTitle="date", yTitle="dividend", asFigure=True).write_html(f"../data/vis/{stock_symbol}_fmp_dividende.html")
        # df_to_plot.iplot(kind="line", x="date", y="value", title=f"Datetime plot '{stock_symbol}' from financal modeling prep", xTitle="x", yTitle="x", asFigure=True).write_html(f"../data/vis/{stock_symbol}_fmp_stock.html")

    pass

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
        df_to_plot.iplot(kind="bar", x="date", y=stock_symbol_list, title=f"Datetime plot '{stock_symbol_list}' from alphavantage", xTitle="date", yTitle="dividenden", asFigure=True).write_html(f"../data/vis/{stock_symbol_list}_alpha_dividenden.html")
    
        pass

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

        # group by information and date
        
        pivot_df.reset_index().iplot(kind="line", x="date", y=['alpha_close', 'alpha_dividend'], title=f"Datetime plot '{stock_symbol}'", xTitle="date", yTitle="dividenden", asFigure=True).write_html(f"../data/vis/{stock_symbol}_stock_vs_dividend.html")
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

    def visualize_histogram_plots(self):
        self.result_data[["money_made"]].iplot(kind="histogram", x="money_made", xTitle="Money made", yTitle="Frequency", title="Money made histogram", asFigure=True).write_html(f"../data/vis/histogram_money_made.html")
        # histogram but with timespan selected before
        
        for x in range(1, 30):
            for y in range(3, 11):
                for z in range(3, 11):
                    if self.result_data[(self.result_data["time_span"] == x)
                                        & (self.result_data["look_backward_years"] == y)
                                        & (self.result_data["look_forward_years"] == z) ].empty:
                        continue

                    self.result_data[(self.result_data["time_span"] == x)
                                        & (self.result_data["look_backward_years"] == y)
                                        & (self.result_data["look_forward_years"] == z) ][["money_made"]].iplot(kind="histogram", x="money_made", xTitle="Money made", yTitle="Frequency", title="Money made histogram", asFigure=True).write_html(f"../data/vis/histogram_money_made_timespan_{1990+x}_look_forward{y}_look_backwards{z}.html")
        # histogram symbols sort by frequency
        self.result_data["symbol"].value_counts().iplot(kind="bar", xTitle="Symbol", yTitle="Frequency", title="Symbol frequency", asFigure=True).write_html(f"../data/vis/histogram_.html")

        # histogram all sort by frequency
        self.result_data["all"].value_counts().iplot(kind="bar", xTitle="All", yTitle="Frequency", title="All frequency", asFigure=True).write_html(f"../data/vis/histogram_.html")

    def visualize_per_iteration(self):
        for x in range(1, 30):
            for y in range(3, 11):
                for z in range(3, 11):
                    if self.result_data[(self.result_data["time_span"] == x)
                                        & (self.result_data["look_backward_years"] == y)
                                        & (self.result_data["look_forward_years"] == z) ].empty:
                        continue

                    self.result_data[(self.result_data["time_span"] == x)
                                        & (self.result_data["look_backward_years"] == y)
                                        & (self.result_data["look_forward_years"] == z) ].iplot(kind="bar", x="symbol",y="money_made" ,xTitle="ticker symbol", yTitle="money made", title="Money made by symbol", asFigure=True).write_html(f"../data/vis/iteration_stuff/money_made_timespan_{1990+x}_look_forward{y}_look_backwards{z}.html")
