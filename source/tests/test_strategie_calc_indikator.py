import pytest

# Import the module(s) you want to test

import data_business_logic.strategie_data_interface as str_data
import data_business_logic.startegie_calc_indikator as str_calc


import pandas as pd
from datetime import timedelta


# Fixture(s) (optional)
@pytest.fixture(name="setup")
def setup_fixture():
    # Setup code that needs to run before each test
    calc_indikator = str_calc.StrategieCalcIndikator()
    calc_data = str_data.StrategieDataInterface()

    # basic dataframe only contains two rows
    dates = ["2021-01", "2021-01", "2022-01", "2022-01", "2023-01", "2023-01"]
    informations = [
        "alpha_close",
        "alpha_dividend",
        "alpha_close",
        "alpha_dividend",
        "alpha_close",
        "alpha_dividend",
    ]
    tests = [2.0, 2.0, 2.0, 2.0, 2.0, 2.0]

    data_combined = [
        {"date": pd.to_datetime(date).to_period("M"), "information": info, "TEST": test}
        for date, info, test in zip(dates, informations, tests)
    ]

    df_combined = pd.DataFrame(data_combined)

    yield calc_indikator, calc_data, df_combined
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


def test_difference_between_consecutive_years(setup):
    calc_indikator, calc_data, df_combined = setup

    dividends = calc_data.get_dividends(
        df_combined, pd.to_datetime("2021-01-01"), 3.0, "TEST"
    )
    print(dividends)
    year_dif = calc_indikator.difference_between_consecutive_years(
        dividends, pd.to_datetime("2021-01-01") + timedelta(days=365 * 3)
    )
    print(year_dif)

    assert year_dif.count().iloc[0] == 2.0


# continuity tests


def test_calculate_dividend_continuity_x_years_calc_numb(setup):
    calc_indikator, calc_data, df_combined = setup

    dividends = calc_data.get_dividends(
        df_combined, pd.to_datetime("2021-01-01"), 3.0, "TEST"
    )
    print(dividends)
    year_dif = calc_indikator.difference_between_consecutive_years(
        dividends, pd.to_datetime("2021-01-01") + timedelta(days=365 * 3)
    )
    result = calc_indikator.calculate_dividend_continuity_x_years_calc_numb(year_dif)

    assert result == 2


def test_calculate_dividend_continuity_no_div_reductions_calc_numb(setup):
    calc_indikator, calc_data, df_combined = setup

    dividends = calc_data.get_dividends(
        df_combined, pd.to_datetime("2021-01-01"), 3.0, "TEST"
    )
    print(dividends)
    year_dif = calc_indikator.difference_between_consecutive_years(
        dividends, pd.to_datetime("2021-01-01") + timedelta(days=365 * 3)
    )
    result = calc_indikator.calculate_dividend_continuity_no_div_reductions_calc_numb(
        year_dif
    )

    assert result == 2


# growth tests


def test_calculate_dividend_growth_calc_numb(setup):
    calc_indikator, calc_data, df_combined = setup

    dividends = calc_data.get_dividends(
        df_combined, pd.to_datetime("2021-01-01"), 3.0, "TEST"
    )
    print(dividends)
    year_dif = calc_indikator.difference_between_consecutive_years(
        dividends, pd.to_datetime("2021-01-01") + timedelta(days=365 * 3)
    )
    result = calc_indikator.calculate_dividend_growth_calc_numb(year_dif)

    assert result == 1


def test_calculate_dividend_growth_indikative_calc_numb(setup):
    calc_indikator, calc_data, df_combined = setup

    dividends = calc_data.get_dividends(
        df_combined, pd.to_datetime("2021-01-01"), 3.0, "TEST"
    )
    print(dividends)
    year_dif = calc_indikator.difference_between_consecutive_years(
        dividends, pd.to_datetime("2021-01-01") + timedelta(days=365 * 3)
    )
    result = calc_indikator.calculate_dividend_growth_indikative_calc_numb(year_dif)

    assert result == 0


# yield tests


def test_calculate_dividend_yield_indikative_calc_numb(setup):
    calc_indikator, calc_data, df_combined = setup

    dividends = calc_data.get_dividends(
        df_combined, pd.to_datetime("2021-01-01"), 3.0, "TEST"
    )

    result = calc_indikator.calculate_dividend_yield_indikative_calc_numb(
        dividends, pd.to_datetime("2021-01-01") + timedelta(days=365 * 3)
    )

    assert result == 2


def test_calculate_dividend_yield_historic_calc_numb(setup):
    calc_indikator, calc_data, df_combined = setup

    dividends = calc_data.get_dividends(
        df_combined, pd.to_datetime("2021-01-01"), 3.0, "TEST"
    )

    result = calc_indikator.calculate_dividend_yield_historic_calc_numb(
        dividends, pd.to_datetime("2021-01-01") + timedelta(days=365 * 3)
    )
    print(dividends)

    assert result == 2


# what happens if a company vanishes
# what happens if the company has no dividends
# what happens if the company has no stock prices at the given dates
