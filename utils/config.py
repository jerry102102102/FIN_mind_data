import os
from dotenv import load_dotenv

# 載入.env文件中的環境變量
load_dotenv()

class Config:
    # API Token
    FINMIND_API_TOKEN = os.getenv('FINMIND_API_TOKEN')

    # 資料庫連接資訊
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 5432))
    DB_USER = os.getenv('DB_USER', 'your_username')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'your_password')
    DB_NAME = os.getenv('DB_NAME', 'your_database')

    # 其他配置參數
    DATA_DIRECTORY = os.getenv('DATA_DIRECTORY', 'data')
