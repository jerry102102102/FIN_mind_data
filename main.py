import subprocess
import json
from config import Config
from datetime import datetime, timedelta

def run_script(script_name, params):
    try:
        result = subprocess.run(['python', script_name] + params, capture_output=True, text=True)
        print(result.stdout)
        if "Requests reach the upper limit" in result.stdout or "Requests reach the upper limit" in result.stderr:
            print(f"Limit reached in {script_name}. Stopping execution.")
            return False
        if result.stderr:
            print(f"Errors in {script_name}:\n", result.stderr)
    except Exception as e:
        print(f"Failed to run {script_name}: {e}")
    return True

def read_progress():
    try:
        with open('progress.txt', 'r') as file:
            progress = json.load(file)
    except FileNotFoundError:
        progress = {"last_script": 0, "last_stock": 0, "last_date": "2022-07-01"}
    return progress

def save_progress(script_idx, stock_idx, last_date):
    progress = {"last_script": script_idx, "last_stock": stock_idx, "last_date": last_date}
    with open('progress.txt', 'w') as file:
        json.dump(progress, file)

def main():
    api_token = Config.FINMIND_API_TOKEN
    db_host = Config.DB_HOST
    db_port = Config.DB_PORT
    db_user = Config.DB_USER
    db_password = Config.DB_PASSWORD
    db_name = Config.DB_NAME

    stock_list = ["2330", "2317", "2454", "2382", "2881", "2308", "2412", "2882", "2891", "3711",
                  "2303", "6505", "2886", "1216", "2884", "2885", "6669", "3008", "1303", "2892",
                  "5880", "2880", "1402", "2344", "2891", "2301", "2353", "1101", "2603", "2890",
                  "2454", "3037", "2408", "2409", "3045", "2458", "2376", "3006", "3037", "2383",
                  "3711", "2357", "2498", "2618", "1605", "2324", "6278", "5483", "4938", "2449"]
    
    scripts = [
        {'name': 'crawl/institutional_investors_buy_sell.py', 'params': stock_list},
        {'name': 'crawl/margin_purchase_short_sale.py', 'params': stock_list},
        {'name': 'crawl/foreign_investment_trust_proprietary_trading_data.py', 'params': None},
        {'name': 'crawl/TaiwanStockGovernmentBankBuySell.py', 'params': None},
        {'name': 'crawl/TaiwanStockWarrantTradingDailyReport.py', 'params': stock_list},
        {'name': 'crawl/total_margin_purchase_short_sale.py', 'params': None}
    ]

    start_date = "2022-07-01"
    end_date = "2024-07-01"

    progress = read_progress()
    current_date = datetime.strptime(progress["last_date"], '%Y-%m-%d')

    while current_date <= datetime.strptime(end_date, '%Y-%m-%d'):
        date_str = current_date.strftime('%Y-%m-%d')
        for script_idx in range(progress["last_script"], len(scripts)):
            script = scripts[script_idx]
            script_name = script['name']
            script_params = script['params']

            if script_params:
                for stock_idx in range(progress["last_stock"], len(script_params)):
                    stock = script_params[stock_idx]
                    print(f"Running script: {script_name} for stock: {stock} on date: {date_str}")
                    if not run_script(script_name, [json.dumps([stock]), date_str]):
                        save_progress(script_idx, stock_idx, date_str)
                        return
                    save_progress(script_idx, stock_idx + 1, date_str)
                progress["last_stock"] = 0  # 重置股票索引，进入下一个脚本
            else:
                print(f"Running script: {script_name} on date: {date_str}")
                if not run_script(script_name, [date_str]):
                    save_progress(script_idx, None, date_str)
                    return
                save_progress(script_idx, None, date_str)

            save_progress(script_idx + 1, 0, date_str)  # 更新到下一个脚本开始

        current_date += timedelta(days=1)

if __name__ == "__main__":
    main()
