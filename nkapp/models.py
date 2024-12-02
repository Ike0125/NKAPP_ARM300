""" models.py """
from sqlalchemy import Column, Float, Date, create_engine,Sequence
from sqlalchemy import Table, Index, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, aliased

# PostgreSQLの接続情報
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:karasuyama4176@localhost:5432/nkapp_db1'

# エンジンの作成
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)

Base = declarative_base()
metadata = MetaData()

def create_sql_table():
    """テーブルの作成"""
    with Session() as session:
        with session.begin():
            Base.metadata.create_all(engine)

class ListedInfo(Base):
    """上場銘柄一覧テーブルの定義"""

    __tablename__ = "listed_info"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date = Column(Date, nullable=False)
    code = Column(String, primary_key=True, nullable=False)
    companyname = Column(String, nullable=True)
    companynameenglish = Column(String, nullable=True)
    sector17code = Column(String, nullable=True)
    sector17codename = Column(String, nullable=True)
    sector33code = Column(String, nullable=True)
    sector33codename = Column(String, nullable=True)
    scalecategory = Column(String, nullable=True)
    marketcode = Column(String, nullable=True)
    marketcodename = Column(String, nullable=True)

    __table_args__ = (
        Index('idx_listed_info_code_marketcode', 'code', 'marketcode'),
        {'extend_existing': True}
    )


class DailyQuotes(Base):
    """株価4本値テーブルの定義（選択）"""

    __tablename__ = "daily_quotes"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date = Column(Date, nullable=False)
    code = Column(String, nullable=False)
    open = Column(Float, nullable=True, default=0.0)
    high = Column(Float, nullable=True, default=0.0)
    low = Column(Float, nullable=True, default=0.0)
    close = Column(Float, nullable=True, default=0.0)
    upperlimit = Column(String, nullable=True, default="0")
    lowerlimit = Column(String, nullable=True, default="0")
    volume = Column(Float, nullable=True, default=0.0)
    turnovervalue = Column(Float, nullable=True, default=0.0)
    adjustmentfactor = Column(Float, nullable=True, default=1.0)
    adjustmentopen = Column(Float, nullable=True, default=0.0)
    adjustmenthigh = Column(Float, nullable=True, default=0.0)
    adjustmentlow = Column(Float, nullable=True, default=0.0)
    adjustmentclose = Column(Float, nullable=True, default=0.0)
    adjustmentvolume = Column(Float, nullable=True, default=0.0)

class DailyQuotesAll(Base):
    """株価4本値テーブルの定義（一括）"""

    __tablename__ = "daily_quotes_all"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date = Column(Date, nullable=False)
    code = Column(String, nullable=False)
    open = Column(Float, nullable=True, default=0.0)
    high = Column(Float, nullable=True, default=0.0)
    low = Column(Float, nullable=True, default=0.0)
    close = Column(Float, nullable=True, default=0.0)
    upperlimit = Column(String, nullable=True, default="0")
    lowerlimit = Column(String, nullable=True, default="0")
    volume = Column(Float, nullable=True, default=0.0)
    turnovervalue = Column(Float, nullable=True, default=0.0)
    adjustmentfactor = Column(Float, nullable=True, default=1.0)
    adjustmentopen = Column(Float, nullable=True, default=0.0)
    adjustmenthigh = Column(Float, nullable=True, default=0.0)
    adjustmentlow = Column(Float, nullable=True, default=0.0)
    adjustmentclose = Column(Float, nullable=True, default=0.0)
    adjustmentvolume = Column(Float, nullable=True, default=0.0)

    __table_args__ = (
        Index('idx_daily_quotes_all_code_date', 'code', 'date'),
        {'extend_existing': True}
    )


# シーケンスを定義し、開始値を10000に設定
trade_date_no_seq = Sequence('trade_date_no_seq', start=10000)
class TradingCalendar(Base):
    """株価4本値テーブルの定義（一括）"""

    __tablename__ = "trading_calendar"

    id            = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    tradingdate   = Column(Date, nullable=False)
    trade_date_no = Column(Integer, trade_date_no_seq, server_default=trade_date_no_seq.next_value())

class Tl:
    """Table Lists"""

    info_table = Table("listed_info", metadata, autoload_with=engine)
    daily_table = Table("daily_quotes", metadata, autoload_with=engine)
    daily_all_table = Table("daily_quotes_all", metadata, autoload_with=engine)
    current_db = SQLALCHEMY_DATABASE_URI
    company = aliased(ListedInfo)
    daily = aliased(DailyQuotesAll)
    t_calendar = Table("trading_calendar", metadata, autoload_with=engine)
