import pandas as pd
import json
import data_preprocessing.preproccess_classes as pre
import matplotlib.pyplot as plt

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
        
        df_to_plot = df_to_plot.set_index("date")

        # plt.plot(df_to_plot)

        df_to_plot.plot()
        plt.show()

    pass

    def visualize_stock_data(self, stock_symbol:str):
        
        import matplotlib.pyplot as plt
        import seaborn as sns



        df_to_plot = self.preproccessed_data_stock[(self.preproccessed_data_stock["variable"] == "low") 
                                             & (self.preproccessed_data_stock["symbol"] == stock_symbol) ][["date", "value"]]

        # df_to_plot["date"] = pd.to_datetime(df_to_plot["date"])
        df_to_plot = df_to_plot.set_index("date")

        # plt.plot(df_to_plot)

        df_to_plot.plot()
        
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

        print(df_to_plot.columns)

        df_to_plot["date"] = df_to_plot["date"].dt.to_timestamp()
        df_to_plot.set_index("date", inplace=True)
        # make a line plot
        # make the line plot wider
        plt.figure(figsize=(10,5))
        # title
        plt.title(f"{' '.join(stock_symbol_list)} Stock Price")
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
    
    def visualize_dividenden_data(self, stock_symbol_list:list = ["COST","AAPL", "T"]):

        df_with_selected_information = self.preproccessed_data[self.preproccessed_data["information"].str.strip() == "dividend amount"]

        df_with_selected_information = df_with_selected_information.groupby(by="date").mean(numeric_only=True).reset_index()

        stock_symbol_list_with_date = stock_symbol_list + ["date"]
        
        # .copy() is only to remove the warning from pandas
        df_to_plot = df_with_selected_information[stock_symbol_list_with_date].copy()
        # df_to_plot = df_to_plot[df_to_plot["date"] > datetime.datetime.fromisoformat("2011-12-31")]
        # df_to_plot = df_to_plot[df_to_plot["date"] < datetime.datetime.fromisoformat("2016-12-31")]
        
        df_to_plot["date"] = df_to_plot["date"].dt.to_timestamp()
        print(stock_symbol_list)
        df_to_plot = df_to_plot.set_index("date")[stock_symbol_list]
        df_to_plot.plot()

        plt.show()
    
        pass

class visualize_combined_data():
     
    def __init__(self, combined_data: pd.DataFrame) -> None:
        self.combined_data = combined_data
          

    def fmp_vs_alpha(self, stock_symbol:str = "ADBE"):


        df_adbe = self.combined_data[[stock_symbol,"information", "date"]]
        # df_adbe["date"] = pd.dt.to_datetime(df_adbe["date"])

        df_adbe_fmp_stock = df_adbe[df_adbe["information"] == "close"]
        df_adbe_alpha_stock = df_adbe[df_adbe["information"].str.contains("adjusted close")]
        
        df_adbe_fmp_stock = df_adbe_fmp_stock.set_index("date")
        df_adbe_alpha_stock = df_adbe_alpha_stock.set_index("date")

        # plot only fmp
        df_adbe_fmp_stock.plot()
        df_adbe_alpha_stock.plot()
        
        
        plt.show()
        pass