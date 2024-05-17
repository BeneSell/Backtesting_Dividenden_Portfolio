# Backtesting_Dividenden_Portfolio
## Table Of Content
- Descirption
- Structure
- Getting Started

## Description

This repository downloads financial data and prepares them for backtesting usage.

At the moment I have two notebooks to download data one for financialmodelingprep and one by alphavantage.

## Structure

There are two important things which are not included directly in the online repository

A `data` folder where all the data is stored. 

the other data is directly scraped from a wikisite and has two lists:
https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#Selected_changes_to_the_list_of_S&P_500_components

- first list is saved in `wikilist_1.csv`
- second list is saved in `wikilist_2.csv`

using tools close to this one: https://wikitable2csv.ggor.de/

### stock_infos folder is the destination folder and the informations are generated while using the programm


A `secret_file.json` where the api keys are saved.

the secrect_file.json looks like this 

```json
{"secret_key":"API_KEY",
"secret_key_fmp":"API_KEY"}
```

A `config.json` where all file paths are stored

```json
{
    "basic_paths":{
        "ticker_symbol_path": "../data/companies/",
        "downloaded_data_path": "../data/stock_infos/",
        "result_data_path": "../data/results/",
        "visualize_data_path": "../data/vis/",
        "visualize_data_iterations": "../data/vis/iteration_stuff/",
        "local_path_fmp_dividend": "../data/stock_infos/local/"
    },
    "file_names":{
        "fmp_dividends": "raw_data_fmp_from_local_div.json"
        , "fmp_stocks": "raw_data_fmp_stock_value.json"
        , "alpha_vantage_data": "result.json"
        , "results_from_strategie_execution": "bruteforce_results.csv"
        , "company_names": "combined_historical_ticker_symbols.csv"
        , "company_names_i_dont_have_local": "companies_i_dont_have_local.csv"
        , "dividend_fmp_from_internet": "raw_data_fmp.json"
        , "stock_fmp_from_internet": "raw_data_fmp_stock_value.json"
        , "temp_stock_info": "_dividend-historical.json"
        , "dividend_fmp_from_local": "raw_data_fmp_from_local_div.json"
        , "company_names_from_wiki_1": "wikilist_1.csv"
        , "company_names_from_wiki_2": "wikilist_2.csv"
        , "histogram_money_made": "histogram_money_made.html"
        , "histogram_symbols": "histogram_symbols.html"
    }
}
```

# Getting Started

1. Create secret_file.json with your secret key
2. Add folder structure as you need 
3. Add `companies` and `stock_info` folder
4. Add `s&p_companies_ticker_name.csv` inside the folder companies

