""" テストプログラム """
from sqlalchemy import Table, MetaData, create_engine
from sqlalchemy.orm import sessionmaker


#  ARM100システムの中の.data/stock.dbのデータを全削除する


# データベース接続を設定
engine = create_engine("sqlite:///data/stocks.db")
Session = sessionmaker(bind=engine)

# セッションを作成
session = Session()

# Coreでは必要
metadata = MetaData()
dailyquoteall = Table("daily_quotes_all", metadata, autoload_with=engine)

try:
    # addressテーブルの全レコードを削除
    daily_quote_delete = session.query(dailyquoteall).delete()

    # 変更をコミット
    session.commit()
    print("全てのアドレスデータが削除されました。")

except Exception as e:
    # エラーが発生した場合はロールバック
    session.rollback()
    print(f"エラーが発生しました: {e}")

finally:
    # セッションを閉じる
    session.close()
