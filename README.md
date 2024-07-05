# Taiwan Stock Market Data Crawler

## Description
This repository contains Python scripts for crawling various datasets related to the Taiwan stock market using the FinMind API. The primary focus is on obtaining comprehensive data on stock transactions, institutional investors' trades, and margin trading.

## Datasets
The following datasets will be crawled and processed:

### 台股八大行庫買賣表資料: Major Taiwanese banks' trading data.
### 上市上櫃的分點資料: Data from brokerage firms on listed and OTC stocks.
### 上市上櫃的外資、投信、自營商買賣表: Trading data of foreign investors, investment trusts, and proprietary traders for listed and OTC stocks.
### 台股市場三大法人(外資、投信、自營商)買賣表: Comprehensive trading data of the three major institutional investors (foreign investors, investment trusts, and proprietary traders) in the Taiwanese stock market.
### 上市上櫃的股票代碼、融資(券)買進、賣出、現金(現券)償還、前日餘額、金額餘額、限額、資券互抵: Codes of listed and OTC stocks, details of margin trading, short selling, and related financial data.
### 台股的融資融券表: Margin trading and short selling data, including date, buy and sell volumes, and monetary amounts.
## Features
Automated Data Crawling: Scripts for automatically fetching data from the FinMind API.
Data Cleaning: Functions to clean and preprocess the raw data.
Data Storage: Methods to store the cleaned data in a structured format.
Data Analysis: Basic analytical tools for initial data examination and visualization.
## Requirements
Python 3.8+
FinMind SDK
Pandas
Requests
Matplotlib (for data visualization)
