import sys
import os
import requests
import pandas as pd
from datetime import datetime
from config import Config

# 將專案根目錄添加到 sys.path 中
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def fetch_institutional_investors_buy_sell(start_date, end_date, token, stock_id):
    url = 'https://api.finmindtrade.com/api/v4/data'
    params = {
        'dataset': 'TaiwanStockInstitutionalInvestorsBuySell',
        'data_id': stock_id,
        'start_date': start_date,
        'end_date': end_date,
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
        print(f"Error fetching data from {start_date} to {end_date}: {data['msg']}")
        return pd.DataFrame()

def save_to_csv(dataframe, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    if os.path.exists(filename):
        dataframe.to_csv(filename, mode='a', header=False, index=False)
    else:
        dataframe.to_csv(filename, index=False)
def save_progress(last_script, last_stock, last_date):
    progress = {"last_script": last_script, "last_stock": last_stock, "last_date": last_date}
    with open('progress.txt', 'w') as file:
        json.dump(progress, file)
def main(stock_list, start_date_str, end_date_str,last_time_execute_stock):
    token = Config.FINMIND_API_TOKEN
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    
    for idx in range(last_time_execute_stock, len(stock_list)):
        stock_id = stock_list[idx]
        print(f"Fetching data for stock: {stock_id}")
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
        print(f"Fetching data from {start_date_str} to {end_date_str}")
        data = fetch_institutional_investors_buy_sell(start_date_str, end_date_str, token, stock_id)
        if data is None:
            save_progress(1, idx, start_date_str)  # 記錄進度，停止執行
            return
        if not data.empty:
            data['stock_id'] = stock_id  # 添加股票代碼作為額外欄位
            filename = os.path.join('data', "institutional_investors_buy_sell.csv")
            save_to_csv(data, filename)

if __name__ == "__main__":
    import json
    stock_list = json.loads(sys.argv[1])
    start_date = sys.argv[2]
    end_date = sys.argv[3]
    last_time_execute_stock = int(sys.argv[4])
    main(stock_list, start_date, end_date, last_time_execute_stock)
