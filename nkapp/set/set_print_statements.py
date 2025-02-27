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
st             = Tl.statements_table

class SETPR:
    """ Print Tests for Statements """
    @staticmethod
    def set_print_statement1():
        """ Print Tests for Statements """
        PAGE_SIZE = 50
        PAGE_NUMBER = 1
        with Session() as db_session:
            try:
                # 銘柄コードを指定する
                code_input = input("表示したい銘柄コードを入力してください: ")
                # 指定された銘柄コードでデータを取得し、companynameとリンクする
                state = (
                    db_session.query(
                        st.c.LocalCode,
                        st.c.DisclosedDate,
                        st.c.DisclosureNumber,
                        st.c.DisclosureNumber,
                        st.c.TypeOfDocument,
                        st.c.TypeOfCurrentPeriod,
                        st.c.CurrentPeriodStartDate,
                        st.c.CurrentPeriodEndDate,
                        st.c.CurrentFiscalYearStartDate,
                        listedinfo.companyname
                    )
                    .join(listedinfo, st.c.LocalCode == listedinfo.code)
                    .filter(st.c.LocalCode == code_input)
                    .order_by(st.c.DisclosedDate.desc())
                )

                # 50件ずつページネーションで表示
                total_records = state.count()  # 総レコード数を取得
                print(f"総レコード数: {total_records}")

                while True:
                    # ページごとにデータを取得
                    statements_records = (
                        state.offset((PAGE_NUMBER - 1) * PAGE_SIZE).limit(PAGE_SIZE).all()
                    )

                    # データがなければ終了
                    if not statements_records:
                        print("これ以上データはありません。")
                        break

                    # 取得したデータを表示
                    for state in statements_records:
                        print(
                            state.LocalCode,
                            state.companyname,
                            state.DisclosedDate,
                            state.DisclosureNumber,
                            state.DisclosureNumber,
                            state.TypeOfDocument,
                            state.TypeOfCurrentPeriod,
                            state.CurrentPeriodStartDate,
                            state.CurrentPeriodEndDate,
                            state.CurrentFiscalYearStartDate,
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
                db_session.rollback()
                print(f"エラーが発生しました: {e}")
                return redirect(url_for("set.main"))
            finally:
                # セッションを閉じる
                db_session.close()

        return


    @staticmethod
    def set_print_statement2():
        """ Print Tests for Statements """
        print("set_print_statement2")
        return


    @staticmethod
    def set_print_statement3():
        """ Print Tests for Statements """
        print("set_print_statement3")
        return


    @staticmethod
    def set_print_statement4():
        """ Print Tests for Statements """
        print("set_print_statement4")

        return


    @staticmethod
    def set_print_statement5():
        """ Print Tests for Statements """
        print("set_print_statement5")

        return





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
