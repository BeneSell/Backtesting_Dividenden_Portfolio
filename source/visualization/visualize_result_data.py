"""
visualize the results data 
"""

from datetime import timedelta
import pandas as pd
import numpy as np
import json

# import matplotlib.pyplot as plt
# from plotly.offline import iplot
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go

import data_business_logic.strategie_data_interface as str_data

import cufflinks

cufflinks.go_offline()

with open("../config.json", "r", encoding="utf-8") as file_data:
    config_file = json.load(file_data)


class VisualizeResultData:
    """
    This class is used to visualize the results from the business logic classes
    Mostly from the results of the function check_along_time_and_timespan
    """

    def __init__(self, result_data: pd.DataFrame) -> None:

        self.result_data = result_data

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

        look_backward_years = 10
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
            start_investment = 3000

            list_msciworld = [
                {
                    "money_made": calc_data.check_money_made_by_div(
                        start_date=pd.to_datetime(start_date)
                        + timedelta(days=365 * (look_backward_years)),
                        look_foward_years=x,
                        symbol="URTH",
                        df_combined=combined_data,
                        money_invested=start_investment,
                    ).iloc[-1]["money"],
                    "date": pd.to_datetime(start_date)
                    + timedelta(days=365 * look_backward_years)
                    + timedelta(days=365 * x),
                }
                for x in range(1, 4)
            ]

            msci_plot_name = "MSCI World, URTH (ISIN: IE00B6R52259)"

            # if money_made is nan we have no data for msci world
            if np.isnan(float(list_msciworld[0]["money_made"])):
                # print("no data for msci world")
                # use 8 % as average return per anno
                # 100 * 1.08**years
                list_msciworld = [
                    {
                        "money_made": start_investment * 1.08**x,
                        "date": pd.to_datetime(start_date)
                        + timedelta(days=365 * look_backward_years)
                        + timedelta(days=365 * x),
                    }
                    for x in range(1, 4)
                ]
                msci_plot_name = "8% Wachstumsrate"

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
                .sum(numeric_only=True)
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

            fig = make_subplots(
                specs=[[{"secondary_y": True}]]
            )  # this a one cell subplot

            close_plot = go.Scatter(
                mode="lines",
                x=portfolio_progression["future_date"],
                y=portfolio_progression["money_made"],
                name=f"Dividendenrendite des Portfolios von {year_selection+look_backward_years+1985} bis {year_selection+1985+look_backward_years+3} Jahren",
                line=dict(color="blue"),
            )
            msci_plot = go.Scatter(
                mode="lines",
                x=msci_money_made["date"],
                y=msci_money_made["money_made"],
                name=msci_plot_name,
                line=dict(color="red"),
            )

            fig.add_trace(close_plot, secondary_y=False)
            fig.add_trace(msci_plot, secondary_y=False)
            # add title to fig
            # its from (1990 + 10 + 7 + 3) = 2010 to (1990 + 10 + 7 + 3 + 7) = 2010
            fig.update_layout(
                title=f"Vergleich der Dividendenrendite des Portfolios von {year_selection+look_backward_years+1985} bis {year_selection+1985+look_backward_years+3} Jahren mit MSCI World"
            )

            fig.write_html(
                config_file["file_names"]["visualize_path"]
                + "msci_world_vs_portfolio_"
                f"{year_selection+ look_backward_years+ 1985}"
                f"_{year_selection+ 1985 + look_backward_years + 3}.html"
            )

    def visualize_symbol_vs_money_after_three_years(self):
        """
        This function is used to visualize the symbol vs money made
        """
        # save all portfolios which got sold on the same year

        copied_df = self.result_data.copy()

        copied_df["together"] = (
            copied_df["time_span"]
            + copied_df["look_backward_years"]
            + copied_df["look_forward_years"]
        )

        # filter copied_df that look_forward_years is 3
        copied_df = copied_df[copied_df["look_forward_years"] == 3]

        for x in range(copied_df["together"].min(), copied_df["together"].max()):

            temp_df = copied_df[(copied_df["together"] == x)].sort_values(
                by="time_span", ascending=False
            )

            # if the time invested and the time sold are the same the result
            # is the same so its no need to clutter the plot with the same data
            temp_df = temp_df.drop_duplicates(subset=["symbol", "money_made"])
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.update_layout(
                title=f"Rendite der Unternehmen bei dem Portfolio am Verkaufszeitpunkt: {1985+x}"
            )
            temp_df = temp_df.sort_values(by="rank_all", ascending=True)
            # combine temp_df[["look_backward_years","look_forward_years", "time_span"] ] with \n
            temp_df["info"] = (
                "past years: "
                + temp_df["look_backward_years"].astype(str)
                + "\n years invested:"
                + temp_df["look_forward_years"].astype(str)
                + "\n start year"
                + (1985 + temp_df["time_span"]).astype(str)
                + "\n rank_all"
                + temp_df["rank_all"].astype(str)
                + "\n number continutiy"
                + temp_df["calc_numb_continuity_x_years"].astype(str)
                + "\n number continutiy dividend"
                + temp_df["calc_numb_growth_x_times"].astype(str)
            )

            fig = px.bar(
                data_frame=temp_df,
                x="symbol",
                y="money_made",
                hover_data="info",
                title=f"Rendite der Unternehmen bei dem Portfolio am Verkaufszeitpunkt: {1985+x} in USD",
                labels={
                    "symbol": "Unternehmen Ticker Symbol",
                    "money_made": "Unternehmensrendite bei Verkauf in USD",
                },
            )

            fig.write_html(
                config_file["file_names"]["visualize_path"]
                + f"symbol_vs_money_made_sold_on{1985 + x}.html"
            )

    def visualize_all_portfolios_one_diagram(self):
        """
        This function is used to visualize all portfolios in one diagram
        """
        rankiest_rank_df = self.result_data.copy()
        rankiest_rank_df = rankiest_rank_df[rankiest_rank_df["look_forward_years"] == 3]

        # exlude timespan 26,27 and 28
        rankiest_rank_df = rankiest_rank_df[
            (rankiest_rank_df["time_span"] != 26)
            & (rankiest_rank_df["time_span"] != 27)
            & (rankiest_rank_df["time_span"] != 28)
        ]

        rankiest_rank_df = (
            rankiest_rank_df.groupby(by="time_span")
            .sum(numeric_only=True)
            .reset_index()
        )
        rankiest_rank_df["year_sold"] = (
            rankiest_rank_df["time_span"].astype(float)
        ) + 1998
        fig = px.bar(
            rankiest_rank_df,
            x="year_sold",
            y="money_made",
            title="Rendite der Portfolios",
        )

        fig.write_html(
            config_file["file_names"]["visualize_path"] + "all_portfolios.html"
        )

    def visualize_vs_eight_precent(self):
        """
        This function is used to visualize the money made with the eight percent growth rate
        """

        dividends_df = self.result_data.copy()

        dividends_df["sold_date"] = (
            dividends_df["time_span"]
            + dividends_df["look_forward_years"]
            + dividends_df["look_backward_years"]
            + 1985
        )
        dividends_df = (
            dividends_df[
                (dividends_df["look_forward_years"] == 3)
                & (dividends_df["time_span"] != 28)
                & (dividends_df["time_span"] != 27)
                & (dividends_df["time_span"] != 26)
            ]
            .groupby(by="sold_date")
            .sum(numeric_only=True)
            .reset_index()
            .sort_values(by="sold_date", ascending=True)
        )

        dividends_df["sold_date"] = dividends_df["sold_date"].astype(str)

        eight_percent = 3000 * 1.08**3

        # do a box in plot with the eight percent growth rate
        fig = px.bar(
            dividends_df,
            x="sold_date",
            y="money_made",
            title="Alle Portfolios, mit 8% Wachstumsrate verglichen",
            color_discrete_sequence=["grey"],
            labels={
                "sold_date": "Verkaufszeitpunkt",
                "money_made": "Unternehmensrendite bei Verkauf in USD",
            },
        )

        # add to fig a line which is has the value 10
        fig.add_hrect(
            y0=eight_percent,
            y1=dividends_df["money_made"].max(),
            line_width=0,
            fillcolor="green",
            opacity=0.2,
        )
        fig.add_hrect(
            y0=0, y1=eight_percent, line_width=0, fillcolor="red", opacity=0.2
        )

        fig.write_html(
            config_file["file_names"]["visualize_path"]
            + "money_made_with_growth_rate_box.html"
        )

    def histogram_money_made_with_median_mode_mean(self):
        """
        This function is used to visualize the histogram of the money made
        """
        to_plot = self.result_data[self.result_data["look_forward_years"] == 3]
        # rankiest_ranked_grouped =  self.result_data.groupby(by="time_span").sum().reset_index()

        # exlude timespan 26,27 and 28 because they are in the future
        to_plot = to_plot[
            (to_plot["time_span"] != 26)
            & (to_plot["time_span"] != 27)
            & (to_plot["time_span"] != 28)
        ]

        fig = px.histogram(
            to_plot,
            x="money_made",
            title="Histogramm, Unternehmensrendite bei Verkauf",
            labels={
                "money_made": "Unternehmensrendite bei Verkauf in USD",
                "count": "Anzahl",
            },
        )

        fig.update_yaxes(title_text="Anzahl")
        # add median to histogram
        fig.add_vline(
            x=to_plot["money_made"].median(),
            line_dash="dash",
            line_color="green",
            annotation_text="median",
            annotation_position="top left",
        )

        # add mean to histogram
        fig.add_vline(
            x=to_plot["money_made"].mean(),
            line_dash="dash",
            line_color="red",
            annotation_text="mean",
            annotation_position="top right",
        )

        # add mode to histogram
        fig.add_vline(
            x=to_plot["money_made"].round(-1).mode()[0],
            line_dash="dash",
            line_color="blue",
            annotation_text="mode",
            annotation_position="bottom right",
        )
        # round money made on from 111 to 110
        fig.write_html(
            config_file["file_names"]["visualize_path"]
            + "histogram_money_made_with_median_mode_mean.html"
        )

    def visualize_by_ranking_position(self):
        """
        This function is used to visualize the money made by ranking position
        """

        rankiest_rank_df = self.result_data[
            (self.result_data["time_span"] != 26)
            & (self.result_data["time_span"] != 27)
            & (self.result_data["time_span"] != 28)
        ]
        rankiest_rank_df = (
            rankiest_rank_df[(rankiest_rank_df["look_forward_years"] == 3)]
            .groupby("rank_of_all_ranks")
            .mean(numeric_only=True)
            .reset_index()
        )
        rankiest_rank_df["rank_of_all_ranks"] = rankiest_rank_df[
            "rank_of_all_ranks"
        ].astype(str)

        fig = px.bar(
            rankiest_rank_df,
            x="rank_of_all_ranks",
            y="money_made",
            title="Unternehmensrendite bei Verkauf, gruppiert nach Rang des Unternehmens (durchschnittlich)",
            labels={
                "rank_of_all_ranks": "Rang des Unternehmens",
                "money_made": "Durchschnittliche Unternehmensrendite bei Verkauf in USD",
            },
        )
        fig.write_html(
            config_file["file_names"]["visualize_path"] + "rank_vs_money_made.html"
        )

    def visualize_brutto_dividend(self):
        """
        This function is used to visualize the brutto dividend
        """
        brutto_dividend = self.result_data.copy()
        brutto_dividend["sold_date"] = (
            brutto_dividend["time_span"]
            + brutto_dividend["look_forward_years"]
            + brutto_dividend["look_backward_years"]
            + 1985
        )
        brutto_dividend = brutto_dividend[brutto_dividend["look_forward_years"] == 3]
        brutto_dividend = (
            brutto_dividend.groupby(by="sold_date").sum(numeric_only=True).reset_index()
        )
        brutto_dividend["sold_date"] = brutto_dividend["sold_date"].astype(str)

        fig = px.bar(
            brutto_dividend,
            x="sold_date",
            y="brutto_dividend_money",
            title="Dividendenrendite ohne Steuern pro Portfolio",
            labels={
                "sold_date": "Verkaufszeitpunkt",
                "brutto_dividend_money": "Dividendenrendite ohne Steuern in USD",
            },
        )
        fig.write_html(
            config_file["file_names"]["visualize_path"] + "brutto_dividend.html"
        )

    def visualize_table_symbol_count_mean_median_added_ranking_ranking(self):
        """
        This function is used to visualize the table with the symbol count mean median and ranking
        """
        result_df = self.result_data.copy()
        dividends_df = result_df[(result_df["look_forward_years"] == 3) & (result_df["time_span"] != 28) & (result_df["time_span"] != 27) & (result_df["time_span"] != 25) & (result_df["time_span"] != 26) ]
        
        grouped_df = dividends_df.groupby(by="symbol")
        new_df = pd.DataFrame()
        new_df["count"] = grouped_df["time_span"].count().round(0)
        new_df["mean"] = grouped_df["money_made"].mean().round(4)
        new_df["median"] = grouped_df["money_made"].median().round(4)
        new_df["added_ranking"] = grouped_df["rank_of_all_ranks"].mean().round(0)
        new_df["ranking"] = new_df["mean"].rank(ascending=False) + new_df["count"].rank(ascending=False)
        new_df = new_df.reset_index().sort_values(by="ranking", ascending=True)

        fig = go.Figure(data=[go.Table(header=dict(values=list(new_df.columns), fill_color="paleturquoise", align="left"), 
                            cells=dict(values=[
                                new_df["count"],
                                new_df["mean"],
                                new_df["median"],
                                new_df["added_ranking"],
                                new_df["ranking"],
                                new_df["symbol"]],
                                fill_color="lavender",
                                align="left"))])
        
        fig.update_layout(updatemenus=[{
            "buttons": [
                {
                    "method": "restyle",
                    "label": "Symbol",
                    "args": [{"cells": {"values": new_df.sort_values(by='symbol').values.T }}],
                    "args2": [{"cells": {"values": new_df.sort_values(by='symbol', ascending=False).values.T }}]
                },
                {
                    "method": "restyle",
                    "label": "Count",
                    "args": [{"cells": {"values": new_df.sort_values(by='count').values.T }}],
                    "args2": [{"cells": {"values": new_df.sort_values(by='count', ascending=False).values.T }}]
                },
                {
                    "method": "restyle",
                    "label": "Mean",
                    "args": [{"cells": {"values": new_df.sort_values(by='mean').values.T }}],
                    "args2": [{"cells": {"values": new_df.sort_values(by='mean', ascending=False).values.T }}]
                },
                {
                    "method": "restyle",
                    "label": "Median",
                    "args": [{"cells": {"values": new_df.sort_values(by='median').values.T }}],
                    "args2": [{"cells": {"values": new_df.sort_values(by='median', ascending=False).values.T }}]
                },
                {
                    "method": "restyle",
                    "label": "Added Ranking",
                    "args": [{"cells": {"values": new_df.sort_values(by='added_ranking').values.T }}],
                    "args2": [{"cells": {"values": new_df.sort_values(by='added_ranking', ascending=False).values.T }}]
                },
                {
                    "method": "restyle",
                    "label": "Ranking",
                    "args": [{"cells": {"values": new_df.sort_values(by='ranking').values.T }}],
                    "args2": [{"cells": {"values": new_df.sort_values(by='ranking', ascending=False).values.T }}]
                }
            ]         
        }])
        fig.write_html(config_file["file_names"]["visualize_path"] + "table_symbol_count_mean_median_added_ranking_ranking.html")

    def vs_eight_precent_table(self):

        years = 3
        dividends_df = self.result_data.copy()
        
        dividends_df = dividends_df[(dividends_df["look_forward_years"] == 3) & (dividends_df["time_span"] != 28) & (dividends_df["time_span"] != 27) & (dividends_df["time_span"] != 25) & (dividends_df["time_span"] != 26) ].groupby(by="time_span").sum().reset_index().sort_values(by="time_span", ascending=False)
        dividends_df["seven_percent"] = 3000 * 1.075 ** 3
        dividends_df["eight_percent"] = 3000 * 1.08 ** 3
        dividends_df["growth_rate"] = ((dividends_df["money_made"] / 3000) ** (1 / years) - 1) * 100
        dividends_df["year"] = dividends_df["time_span"] + 1999
        dividends_df = dividends_df.sort_values(by="growth_rate", ascending=False)

        fig = go.Figure(data=[go.Table(header=dict(values=list(["time_span", "money_made", "brutto_dividend_money", "seven_percent", "eight_percent", "growth_rate"]), fill_color="paleturquoise", align="left"),
                            cells=dict(values=[
                                dividends_df["year"],
                                dividends_df["money_made"],
                                dividends_df["brutto_dividend_money"],
                                dividends_df["seven_percent"],
                                dividends_df["eight_percent"],
                                dividends_df["growth_rate"]],
                                fill_color="lavender",
                                align="left"))])
        fig.write_html(config_file["file_names"]["visualize_path"] + "table_vs_eight_percent.html")