import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from event_study.data_loader import load_data
from event_study.car_calculations import calculate_CAR_AR
from event_study.statistical_tests import run_tests

warnings.filterwarnings("ignore")

def run_event_study(models_to_use=None, event_window_days=(-1, 1), estimation_window_days=250,
                    generate_plots=True, event_file='Event.xlsx', firm_file='Firm.xlsx',
                    market_file='Market.xlsx', ff_factors_file='FF factor.xlsx'):
    """
    运行事件研究分析。

    参数：
    - models_to_use：要使用的模型列表。
    - event_window_days：事件窗口大小（区间，如 (-1, 1) 表示 [前 1 天，后 1 天]）。
    - estimation_window_days：估计窗口大小。
    - generate_plots：是否生成可视化结果。
    - event_file：事件数据文件路径。
    - firm_file：公司数据文件路径。
    - market_file：市场数据文件路径。
    - ff_factors_file：FF因子数据文件路径。
    """
    if models_to_use is None:
        models_to_use = ['MarketModel', 'MarketAdjusted', '3F', '4F', '5F']

    # 加载数据
    event_data, firm_data, market_data, ff_factors = load_data(
        event_file=event_file,
        firm_file=firm_file,
        market_file=market_file,
        ff_factors_file=ff_factors_file
    )

    summary_results = []
    all_event_data = []

    for idx, row in event_data.iterrows():
        symbol = row['Symbol']
        event_date = row['Date']

        res = calculate_CAR_AR(
            symbol=symbol,
            event_date=event_date,
            firm_data=firm_data,
            market_data=market_data,
            ff_factors=ff_factors,
            event_window_days=event_window_days,  # 传入事件窗口范围
            estimation_window_days=estimation_window_days,
            models_to_use=models_to_use
        )

        if res:
            result, merged_event = res
            summary_results.append(result)
            all_event_data.append(merged_event)

    if not summary_results:
        print("No valid event result was found.")
        return

    summary_df = pd.DataFrame(summary_results)

    # 保存 individual CAR results with tests
    with pd.ExcelWriter("event_study_individual_CAR_results_with_tests.xlsx", engine='xlsxwriter') as writer:
        for model in models_to_use:
            cols = ['Symbol', 'EventDate',
                    f'AvgCAR_{model}', f't_statistic_{model}', f't_p_value_{model}',
                    f'patell_statistic_{model}', f'patell_p_value_{model}',
                    f'wilcoxon_statistic_{model}', f'wilcoxon_p_value_{model}',
                    f'binomial_statistic_{model}', f'binomial_p_value_{model}',
                    f'permutation_statistic_{model}', f'permutation_p_value_{model}',
                    f'corrado_statistic_{model}', f'corrado_p_value_{model}',
                    f'AvgAR_{model}', f't_statistic_AR_{model}', f't_p_value_AR_{model}',
                    f'patell_statistic_AR_{model}', f'patell_p_value_AR_{model}',
                    f'wilcoxon_statistic_AR_{model}', f'wilcoxon_p_value_AR_{model}',
                    f'binomial_statistic_AR_{model}', f'binomial_p_value_AR_{model}',
                    f'permutation_statistic_AR_{model}', f'permutation_p_value_AR_{model}',
                    f'corrado_statistic_AR_{model}', f'corrado_p_value_AR_{model}']
            existing_cols = [col for col in cols if col in summary_df.columns]
            model_df = summary_df[existing_cols].copy()
            model_df.rename(columns={
                f'AvgCAR_{model}': 'AvgCAR',
                f't_statistic_{model}': 't_statistic',
                f't_p_value_{model}': 't_p_value',
                f'patell_statistic_{model}': 'Patell_statistic',
                f'patell_p_value_{model}': 'Patell_p_value',
                f'wilcoxon_statistic_{model}': 'Wilcoxon_statistic',
                f'wilcoxon_p_value_{model}': 'Wilcoxon_p_value',
                f'binomial_statistic_{model}': 'Binomial_statistic',
                f'binomial_p_value_{model}': 'Binomial_p_value',
                f'permutation_statistic_{model}': 'Permutation_statistic',
                f'permutation_p_value_{model}': 'Permutation_p_value',
                f'corrado_statistic_{model}': 'Corrado_statistic',
                f'corrado_p_value_{model}': 'Corrado_p_value',
                f'AvgAR_{model}': 'AvgAR',
                f't_statistic_AR_{model}': 't_statistic_AR',
                f't_p_value_AR_{model}': 't_p_value_AR',
                f'patell_statistic_AR_{model}': 'Patell_statistic_AR',
                f'patell_p_value_AR_{model}': 'Patell_p_value_AR',
                f'wilcoxon_statistic_AR_{model}': 'Wilcoxon_statistic_AR',
                f'wilcoxon_p_value_AR_{model}': 'Wilcoxon_p_value_AR',
                f'binomial_statistic_AR_{model}': 'Binomial_statistic_AR',
                f'binomial_p_value_AR_{model}': 'Binomial_p_value_AR',
                f'permutation_statistic_AR_{model}': 'Permutation_statistic_AR',
                f'permutation_p_value_AR_{model}': 'Permutation_p_value_AR',
                f'corrado_statistic_AR_{model}': 'Corrado_statistic_AR',
                f'corrado_p_value_AR_{model}': 'Corrado_p_value_AR'
            }, inplace=True)
            model_df.to_excel(writer, sheet_name=model, index=False)

    # 保存事件窗口最后一天的CAR测试结果
    with pd.ExcelWriter("event_study_CAR_last_day_tests.xlsx", engine='xlsxwriter') as writer:
        cols = ['Symbol', 'EventDate'] + [f'CAR_LastDay_{model}' for model in models_to_use]
        existing_cols = [col for col in cols if col in summary_df.columns]
        model_df = summary_df[existing_cols].copy()
        model_df.to_excel(writer, sheet_name='CAR_Last_Day', index=False)

    # 保存每日平均AR及其测试结果
    combined_event_data = pd.concat(all_event_data, ignore_index=True)

    ar_cols = {f'AbnormalReturn_{model}': 'mean' for model in models_to_use}
    average_AR_per_day = combined_event_data.groupby('EventDay').agg(ar_cols).reset_index()

    with pd.ExcelWriter("event_study_daily_AR_results_with_tests.xlsx", engine='xlsxwriter') as writer:
        for model in models_to_use:
            ar_col = f'AbnormalReturn_{model}'
            ar_grouped = combined_event_data.groupby('EventDay')[ar_col]

            test_results = []
            for day, group in ar_grouped:
                data = group.dropna().values
                if len(data) > 0:
                    tests = run_tests(data)
                else:
                    tests = {}
                result = {'EventDay': day, 'AvgAR': average_AR_per_day.loc[average_AR_per_day['EventDay'] == day, ar_col].values[0]}
                for key, value in tests.items():
                    result[f'{key}'] = value
                test_results.append(result)

            test_df = pd.DataFrame(test_results)

            test_df.rename(columns={
                't_statistic': 't_statistic',
                't_p_value': 't_p_value',
                'patell_statistic': 'Patell_statistic',
                'patell_p_value': 'Patell_p_value',
                'wilcoxon_statistic': 'Wilcoxon_statistic',
                'wilcoxon_p_value': 'Wilcoxon_p_value',
                'binomial_statistic': 'Binomial_statistic',
                'binomial_p_value': 'Binomial_p_value',
                'permutation_statistic': 'Permutation_statistic',
                'permutation_p_value': 'Permutation_p_value',
                'corrado_statistic': 'Corrado_statistic',
                'corrado_p_value': 'Corrado_p_value'
            }, inplace=True)

            test_df.to_excel(writer, sheet_name=f'{model}_AR', index=False)

    # 保存每日平均CAR及其测试结果
    car_cols = {f'CAR_{model}': 'mean' for model in models_to_use}
    average_CAR_per_day = combined_event_data.groupby('EventDay').agg(car_cols).reset_index()

    with pd.ExcelWriter("event_study_daily_CAR_results_with_tests.xlsx", engine='xlsxwriter') as writer:
        for model in models_to_use:
            car_col = f'CAR_{model}'
            car_grouped = combined_event_data.groupby('EventDay')[car_col]

            test_results = []
            for day, group in car_grouped:
                data = group.dropna().values
                if len(data) > 0:
                    tests = run_tests(data)
                else:
                    tests = {}
                result = {'EventDay': day, 'AvgCAR': average_CAR_per_day.loc[average_CAR_per_day['EventDay'] == day, car_col].values[0]}
                for key, value in tests.items():
                    result[f'{key}'] = value
                test_results.append(result)

            test_df = pd.DataFrame(test_results)

            test_df.rename(columns={
                't_statistic': 't_statistic',
                't_p_value': 't_p_value',
                'patell_statistic': 'Patell_statistic',
                'patell_p_value': 'Patell_p_value',
                'wilcoxon_statistic': 'Wilcoxon_statistic',
                'wilcoxon_p_value': 'Wilcoxon_p_value',
                'binomial_statistic': 'Binomial_statistic',
                'binomial_p_value': 'Binomial_p_value',
                'permutation_statistic': 'Permutation_statistic',
                'permutation_p_value': 'Permutation_p_value',
                'corrado_statistic': 'Corrado_statistic',
                'corrado_p_value': 'Corrado_p_value'
            }, inplace=True)

            test_df.to_excel(writer, sheet_name=f'{model}_CAR', index=False)

    # 可视化部分
    if generate_plots:
        plot_models = []
        color_map = {'MarketModel': 'blue', 'MarketAdjusted': 'green', '3F': 'purple', '4F': 'orange', '5F': 'red'}
        for model in models_to_use:
            plot_models.append({
                "model": model,
                "color": color_map.get(model, 'black'),
                "title": f"Average AR by Event Day ({model})"
            })

        for plot_model in plot_models:
            model = plot_model['model']
            ar_col = f'AbnormalReturn_{model}'
            plt.figure(figsize=(10, 6))
            sns.lineplot(data=average_AR_per_day, x='EventDay', y=ar_col, color=plot_model['color'], marker='o')
            plt.title(plot_model['title'], fontsize=14, fontweight='bold')
            plt.xlabel("Event Day (Relative to Event Date)", fontsize=12)
            plt.ylabel("Average Abnormal Return (AR)", fontsize=12)
            plt.axvline(x=0, linestyle='--', color='gray')
            plt.xticks(ticks=range(event_window_days[0], event_window_days[1] + 1))
            plt.grid(True, which='both', linestyle='--', linewidth=0.5)
            plt.tight_layout()
            plt.savefig(f"AR_{model}.png")
            plt.close()

    print("The event study analysis has been successfully completed and all output files have been generated.")