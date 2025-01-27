"""  test_daily_print_list.py  """
from flask import redirect, url_for
from flask import flash, request
from nkapp.models import Session
from nkapp.models import Tl

dailyquotes    = Tl.dailyquotes
dailyquotesall = Tl.daily
listedinfo     = Tl.company
calendar       = Tl.t_calendar
jqcalendar     = Tl.jq_calendar

class DBC:
    """  test_daily_print_list.py  """

    @staticmethod
    def calendar_printout():
        """  test_daily_print_list.py  """
        # ページネーション用設定
        PAGE_SIZE = 50
        PAGE_NUMBER = 1

        with Session() as session:
            try:
                # 指定された銘柄コードでデータを取得し、companynameとリンクする
                query = (
                    session.query(
                        calendar.c.id,
                        calendar.c.trade_date_no,
                        calendar.c.tradingdate,
                    )
                    .order_by(calendar.c.tradingdate.desc())
                )

                # 50件ずつページネーションで表示
                total_records = query.count()  # 総レコード数を取得
                print(f"総レコード数: {total_records}")

                while True:
                    # ページごとにデータを取得
                    calendar_records = (
                        query.offset((PAGE_NUMBER - 1) * PAGE_SIZE).limit(PAGE_SIZE).all()
                    )

                    # データがなければ終了
                    if not calendar_records:
                        print("これ以上データはありません。")
                        break

                    # 取得したデータを表示
                    for quote in calendar_records:
                        print(
                            #quote.id,
                            quote.trade_date_no,
                            quote.tradingdate,
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
                return redirect(url_for("set.main"))
            finally:
                # セッションを閉じる
                session.close()

            return redirect(url_for("set.main"))


    @staticmethod
    def jq_calendar_printout():
        """  test_daily_print_list.py  """
        # ページネーション用設定
        PAGE_SIZE = 50
        PAGE_NUMBER = 1

        with Session() as session:
            try:
                # 指定された銘柄コードでデータを取得し、companynameとリンクする
                query = (
                    session.query(
                        jqcalendar.c.id,
                        jqcalendar.c.date,
                        jqcalendar.c.holidaydivision,
                    )
                    .order_by(jqcalendar.c.id.desc())
                )

                # 50件ずつページネーションで表示
                total_records = query.count()  # 総レコード数を取得
                print(f"総レコード数: {total_records}")

                while True:
                    # ページごとにデータを取得
                    calendar_records = (
                        query.offset((PAGE_NUMBER - 1) * PAGE_SIZE).limit(PAGE_SIZE).all()
                    )

                    # データがなければ終了
                    if not calendar_records:
                        print("これ以上データはありません。")
                        break

                    # 取得したデータを表示
                    for quote in calendar_records:
                        print(
                            #quote.id,
                            quote.date,
                            quote.holidaydivision,
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
                return redirect(url_for("set.main"))
            finally:
                # セッションを閉じる
                session.close()

            return redirect(url_for("set.main"))


    @staticmethod
    def daily_printout():
        """ Ptint out for trading_calender """
        # データベース選択
        setckbox03 = False
        setckbox04 = False
        set_table = dailyquotes
        # ページネーション用設定
        PAGE_SIZE = 50
        PAGE_NUMBER = 1

        with Session() as session:
            try:
                if request.method == "POST":
                    setckbox03 = 'setckbox03' in request.form.getlist('ckbox')
                    setckbox04 = 'setckbox04' in request.form.getlist('ckbox')
                    if setckbox03:
                        set_table = dailyquotes
                    elif setckbox04:
                        set_table = dailyquotesall
                    else:
                        flash("Not select checkbox", "error")
                        print("Not select checkbox")
                        return redirect(url_for("set.main"))

                # 銘柄コードを指定する
                code_input = input("表示したい銘柄コードを入力してください: ")
                # 指定された銘柄コードでデータを取得し、companynameとリンクする
                query = (
                    session.query(
                        set_table.id,
                        set_table.date,
                        set_table.code,
                        set_table.open,
                        set_table.high,
                        set_table.low,
                        set_table.close,
                        set_table.upperlimit,
                        set_table.lowerlimit,
                        set_table.volume,
                        set_table.turnovervalue,
                        set_table.adjustmentfactor,
                        set_table.adjustmentopen,
                        set_table.adjustmenthigh,
                        set_table.adjustmentlow,
                        set_table.adjustmentclose,
                        set_table.adjustmentvolume,
                        listedinfo.companyname,
                    )
                    .join(listedinfo, set_table.code == listedinfo.code)
                    .filter(set_table.code == code_input)
                    .order_by(set_table.date.desc())
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
                            quote.open,
                            quote.high,
                            quote.low,
                            quote.close,
                            quote.upperlimit,
                            quote.lowerlimit,
                            quote.volume,
                            quote.turnovervalue,
                            quote.adjustmentfactor,
                            quote.adjustmentopen,
                            quote.adjustmenthigh,
                            quote.adjustmentlow,
                            quote.adjustmentclose,
                            quote.adjustmentvolume,
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
                return redirect(url_for("set.main"))
            finally:
                # セッションを閉じる
                session.close()

            return redirect(url_for("set.main"))
