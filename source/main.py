import preproccess_classes as pre
import visualize_classes as vis

import pandas as pd
import download_classes as dl


# pre_fmp = pre.preproccessing_fmp_data()
# pre_alpha = pre.preproccessing_alphavantage_data()
# down_alpha = dl.download_alphavantage_data()


vis_alpha = vis.visualize_alphavantage()
vis_fmp = vis.visualize_fmp()

# down_alpha.download_alphavantage_stock_and_dividend_data()



# vis_alpha.visualize_dividenden_data("AAPL")


vis_fmp.visualize_dividenden_data("AAPL")

vis_alpha.visualize_stock_data("AAPL")