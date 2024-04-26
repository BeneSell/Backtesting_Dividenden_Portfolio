"""
This is the execution Module, and shouldn't be used for anything
else than calling other functions and classes
"""

import json
# import datetime

# import data_download.download_classes as dl



import data_preprocessing.preproccess_classes as pre
import visualization.visualize_classes as vis
import data_business_logic.bussiness_logic_classes as bl


import pandas as pd



# down_alpha = dl.download_alphavantage_data()

# dl.download_fmp("").download_fmp_dividend_from_local()

def main():
    """ 
    This is the main function of the project. It is used to call all the other functions and classes
    """
    raw_data_fmp_dividends = {}
    raw_data_fmp_stock_value = {}

    raw_data_alpha = {}



    with open('../data/stock_infos/raw_data_fmp_from_local_div.json',\
              "r", encoding="utf-8") as json_file:
        raw_data_fmp_dividends = json.load(json_file)

    with open('../data/stock_infos/raw_data_fmp_stock_value.json', \
              "r", encoding="utf-8") as json_file:
        raw_data_fmp_stock_value = json.load(json_file)

    with open('../data/stock_infos/result.json', encoding="utf-8") as json_file:
        data = json_file.read()
        raw_data_alpha = json.loads(data)

    # results_sorted_06 is a good result file and not dynamic (it dosent get overwritten)
    result_df = pd.read_csv("../data/results/bruteforce_results_sorted_06.csv")

    pre_fmp = pre.preproccessing_fmp_data(raw_data_fmp_dividends, raw_data_fmp_stock_value)
    pre_alpha = pre.preproccessing_alphavantage_data(raw_data_alpha)

    # good_format_df = pre_fmp.pivot_dividenden_data(pre_fmp.normalized_data_dividend)
    # print(good_format_df[good_format_df["variable"].str.contains("adjDividend")])

    pre_combine = pre.preproccessing_combined_data(pre_fmp, pre_alpha)



    vis_alpha = vis.visualize_alphavantage(pre_alpha)
    # vis_alpha.visualize_stock_data(["600983"])
    vis_alpha.visualize_stock_data(["GGP", "MSCI"])
    vis_alpha.visualize_stock_data(["MO"])
    vis_alpha.visualize_dividenden_data(["T", "XOM", "WBA", "ABBV", "IBM", "MMM", "CAT"])
    # vis_alpha.visualize_all_dividend_data()
    # visualize more dividend data
    vis_alpha.visualize_dividenden_data(["COST"])
    vis_alpha.visualize_dividenden_data(["BTU"])
    vis_alpha.visualize_dividenden_data(["TDG"])
    vis_alpha.visualize_stock_as_candlestick("GGP")
    vis_alpha.visualize_stock_data(["CTAS"])
    # vis_alpha.visualize_dividenden_data(["GGP"])
    vis_alpha.visualize_dividenden_data(["DPZ"])
    vis_fmp = vis.visualize_fmp(pre_fmp)
    vis_fmp.visualize_dividenden_data("ADBE")
    vis_fmp.visualize_stock_as_candlestick("AAPL")
    vis_fmp.visualize_stock_data("AAPL")




    vis_combined = vis.visualize_combined_data(pre_combine)
    vis_combined.fmp_vs_alpha("AAPL")
    vis_combined.fmp_stock_vs_fmp_dividend("GGP")
    vis_combined.fmp_stock_vs_fmp_dividend("DPZ")

    vis_result = vis.visualize_result_data(result_df)
    # vis_result.visualize_histogram_plots()
    vis_result.visualize_portfolio_vs_money_made_same_future_date()
    # vis_result.visualize_portfolios_with_same_middledate()
    # vis_result.visualize_scatter_plots()
    # vis_result.visualize_vs_msiw(combined_data=pre_combine.combined_data)
    # vis_result.visualize_per_iteration()

    # bl.single_stock_check().check_for_increased_stock(pre_combine.combined_data)
    print("money after 24 months:",
            bl.single_stock_check().compound_interest_calc_recursive(15000, 24, 24))
    # try:

    print("MO")
    print(bl.single_stock_check().check_money_made_by_div(start_date=pd.to_datetime("2007-12-26"),
                                                          look_foward_years=3,
                                                          symbol="MO",
                                                          df_combined=pre_combine.combined_data,
                                                          money_invested=100))


    # pre_combine.combined_data["DPZ"].to_csv("../data/results/DPZ_to_check.csv")
    bl.single_stock_check().get_dividends(pre_combine.combined_data,
                                          pd.to_datetime("2008-12-26"),
                                          10,
                                          "DPZ")\
                                            .to_csv("../data/results/DPZ_dividends.csv")

    # apple_dividends = bl.single_stock_check()\
    # .get_dividends(pre_combine.combined_data, pd.to_datetime("2011-03-01"), 15, "AAPL")

    # stock_results = bl.bruteforce_checks(pre_combine.combined_data).check_all_stocks()

    # print(bl.bruteforce_checks(pre_combine.combined_data)\
    #                            .test_a_portfolio(stock_results\
    #                            .sort_values(by="all", ascending=True)\
    #                            .iloc[:30]))


    # print(stock_results.sort_values(by="all", ascending=True)[0:30])

    # print(bl.bruteforce_checks(pre_combine.combined_data).check_along_time_and_timespan())

    # result = bl.bruteforce_checks(pre_combine.combined_data).check_along_time_and_timespan()
    # result.to_csv("../data/results/bruteforce_results.csv")


    # bl.single_stock_check().calculate_dividend_growth(apple_dividends)
    # bl.single_stock_check().calculate_dividend_stability(apple_dividends)
    # bl.single_stock_check().calculate_dividend_yield(apple_dividends)
    # except Exception as e:
    # print("No dividends found in this time period"\
    #     f"{pd.to_datetime('2001-12-31')} - "\
    #     f"{pd.to_datetime('2s001-12-31') + datetime.timedelta(days=365 * 4)}")
    #     print("")
    #     print(e)

    # bl.single_stock_check().get_dividends(pre_combine.combined_data,\
    #                                       pd.to_datetime("2005-03-01"), 1, "AAPL")


    # print(pd.Period("03.2010"))

    # print(pre_fmp.pivot_dividenden_data(pre_fmp.normalized_data_dividend))
    # print(pre_fmp.pivot_stock_data(pre_fmp.normalized_stock_data))
    # print("##")
    # print(pre_alpha.normalized_data)


    # down_alpha.download_alphavantage_stock_and_dividend_data()



if __name__ == "__main__":
    main()
