# Backtesting Dividend Portfolio

## Description

This repository performs backtesting on financial data for dividend portfolios. It requires specific configurations and datasets to operate fully. However, for testing purposes, there are provided test classes that are not constrained by specific data.

## Quick Start

### Local Setup
1. Clone the repository.
2. Install the required packages from `requirements.txt`.
3. Copy and Paste the `config.json` file from the setup inside the root directory.
4. Navigate to the source folder using a terminal.
5. Run the command: `python main.py`.
- **Note:** You can only use options 7a or 7b.

### Docker Setup
1. Clone the repository.
2. Copy and Paste the `config.json` file from the setup inside the root directory
3. Build the Docker image: `docker build -t backtesting_dividend_portfolio .`
4. Run the Docker container: `docker run -it backtesting_dividend_portfolio`.
- **Note:** You can only use options 7a or 7b.

## Setup

Follow these steps to set up the project. 

Alternatively, you can download and extract this setup directory https://th-koeln.sciebo.de/s/TJeKTtYPWlVtwph in the main folder of this project. 
It includes: 
- Folder directory
- Ticker names
- Config files

**Note:** You still need to download data and use your own API keys.

### Get Company Ticker Symbols

Company names are all the unique values from these two lists:
- [List of S&P 500 Companies](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#Selected_changes_to_the_list_of_S&P_500_components)

You can scrape the data using tools like [wikitable2csv](https://wikitable2csv.ggor.de/).

### Create Folders

Ensure the following folders are created:

```
data/ticker_names
data/stock_data
data/stock_data/downloaded_divs_from_fmp
data/strategy_result
data/visualize
```

### Configuration Files

#### `secret_file.json`

Store your API keys in `secret_file.json`:

```json
{
    "secret_key_alphavantage": "API_KEY",
    "secret_key_fmp": "API_KEY"
}
```

#### `config.json`

Store all file paths in `config.json`:

```json
{
    "file_names": {
        "company_names": "../data/ticker_names/ticker_symbols.csv",
        "company_names_from_wiki_1": "../data/ticker_names/wikilist_1.csv",
        "company_names_from_wiki_2": "../data/ticker_names/wikilist_2.csv",
        "fmp_dividends": "../data/stock_infos/fmp_dividend_data.json",
        "fmp_stocks": "../data/stock_infos/fmp_stock_data.json",
        "alpha_vantage_data": "../data/stock_infos/alpha_vantage_dividend_and_stock_data.json",
        "temp_dividend_fmp": "../data/stock_infos/downloaded_divs_from_fmp/REPLACEDBYCODE_dividend-historical.json",
        "results_from_strategie_execution": "../data/results/strategy_results.csv",
        "histogram_money_made": "../data/vis/histogram_money_made.html",
        "histogram_symbols": "../data/vis/histogram_symbols.html",
        "visualize_path": "../data/visualize/",
        "test_strategie_data_interface": "./tests/test_strategie_data_interface.py",
        "test_strategie_calc_indikator": "./tests/test_strategie_calc_indikator.py",
        "secret_file": "../secret_file.json"
    }
}
```

## Getting Started

### Local Setup

1. Clone the repository.
2. Install the required packages from `requirements.txt`.
3. Obtain the company ticker symbols.
4. Create the `config.json` and set up all paths as needed.
5. Navigate to the source folder using a terminal.
6. Start the program with `python run`.
7. Download the data from the APIs using options 1, 2a, and 2c.
8. Generate results using option 4.
9. Generate visualizations using option 4.

### Docker Setup

1. Clone the repository.
2. Obtain the company ticker symbols.
3. Create the `config.json` and set up all paths as needed.
4. Build the Docker image: `docker build -t backtesting_dividend_portfolio .`
5. Run the Docker container: `docker run -it -v /path/to/local/data:/app/data/visualize backtesting_dividend_portfolio`
   - The volume mount is necessary to get the visualizations from the program.
   - The `-it` flag is necessary for an interactive terminal.
6. Download the data from the APIs using options 1, 2a, and 2c.
7. Generate results using option 4.
8. Generate visualizations using option 5.

---

This README provides a comprehensive guide to setting up and running the backtesting dividend portfolio project both locally and using Docker. 
If you encounter any issues or get stuck during the setup or execution of this project, please don't hesitate to reach out. You can write to me directly or open an issue in the repository. 
I'll do my best to assist you promptly.
