"""
This is the execution Module, and shouldn't be used for anything
else than calling other functions and classes
"""

import json

# import datetime

# import data_download.download_classes as dl

import pandas as pd

import data_business_logic.strategie_data_interface as str_data
import data_business_logic.startegie_calc_indikator as str_calc
import data_business_logic.strategie_execution as str_exec

import data_preprocessing.preproccess_classes as pre
import visualization.visualize_preproccesed_data as vis_pre
import visualization.visualize_result_data as vis_results_package


# down_alpha = dl.DownloadAlphavantageData()

# dl.DownloadFMP("").DownloadFMP_dividend_from_local()
# get config.json data

with open("../config.json", "r", encoding="utf-8") as file_data:
    file_names = json.load(file_data)


def main():
    """
    This is the main function of the project. It is used to call all the other functions and classes
    """
    raw_data_fmp_dividends = {}
    raw_data_fmp_stock_value = {}

    raw_data_alpha = {}

    with open(
        file_names["basic_paths"]["downloaded_data_path"]
        + file_names["file_names"]["fmp_dividends"],
        "r",
        encoding="utf-8",
    ) as json_file:
        raw_data_fmp_dividends = json.load(json_file)

    with open(
        file_names["basic_paths"]["downloaded_data_path"]
        + file_names["file_names"]["fmp_stocks"],
        "r",
        encoding="utf-8",
    ) as json_file:
        raw_data_fmp_stock_value = json.load(json_file)

    with open(
        file_names["basic_paths"]["downloaded_data_path"]
        + file_names["file_names"]["alpha_vantage_data"],
        encoding="utf-8",
    ) as json_file:
        data = json_file.read()
        raw_data_alpha = json.loads(data)

    # results_sorted_06 is a good result file and not dynamic (it dosent get overwritten)
    result_df = pd.read_csv(
        file_names["basic_paths"]["result_data_path"]
        + file_names["file_names"]["results_from_strategie_execution"]
    )

    pre_fmp = pre.PreproccessingFMPData(
        raw_data_fmp_dividends, raw_data_fmp_stock_value
    )
    pre_alpha = pre.PreproccessingAlphavantageData(raw_data_alpha)

    pre_combine = pre.PreproccessingCombinedData(pre_fmp, pre_alpha)

    vis_alpha = vis_pre.VisualizeAlphavantage(pre_alpha)
    # vis_alpha.visualize_stock_data(["600983"])
    # vis_alpha.visualize_stock_data(["GGP", "SC0J.DE"])
    vis_alpha.visualize_stock_data(["MO"])
    vis_alpha.visualize_stock_data(["GGP"])
    vis_alpha.visualize_stock_as_candlestick("GGP")
    # vis_alpha.visualize_stock_data(["SC0J.DE"])
    vis_alpha.visualize_dividenden_data(
        ["T", "XOM", "WBA", "ABBV", "IBM", "MMM", "CAT"]
    )
    # vis_alpha.visualize_all_dividend_data()
    # visualize more dividend data
    vis_alpha.visualize_dividenden_data(["COST"])
    vis_alpha.visualize_dividenden_data(["BTU"])
    vis_alpha.visualize_dividenden_data(["TDG"])
    vis_alpha.visualize_stock_as_candlestick("GGP")
    vis_alpha.visualize_stock_data(["CTAS"])
    # vis_alpha.visualize_dividenden_data(["GGP"])
    vis_alpha.visualize_dividenden_data(["GGP"])

    vis_fmp = vis_pre.VisualizeFMP(pre_fmp)
    vis_fmp.visualize_dividenden_data("GGP")
    vis_fmp.visualize_stock_as_candlestick("AAPL")
    vis_fmp.visualize_stock_data("GGP")

    vis_results = vis_results_package.VisualizeResultData(result_df)
    vis_results.visualize_symbol_vs_money_after_three_years()
    vis_results.visualize_vs_msiw(combined_data=pre_combine.combined_data)
    vis_results.visualize_scatter_plots()

    vis_results.visualize_vs_eight_precent()
    vis_results.visualize_all_portfolios_one_diagram()
    vis_results.visualize_by_ranking_position()
    vis_results.histogram_money_made_with_median_mode_mean()
    vis_results.visualize_brutto_dividend()

    vis_combined = vis_pre.VisualizeCombinedData(pre_combine)
    vis_combined.fmp_vs_alpha("AAPL")
    vis_combined.alpha_stock_vs_alpha_dividend("COST")
    vis_combined.alpha_stock_vs_alpha_dividend("XOM")
    vis_combined.alpha_stock_vs_alpha_dividend("GGP")
    vis_combined.alpha_stock_vs_alpha_dividend("IBM")

    # bl.SingleStockCheck().check_for_increased_stock(pre_combine.combined_data)
    # print(
    #     "money after 24 months:",
    #     str_data.StrategieDataInterface().compound_interest_calc_recursive(
    #         15000, 24, 24
    #     ),
    # )
    # try:

    # print("MO")
    # print(
    #     str_data.StrategieDataInterface().check_money_made_by_div(
    #         start_date=pd.to_datetime("2007-12-26"),
    #         look_foward_years=3,
    #         symbol="MO",
    #         df_combined=pre_combine.combined_data,
    #         money_invested=100,
    #     )
    # )

    str_data.StrategieDataInterface().get_dividends(
        df_combined=pre_combine.combined_data,
        x=pd.to_datetime("2005-12-26"),
        look_forward_years=7,
        symbol="IBM",
    )
    # str_exec.StrategieExecution(pre_combine.combined_data).check_all_stocks(
    #     start_date=pd.to_datetime("1995-01-01"), look_forward_years=7
    # ).to_csv("../data/results/one_year_result.csv")

    # apple_dividends = bl.SingleStockCheck()\
    # .get_dividends(pre_combine.combined_data, pd.to_datetime("2011-03-01"), 15, "AAPL")

    # print(bl.BruteforceChecks(pre_combine.combined_data)\
    #                            .test_a_portfolio(stock_results\
    #                            .sort_values(by="all", ascending=True)\
    #                            .iloc[:30]))

    # print(stock_results.sort_values(by="all", ascending=True)[0:30])

    # result = str_exec.StrategieExecution(
    #     pre_combine.combined_data
    # ).check_along_time_and_timespan()
    # result.to_csv(file_names['basic_paths']['result_data_path'] + file_names['file_names']['results_from_strategie_execution'])

    # except Exception as e:
    # print("No dividends found in this time period"\
    #     f"{pd.to_datetime('2001-12-31')} - "\
    #     f"{pd.to_datetime('2s001-12-31') + datetime.timedelta(days=365 * 4)}")
    #     print("")
    #     print(e)

    # bl.SingleStockCheck().get_dividends(pre_combine.combined_data,\
    #                                       pd.to_datetime("2005-03-01"), 1, "AAPL")

    # down_alpha.download_alphavantage_stock_and_dividend_data()


if __name__ == "__main__":
    main()
