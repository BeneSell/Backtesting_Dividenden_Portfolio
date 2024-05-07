import datetime
from datetime import timedelta
import concurrent.futures
import pandas as pd
import data_business_logic.startegie_calc_indikator as str_calc
import data_business_logic.strategie_data_interface as str_data


class StrategieExecution:
    """
    well this is kinda changing i think but its for checking a lot of stocks
    the code is heavy using SingleStockChecker
    """

    def __init__(self, combined_data) -> None:
        self.combined_data = combined_data

    def check_all_stocks(
        self,
        start_date: datetime.datetime = datetime.date(2005, 12, 31),
        look_forward_years: int = 12,
    ) -> pd.DataFrame:
        """
        it checks all stocks which are in the combined_data
        for there dividend growth, stability and yield

        The two arguments generate a period where the stocks are checked

        args :
            start_date (datetime.datetime, optional): the start date.
            look_forward_years (int, optional): how many years to look forward.

        returns:
            pd.DataFrame: a DataFrame with the growth, stability and yield of the stocks
        """

        result = []

        for x in self.combined_data.columns:

            # stop when the column is not a stock symbol
            # TODO rework this
            if (
                x == "date"
                or x == "information"
                or x == "index"
                or x == "index_extracted"
                or x == "random_counter"
            ):
                continue

            calc_indikator = str_calc.StrategieCalcIndikator()
            calc_data = str_data.StrategieDataInterface()

            temp_dividends = calc_data.get_dividends(
                self.combined_data, start_date, look_forward_years, x
            )

            # stop when no dividends are found
            if temp_dividends.empty:
                continue

            # maybe not a good name for this variable
            yearly_difference = calc_indikator.difference_between_consecutive_years(
                temp_dividends,
                start_date + timedelta(days=365 * look_forward_years),
            )
            if yearly_difference.empty:
                continue

            # stop when no yearly difference is found
            # not enough data or gaps to big between years
            if yearly_difference.empty:
                continue

            temp_continuity_x_years = (
                calc_indikator.calculate_dividend_continuity_x_years_filter(
                    yearly_difference, 5
                )
            )
            temp_continuity_no_cuts = (
                calc_indikator.calculate_dividend_continuity_no_div_reductions_filter(
                    yearly_difference, 5
                )
            )
            temp_growth_x_times = calc_indikator.calculate_dividend_growth_filter(
                yearly_difference, 2, 5
            )
            temp_growth_indikative = (
                calc_indikator.calculate_dividend_growth_indikative_filter(
                    yearly_difference
                )
            )
            temp_yield_indikative = (
                calc_indikator.calculate_dividend_yield_indikative_filter(
                    temp_dividends,
                    start_date + timedelta(days=365 * look_forward_years),
                )
            )
            temp_yield_historic = (
                calc_indikator.calculate_dividend_yield_historic_filter(
                    temp_dividends,
                    start_date + timedelta(days=365 * look_forward_years),
                )
            )

            # now the calc_numbs
            temp_continuity_x_years_calc_numb = (
                calc_indikator.calculate_dividend_continuity_x_years_calc_numb(
                    yearly_difference
                )
            )
            temp_continuity_no_cuts_calc_numb = calc_indikator.calculate_dividend_continuity_no_div_reductions_calc_numb(
                yearly_difference
            )
            temp_growth_x_times_calc_numb = (
                calc_indikator.calculate_dividend_growth_calc_numb(yearly_difference)
            )
            temp_growth_indikative_calc_numb = (
                calc_indikator.calculate_dividend_growth_indikative_calc_numb(
                    yearly_difference
                )
            )
            temp_yield_indikative_calc_numb = (
                calc_indikator.calculate_dividend_yield_indikative_calc_numb(
                    temp_dividends,
                    start_date + timedelta(days=365 * look_forward_years),
                )
            )
            temp_yield_historic_calc_numb = (
                calc_indikator.calculate_dividend_yield_historic_calc_numb(
                    temp_dividends,
                    start_date + timedelta(days=365 * look_forward_years),
                )
            )

            bool_statements = [
                temp_continuity_x_years,
                temp_continuity_no_cuts,
                temp_growth_x_times,
                temp_growth_indikative,
                temp_yield_indikative,
                temp_yield_historic,
            ]

            true_count = sum(bool_statements)

            # if true_count < 5:
            #     continue

            # if true_count < 5:
            #     continue

            result.append(
                {
                    "symbol": x,
                    "all": temp_continuity_x_years
                    and temp_continuity_no_cuts
                    and temp_growth_x_times
                    and temp_growth_indikative
                    and temp_yield_indikative
                    and temp_yield_historic,
                    "filter_continuity": temp_continuity_no_cuts,
                    "filter_continuity_x_years": temp_continuity_x_years,
                    "filter_growth_x_times": temp_growth_x_times,
                    "filter_growth_indikative": temp_growth_indikative,
                    "filter_yield_indikative": temp_yield_indikative,
                    "filter_yield_historic": temp_yield_historic,
                    "calc_numb_continuity_no_cuts": temp_continuity_no_cuts_calc_numb,
                    "calc_numb_continuity_x_years": temp_continuity_x_years_calc_numb,
                    "calc_numb_growth_x_times": temp_growth_x_times_calc_numb,
                    "calc_numb_growth_indikative": temp_growth_indikative_calc_numb,
                    "calc_numb_yield_indikative": temp_yield_indikative_calc_numb,
                    "calc_numb_yield_historic": temp_yield_historic_calc_numb,
                }
            )

        result_df = pd.DataFrame(result)

        if result_df.empty:
            return result_df

        # now the ranks
        result_df["rank_continuity_no_cuts"] = result_df[
            "calc_numb_continuity_no_cuts"
        ].rank(ascending=False)
        result_df["rank_continuity_x_years"] = result_df[
            "calc_numb_continuity_x_years"
        ].rank(ascending=False)
        result_df["rank_growth_x_times"] = result_df["calc_numb_growth_x_times"].rank(
            ascending=False
        )
        # the growth is a negative value so we need to rank it ascending
        result_df["rank_growth_indikative"] = result_df[
            "calc_numb_growth_indikative"
        ].rank(ascending=True)
        result_df["rank_yield_indikative"] = result_df[
            "calc_numb_yield_indikative"
        ].rank(ascending=False)
        result_df["rank_yield_historic"] = result_df["calc_numb_yield_historic"].rank(
            ascending=False
        )
        result_df["rank_all"] = (
            result_df["rank_continuity_no_cuts"]
            + result_df["rank_continuity_x_years"]
            + result_df["rank_growth_x_times"]
            + result_df["rank_growth_indikative"]
            + result_df["rank_yield_indikative"]
            + result_df["rank_yield_historic"]
        )
        result_df["rank_of_all_ranks"] = result_df["rank_all"].rank(ascending=True)

        return result_df

    def test_a_portfolio(
        self,
        df_of_stocks: pd.DataFrame,
        start_date: datetime.datetime = datetime.date(2015, 12, 31),
        look_forward_years: int = 5,
    ):
        """
        This generates a period time where the start date the investment date is
        and the look_forward_years the time the investment is hold

        args:
            df_of_stocks (pd.DataFrame): a DataFrame with the growth,
                            stability and yield of the stocks (often generated by check_all_stocks)
            start_date (datetime.datetime, optional): the start date.
            look_forward_years (int, optional): how many years to look forward.
        """
        result = []

        calc_data = str_data.StrategieDataInterface()

        for x in df_of_stocks["symbol"].to_list():

            temp = calc_data.check_money_made_by_div(
                start_date, look_forward_years, x, self.combined_data, 100
            )

            if temp.empty:
                continue

            # TODO rework this for loop because its not the pandas way
            temp_df_symbol = df_of_stocks[df_of_stocks["symbol"] == x]

            temp_money_made = temp["money"].iloc[-1]
            temp_dividend_made = temp["summed_dividend_money"].iloc[-1]
            result.append(
                {
                    "symbol": x,
                    "money_made": temp_money_made,
                    "brutto_dividend_money": temp_dividend_made,
                    "filter_continuity": temp_df_symbol["filter_continuity"].iloc[0],
                    "filter_continuity_x_years": temp_df_symbol[
                        "filter_continuity_x_years"
                    ].iloc[0],
                    "filter_growth_x_times": temp_df_symbol[
                        "filter_growth_x_times"
                    ].iloc[0],
                    "filter_growth_indikative": temp_df_symbol[
                        "filter_growth_indikative"
                    ].iloc[0],
                    "filter_yield_indikative": temp_df_symbol[
                        "filter_yield_indikative"
                    ].iloc[0],
                    "filter_yield_historic": temp_df_symbol[
                        "filter_yield_historic"
                    ].iloc[0],
                    "all": temp_df_symbol["all"].iloc[0],
                    "calc_numb_continuity_no_cuts": temp_df_symbol[
                        "calc_numb_continuity_no_cuts"
                    ].iloc[0],
                    "calc_numb_continuity_x_years": temp_df_symbol[
                        "calc_numb_continuity_x_years"
                    ].iloc[0],
                    "calc_numb_growth_x_times": temp_df_symbol[
                        "calc_numb_growth_x_times"
                    ].iloc[0],
                    "calc_numb_growth_indikative": temp_df_symbol[
                        "calc_numb_growth_indikative"
                    ].iloc[0],
                    "calc_numb_yield_indikative": temp_df_symbol[
                        "calc_numb_yield_indikative"
                    ].iloc[0],
                    "calc_numb_yield_historic": temp_df_symbol[
                        "calc_numb_yield_historic"
                    ].iloc[0],
                    "rank_continuity_no_cuts": temp_df_symbol[
                        "rank_continuity_no_cuts"
                    ].iloc[0],
                    "rank_continuity_x_years": temp_df_symbol[
                        "rank_continuity_x_years"
                    ].iloc[0],
                    "rank_growth_x_times": temp_df_symbol["rank_growth_x_times"].iloc[
                        0
                    ],
                    "rank_growth_indikative": temp_df_symbol[
                        "rank_growth_indikative"
                    ].iloc[0],
                    "rank_yield_indikative": temp_df_symbol[
                        "rank_yield_indikative"
                    ].iloc[0],
                    "rank_yield_historic": temp_df_symbol["rank_yield_historic"].iloc[
                        0
                    ],
                    "rank_all": temp_df_symbol["rank_all"].iloc[0],
                    "rank_of_all_ranks": temp_df_symbol["rank_of_all_ranks"].iloc[0],
                }
            )

        return pd.DataFrame(result)

    def parallelize_check_along_time_method(
        self,
        x,
        start_date: datetime.datetime = datetime.date(1990, 12, 31),
        look_backward_years: int = 5,
        look_forward_years: int = 5,
    ) -> pd.DataFrame:
        """
        is used inside of check_along_time for parallelizing the check_along_time_method.

        args:
            x (int): the time span
            start_date (datetime.datetime, optional): the start date.
            look_backward_years (int, optional): how many years to look backward.
            look_forward_years (int, optional): how many years to look forward.

        """
        # look_backward_years + start_date + the time span
        # 2000 + 5 + 0
        # 2000 + 5 + 1
        temp_list_of_stocks = self.check_all_stocks(
            start_date + timedelta(days=365 * x), look_backward_years
        )
        if temp_list_of_stocks.empty:
            return pd.DataFrame()
        if temp_list_of_stocks["symbol"].count() == 1:
            return pd.DataFrame()
        # look_backward_years + look_forward_years + start_date + the time span
        # 2000 + 10 + 0
        # 2000 + 10 + 1
        temp_df = self.test_a_portfolio(
            temp_list_of_stocks.sort_values(by="rank_all", ascending=True).iloc[:30],
            start_date
            + timedelta(days=365 * (look_backward_years))
            + timedelta(days=365 * x),
            look_forward_years,
        )

        temp_df["time_span"] = x
        temp_df["start_date"] = start_date + timedelta(days=365 * x)
        temp_df["middle_date"] = (
            start_date
            + timedelta(days=365 * x)
            + timedelta(days=365 * look_backward_years)
        )
        temp_df["future_date"] = (
            start_date
            + timedelta(days=365 * (look_forward_years + look_backward_years))
            + timedelta(days=365 * x)
        )
        temp_df["look_backward_years"] = look_backward_years
        temp_df["look_forward_years"] = look_forward_years
        # stock start stock end etc

        return temp_df

    def check_along_time_axis(
        self,
        start_date: datetime.datetime = datetime.date(1990, 12, 31),
        look_backward_years: int = 12,
        look_forward_years: int = 3,
    ) -> pd.DataFrame:
        """
        this function combine the check_all_stocks and test_a_portfolio function
        basiscally it does a Hyperparamter iteration over time_span

        args:
            start_date (datetime.datetime, optional): the start date.
            look_backward_years (int, optional): how many years to look backward.
            look_forward_years (int, optional): how many years to look forward.
        """

        future_results = []
        num_workers = 30

        with concurrent.futures.ProcessPoolExecutor(
            max_workers=num_workers
        ) as executor:
            for x in range(0, 30):
                # create copy of self.combined_data

                future_results.append(
                    executor.submit(
                        self.parallelize_check_along_time_method,
                        x,
                        start_date,
                        look_backward_years,
                        look_forward_years,
                    )
                )

            results = [
                future.result()
                for future in concurrent.futures.as_completed(future_results)
            ]

        final_result = pd.concat(results, ignore_index=True)

        return final_result

    def check_along_time_and_timespan(self):
        """
        This function is used to generated Portfolio progression.
        Additional to the results.

        """

        result = pd.DataFrame()

        for x in range(1, 4):
            print(f"look_forward_years: {x}, time: {datetime.datetime.now()}")
            temp_result = self.check_along_time_axis(
                look_backward_years=5, look_forward_years=x
            )

            if x == 1:
                result = temp_result
            else:
                result = pd.concat([result, temp_result], ignore_index=True)

        return result
