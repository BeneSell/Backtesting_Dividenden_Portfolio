import preproccess_classes as pre
import visualize_classes as vis

import pandas as pd
import download_classes as dl
import json


# down_alpha = dl.download_alphavantage_data()

raw_data_fmp_dividends = {}
raw_data_fmp_stock_value = {}

raw_data_alpha = {}

with open('../data/stock_infos/raw_data_fmp.json', "r") as json_file:
    raw_data_fmp_dividends = json.load(json_file)

with open('../data/stock_infos/raw_data_fmp_stock_value.json', "r") as json_file:
    raw_data_fmp_stock_value = json.load(json_file)

with open('../data/stock_infos/result.json') as json_file:
    data = json_file.read()
    raw_data_alpha = json.loads(data)


pre_fmp = pre.preproccessing_fmp_data(raw_data_fmp_dividends, raw_data_fmp_stock_value)
pre_alpha = pre.preproccessing_alphavantage_data(raw_data_alpha)


# preproccessing_combined = pre.preproccessing_combined_data(pre_fmp, pre_alpha)
# print(preproccessing_combined.combine_data().head())

vis_alpha = vis.visualize_alphavantage(pre_alpha)
vis_fmp = vis.visualize_fmp(pre_fmp)

# down_alpha.download_alphavantage_stock_and_dividend_data()



# vis_alpha.visualize_dividenden_data("AAPL")


vis_fmp.visualize_dividenden_data("AAPL")

vis_alpha.visualize_stock_data("AAPL")