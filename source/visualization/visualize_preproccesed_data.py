"""
This Package is used to visualize the data from the preproccessing classes
"""

# from datetime import timedelta
# import pandas as pd

import json

import data_preprocessing.preproccess_classes as pre

# import matplotlib.pyplot as plt
# from plotly.offline import iplot
from plotly.subplots import make_subplots

# import plotly.express as px
import plotly.graph_objects as go
import plotly.express as px


import cufflinks

cufflinks.go_offline()

with open("../config.json", "r", encoding="utf-8") as file_data:
    file_names = json.load(file_data)


class VisualizeFMP:
    """
    This class is used to visualize the data from fmp
    (financial modeling prep)
    """

    def __init__(self, pre_fmp: pre.PreproccessingFMPData) -> None:

        self.preproccessed_data = pre_fmp.normalized_data_dividend
        self.preproccessed_data_stock = pre_fmp.normalized_stock_data

    def visualize_dividenden_data(self, stock_symbol: str):
        """
        This function is used to visualize the dividend data from fmp
        It will write the diagram to a html file
        """

        print(self.preproccessed_data.columns)

        df_to_plot = self.preproccessed_data[
            (self.preproccessed_data["variable"] == "adjDividend")
            & (self.preproccessed_data["symbol"] == stock_symbol)
        ][["date", "value"]]
        # df_to_plot["date"] = pd.to_datetime(df_to_plot["date"])

        # df_to_plot = df_to_plot.set_index("date")

        # plt.plot(df_to_plot)

        df_to_plot.iplot(
            kind="bar",
            x="date",
            y="value",
            title=f"Datetime plot '{stock_symbol}' from financal modeling prep",
            xTitle="date",
            yTitle="dividend",
            asFigure=True,
        ).write_html(
            file_names["basic_paths"]["visualize_data_path"]
            + f"{stock_symbol}_fmp_dividende.html"
        )

    def visualize_stock_as_candlestick(self, stock_symbol: str):
        """
        This function is used to visualize the stock data from fmp
        With a candlestick chart

        args:
            stock_symbol: str

        It will write the diagram to a html file

        """

        # only get where column stock_symbol is filled
        temp_df = self.preproccessed_data_stock[
            (self.preproccessed_data_stock["symbol"] == stock_symbol)
        ]

        temp_df = self.preproccessed_data_stock[
            (
                self.preproccessed_data_stock["variable"].isin(
                    ["open", "high", "low", "close"]
                )
            )
        ]

        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=temp_df["date"].dt.to_timestamp(),
                    open=temp_df[temp_df["variable"].isin(["open"])]["value"],
                    high=temp_df[temp_df["variable"].isin(["high"])]["value"],
                    low=temp_df[temp_df["variable"].isin(["low"])]["value"],
                    close=temp_df[temp_df["variable"].isin(["close"])]["value"],
                )
            ]
        )
        fig.write_html(
            file_names["basic_paths"]["visualize_data_path"]
            + f"{stock_symbol}_fmp_stock_candlestick.html"
        )

    def visualize_stock_data(self, stock_symbol: str):
        """
        This function is used to visualize the stock data from fmp
        It will write the diagram to a html file
        """

        df_to_plot = self.preproccessed_data_stock[
            (self.preproccessed_data_stock["variable"] == "low")
            & (self.preproccessed_data_stock["symbol"] == stock_symbol)
        ][["date", "value"]]

        # df_to_plot["date"] = pd.to_datetime(df_to_plot["date"])
        # df_to_plot = df_to_plot.set_index("date")

        # plt.plot(df_to_plot)

        df_to_plot.iplot(
            kind="line",
            x="date",
            y="value",
            title=f"Datetime plot '{stock_symbol}' from financal modeling prep",
            xTitle="x",
            yTitle="x",
            asFigure=True,
        ).write_html(
            file_names["basic_paths"]["visualize_data_path"]
            + f"{stock_symbol}_fmp_stock.html"
        )


class VisualizeAlphavantage:
    """
    This class is used to visualize the data from alphavantage
    """

    def __init__(self, pre_alpha: pre.PreproccessingAlphavantageData) -> None:

        self.preproccessed_data = pre_alpha.normalized_data

    def visualize_stock_as_candlestick(self, stock_symbol: str = "AAPL"):
        """
        The function is used to visualize the stock data from alphavantage
        With a candlestick chart

        args:
            stock_symbol: str

        It will write the diagram to a html file
        """

        df_with_selected_information = self.preproccessed_data[
            (self.preproccessed_data["information"].str.strip() == "close")
            | (self.preproccessed_data["information"].str.strip() == "open")
            | (self.preproccessed_data["information"].str.strip() == "high")
            | (self.preproccessed_data["information"].str.strip() == "low")
        ]

        # df_with_selected_information = df_with_selected_information\
        #                               .groupby(by="date").first().reset_index()

        stock_symbol_list_with_date = [stock_symbol] + ["date"] + ["information"]

        df_to_plot = df_with_selected_information[stock_symbol_list_with_date].copy()

        df_to_plot = df_to_plot.dropna(subset=[stock_symbol])

        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=df_to_plot["date"].dt.to_timestamp(),
                    open=df_to_plot[df_to_plot["information"].str.strip() == "open"][
                        stock_symbol
                    ],
                    high=df_to_plot[df_to_plot["information"].str.strip() == "high"][
                        stock_symbol
                    ],
                    low=df_to_plot[df_to_plot["information"].str.strip() == "low"][
                        stock_symbol
                    ],
                    close=df_to_plot[df_to_plot["information"].str.strip() == "close"][
                        stock_symbol
                    ],
                )
            ]
        )

        fig.update_layout(title=f"{stock_symbol} candlestick chart")
        # add x axis label
        fig.update_xaxes(title_text="Date")
        # add y axis label
        fig.update_yaxes(title_text="Price")
        fig.write_html(
            file_names["basic_paths"]["visualize_data_path"]
            + f"{stock_symbol}_alpha_stock_candlestick.html"
        )

    def visualize_stock_data(self, stock_symbol_list=None):
        """
        The function is used to visualize the stock data from alphavantage
        With a line chart

        args:
            stock_symbol_list: list[str]

        It will write the diagram to a html file
        """
        if stock_symbol_list is None:
            stock_symbol_list = ["AAPL", "ADBE", "MSFT"]

        # only take values where "closed" in column information stands
        df_with_selected_information = self.preproccessed_data[
            self.preproccessed_data["information"].str.strip() == "adjusted close"
        ]

        # for x in df_with_selected_information.columns:
        #     if(x \!= "date" \
        #          and x \!= "random_counter" \
        #          and x \!= "information" \
        #          and x \!= "index_extracted" \
        #          and x \!= "index"):
        #        df_with_selected_information[x] = df_with_selected_information\
        #                                          [df_with_selected_information[x] != 0][x]

        # TODO: one month later i can say you should probably use to_period
        # grouping the data by month so there
        # is no varriance occuring when plotting more than one column
        # for example
        # 2020-01-01 | 2020-01-02 --|transferd to|--> 2020-01-01 | 2020-01-01
        # ----------------------^-------------------------------------------^

        df_with_selected_information = (
            df_with_selected_information.groupby(by="date").first().reset_index()
        )

        # print(df_with_selected_information.columns)

        # careful attempts with .append() will not work as expected
        stock_symbol_list_with_date = stock_symbol_list + ["date"]

        # .copy() is only to remove the warning from pandas
        df_to_plot = df_with_selected_information[stock_symbol_list_with_date].copy()

        df_to_plot["date"] = df_to_plot["date"].dt.to_timestamp()

        # df_to_plot.iplot(
        #     kind="line",
        #     x="date",
        #     y=stock_symbol_list,
        #     title=f"Datetime plot '{stock_symbol_list}' from alphavantage",
        #     xTitle="date",
        #     yTitle="stock price",
        #     asFigure=True,
        # ).write_html(f"../data/vis/{stock_symbol_list}_alpha_stock.html")

        fig = px.line(
            data_frame=df_to_plot, x="date", y=stock_symbol_list, title="stock price"
        )
        fig.write_html(
            file_names["basic_paths"]["visualize_data_path"]
            + f"{stock_symbol_list}_alpha_stock.html"
        )

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

    def visualize_dividenden_data(self, stock_symbol_list=None):
        """
        This function is used to visualize the dividend data from alphavantage
        It will write the diagram to a html file

        args:
            stock_symbol_list: list[str]

        """
        if stock_symbol_list is None:
            stock_symbol_list = ["AAPL", "ADBE", "MSFT"]

        df_with_selected_information = self.preproccessed_data[
            self.preproccessed_data["information"].str.strip() == "dividend amount"
        ]

        df_with_selected_information = (
            df_with_selected_information.groupby(by="date")
            .mean(numeric_only=True)
            .reset_index()
        )

        stock_symbol_list_with_date = stock_symbol_list + ["date"]

        # .copy() is only to remove the warning from pandas
        df_to_plot = df_with_selected_information[stock_symbol_list_with_date].copy()

        # df_to_plot["date"] = df_to_plot["date"].dt.to_timestamp()
        # print(stock_symbol_list)
        # df_to_plot = df_to_plot.set_index("date")[stock_symbol_list]
        # df_to_plot.plot()

        # plt.show()
        df_to_plot.iplot(
            kind="bar",
            x="date",
            y=stock_symbol_list,
            title=f"Datetime plot '{stock_symbol_list}' from alphavantage",
            xTitle="date",
            yTitle="dividenden",
            asFigure=True,
        ).write_html(
            file_names["basic_paths"]["visualize_data_path"]
            + f"{stock_symbol_list}_alpha_dividenden.html"
        )


class VisualizeCombinedData:
    """
    this class is used to visualize the combined data from fmp and alphavantage
    While combined data means that they have the same structure
    and are on dates synchronized
    """

    def __init__(self, pre_combine: pre.PreproccessingCombinedData) -> None:
        self.pre_combine = pre_combine
        self.combined_data = pre_combine.combined_data

    def fmp_vs_alpha(self, stock_symbol: str = "ADBE"):
        """
        visualize the stock data from fmp and alphavantage in same diagram
        from a given stock symbol

        args:
            stock_symbol: str
        """

        # Filter for 'adjusted close' and 'close' rows
        filtered_df = self.combined_data[
            self.combined_data["information"].isin(["alpha_close", "fmp_close"])
        ]

        filtered_df = filtered_df[[stock_symbol, "date", "information"]]

        # Pivot the DataFrame to have 'adbe' as columns
        pivot_df = filtered_df.pivot_table(
            index="date", columns="information", values=stock_symbol, aggfunc="mean"
        ).rename(columns={"alpha_close": "alphavantage", "fmp_close": "fmp"})
        print(pivot_df)

        # group by information and date

        pivot_df.reset_index().iplot(
            kind="bar",
            x="date",
            y=["alphavantage", "fmp"],
            title=f"Datetime plot '{stock_symbol}'",
            xTitle="date",
            yTitle="dividenden",
            asFigure=True,
        ).write_html(
            file_names["basic_paths"]["visualize_data_path"]
            + f"{stock_symbol}_alpha_vs_fmp.html"
        )
        # plt.show()

    def alpha_stock_vs_alpha_dividend(self, stock_symbol: str = "ADBE"):
        """
        This function is used to visualize the stock data from fmp and the dividend data from fmp
        For a given stock symbol

        args:
            stock_symbol: str
        """

        # Filter for 'adjusted close' and 'close' rows
        print(self.combined_data["information"].unique())
        filtered_df = self.combined_data[
            self.combined_data["information"].isin(["alpha_close", "alpha_dividend"])
        ]

        filtered_df = filtered_df[[stock_symbol, "date", "information"]]
        filtered_df.sort_values(by="date", inplace=True)

        # alpha close
        df_alpha_close = filtered_df[
            filtered_df["information"].isin(["alpha_close"])
        ].dropna()
        # alpha dividend
        df_alpha_dividend = filtered_df[
            filtered_df["information"].isin(["alpha_dividend"])
        ].dropna()

        fig = make_subplots(specs=[[{"secondary_y": True}]])  # this a one cell subplot


        close_plot = go.Scatter(
            mode="lines",
            x=df_alpha_close["date"].dt.to_timestamp(),
            y=df_alpha_close[stock_symbol],
            name=f"close {stock_symbol}",
        )
        dividend_plot = go.Scatter(
            mode="lines",
            x=df_alpha_dividend["date"].dt.to_timestamp(),
            y=df_alpha_dividend[stock_symbol],
            name=f"dividend {stock_symbol}",
        )

        fig.add_trace(close_plot, secondary_y=True)
        fig.add_trace(dividend_plot, secondary_y=False)
        # add title to fig
        fig.update_layout(title=f"{stock_symbol} dividends vs stocks")

        fig.write_html(f"../data/vis/{stock_symbol}_stock_vs_dividend.html")

        # pivot_df.reset_index().iplot(kind="line", x="date",\
        #  y=['alpha_close', 'alpha_dividend'],\
        #  title=f"Datetime plot '{stock_symbol}'",\
        #  xTitle="date",\
        #  yTitle="dividenden",\
        #  asFigure=True).write_html(f"../data/vis/{stock_symbol}_stock_vs_dividend.html")
        # plt.show()
