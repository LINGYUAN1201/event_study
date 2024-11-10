# event_study/data_loader.py

import pandas as pd

def load_data(event_file, firm_file, market_file, ff_factors_file):
    """
    加载Excel文件，并确保'Stkcd'和'Symbol'列以字符串形式读取，以保留前置零。
    """
    event_data = pd.read_excel(event_file, dtype={'Symbol': str})
    firm_data = pd.read_excel(firm_file, dtype={'Stkcd': str})
    market_data = pd.read_excel(market_file)
    ff_factors = pd.read_excel(ff_factors_file)

    for df in [event_data, firm_data, market_data, ff_factors]:
        df['Date'] = pd.to_datetime(df['Date'])

    return event_data, firm_data, market_data, ff_factors
