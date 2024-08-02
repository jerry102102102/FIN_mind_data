# FINMind Data Crawler

This project is designed to use the FINMind API to fetch Taiwan stock market data and save it as CSV files. It includes multiple Python scripts, each responsible for different datasets.

## Installation

### Create Virtual Environment

```bash
python -m venv venv
```
### Install Dependencies
```bash
pip install -r requirements.txt
```
## Usage
### Run Main Script
To execute the main script, which will run all the data fetching scripts in sequence, use the following command:
```bash
python main.py
```
## Scripts
### foreign_investment_trust_proprietary_trading_data.py
    - Dataset: TaiwanStockTotalInstitutionalInvestors
    - CSV Output: foreign_investment_trust_proprietary_trading_data.csv
### institutional_investors_buy_sell.py
    - Dataset: TaiwanStockInstitutionalInvestorsBuySell
    - CSV Output: institutional_investors_buy_sell.csv
### margin_purchase_short_sale.py
    - Dataset: TaiwanStockMarginPurchaseShortSale
    - CSV Output: margin_purchase_short_sale.csv
### TaiwanStockGovernmentBankBuySell.py
    - Dataset: TaiwanStockGovernmentBankBuySell
    - CSV Output: TaiwanStockGovernmentBankBuySell.csv
### TaiwanStockWarrantTradingDailyReport.py
    - Dataset: TaiwanStockTradingDailyReport
    - CSV Output: TaiwanStockWarrantTradingDailyReport.csv
### total_margin_purchase_short_sale.py
    - Dataset: TaiwanStockTotalMarginPurchaseShortSale
    - CSV Output: total_margin_purchase_short_sale.csv
## Progress Tracking
The progress of the script execution is saved in progress.txt. If the limit is reached or an error occurs, the script will stop and save the current progress, which includes:
    - Last executed script
    - Last executed stock index
    - Last executed date (for specific scripts)