import subprocess
import json
from config import Config

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
            print(f"Reading progress from progress.txt...")
            progress = json.load(file)
            print(f"Last executed script: {progress}")
    except FileNotFoundError:
        progress = {"last_script": 0, "last_stock": 0, "last_date": "2024-07-01"}
        save_progress(progress["last_script"], progress["last_stock"], progress["last_date"])
        print("No progress found, starting from the beginning.")
    return progress

def save_progress(script_idx, stock_idx, last_date):
    progress = {"last_script": script_idx, "last_stock": stock_idx, "last_date": last_date}
    with open('progress.txt', 'w') as file:
        json.dump(progress, file)

def main():
    api_token = Config.FINMIND_API_TOKEN

    stock_list = ["2330", "2317", "2454", "2382", "2881", "2308", "2412", "2882", "2891", "3711",
                  "2303", "6505", "2886", "1216", "2884", "2885", "6669", "3008", "1303", "2892",
                  "5880", "2880", "1402", "2344", "2891", "2301", "2353", "1101", "2603", "2890",
                  "2454", "3037", "2408", "2409", "3045", "2458", "2376", "3006", "3037", "2383",
                  "3711", "2357", "2498", "2618", "1605", "2324", "6278", "5483", "4938", "2449"]
    
    scripts = [
        {'name': 'crawl/foreign_investment_trust_proprietary_trading_data.py', 'params': None},
        {'name': 'crawl/institutional_investors_buy_sell.py', 'params': stock_list},
        {'name': 'crawl/margin_purchase_short_sale.py', 'params': stock_list},
        {'name': 'crawl/TaiwanStockGovernmentBankBuySell.py', 'params': None},
        {'name': 'crawl/TaiwanStockWarrantTradingDailyReport.py', 'params': stock_list},
        {'name': 'crawl/total_margin_purchase_short_sale.py', 'params': None}
    ]

    start_date = "2024-07-01"
    end_date = "2024-07-05"
    progress = read_progress()
    
    for script_idx in range(progress['last_script'], len(scripts)):
        script = scripts[script_idx]
        script_name = script['name']
        script_params = script['params']
        special_start = None
        if progress['last_script'] == 3 or progress['last_script'] == 4:
            special_start = progress['last_date']
        
        if script_params:
            last_time_execute_stock = progress['last_stock']
            if special_start:
                print(f"Running script: {script_name} from {special_start} for stock list starting from index {last_time_execute_stock}")
                if not run_script(script_name, [json.dumps(script_params), special_start, end_date, str(last_time_execute_stock)]):
                    save_progress(script_idx, last_time_execute_stock, special_start)
                    return
            else:
                print(f"Running script: {script_name} for stock list starting from index {last_time_execute_stock}")
                if not run_script(script_name, [json.dumps(script_params), start_date, end_date, str(last_time_execute_stock)]):
                    save_progress(script_idx, last_time_execute_stock, start_date)
                    return
        else:
            if special_start:
                print(f"Running script: {script_name} from {special_start}")
                if not run_script(script_name, [special_start, end_date]):
                    save_progress(script_idx, last_time_execute_stock, special_start)
                    return
            print(f"Running script: {script_name}")
            if not run_script(script_name, [start_date, end_date]):
                save_progress(script_idx, None, None)
                return

if __name__ == "__main__":
    main()
