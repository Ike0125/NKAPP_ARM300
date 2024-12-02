from sqlalchemy import Column, Integer, Date, Sequence, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()
metadata = MetaData()

# シーケンスを定義し、開始値を10000に設定
trade_date_no_seq = Sequence('trade_date_no_seq', start=10000)

class TradingCalendar(Base):
    """取引カレンダーテーブルの定義"""
    __tablename__ = "trading_calendar"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    tradingdate = Column(Date, nullable=False)
    trade_date_no = Column(Integer, trade_date_no_seq, server_default=trade_date_no_seq.next_value())