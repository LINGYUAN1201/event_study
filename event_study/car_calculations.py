# event_study/car_calculations.py

import numpy as np
from datetime import timedelta
from .regression_models import perform_regressions, calculate_abnormal_returns
from .statistical_tests import run_tests

def calculate_CAR_AR(symbol, event_date, firm_data, market_data, ff_factors, event_window_days, estimation_window_days, models_to_use):
    """
    对于每个事件，计算CAR和AR，执行统计检验，并返回结果。
    """

    event_window_start, event_window_end = event_window_days


    estimation_start = event_date - timedelta(days=estimation_window_days)
    estimation_end = event_date - timedelta(days=1)
    event_start = event_date + timedelta(days=event_window_start)
    event_end = event_date + timedelta(days=event_window_end)


    firm_estimation = firm_data[
        (firm_data['Stkcd'] == symbol) &
        (firm_data['Date'] >= estimation_start) &
        (firm_data['Date'] <= estimation_end)
    ]

    market_estimation = market_data[
        (market_data['Date'] >= estimation_start) &
        (market_data['Date'] <= estimation_end)
    ]

    ff_estimation = ff_factors[
        (ff_factors['Date'] >= estimation_start) &
        (ff_factors['Date'] <= estimation_end)
    ]

    merged_estimation = firm_estimation.merge(market_estimation, on='Date', how='inner')\
                                     .merge(ff_estimation, on='Date', how='inner')

    if len(merged_estimation) < estimation_window_days * 0.8:
        return None


    models = perform_regressions(merged_estimation, models_to_use)


    firm_event = firm_data[
        (firm_data['Stkcd'] == symbol) &
        (firm_data['Date'] >= event_start) &
        (firm_data['Date'] <= event_end)
    ]

    market_event = market_data[
        (market_data['Date'] >= event_start) &
        (market_data['Date'] <= event_end)
    ]

    ff_event = ff_factors[
        (ff_factors['Date'] >= event_start) &
        (ff_factors['Date'] <= event_end)
    ]

    merged_event = firm_event.merge(market_event, on='Date', how='inner')\
                             .merge(ff_event, on='Date', how='inner')

    if merged_event.empty:
        return None


    merged_event = calculate_abnormal_returns(models, merged_event, models_to_use)


    merged_event['EventDay'] = (merged_event['Date'] - event_date).dt.days

    merged_event = merged_event.sort_values('EventDay')

    for model in models_to_use:
        ar_col = f'AbnormalReturn_{model}'
        car_col = f'CAR_{model}'
        merged_event[car_col] = merged_event[ar_col].cumsum()

    test_results = {}
    for model in models_to_use:

        car_col = f'CAR_{model}'
        car_values = merged_event[car_col].dropna().values
        car_mean = np.mean(car_values)
        car_tests = run_tests(car_values)


        ar_col = f'AbnormalReturn_{model}'
        ar_values = merged_event[ar_col].dropna().values
        ar_mean = np.mean(ar_values)
        ar_tests = run_tests(ar_values)


        test_results[f'AvgCAR_{model}'] = car_mean
        test_results[f't_statistic_{model}'] = car_tests.get('t_statistic', np.nan)
        test_results[f't_p_value_{model}'] = car_tests.get('t_p_value', np.nan)
        test_results[f'binomial_statistic_{model}'] = car_tests.get('binomial_statistic', np.nan)
        test_results[f'binomial_p_value_{model}'] = car_tests.get('binomial_p_value', np.nan)
        test_results[f'wilcoxon_statistic_{model}'] = car_tests.get('wilcoxon_statistic', np.nan)
        test_results[f'wilcoxon_p_value_{model}'] = car_tests.get('wilcoxon_p_value', np.nan)
        test_results[f'permutation_statistic_{model}'] = car_tests.get('permutation_statistic', np.nan)
        test_results[f'permutation_p_value_{model}'] = car_tests.get('permutation_p_value', np.nan)

        test_results[f'AvgAR_{model}'] = ar_mean
        test_results[f't_statistic_AR_{model}'] = ar_tests.get('t_statistic', np.nan)
        test_results[f't_p_value_AR_{model}'] = ar_tests.get('t_p_value', np.nan)
        test_results[f'binomial_statistic_AR_{model}'] = ar_tests.get('binomial_statistic', np.nan)
        test_results[f'binomial_p_value_AR_{model}'] = ar_tests.get('binomial_p_value', np.nan)
        test_results[f'wilcoxon_statistic_AR_{model}'] = ar_tests.get('wilcoxon_statistic', np.nan)
        test_results[f'wilcoxon_p_value_AR_{model}'] = ar_tests.get('wilcoxon_p_value', np.nan)
        test_results[f'permutation_statistic_AR_{model}'] = ar_tests.get('permutation_statistic', np.nan)
        test_results[f'permutation_p_value_AR_{model}'] = ar_tests.get('permutation_p_value', np.nan)


    last_day = merged_event['EventDay'].max()
    last_day_data = merged_event[merged_event['EventDay'] == last_day]
    last_day_tests = {}

    for model in models_to_use:
        car_col = f'CAR_{model}'
        if not last_day_data.empty:
            car_value = last_day_data.iloc[0][car_col]
            last_day_tests[f'CAR_LastDay_{model}'] = car_value
        else:
            last_day_tests[f'CAR_LastDay_{model}'] = np.nan

    result = {
        'Symbol': symbol,
        'EventDate': event_date,
    }
    result.update(test_results)
    result.update(last_day_tests)

    return result, merged_event
