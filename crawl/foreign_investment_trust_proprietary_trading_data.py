import sys
import os
import requests
import pandas as pd
from datetime import datetime
from config import Config

# 將專案根目錄添加到 sys.path 中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def fetch_foreign_investment_trust_proprietary_trading_data(start_date, end_date, token):
    url = 'https://api.finmindtrade.com/api/v4/data'
    params = {
        'dataset': 'TaiwanStockTotalInstitutionalInvestors',  # 使用正確的數據集名稱
        'start_date': start_date,
        'end_date': end_date,
        'token': token
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data['msg'] == 'success':
        if len(data['data']):
            return pd.DataFrame(data['data'])
        else:
            return pd.DataFrame()
    else:
        print(f"Error fetching data from {start_date} to {end_date}: {data['msg']}")
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
    
    print(f"Fetching data from {start_date_str} to {end_date_str}")
    data = fetch_foreign_investment_trust_proprietary_trading_data(start_date_str, end_date_str, token)
        
    if not data.empty:
        filename = os.path.join('data', "foreign_investment_trust_proprietary_trading_data.csv")
        save_to_csv(data, filename)

if __name__ == "__main__":
    start_date = sys.argv[1]
    end_date = sys.argv[2]
    main(start_date, end_date)