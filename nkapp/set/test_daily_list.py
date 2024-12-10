"""  test_daily_print_list.py  """
from sqlalchemy import Table, MetaData, create_engine
from sqlalchemy.orm import sessionmaker
# from configdb import Test

# DBとの接続
DATABASE1 = "sqlite:///data/stocks.db"  # J-Quontesから取得したDB
DATABASE2 = "sqlite:///data/stocks2.db"  # nkapp/rpt用のDB
DATABASE3 = "sqlite:///data/stocks3.db"  # Test Program用のDB


engine = create_engine(DATABASE1)
Session = sessionmaker(bind=engine)

# セッションを作成
session = Session()

# Coreでは必要
metadata = MetaData()
dailyquotes = Table("daily_quotes", metadata, autoload_with=engine)
listedinfo = Table("listed_info", metadata, autoload_with=engine)

# 銘柄コードを指定する
code_input = input("表示したい銘柄コードを入力してください: ")
# 銘柄コードが４桁の場合０を最後に追加することcode+0
# ページネーション用設定
PAGE_SIZE = 50
PAGE_NUMBER = 1

try:
    # 指定された銘柄コードでデータを取得し、companynameとリンクする
    query = (
        session.query(
            dailyquotes.c.id,
            dailyquotes.c.date,
            dailyquotes.c.code,
            #dailyquotes.c.open,
            #dailyquotes.c.high,
            #dailyquotes.c.low,
            #dailyquotes.c.close,
            #dailyquotes.c.upperlimit,
            #dailyquotes.c.lowerlimit,
            #dailyquotes.c.volume,
            #dailyquotes.c.turnovervalue,
            #dailyquotes.c.adjustmentfactor,
            #dailyquotes.c.adjustmentopen,
            #dailyquotes.c.adjustmenthigh,
            #dailyquotes.c.adjustmentlow,
            #dailyquotes.c.adjustmentclose,
            #dailyquotes.c.adjustmentvolume,
            listedinfo.c.companyname,
        )
        .join(listedinfo, dailyquotes.c.code == listedinfo.c.code)
        .filter(dailyquotes.c.code == code_input)
        .order_by(dailyquotes.c.date.asc()) # ここでdateの古い順に並び替え
    )

    # 50件ずつページネーションで表示
    total_records = query.count()  # 総レコード数を取得
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

        # 取得したデータを表示
        for quote in daily_quote_records:
            print(
                quote.id,
                quote.date,
                quote.code,
                quote.companyname,  # companynameを表示
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
