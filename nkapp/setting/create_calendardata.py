from sqlalchemy import select, func
from sqlalchemy.orm import sessionmaker
from models import TradingCalendar, Tl, engine  # `Tl`は`daily_all_table`を含むモデル

# セッションを作成
Session = sessionmaker(bind=engine)
session = Session()

def populate_trading_calendar():
    try:
        # `Tl.daily_all_table`から日付を取得し、重複を排除
        dates = session.query(Tl.daily_all_table.c.date).distinct().order_by(Tl.daily_all_table.c.date).all()
        date_list = [date[0] for date in dates]  # 日付をリストに変換
        print(f"date_list: {date_list}")

        # 既存のデータを確認し、追加する必要がある日付だけを抽出
        existing_dates = session.query(Tl.t_calendar.c.tradingdate).distinct().all()
        existing_dates_set = {date[0] for date in existing_dates}
        new_dates = [date for date in date_list if date not in existing_dates_set]
        print(f"new_dates: {new_dates}")

        # `trading_calendar`にデータを挿入
        for trading_date in new_dates:
            calendar_entry = TradingCalendar(
                tradingdate=trading_date  # trade_date_noはシーケンスに任せる
            )
            session.add(calendar_entry)

        session.commit()
        print(f"{len(new_dates)}件の日付がtrading_calendarに追加されました。")

    except Exception as e:
        session.rollback()
        print(f"エラーが発生しました: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    populate_trading_calendar()
