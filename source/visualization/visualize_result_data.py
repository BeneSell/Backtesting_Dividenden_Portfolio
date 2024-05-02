"""
visualize the results data 
"""

from datetime import timedelta
import pandas as pd

# import matplotlib.pyplot as plt
# from plotly.offline import iplot
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go

import data_business_logic.strategie_execution as str_exec
import data_business_logic.strategie_data_interface as str_data

import cufflinks

cufflinks.go_offline()


class VisualizeResultData:
    """
    This class is used to visualize the results from the business logic classes
    Mostly from the results of the function check_along_time_and_timespan
    """

    def __init__(self, result_data: pd.DataFrame) -> None:

        self.result_data = result_data

    def visualize_scatter_plots(self):
        """
        Generate some basic scatter plots

        - rank_growth vs money_made
        - rank_stability vs money_made
        - rank_yield vs money_made
        - yield vs money_made
        - growth vs money_made
        - stability vs money_made
        - all vs money_made (no duplicates)

        all written to a html file
        """
        self.result_data.iplot(
            kind="bar",
            x="symbol",
            y="money_made",
            title="Top 30 symbols",
            xTitle="Symbol",
            yTitle="Money made (AVG)",
            asFigure=True,
        ).write_html("../data/vis/results_symbol_vs_money_made.html")
        self.result_data.iplot(
            kind="scatter",
            x="time_span",
            y="money_made",
            mode="markers",
            xTitle="Time span",
            yTitle="Money made",
            title="Money made vs time span",
            asFigure=True,
        ).write_html("../data/vis/results_time_span_vs_money_made.html")
        self.result_data.iplot(
            kind="scatter",
            x="look_forward_years",
            y="money_made",
            mode="markers",
            xTitle="Look forward years",
            yTitle="Money made",
            title="Money made vs look forward years",
            asFigure=True,
        ).write_html("../data/vis/results_look_forward_years_vs_money_made.html")
        self.result_data.iplot(
            kind="scatter",
            x="look_backward_years",
            y="money_made",
            mode="markers",
            xTitle="Look backward years",
            yTitle="Money made",
            title="Money made vs look backward years",
            asFigure=True,
        ).write_html("../data/vis/results_look_backward_years_vs_money_made.html")

        self.result_data.iplot(
            kind="scatter",
            x="all",
            y="money_made",
            mode="markers",
            xTitle="All",
            yTitle="Money made",
            title="Money made vs all",
            asFigure=True,
        ).write_html("../data/vis/results_all_vs_money_made.html")
        self.result_data.drop_duplicates(subset=["symbol", "money_made"]).iplot(
            kind="scatter",
            x="all",
            y="money_made",
            mode="markers",
            xTitle="All",
            yTitle="Money made",
            title="Money made vs all",
            asFigure=True,
        ).write_html("../data/vis/results_all_vs_money_made_no_dup.html")

    def visualize_vs_msiw(self, combined_data: pd.DataFrame):
        """
        This function is used to compare all the data from the result data
        with the msci world stock.

        args:
            combined_data: pd.DataFrame

        """

        # thats a little bit anyoing because,
        # you need to know if the data is there on the time
        # whats the time you ask?
        # well its 1990 + 10 + 7 + x = 2007
        # so we look at the portfolio from 2007 to x years in the future
        # but important is that
        # i dont show what happens if we sell after 1 year but after 4 years the first time
        # so the first future date is 2011
        # that is only an example and i want to try more than this
        # and obviously i want to compare data from the msi world
        # with the same data as the portfolio
        # so the missing point is add the future date to the msci world stock

        look_backward_years = 12
        strategie_execution = str_exec.StrategieExecution(combined_data)
        calc_data = str_data.StrategieDataInterface()

        for year_selection in range(1, 30):
            

            # so the future date is calculated by
            # 1990 + year_selection + look_backward_years + look_forward_years
            # lookforward years variy between 3 and 10
            # for example 1990 + 15 + 6 + 3 = 2014 is the first year

            # msic_world_stock = msciw_data[msciw_data["information"].isin(["alpha_close"])]
            start_date_list_type = (
                self.result_data[
                    (self.result_data["time_span"] == year_selection)
                    & (self.result_data["look_backward_years"] == look_backward_years)
                ]
                .groupby("future_date")
                .first()["start_date"]
            )
            if start_date_list_type.empty:
                continue
            start_date = start_date_list_type.iloc[0]
            # print(start_date, msciw_data.reset_index().columns)
            # print(msic_world_stock.reset_index().head(50))
            print(start_date)

            middle_date = pd.to_datetime(start_date) + timedelta(
                days=365 * look_backward_years
            )
            start_investment = 100

            list_msciworld = [
                {
                    "money_made": calc_data.check_money_made_by_div(
                        start_date=pd.to_datetime(start_date)
                        + timedelta(days=365 * (look_backward_years)),
                        look_foward_years=x,
                        symbol="MSCI",
                        df_combined=combined_data,
                        money_invested=100,
                    ).iloc[-1]["money"],
                    "date": pd.to_datetime(start_date)
                    + timedelta(days=365 * look_backward_years)
                    + timedelta(days=365 * x),
                }
                for x in range(1, 4)
            ]
            list_msciworld = list_msciworld + [
                {"money_made": start_investment, "date": middle_date}
            ]

            msci_money_made = pd.DataFrame(list_msciworld).sort_values(by="date")

            # print(msic_money_made)

            portfolio_progression = (
                self.result_data[
                    (self.result_data["time_span"] == year_selection)
                    & (self.result_data["look_backward_years"] == look_backward_years)
                ]
                .groupby("future_date")
                .mean(numeric_only=True)
                .reset_index()[["future_date", "money_made"]]
            )
            portfolio_progression["future_date"] = pd.to_datetime(
                portfolio_progression["future_date"]
            )

            portfolio_progression = pd.concat(
                [
                    portfolio_progression,
                    pd.DataFrame(
                        [{"money_made": start_investment, "future_date": middle_date}]
                    ),
                ]
            ).sort_values(by="future_date")

            # print(portfolio_progression.columns)
            # print(portfolio_progression)

            # print(msic_money_made.head(10))
            if not isinstance(msci_money_made, pd.DataFrame):
                msci_money_made = pd.DataFrame()

            fig = make_subplots(specs=[[{"secondary_y": True}]])  # this a one cell subplot

            close_plot = go.Scatter(
                mode="lines",
                x=portfolio_progression["future_date"],
                y=portfolio_progression["money_made"],
                name=f"close from portfolio {year_selection+1990}"
                f"to {year_selection+ 1990 + look_backward_years} years",
                line=dict(color="blue"),
            )
            msci_plot = go.Scatter(
                mode="lines",
                x=msci_money_made["date"],
                y=msci_money_made["money_made"],
                name="msci world stock",
                line=dict(color="red"),
            )

            fig.add_trace(close_plot, secondary_y=False)
            fig.add_trace(msci_plot, secondary_y=False)
            # add title to fig
            # its from (1990 + 10 + 7 + 3) = 2010 to (1990 + 10 + 7 + 3 + 7) = 2010
            fig.update_layout(
                title=f"msci world vs portfolio from"
                f"{year_selection+look_backward_years+1990}"
                f"to {year_selection+ 1990 +  look_backward_years + 3} years"
            )

            fig.write_html(
                "../data/vis/iteration_stuff/msci_world_vs_portfolio_"
                f"{year_selection+ look_backward_years+ 1990}"
                f"_{year_selection+ 1990 + look_backward_years + 3}.html"
            )

    def visualize_histogram_plots(self):
        """
        This function is used to visualize the histogram plots from the result data
        """
        self.result_data[["money_made"]].iplot(
            kind="histogram",
            x="money_made",
            xTitle="Money made",
            yTitle="Frequency",
            title="Money made histogram",
            asFigure=True,
        ).write_html("../data/vis/histogram_money_made.html")
        # histogram symbols sort by frequency
        self.result_data["symbol"].value_counts().iplot(
            kind="bar",
            xTitle="Symbol",
            yTitle="Frequency",
            title="Symbol frequency",
            asFigure=True,
        ).write_html("../data/vis/histogram_.html")

        # histogram all sort by frequency
        self.result_data["all"].value_counts().iplot(
            kind="bar",
            xTitle="All",
            yTitle="Frequency",
            title="All frequency",
            asFigure=True,
        ).write_html("../data/vis/histogram_.html")

        # histogram but with timespan selected before

        for x in range(1, 30):
            if self.result_data[(self.result_data["time_span"] == x)].empty:
                continue

            self.result_data[(self.result_data["time_span"] == x)]["money_made"].iplot(
                kind="histogram",
                x="money_made",
                xTitle="Money made",
                yTitle="Frequency",
                title="Money made histogram",
                asFigure=True,
            ).write_html(
                "../data/vis/iteration_stuff/"
                f"histogram_money_made_timespan_{1990+x}_combined.html"
            )

            for y in range(3, 11):
                if self.result_data[
                    (self.result_data["time_span"] == x)
                    & (self.result_data["look_backward_years"] == y)
                ].empty:
                    continue

                self.result_data[
                    (self.result_data["time_span"] == x)
                    & (self.result_data["look_backward_years"] == y)
                ][["money_made"]].iplot(
                    kind="histogram",
                    x="money_made",
                    xTitle="Money made",
                    yTitle="Frequency",
                    title="Money made histogram",
                    asFigure=True,
                ).write_html(
                    "../data/vis/iteration_stuff/"
                    f"histogram_money_made_timespan_{1990+x}"
                    f"_look_forward{y}_combined.html"
                )

                for z in range(3, 11):
                    if self.result_data[
                        (self.result_data["time_span"] == x)
                        & (self.result_data["look_backward_years"] == y)
                        & (self.result_data["look_forward_years"] == z)
                    ].empty:
                        continue

                    # self.result_data[(self.result_data["time_span"] == x)
                    #                     & (self.result_data["look_backward_years"] == y)
                    #                     & (self.result_data["look_forward_years"] == z) ]\
                    #                        [["money_made"]].iplot(kind="histogram",\
                    #                        x="money_made",\
                    #                        xTitle="Money made",\
                    #                        yTitle="Frequency",\
                    #                        title="Money made histogram",\
                    #                        asFigure=True)\
                    #                   .write_html("../data/vis/iteration_stuff/"\
                    #                   f"histogram_money_made_timespan_{1990+x}"\
                    #                   f"_look_forward{y}_look_backwards{z}.html")

    def visualize_symbol_vs_money_made(self):
        """
        Actually it is really bad because of variable middle dates!
        """
        # histogram but with timespan selected before

        for x in range(1, 30):
            if self.result_data[(self.result_data["time_span"] == x)].empty:
                continue

            self.result_data[(self.result_data["time_span"] == x)][
                ["money_made", "symbol"]
            ].groupby("symbol").mean().reset_index().iplot(
                kind="bar",
                y="money_made",
                x="symbol",
                xTitle="Money made",
                yTitle="Frequency",
                title="Money made histogram",
                asFigure=True,
            ).write_html(
                f"../data/vis/iteration_stuff/"
                f"symbol_vs_money_made_timespan_{1990+x}_combined.html"
            )

            for y in range(3, 11):
                if self.result_data[
                    (self.result_data["time_span"] == x)
                    & (self.result_data["look_backward_years"] == y)
                ].empty:
                    continue

                to_plot = (
                    self.result_data[
                        (self.result_data["time_span"] == x)
                        & (self.result_data["look_backward_years"] == y)
                    ][["money_made", "symbol", "all"]]
                    .groupby("symbol")
                    .mean()
                    .reset_index()
                    .sort_values(by="all", ascending=False)
                )

                fig = go.Figure()

                fig.add_trace(
                    go.Bar(
                        x=to_plot["symbol"],
                        y=to_plot["money_made"],
                        hovertext=to_plot["all"],
                    )
                )

                fig.update_layout(
                    title=f"Money made vs symbol timespan  Start_date:"
                    f"{1990+x}, Middle_date {1990+x+y} "
                    f"Future_date combined from {1990+x+y + 3} to {1990+x+y+10} years"
                )
                fig.write_html(
                    "../data/vis/iteration_stuff/"
                    f"symbol_vs_money_made_timespan_"
                    f"{1990+x}_look_forward{y}_combined.html"
                )

                for z in range(3, 11):
                    if self.result_data[
                        (self.result_data["time_span"] == x)
                        & (self.result_data["look_backward_years"] == y)
                        & (self.result_data["look_forward_years"] == z)
                    ].empty:
                        continue

                    # here we could do actions per portfolio



    def visualize_symbol_vs_money_after_three_years(self):
        """
        This function is used to visualize the symbol vs money made
        """
        # save all portfolios which got sold on the same year

        some_df = self.result_data.copy()

        some_df["together"] = (
            some_df["time_span"]
            + some_df["look_backward_years"]
            + some_df["look_forward_years"]
        )

        # filter some_df that look_forward_years is 3
        some_df = some_df[some_df["look_forward_years"] == 3]

        for x in range(some_df["together"].min(), some_df["together"].max()):

            temp_df = some_df[(some_df["together"] == x)].sort_values(
                by="time_span", ascending=False
            )

            # if the time invested and the time sold are the same the result
            # is the same so its no need to clutter the plot with the same data
            temp_df = temp_df.drop_duplicates(subset=["symbol", "money_made"])
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.update_layout(
                title=f"Money made vs symbol, Year the Investment ended: {1990+x}"
            )

            # combine temp_df[["look_backward_years","look_forward_years", "time_span"] ] with \n
            temp_df["info"] = (
                "past years: "
                + temp_df["look_backward_years"].astype(str)
                + "\n years invested:"
                + temp_df["look_forward_years"].astype(str)
                + "\n start year"
                + (1990 + temp_df["time_span"]).astype(str)
            )

            bar_chart = go.Bar(
                x=temp_df["symbol"],
                y=temp_df["money_made"],
                hovertext=temp_df["info"],
                name=f"Sold end of year:{1990 + x}",
            )
            fig.add_trace(bar_chart, secondary_y=False)

            fig.write_html(
                "../data/vis/iteration_stuff/"
                f"symbol_vs_money_made_sold_on{1990 + x}.html"
            )

    def visualize_portfolio_vs_money_made_same_future_date(self):
        """
        This function is used to visualize the portfolio vs money made
        But with the same future date
        that means the same date where the investment got sold
        """

        # save all portfolios which got sold on the same year

        some_df = self.result_data.copy()

        some_df["together"] = (
            some_df["time_span"]
            + some_df["look_backward_years"]
            + some_df["look_forward_years"]
        )

        for x in range(some_df["together"].min(), some_df["together"].max()):

            temp_df = some_df[(some_df["together"] == x)].sort_values(
                by="time_span", ascending=False
            )

            # if the time invested and the time sold
            # are the same the result is
            # the same so its no need to clutter the plot with the same data
            temp_df = (
                temp_df.groupby(
                    by=["time_span", "look_backward_years", "look_forward_years"]
                )["money_made"]
                .mean()
                .reset_index()
            )

            # fig = make_subplots(specs=[[{"secondary_y": True}]])
            # fig.update_layout(title=f"Money made vs symbol, Year the Investment ended: {1990+x}")

            # combine temp_df[["look_backward_years","look_forward_years", "time_span"] ] with \n
            temp_df["info"] = (
                "past years: "
                + temp_df["look_backward_years"].astype(str)
                + "\n years invested:"
                + temp_df["look_forward_years"].astype(str)
                + "\n start year"
                + (1990 + temp_df["time_span"]).astype(str)
            )

            temp_df["time_span_to_show"] = (temp_df["time_span"] + 1990).astype(str)

            fig = px.bar(
                temp_df,
                x="time_span_to_show",
                y="money_made",
                color="look_backward_years",
                hover_name="info",
                title=f"Sold end of year:{1990 + x}",
                color_continuous_scale=px.colors.sequential.Viridis,
                barmode="group",
            )

            fig.write_html(
                "../data/vis/iteration_stuff/"
                f"portfolio_vs_money_made_sold_on{1990 + x}.html"
            )

    def visualize_portfolios_with_same_middledate(self):
        """
        This function is used to visualize the portfolios with the same middle date
        Portfolios means that the 30 Stocks are grouped with mean
        (Portfolios have a unique forward, backward, timespan)
        """

        for y in range(11, 30):
            middle_year = y

            to_plot = pd.DataFrame()
            for x in range(3, 11):

                temp_year_selection = middle_year - x
                temp_look_backward_years = x

                start_date = (
                    self.result_data[
                        (self.result_data["time_span"] == temp_year_selection)
                        & (
                            self.result_data["look_backward_years"]
                            == temp_look_backward_years
                        )
                    ]
                    .groupby("future_date")
                    .first()["start_date"]
                )
                if start_date.empty:
                    continue
                start_date = start_date.iloc[0]

                portfolio_progression = (
                    self.result_data[
                        (self.result_data["time_span"] == temp_year_selection)
                        & (
                            self.result_data["look_backward_years"]
                            == temp_look_backward_years
                        )
                    ]
                    .groupby("future_date")
                    .mean(numeric_only=True)
                    .reset_index()[["future_date", "money_made"]]
                )

                portfolio_progression["future_date"] = pd.to_datetime(
                    portfolio_progression["future_date"]
                )

                portfolio_progression["temp_look_backward_years"] = (
                    temp_look_backward_years
                )

                to_plot = pd.concat([to_plot, portfolio_progression])

            to_plot = to_plot.pivot_table(
                index="future_date",
                columns="temp_look_backward_years",
                values="money_made",
                aggfunc="mean",
            ).reset_index()

            fig = make_subplots(
                specs=[[{"secondary_y": True}]]
            )  # this a one cell subplot
            fig.update_layout(title="all portfolios with same middle date")
            for x in to_plot.columns:
                if x == "future_date":
                    continue
                fig.add_trace(
                    go.Scatter(
                        mode="lines",
                        x=to_plot["future_date"],
                        y=to_plot[x],
                        name=f"portfolio with {x}"
                        "years looked back, date in the middle is "
                        f"{1990 + middle_year}",
                    ),
                    secondary_y=False,
                )
            fig.write_html(
                "../data/vis/"
                f"portfolios_with_same_middle_date{1990+middle_year}.html"
            )
