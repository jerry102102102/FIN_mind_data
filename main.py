from config import Config

def main():
    api_token = Config.FINMIND_API_TOKEN
    db_host = Config.DB_HOST
    db_port = Config.DB_PORT
    db_user = Config.DB_USER
    db_password = Config.DB_PASSWORD
    db_name = Config.DB_NAME

    # 使用這些配置參數來初始化 API 或資料庫連接
    print(f"Connecting to database {db_name} at {db_host}:{db_port} with user {db_user}")

    # 其他程式邏輯
    # ...

if __name__ == "__main__":
    main()
