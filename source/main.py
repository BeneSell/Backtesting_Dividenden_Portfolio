"""
This is the execution Module, and shouldn't be used for anything
else than calling other functions and classes
"""

import json

# import datetime

import data_download.download_classes as dl

import pandas as pd

import data_business_logic.strategie_data_interface as str_data
import data_business_logic.startegie_calc_indikator as str_calc
import data_business_logic.strategie_execution as str_exec

import data_preprocessing.preproccess_classes as pre
import visualization.visualize_preproccesed_data as vis_pre
import visualization.visualize_result_data as vis_results_package


# down_alpha = dl.DownloadAlphavantageData()


# get config.json data

with open("../config.json", "r", encoding="utf-8") as file_data:
    file_names = json.load(file_data)


def main():
    """
    This is the main function of the project. It is used to call all the other functions and classes
    """
    while True:
        print("What do you want to do?")
        print("1: Download data from Alphavantage")
        print("2: Download data from Financial Modeling Prep")
        print("3: Preprocess data")
        print("4: Generate results")
        print("5: Generate visualizations from results")
        print("6: Not implemented yet")
        print("7: Generate visualizations from preproccessed data")
        print("8: Exit")
        user_input = input("Please enter a number: ")


        if user_input == "1":
            execute_download_alpha()
        if user_input == "2":
            execute_download_fmp()
        elif user_input == "3":
            execute_preproccesing()
        elif user_input == "4":
            execute_results()
        elif user_input == "5":
            execute_generating_visualizations_from_results()
        elif user_input == "6":
            execute_stuff()
        elif user_input == "7":
            execute_generating_visualizations_from_preproccessed_data()
        elif user_input == "8":
            break
        else:
            print("Please enter a valid number")


def execute_download_fmp():
    """
    This function is used to download the data from the Financial Modeling Prep API
    """

    down_fmp = dl.DownloadFMP()
    
    down_fmp.downloadFMP_dividend_from_local()


def execute_download_alpha():
    """
    This function is used to download the data from the Alphavantage API
    """

    down_alpha = dl.DownloadAlphavantageData()
    down_alpha.download_alphavantage_stock_and_dividend_data()




def execute_preproccesing():
    """
    This function is used to generate the results from the data
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

    pre_fmp = pre.PreproccessingFMPData(
        raw_data_fmp_dividends, raw_data_fmp_stock_value
    )
    pre_alpha = pre.PreproccessingAlphavantageData(raw_data_alpha)

    pre_combine = pre.PreproccessingCombinedData(pre_fmp, pre_alpha)

    return pre_combine, pre_fmp, pre_alpha


def execute_results():
    """
    This function is used to generate the results from the data
    """
    pre_combine = execute_preproccesing()[0]

    str_exec.StrategieExecution(
        pre_combine.combined_data
    ).check_along_time_and_timespan().to_csv(
        file_names["basic_paths"]["result_data_path"]
        + file_names["file_names"]["results_from_strategie_execution"]
    )


def execute_generating_visualizations_from_results():
    """
    This function is used to generate the results from the data
    """
    result_df = pd.read_csv(
        file_names["basic_paths"]["result_data_path"]
        + file_names["file_names"]["results_from_strategie_execution"]
    )

    pre_combine = execute_preproccesing()[0]

    vis_results = vis_results_package.VisualizeResultData(result_df)
    vis_results.visualize_symbol_vs_money_after_three_years()
    vis_results.visualize_vs_msiw(pre_combine.combined_data)
    

    vis_results.visualize_vs_eight_precent()
    vis_results.visualize_all_portfolios_one_diagram()
    vis_results.visualize_by_ranking_position()
    vis_results.histogram_money_made_with_median_mode_mean()
    vis_results.visualize_brutto_dividend()


def execute_generating_visualizations_from_preproccessed_data():
    """
    This function is used to generate stocks and dividend data
    """
    preproccesed = execute_preproccesing()

    pre_combine = preproccesed[0]
    pre_fmp = preproccesed[1]
    pre_alpha = preproccesed[2]

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

    vis_combined = vis_pre.VisualizeCombinedData(pre_combine)
    vis_combined.fmp_vs_alpha_dividends("AAPL")
    vis_combined.alpha_stock_vs_alpha_dividend("COST")
    vis_combined.alpha_stock_vs_alpha_dividend("BEN")
    vis_combined.alpha_stock_vs_alpha_dividend("GGP")
    vis_combined.alpha_stock_vs_alpha_dividend("IBM")

def execute_stuff():
    pre_combine = execute_preproccesing()[0]

    str_exec.StrategieExecution(
        pre_combine.combined_data
    ).check_all_stocks(look_forward_years=15).to_csv(
        file_names["basic_paths"]["result_data_path"]
        + "all_stocks_2005.csv")
    

if __name__ == "__main__":
    main()
