import pandas as pd
import json
import preproccess_classes as pre
import matplotlib.pyplot as plt

class visualize_fmp():

    def __init__(self) -> None:
            
            pre_fmp = pre.preproccessing_fmp_data()
    
            self.preproccessed_data = pre_fmp.normalize_dividenden_data()
            self.preproccessed_data_stock = pre_fmp.normalize_stock_data()

    def visualize_dividenden_data(self, stock_symbol:str):
        import matplotlib.pyplot as plt
        import seaborn as sns

        print(self.preproccessed_data.columns)

        df_to_plot = self.preproccessed_data[(self.preproccessed_data["variable"] == "adjDividend") & (self.preproccessed_data["symbol"] == "AAPL") ][["date", "value"]]
        # df_to_plot["date"] = pd.to_datetime(df_to_plot["date"])
        
        df_to_plot = df_to_plot.set_index("date")

        # plt.plot(df_to_plot)

        df_to_plot.plot()
        plt.show()

    pass

    def visualize_stock_data(self, stock_symbol:str):
        
        import matplotlib.pyplot as plt
        import seaborn as sns



        df_to_plot = self.preproccessed_data_stock[(self.preproccessed_data_stock["variable"] == "low") 
                                             & (self.preproccessed_data_stock["symbol"] == "MSFT") ][["date", "value"]]

        # df_to_plot["date"] = pd.to_datetime(df_to_plot["date"])
        df_to_plot = df_to_plot.set_index("date")

        # plt.plot(df_to_plot)

        df_to_plot.plot()
        
        pass

class visualize_alphavantage():

    def __init__(self) -> None:
        
        pre_alpha = pre.preproccessing_alphavantage_data()

        self.preproccessed_data = pre_alpha.normalize_data()

    def visualize_stock_data(self, stock_symbol:str):
        

        # only take values where "closed" in column information stands
        df_with_selected_information = self.preproccessed_data[self.preproccessed_data["information"].str.strip() == "adjusted close"]

        # for x in df_with_selected_information.columns:
        #     if(x != "date" and x != "random_counter" and x != "information" and x != "index_extracted" and x != "index"):
        #        df_with_selected_information[x] = df_with_selected_information[df_with_selected_information[x] != 0][x]

        # grouping the data by month so there is no varriance occuring when plotting more than one column 
        # for example 
        # 2020-01-01 | 2020-01-02 --|transferd to|--> 2020-01-01 | 2020-01-01
        # ----------------------^-------------------------------------------^

        df_with_selected_information = df_with_selected_information.groupby(pd.Grouper(freq='M', key="date")).first().reset_index()

        # print(df_with_selected_information.columns)

        df_to_plot = df_with_selected_information[["AAPL","ADBE", "MSFT", "date"]]
        # df_to_plot = df_to_plot[df_to_plot["date"] > datetime.datetime.fromisoformat("2011-12-31T00:00:00")]
        # df_to_plot = df_to_plot[df_to_plot["date"] < datetime.datetime.fromisoformat("2022-12-31T00:00:00")]

        print(df_to_plot.columns)


        df_to_plot.set_index("date", inplace=True)
        # make a line plot
        # make the line plot wider
        plt.figure(figsize=(10,5))
        # title
        plt.title("Apple Stock Price")
        # ylabel
        plt.ylabel("Price")
        # xlabel
        plt.xlabel("Date")
        # reference line at 50 100 and 200
        plt.axhline(50, color="gray", linestyle="--")
        plt.axhline(100, color="gray", linestyle="--")
        plt.axhline(200, color="gray", linestyle="--")

        # add xticks every 2 years



        # plot the data
        plt.plot(df_to_plot)
        plt.show()
    
    def visualize_dividenden_data(self, stock_symbol:str):

        df_with_selected_information = self.preproccessed_data[self.preproccessed_data["information"].str.strip() == "dividend amount"]

        df_with_selected_information = df_with_selected_information.groupby(pd.Grouper(freq='Y', key="date")).mean(numeric_only=True).reset_index()

        df_to_plot = df_with_selected_information[["COST","AAPL", "T", "date"]]
        # df_to_plot = df_to_plot[df_to_plot["date"] > datetime.datetime.fromisoformat("2011-12-31")]
        # df_to_plot = df_to_plot[df_to_plot["date"] < datetime.datetime.fromisoformat("2016-12-31")]

        df_to_plot = df_to_plot.set_index("date")[["COST","AAPL", "T"]]
        df_to_plot.plot()

        plt.show()
    
        pass

    