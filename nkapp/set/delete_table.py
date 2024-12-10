from sqlalchemy import Table, MetaData
from models import engine

metadata = MetaData()
def delete_trading_calender():
    # 対象テーブルだけ削除
    trading_calender = Table("trading_calender", metadata, autoload_with=engine)
    trading_calender.drop(engine, checkfirst=True)  # テーブルが存在する場合のみ削除

    # 再作成
    # metadata.create_all(engine, tables=[trading_calendar])

if __name__ == "__main__":
    delete_trading_calender()
