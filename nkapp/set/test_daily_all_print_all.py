""" test_daily_all_print_all.py """
# pylint: disable=Unable to import
# pylint: disable=import-error
import sys
from sqlalchemy import Table, MetaData, create_engine
from sqlalchemy import func, select
from sqlalchemy.orm import sessionmaker
#from syspath import TSConfig
# from nkapp.api.config import Config

print(sys.path)
#print(TSConfig.Comment, TSConfig.SysPath)
#  【テストプログラム】test_daily_all_print_all.py
#  ARM100システムの中の.data/stock.dbのデータを全て表示する

DATABASE1 = "sqlite:///data/stocks.db"  # J-Quontesから取得したDB
DATABASE2 = "sqlite:///data/stocks2.db"  # nkapp/rpt用のDB
DATABASE3 = "sqlite:///data/stocks3.db"  # Test Program用のDB

# DBとの接続

engine = create_engine(DATABASE1)
Session = sessionmaker(bind=engine)

# セッションを作成
session = Session()

# Coreでは必要
metadata = MetaData()
quote = Table("daily_quotes_all", metadata, autoload_with=engine)

# 銘柄コードを指定する
code_input = input("表示したい銘柄コードを入力してください: ")
# 銘柄コードが４桁の場合０を最後に追加することcode+0

# ページネーション用設定
PAGE_SIZE = 30
PAGE_NUMBER = 1

try:
    query = (
        session.query(
            quote.c.id,
            quote.c.date,
            quote.c.code,
            #quote.c.open,
            #quote.c.high,
            #quote.c.low,
            #quote.c.close,
            #quote.c.upperlimit,
            #quote.c.lowerlimit,
            #quote.c.volume,
            #quote.c.turnovervalue,
            #quote.c.adjustmentfactor,
            #quote.c.adjustmentopen,
            #quote.c.adjustmenthigh,
            #quote.c.adjustmentlow,
            #quote.c.adjustmentclose,
            #quote.c.adjustmentvolume,
        )
        .filter(quote.c.code == code_input)
        .order_by(quote.c.date.asc()) # ここでdateの古い順に並び替え
    )

    # 50件ずつページネーションで表示
    count_query = select(func.count()).select_from(query.subquery())
    # base_queryをサブクエリとし、その結果の行数をカウント
    total_records = session.execute(count_query).scalar()

    # total_records = query.count()  # 総レコード数を取得
    print(f"総レコード数: {total_records}")

    while True:
        # ページごとにデータを取得
        daily_quote_records = (
            query.offset((PAGE_NUMBER - 1) * PAGE_SIZE).limit(PAGE_SIZE).all()
        )

        # データがなければ終了
        if not daily_quote_records:
            print("これ以上データはありません。")
            break

        for quote in daily_quote_records:
            print(
                quote.id,
                quote.date,
                quote.code,
                #quote.open,
                #quote.high,
                #quote.low,
                #quote.close,
                #quote.upperlimit,
                #quote.lowerlimit,
                #quote.volume,
                #quote.turnovervalue,
                #quote.adjustmentfactor,
                #quote.adjustmentopen,
                #quote.adjustmenthigh,
                #quote.adjustmentlow,
                #quote.adjustmentclose,
                #quote.adjustmentvolume,
            )
        # 次のページに進むか終了するかを確認
        next_page = input(
            f"次のページに進むには 'n' を入力してください (ページ {PAGE_NUMBER} / {total_records // PAGE_SIZE + 1}）: "
        )
        if next_page.lower() != "n":
            break
        PAGE_NUMBER += 1

except Exception as e:
    # エラーが発生した場合はロールバック
    session.rollback()
    print(f"エラーが発生しました: {e}")

finally:
    # セッションを閉じる
    session.close()
