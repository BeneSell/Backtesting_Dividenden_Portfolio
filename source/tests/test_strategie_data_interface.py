import pytest

# Import the module(s) you want to test

import data_business_logic.strategie_data_interface as str_data


import pandas as pd


# Fixture(s) (optional)
@pytest.fixture(name="setup")
def setup_fixture():
    # Setup code that needs to run before each test
    calc_data = str_data.StrategieDataInterface()

    # basic dataframe only contains two rows
    dates = ["2021-01", "2021-01", "2022-01", "2022-01"]
    informations = ["alpha_close", "alpha_dividend", "alpha_close", "alpha_dividend"]
    tests = [2.0, 2.0, 2.0, 2.0]

    data_combined = [
        {"date": pd.to_datetime(date).to_period("M"), "information": info, "TEST": test}
        for date, info, test in zip(dates, informations, tests)
    ]

    df_combined = pd.DataFrame(data_combined)

    yield calc_data, df_combined
    # Teardown code that needs to run after each test


def add_row_to_test_data(df_combined, date, information, value):

    new_data = [
        {
            "date": pd.to_datetime(date).to_period("M"),
            "information": information,
            "TEST": value,
        }
    ]
    df_combined = pd.concat([df_combined, pd.DataFrame(new_data)], ignore_index=True)
    return df_combined


def test_invest_on_date(setup):
    calc_data, df_combined = setup

    result = calc_data.invest_on_date(pd.to_datetime("2021-01-01"), "TEST", df_combined)
    # print(df_combined)
    # print(result)
    assert result.iloc[0] == 2.0


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
    assert result["money"].astype(float).iloc[0] == 100


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


def test_check_for_increased_stock(setup):
    calc_data, df_combined = setup

    df_to_test = add_row_to_test_data(df_combined, "2023-01", "alpha_close", 2)
    df_to_test = add_row_to_test_data(df_to_test, "2023-01", "alpha_dividend", 2)

    result = calc_data.check_for_increased_stock(
        df_to_test,
        "TEST",
        100,
        start_date=pd.to_datetime("2021-01-01"),
        look_forward_years=2,
    )
    print(df_to_test)
    print(result)
    assert True


def test_compound_interest_calc_recursive(setup):
    calc_data, df_combined = setup

    years = 2
    result = calc_data.compound_interest_calc_recursive(100, years, years, 0.04)
    print(result)

    calculate_by_myself = 100 * 1.04**years

    assert int(result) == int(calculate_by_myself)


def test_compound_interest_calc_recursive_with_extras(setup):
    calc_data, df_combined = setup

    df_to_test = add_row_to_test_data(df_combined, "2023-01", "alpha_close", 4)
    df_to_test = add_row_to_test_data(df_to_test, "2023-01", "alpha_dividend", 4)

    start_stock_price_in_a_list = calc_data.invest_on_date(
        pd.to_datetime("2021-01-01"), "TEST", df_to_test
    )
    if start_stock_price_in_a_list.empty:
        return pd.DataFrame()

    start_stock_price = start_stock_price_in_a_list.iloc[0]

    dividends = calc_data.get_dividends(
        df_to_test, pd.to_datetime("2021-01-01"), 2.0, "TEST"
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
    print(
        pd.DataFrame(output)[
            ["money", "dividend", "current stock price", "dividend_money"]
        ]
    )
    print(result)
    assert int(result) == 200
