"""  api.config.py  """
import os

# SQL DBとの接続先
DATABASE1 = "sqlite:///data/stocks.db"  # J-Quontesから取得したDB
DATABASE2 = "sqlite:///data/stocks.db"  # NKsys用のDB
DATABASE3 = "sqlite:///data/stocks.db"  # Test Program用のDB


class Config:
    """J-QuontesのAPIとの接続先"""
    JQ_Token_URL = os.getenv(
        "JQ_token_URL", "https://api.jquants.com/v1/token/auth_refresh"
    )  # ID_Tookenとの接続先
    JQ_Daily_URL = os.getenv(
        "JQ_Daily_URL", "https://api.jquants.com/v1/prices/daily_quotes"
    )  # prices/daily との接続先
    JQ_Listed_URL = os.getenv(
        "JQ_Listed_URL", "https://api.jquants.com/v1/listed/info"
    )  # listed/info　との接続先
    JQ_Calendar_URL = os.getenv(
        "JQ_Calendar_URL", "https://api.jquants.com/v1/markets/trading_calendar"
    )  # markets/trading_calendar　との接続先
    JQ_Statements_URL = os.getenv(
        "JQ_Statements_URL", "https://api.jquants.com/v1/fins/statements"
    )  # fins/statements　との接続先
    JQ_Announcement_URL = os.getenv(
        "JQ_Announcement_URL", "https://api.jquants.com/v1/fins/announcement"
    )  # fins/annoucement　との接続先

    """SQL DBとの接続先"""
    SQL_DataBase1 = DATABASE1   # J-Quontesから取得したDB
    SQL_DataBase2 = DATABASE2   # NKsys用のDB
    SQL_DataBase3 = DATABASE3   # Test Program用のDB

    SECRET_KEY = os.getenv('SECRET_KEY', 'JqArmBond60key')  # My Secret key
