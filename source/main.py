import data_preprocessing.preproccess_classes as pre
import visualization.visualize_classes as vis
import data_business_logic.bussiness_logic_classes as bl


import pandas as pd
import data_download.download_classes as dl
import json
import datetime

# down_alpha = dl.download_alphavantage_data()

# dl.download_fmp("").download_fmp_dividend_from_local()


raw_data_fmp_dividends = {}
raw_data_fmp_stock_value = {}

raw_data_alpha = {}



with open('../data/stock_infos/raw_data_fmp_from_local_div.json', "r") as json_file:
    raw_data_fmp_dividends = json.load(json_file)

with open('../data/stock_infos/raw_data_fmp_stock_value.json', "r") as json_file:
    raw_data_fmp_stock_value = json.load(json_file)

with open('../data/stock_infos/result.json') as json_file:
    data = json_file.read()
    raw_data_alpha = json.loads(data)


pre_fmp = pre.preproccessing_fmp_data(raw_data_fmp_dividends, raw_data_fmp_stock_value)
pre_alpha = pre.preproccessing_alphavantage_data(raw_data_alpha)

# good_format_df = pre_fmp.pivot_dividenden_data(pre_fmp.normalized_data_dividend)
# print(good_format_df[good_format_df["variable"].str.contains("adjDividend")])

pre_combine = pre.preproccessing_combined_data(pre_fmp, pre_alpha)


vis_alpha = vis.visualize_alphavantage(pre_alpha)
vis_alpha.visualize_stock_data(["ADBE"])

vis_fmp = vis.visualize_fmp(pre_fmp)
vis_fmp.visualize_dividenden_data("ADBE")


vis_alpha.visualize_dividenden_data(["AAPL"])





vis_combined = vis.visualize_combined_data(pre_combine.combined_data)
vis_combined.fmp_vs_alpha("ADBE")


# bl.single_stock_check().check_for_increased_stock(pre_combine.combined_data)
# print(f"money after 24 months: {bl.single_stock_check().compound_interest_calc_recursive(15000, 24, 24)}")
# try: 
bl.single_stock_check().check_money_made_by_div(start_date=pd.to_datetime("2011-12-31"), look_foward_years=15, symbol="C", df_combined=pre_combine.combined_data, money_invested=100)


apple_dividends = bl.single_stock_check().get_dividends(pre_combine.combined_data, pd.to_datetime("2011-03-01"), 15, "AAPL")

stock_results = bl.bruteforce_checks(pre_combine.combined_data).check_all_stocks()

bl.bruteforce_checks(pre_combine.combined_data).test_a_portfolio(stock_results.sort_values(by="all", ascending=True)["symbol"][0:30].to_list())

# bl.single_stock_check().calculate_dividend_growth(apple_dividends)
# bl.single_stock_check().calculate_dividend_stability(apple_dividends)
# bl.single_stock_check().calculate_dividend_yield(apple_dividends)
# except Exception as e:
#     print(f"No dividends found in this time period  {pd.to_datetime('2001-12-31')} - {pd.to_datetime('2001-12-31') + datetime.timedelta(days=365 * 4)}")
#     print("")
#     print(e)
# bl.single_stock_check().check_for_min_dividend(pre_combine.combined_data, 0.05, pd.to_datetime("2020-01-01"), 15)

# bl.single_stock_check().get_dividends(pre_combine.combined_data, pd.to_datetime("2005-03-01"), 1, "AAPL")


# print(pd.Period("03.2010"))

# print(pre_fmp.pivot_dividenden_data(pre_fmp.normalized_data_dividend))
# print(pre_fmp.pivot_stock_data(pre_fmp.normalized_stock_data))
# print("##")
# print(pre_alpha.normalized_data)


# down_alpha.download_alphavantage_stock_and_dividend_data()



