import pytest

# Import the module(s) you want to test

import data_business_logic.strategie_data_interface as str_data


import pandas as pd


# Fixture(s) (optional)
@pytest.fixture(name="setup")
def setup_fixture():
    # Setup code that needs to run before each test
    calc_data = str_data.StrategieDataInterface()

    data_combined = [
        {
            "date": pd.to_datetime("2021-01-01").to_period("M"),
            "information": "alpha_close",
            "TEST": 2.0,
        },
        {
            "date": pd.to_datetime("2021-01-01").to_period("M"),
            "information": "alpha_dividend",
            "TEST": 2.0,
        },
        {
            "date": pd.to_datetime("2022-01-01").to_period("M"),
            "information": "alpha_close",
            "TEST": 5.0,
        },
        {
            "date": pd.to_datetime("2023-01-01").to_period("M"),
            "information": "alpha_close",
            "TEST": 10.0,
        },
        {
            "date": pd.to_datetime("2024-01-01").to_period("M"),
            "information": "alpha_close",
            "TEST": 11.0,
        },
        {
            "date": pd.to_datetime("2023-01-01").to_period("M"),
            "information": "alpha_dividend",
            "TEST": 3.0,
        },
        {
            "date": pd.to_datetime("2024-01-01").to_period("M"),
            "information": "alpha_dividend",
            "TEST": 3.0,
        },
        {
            "date": pd.to_datetime("2025-01-01").to_period("M"),
            "information": "alpha_dividend",
            "TEST": 3.0,
        },
        {
            "date": pd.to_datetime("2025-02-01").to_period("M"),
            "information": "alpha_dividend",
            "TEST": 4.0,
        },
        {
            "date": pd.to_datetime("2025-01-01").to_period("M"),
            "information": "alpha_close",
            "TEST": 12.0,
        },
    ]

    df_combined = pd.DataFrame(data_combined)
    yield calc_data, df_combined
    # Teardown code that needs to run after each test


# Test cases
def test_invest_on_date(setup):
    calc_data, df_combined = setup

    result = calc_data.invest_on_date(pd.to_datetime("2021-01-01"), "TEST", df_combined)
    # print(df_combined)
    # print(result)
    assert result.iloc[0] == 2.0

    pass


# TODO: not happy path when no dividend is given
def test_get_dividends(setup):
    calc_data, df_combined = setup

    # well there is missing the symbol variable
    result = calc_data.get_dividends(
        df_combined, pd.to_datetime("2021-01-01"), 2.0, "TEST"
    )
    # print(df_combined)
    # print(result["alpha_dividend"])
    assert result["alpha_dividend"].iloc[0] == 2.0

    pass


def test_check_money_made_by_div(setup):
    calc_data, df_combined = setup

    result = calc_data.check_money_made_by_div(
        start_date=pd.to_datetime("2021-01-01"),
        look_foward_years=5,
        symbol="TEST",
        df_combined=df_combined,
        money_invested=100,
    )
    print(df_combined)
    print(result)
    assert result["money"].astype(float).iloc[0] == 102.0


# TODO error when no stock on the given dates
def test_check_money_made_by_div_sad_path(setup):
    calc_data, df_combined = setup

    result = calc_data.check_money_made_by_div(
        start_date=pd.to_datetime("2021-01-01"),
        look_foward_years=15,
        symbol="TEST",
        df_combined=df_combined,
        money_invested=100,
    )
    print(df_combined)
    print(result)
    assert result["money"].astype(float).iloc[0] == 103.0

    pass


def test_check_for_increased_stock(setup):
    calc_data, df_combined = setup

    result = calc_data.check_for_increased_stock(
        df_combined,
        "TEST",
        100,
        start_date=pd.to_datetime("2021-01-01"),
        look_forward_years=2,
    )
    print(df_combined)
    print(result)
    assert True
    pass


def test_compound_interest_calc_recursive(setup):
    calc_data, df_combined = setup

    years = 2
    result = calc_data.compound_interest_calc_recursive(100, years, years, 0.04)
    print(result)

    calculate_by_myself = 100 * 1.04**years

    assert int(result) == int(calculate_by_myself)


def test_compound_interest_calc_recursive_with_extras(setup):
    calc_data, df_combined = setup

    start_stock_price_in_a_list = calc_data.invest_on_date(
        pd.to_datetime("2021-01-01"), "TEST", df_combined
    )        
    if start_stock_price_in_a_list.empty:
        return pd.DataFrame()

    start_stock_price = start_stock_price_in_a_list.iloc[0]

    dividends = calc_data.get_dividends(
        df_combined, pd.to_datetime("2021-01-01"), 2.0, "TEST"
    )
    output = []

    result = calc_data.compound_interest_calc_recursive_with_extras(
        100,
        dividends["alpha_close"].count(),
        dividends["alpha_close"].count(),
        start_stock_price,
        dividends["alpha_dividend"],
        dividends["alpha_close"],
        output,
    )
    print(pd.DataFrame(output).columns)
    print(pd.DataFrame(output)[["money", "dividend", "current stock price", "dividend_money"]])
    print(result)
    assert int(result) == 500
