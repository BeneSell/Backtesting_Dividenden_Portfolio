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
            "TEST": 1.0,
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
    yield calc_indikator, calc_data, df_combined
    # Teardown code that needs to run after each test


def test_difference_between_consecutive_years(setup):
    calc_indikator, calc_data, df_combined = setup

    dividends = calc_data.get_dividends(
        df_combined, pd.to_datetime("2021-01-01"), 6.0, "TEST"
    )
    print(dividends)
    year_dif = calc_indikator.difference_between_consecutive_years(
        dividends, pd.to_datetime("2021-01-01") + timedelta(days=365 * 6)
    )
    print(year_dif)

    assert year_dif.count().iloc[0] == 1.0


# continuity tests


def test_calculate_dividend_continuity_x_years_filter(setup):
    calc_indikator, calc_data, df_combined = setup

    dividends = calc_data.get_dividends(
        df_combined, pd.to_datetime("2021-01-01"), 6.0, "TEST"
    )
    print(dividends)
    year_dif = calc_indikator.difference_between_consecutive_years(
        dividends, pd.to_datetime("2021-01-01") + timedelta(days=365 * 6)
    )
    result = calc_indikator.calculate_dividend_continuity_x_years_filter(year_dif, 2)

    assert result


def test_calculate_dividend_continuity_x_years_calc_numb(setup):
    calc_indikator, calc_data, df_combined = setup

    dividends = calc_data.get_dividends(
        df_combined, pd.to_datetime("2021-01-01"), 6.0, "TEST"
    )
    print(dividends)
    year_dif = calc_indikator.difference_between_consecutive_years(
        dividends, pd.to_datetime("2021-01-01") + timedelta(days=365 * 6)
    )
    result = calc_indikator.calculate_dividend_continuity_x_years_calc_numb(year_dif)

    assert result == 2


def test_calculate_dividend_continuity_no_div_reductions_filter(setup):
    calc_indikator, calc_data, df_combined = setup

    dividends = calc_data.get_dividends(
        df_combined, pd.to_datetime("2021-01-01"), 6.0, "TEST"
    )
    print(dividends)
    year_dif = calc_indikator.difference_between_consecutive_years(
        dividends, pd.to_datetime("2021-01-01") + timedelta(days=365 * 6)
    )
    result = calc_indikator.calculate_dividend_continuity_no_div_reductions_filter(
        year_dif
    )

    assert result


def test_calculate_dividend_continuity_no_div_reductions_calc_numb(setup):
    calc_indikator, calc_data, df_combined = setup

    dividends = calc_data.get_dividends(
        df_combined, pd.to_datetime("2021-01-01"), 6.0, "TEST"
    )
    print(dividends)
    year_dif = calc_indikator.difference_between_consecutive_years(
        dividends, pd.to_datetime("2021-01-01") + timedelta(days=365 * 6)
    )
    result = calc_indikator.calculate_dividend_continuity_no_div_reductions_calc_numb(
        year_dif
    )

    assert result == 2


# growth tests


def test_calculate_dividend_growth_filter(setup):
    calc_indikator, calc_data, df_combined = setup

    dividends = calc_data.get_dividends(
        df_combined, pd.to_datetime("2021-01-01"), 6.0, "TEST"
    )
    print(dividends)
    year_dif = calc_indikator.difference_between_consecutive_years(
        dividends, pd.to_datetime("2021-01-01") + timedelta(days=365 * 6)
    )
    result = calc_indikator.calculate_dividend_growth_filter(year_dif, 2)

    assert not result


def test_calculate_dividend_growth_calc_numb(setup):
    calc_indikator, calc_data, df_combined = setup

    dividends = calc_data.get_dividends(
        df_combined, pd.to_datetime("2021-01-01"), 6.0, "TEST"
    )
    print(dividends)
    year_dif = calc_indikator.difference_between_consecutive_years(
        dividends, pd.to_datetime("2021-01-01") + timedelta(days=365 * 6)
    )
    result = calc_indikator.calculate_dividend_growth_calc_numb(year_dif)

    assert result == 1


def test_calculate_dividend_growth_indikative_filter(setup):
    calc_indikator, calc_data, df_combined = setup

    dividends = calc_data.get_dividends(
        df_combined, pd.to_datetime("2021-01-01"), 6.0, "TEST"
    )
    print(dividends)
    year_dif = calc_indikator.difference_between_consecutive_years(
        dividends, pd.to_datetime("2021-01-01") + timedelta(days=365 * 6)
    )
    result = calc_indikator.calculate_dividend_growth_indikative_filter(year_dif)

    assert result


def test_calculate_dividend_growth_indikative_calc_numb(setup):
    calc_indikator, calc_data, df_combined = setup

    dividends = calc_data.get_dividends(
        df_combined, pd.to_datetime("2021-01-01"), 6.0, "TEST"
    )
    print(dividends)
    year_dif = calc_indikator.difference_between_consecutive_years(
        dividends, pd.to_datetime("2021-01-01") + timedelta(days=365 * 6)
    )
    result = calc_indikator.calculate_dividend_growth_indikative_calc_numb(year_dif)

    assert result == -4


# yield tests


def test_calculate_dividend_yield_indikative_filter(setup):
    calc_indikator, calc_data, df_combined = setup

    dividends = calc_data.get_dividends(
        df_combined, pd.to_datetime("2021-01-01"), 6.0, "TEST"
    )

    result = calc_indikator.calculate_dividend_yield_indikative_filter(
        dividends, pd.to_datetime("2021-01-01") + timedelta(days=365 * 6)
    )

    assert result


def test_calculate_dividend_yield_indikative_calc_numb(setup):
    calc_indikator, calc_data, df_combined = setup

    dividends = calc_data.get_dividends(
        df_combined, pd.to_datetime("2021-01-01"), 6.0, "TEST"
    )

    result = calc_indikator.calculate_dividend_yield_indikative_calc_numb(
        dividends, pd.to_datetime("2021-01-01") + timedelta(days=365 * 6)
    )

    assert result == 3


def test_calculate_dividend_yield_historic_filter(setup):
    calc_indikator, calc_data, df_combined = setup

    dividends = calc_data.get_dividends(
        df_combined, pd.to_datetime("2021-01-01"), 6.0, "TEST"
    )

    result = calc_indikator.calculate_dividend_yield_historic_filter(
        dividends, pd.to_datetime("2021-01-01") + timedelta(days=365 * 6)
    )

    assert result


def test_calculate_dividend_yield_historic_calc_numb(setup):
    calc_indikator, calc_data, df_combined = setup

    dividends = calc_data.get_dividends(
        df_combined, pd.to_datetime("2021-01-01"), 6.0, "TEST"
    )

    result = calc_indikator.calculate_dividend_yield_historic_calc_numb(
        dividends, pd.to_datetime("2021-01-01") + timedelta(days=365 * 6)
    )
    print(dividends)

    assert result == 3


# what happens if a company vanishes
# what happens if the company has no dividends
# what happens if the company has no stock prices at the given dates
