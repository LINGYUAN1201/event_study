# event_study/regression_models.py

import statsmodels.api as sm

def perform_regressions(merged_estimation_data, models_to_use):
    """
    针对不同模型执行回归分析，并返回拟合的模型。
    """
    models = {}

    if 'MarketModel' in models_to_use:
        X_market = sm.add_constant(merged_estimation_data['Retindex'])
        models['MarketModel'] = sm.OLS(merged_estimation_data['Dretnd'], X_market).fit()

    if '3F' in models_to_use or '4F' in models_to_use or '5F' in models_to_use:
        X_3F = sm.add_constant(merged_estimation_data[['RiskPremium1', 'SMB1', 'HML1']])
        models['3F'] = sm.OLS(merged_estimation_data['Dretnd'], X_3F).fit()

    if '4F' in models_to_use or '5F' in models_to_use:
        X_4F = sm.add_constant(merged_estimation_data[['RiskPremium1', 'SMB1', 'HML1', 'RMW1']])
        models['4F'] = sm.OLS(merged_estimation_data['Dretnd'], X_4F).fit()

    if '5F' in models_to_use:
        X_5F = sm.add_constant(merged_estimation_data[['RiskPremium1', 'SMB1', 'HML1', 'RMW1', 'CMA1']])
        models['5F'] = sm.OLS(merged_estimation_data['Dretnd'], X_5F).fit()

    return models

def calculate_abnormal_returns(models, merged_event_data, models_to_use):
    """
    计算不同模型下的异常收益（AR）。
    """
    if 'MarketModel' in models_to_use:
        merged_event_data['AbnormalReturn_MarketModel'] = merged_event_data['Dretnd'] - (
            models['MarketModel'].params['const'] + models['MarketModel'].params['Retindex'] * merged_event_data['Retindex']
        )

    if 'MarketAdjusted' in models_to_use:
        merged_event_data['AbnormalReturn_MarketAdjusted'] = merged_event_data['Dretnd'] - merged_event_data['Retindex']

    if '3F' in models_to_use:
        merged_event_data['AbnormalReturn_3F'] = merged_event_data['Dretnd'] - (
            models['3F'].params['const'] +
            models['3F'].params['RiskPremium1'] * merged_event_data['RiskPremium1'] +
            models['3F'].params['SMB1'] * merged_event_data['SMB1'] +
            models['3F'].params['HML1'] * merged_event_data['HML1']
        )

    if '4F' in models_to_use:
        merged_event_data['AbnormalReturn_4F'] = merged_event_data['Dretnd'] - (
            models['4F'].params['const'] +
            models['4F'].params['RiskPremium1'] * merged_event_data['RiskPremium1'] +
            models['4F'].params['SMB1'] * merged_event_data['SMB1'] +
            models['4F'].params['HML1'] * merged_event_data['HML1'] +
            models['4F'].params['RMW1'] * merged_event_data['RMW1']
        )

    if '5F' in models_to_use:
        merged_event_data['AbnormalReturn_5F'] = merged_event_data['Dretnd'] - (
            models['5F'].params['const'] +
            models['5F'].params['RiskPremium1'] * merged_event_data['RiskPremium1'] +
            models['5F'].params['SMB1'] * merged_event_data['SMB1'] +
            models['5F'].params['HML1'] * merged_event_data['HML1'] +
            models['5F'].params['RMW1'] * merged_event_data['RMW1'] +
            models['5F'].params['CMA1'] * merged_event_data['CMA1']
        )

    return merged_event_data
