""" models.py """
from sqlalchemy import create_engine, Column, Integer, Float, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from nkapp.api.config import Config

# データベースエンジンの作成
engine = create_engine(Config.SQL_DataBase1, echo=True)

# ベースクラスの作成
Base = declarative_base()


class ListedInfo(Base):
    """ 上場銘柄一覧テーブルの定義 """
    __tablename__ = 'listed_info'

    date = Column(Date, nullable=False)                      # 情報適用年月日
    code = Column(String, primary_key=True, nullable=False)  # 銘柄コード
    companyname = Column(String, nullable=True)         # 会社名
    companynameenglish = Column(String, nullable=True)  # 会社名（英語）
    sector17code = Column(String, nullable=True)        # 17業種コード
    sector17codename = Column(String, nullable=True)    # 17業種コード名
    sector33code = Column(String, nullable=True)        # 33業種コード
    sector33codename = Column(String, nullable=True)    # 33業種コード名
    scalecategory = Column(String, nullable=True)       # 規模コード
    marketcode = Column(String, nullable=True)          # 市場区分コード
    marketcodename = Column(String, nullable=True)      # 市場区分名
    # margincode = Column(String, nullable=True, default="3")
    # 賃借信用区分, 1:信用, 2:賃借, 3:その他
    # margincodename = Column(String, nullable=True)      # 賃借信用区分名


class DailyQuotes(Base):
    """ 株価4本値テーブルの定義（選択） """
    __tablename__ = 'daily_quotes'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date = Column(Date, nullable=False)     # 日付
    code = Column(String, nullable=False)   # 銘柄コード
    open = Column(Float, nullable=True, default=0.0)   # 始値（調整前）
    high = Column(Float, nullable=True, default=0.0)   # 高値（調整前）
    low = Column(Float, nullable=True, default=0.0)    # 安値（調整前）
    close = Column(Float, nullable=True, default=0.0)  # 終値（調整前）
    upperlimit = Column(String, nullable=True, default="0")  # ストップ高(1:高,0:高以外)
    lowerlimit = Column(String, nullable=True, default="0")  # ストップ安(1:安,0:安以外)
    volume = Column(Float, nullable=True, default=0.0)       # 取引高（調整前）
    turnovervalue = Column(Float, nullable=True, default=0.0)  # 取引代金
    adjustmentfactor = Column(Float, nullable=True, default=1.0)  # 調整係数
    adjustmentopen = Column(Float, nullable=True, default=0.0)    # 調整済み始値 　
    adjustmenthigh = Column(Float, nullable=True, default=0.0)    # 調整済み高値
    adjustmentlow = Column(Float, nullable=True, default=0.0)     # 調整済み安値
    adjustmentclose = Column(Float, nullable=True, default=0.0)   # 調整済み終値
    adjustmentvolume = Column(Float, nullable=True, default=0.0)  # 調整済み取引高


class DailyQuotesAll(Base):
    """ 株価4本値テーブルの定義（一括）"""
    __tablename__ = 'daily_quotes_all'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date = Column(Date, nullable=False)     # 日付
    code = Column(String, nullable=False)   # 銘柄コード
    open = Column(Float, nullable=True, default=0.0)   # 始値（調整前）
    high = Column(Float, nullable=True, default=0.0)   # 高値（調整前）
    low = Column(Float, nullable=True, default=0.0)    # 安値（調整前）
    close = Column(Float, nullable=True, default=0.0)  # 終値（調整前）
    upperlimit = Column(String, nullable=True, default="0")  # ストップ高(1:高,0:高以外)
    lowerlimit = Column(String, nullable=True, default="0")  # ストップ安(1:安,0:安以外)
    volume = Column(Float, nullable=True, default=0.0)       # 取引高（調整前）
    turnovervalue = Column(Float, nullable=True, default=0.0)  # 取引代金
    adjustmentfactor = Column(Float, nullable=True, default=1.0)  # 調整係数
    adjustmentopen = Column(Float, nullable=True, default=0.0)    # 調整済み始値 　
    adjustmenthigh = Column(Float, nullable=True, default=0.0)    # 調整済み高値
    adjustmentlow = Column(Float, nullable=True, default=0.0)     # 調整済み安値
    adjustmentclose = Column(Float, nullable=True, default=0.0)   # 調整済み終値
    adjustmentvolume = Column(Float, nullable=True, default=0.0)  # 調整済み取引高


Base.metadata.create_all(engine)        # テーブルの作成


Session = sessionmaker(bind=engine)     # セッションの作成
session = Session()
