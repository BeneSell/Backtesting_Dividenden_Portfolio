import datetime

from datetime import timedelta

import pandas as pd


class StrategieCalcIndikator:
    def difference_between_consecutive_years(
        self, dividends_of_stock: pd.DataFrame, start_date: datetime.date
    ):
        """
        Delivers a dataframe which gives dividend and stock price differences
            between years
        This dataframe is for the measures of dividend continuity and dividend growth
        If the sequence breaks, the dataframe is cut at this point
        The sequence starts at the invest date (start date)
        Use the Dataframe from get_dividends
        args:
            df (pd.DataFrame): dataframe with a date column
            start_date (datetime.date): the start date
        """
        # to year period with sum
        dividends_of_stock["year"] = dividends_of_stock["date"].dt.year
        dividends_of_stock = dividends_of_stock.sort_values(by="year", ascending=False)
        # check if the first year is the same as the start date or the year before
        if (
            dividends_of_stock["date"].iloc[0].to_timestamp().year != start_date.year
        ) and (
            dividends_of_stock["date"].iloc[0].to_timestamp().year
            != start_date.year - 1
        ):
            # print("start date is not the same as the first year",\
            #       dividends_of_stock["date"].iloc[0].to_timestamp().year, start_date.year)

            return pd.DataFrame()
        diffs = (
            dividends_of_stock.groupby("year")
            .sum(numeric_only=False)
            .reset_index()[["year", "alpha_dividend"]]
            .sort_values(by="year", ascending=False)
            .reset_index()[["year", "alpha_dividend"]]
            .diff()
            .iloc[1:]
            .reset_index(drop=True)
        )
        # if there is only one year, there is no difference to calculate
        if diffs.empty:
            return pd.DataFrame()

        # if the diff is that the year is still consecutive
        # < -1 because it could be zero if the year is the same
        # apply consectutive filters is not easy
        first_missed_year_index = diffs["year"].astype(int)[
            diffs["year"].astype(int) < -1
        ]
        if not first_missed_year_index.empty:
            cut_df = diffs.iloc[: first_missed_year_index.index[0]]
            # Cut the series from the beginning until the first occurrence of value 2

        else:
            # it could mean that every year has a dividend
            # it could mean that there is no dividend at all

            cut_df = diffs

        return cut_df

    def calculate_dividend_continuity_x_years_calc_numb(
        self, yearly_difference: pd.DataFrame
    ):
        """
        a calc_numb which shows how many years the dividend is paid consecutively
        """
        return yearly_difference["year"].count()

    def calculate_dividend_continuity_no_div_reductions_calc_numb(
        self, yearly_difference: pd.DataFrame
    ):
        """
        a calc_numb which shows how many years the dividend isnt reduced
        """
        return (
            yearly_difference[(yearly_difference["alpha_dividend"] <= 0.0)]
            .count()
            .iloc[0]
        )

    # growth

    def calculate_dividend_growth_calc_numb(self, yearly_difference: pd.DataFrame):
        """
        a calc_numb which shows how many times the dividend grows
        """
        return yearly_difference[yearly_difference["alpha_dividend"] < 0.0][
            "alpha_dividend"
        ].count()

    def calculate_dividend_growth_indikative_calc_numb(self, yearly_difference):
        """
        a calc_numb which shows the growth in the last year
        """
        return yearly_difference["alpha_dividend"].iloc[0]

    # yield

    def calculate_dividend_yield_indikative_calc_numb(
        self, dividends_of_stock, start_date
    ):
        """
        a calc_numb which shows the yield of the last year
        """

        # to year period with sum
        dividends_of_stock["year"] = dividends_of_stock["date"].dt.year
        dividends_of_stock = dividends_of_stock.sort_values(by="year", ascending=False)
        # check if the first year is the same as the start date or the year before
        if (
            dividends_of_stock["date"].iloc[0].to_timestamp().year != start_date.year
        ) and (
            dividends_of_stock["date"].iloc[0].to_timestamp().year
            != start_date.year - 1
        ):
            # print("start date is not the same as the first year")

            return False

        return dividends_of_stock["alpha_dividend"].iloc[0]

    def calculate_dividend_yield_historic_calc_numb(
        self, dividends_of_stock, start_date
    ):
        """
        a calc_numb which shows the yield of the history
        """

        # to year period with sum
        dividends_of_stock["year"] = dividends_of_stock["date"].dt.year
        dividends_of_stock = dividends_of_stock.sort_values(by="year", ascending=False)
        # check if the first year is the same as the start date or the year before
        if (
            dividends_of_stock["date"].iloc[0].to_timestamp().year != start_date.year
        ) and (
            dividends_of_stock["date"].iloc[0].to_timestamp().year
            != start_date.year - 1
        ):
            # print("start date is not the same as the first year")

            return False

        return dividends_of_stock["alpha_dividend"].mean()
