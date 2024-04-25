import pytest

# Import the module(s) you want to test
import data_business_logic.bussiness_logic_classes as bl
import pandas as pd
import datetime as dt


# Fixture(s) (optional)
@pytest.fixture
def setup():
    # Setup code that needs to run before each test
    single_stock_checker = bl.single_stock_check()

    data_combined = [{'date': pd.to_datetime('2021-01-01').to_period("M"), "information": "alpha_close", "TEST": 2.0},
                     {'date': pd.to_datetime('2021-01-01').to_period("M"), "information": "alpha_dividend", "TEST": 2.0},
                     {'date': pd.to_datetime('2022-01-01').to_period("M"), "information": "alpha_close", "TEST": 5.0},
                     {'date': pd.to_datetime('2023-01-01').to_period("M"), "information": "alpha_close", "TEST": 10.0},
                     {'date': pd.to_datetime('2024-01-01').to_period("M"), "information": "alpha_close", "TEST": 11.0},
                     {'date': pd.to_datetime('2025-01-01').to_period("M"), "information": "alpha_close", "TEST": 12.0},
                     {'date': pd.to_datetime('2025-01-01').to_period("M"), "information": "alpha_dividend", "TEST": 3.0},
                     {'date': pd.to_datetime('2025-02-01').to_period("M"), "information": "alpha_dividend", "TEST": 4.0}]

    df_combined = pd.DataFrame(data_combined)
    yield single_stock_checker, df_combined
    # Teardown code that needs to run after each test


# Test cases
def test_invest_on_date(setup):
    single_stock_checker, df_combined = setup

    result = single_stock_checker.invest_on_date(pd.to_datetime('2021-01-01'), "TEST", df_combined)
    # print(df_combined)
    # print(result)
    assert result.iloc[0] == 2.0

    pass

# TODO: not happy path when no dividend is given
def test_get_dividends(setup):
    single_stock_checker, df_combined = setup

    # well there is missing the symbol variable
    result = single_stock_checker.get_dividends(df_combined, pd.to_datetime('2021-01-01'),2.0 ,"TEST")
    # print(df_combined)
    # print(result["alpha_dividend"])
    assert result["alpha_dividend"].iloc[0] == 2.0

    pass


def test_check_money_made_by_div(setup):
    single_stock_checker, df_combined = setup

    result = single_stock_checker.check_money_made_by_div(start_date=pd.to_datetime("2021-01-01"), look_foward_years=5, symbol="TEST", df_combined=df_combined, money_invested=100)
    print(df_combined)
    print(result)
    assert result["money"].astype(float).iloc[0] == 102.0

    pass


# TODO error when no stock on the given dates 
def test_check_for_increased_stock(setup):
    single_stock_checker, df_combined = setup

    result = single_stock_checker.check_for_increased_stock(df_combined, "TEST", 100, start_date=pd.to_datetime("2021-01-01"), look_forward_years=2)
    print(df_combined)
    print(result)
    assert True
    pass

def test_compound_interest_calc_recursive():
    single_stock_checker = bl.single_stock_check()

    years = 2
    result = single_stock_checker.compound_interest_calc_recursive(100, years, years, 0.04)
    print(result)

    calculate_by_myself = 100 * 1.04 ** years

    assert int(result) == int(calculate_by_myself)


def test_compound_interest_calc_recursive_with_extras(setup):
    single_stock_checker, df_combined = setup

    first_stock_price = single_stock_checker.invest_on_date(pd.to_datetime('2021-01-01'), "TEST", df_combined)
    dividends = single_stock_checker.get_dividends(df_combined, pd.to_datetime('2021-01-01'), 2.0, "TEST")
    output = []

    result = single_stock_checker.compound_interest_calc_recursive_with_extras(100, dividends["alpha_close"].count(), dividends["alpha_close"].count(),first_stock_price, dividends["alpha_dividend"], dividends["alpha_close"], output) 
    print(output)
    assert int(result) == 102

    pass

def test_calculate_dividend_yield(setup):
    single_stock_checker, df_combined = setup

    dividends = single_stock_checker.get_dividends(df_combined, pd.to_datetime('2021-01-01'), 2.0, "TEST")
    print(dividends)
    result = single_stock_checker.calculate_dividend_yield(dividends)
    print(result)
    assert result == 2.0

    pass

def test_calculate_dividend_growth(setup):
    single_stock_checker, df_combined = setup

    dividends = single_stock_checker.get_dividends(df_combined, pd.to_datetime('2021-01-01'), 10.0, "TEST")
    result = single_stock_checker.calculate_dividend_growth(dividends)
    print(result)
    assert result == 0.41666666666666663

    pass

def test_calculate_dividend_stability(setup):
    single_stock_checker, df_combined = setup

    dividends = single_stock_checker.get_dividends(df_combined, pd.to_datetime('2021-01-01'), 10.0, "TEST")
    print(dividends)
    result = single_stock_checker.calculate_dividend_stability(dividends)
    print(result)
    assert result == 1022450.0

    pass

# what happens if a company vanishes
# what happens if the company has no dividends
# what happens if the company has no stock prices at the given dates