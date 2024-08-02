import sys
import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from config import Config

# 將專案根目錄添加到 sys.path 中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def fetch_bank_trading_data(date, token):
    url = 'https://api.finmindtrade.com/api/v4/data'
    params = {
        'dataset': 'TaiwanStockGovernmentBankBuySell',
        'start_date': date,
        'end_date': None,
        'token': token
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "Requests reach the upper limit" in data['msg']:
        print(f"Requests reach the upper limit for date {date}. Stopping execution.")
        return None
    if data['msg'] == 'success':
        if len(data['data']):
            return pd.DataFrame(data['data'])
        else:
            return pd.DataFrame()
    else:
        print(f"Error fetching data for date {date}: {data['msg']}")
        return pd.DataFrame()

def save_to_csv(dataframe, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    if os.path.exists(filename):
        dataframe.to_csv(filename, mode='a', header=False, index=False)
    else:
        dataframe.to_csv(filename, index=False)

def main(start_date_str, end_date_str):
    token = Config.FINMIND_API_TOKEN
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        print(f"Fetching data for {date_str}")
        daily_data = fetch_bank_trading_data(date_str, token)
        if data is None:
            save_progress(3, None, date_str)  # 記錄進度，停止執行
            return
        if not daily_data.empty:
            filename = os.path.join('data', "TaiwanStockGovernmentBankBuySell.csv")
            save_to_csv(daily_data, filename)
        current_date += timedelta(days=1)

if __name__ == "__main__":
    start_date = sys.argv[1]
    end_date = sys.argv[2]
    main(start_date, end_date)
