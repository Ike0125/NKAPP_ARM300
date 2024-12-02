from sqlalchemy import text
from models import TradingCalendar, engine

# テーブルの削除と再作成
def recreate_trading_calendar():
    print("テーブル 'trading_calendar' を削除しています...")
    TradingCalendar.__table__.drop(engine, checkfirst=True)  # テーブル削除
    print("テーブル 'trading_calendar' を再作成しています...")
    TradingCalendar.__table__.create(engine)  # テーブル再作成
    print("テーブル 'trading_calendar' を再作成しました。")

# シーケンスの再作成
def reset_trade_date_no_sequence():
    print("シーケンス 'trade_date_no_seq' を初期化しています...")
    with engine.connect() as conn:
        # シーケンス削除（CASCADEを使用）
        conn.execute(text("DROP SEQUENCE IF EXISTS trade_date_no_seq CASCADE;"))
        # シーケンス作成
        conn.execute(text("CREATE SEQUENCE trade_date_no_seq START 10000;"))
    print("シーケンス 'trade_date_no_seq' を初期化しました。")

if __name__ == "__main__":
    recreate_trading_calendar()
    reset_trade_date_no_sequence()