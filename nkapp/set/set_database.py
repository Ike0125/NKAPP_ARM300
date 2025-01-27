"""  nkapp.set.database.py  """
from datetime import datetime
from flask import flash, redirect, url_for
from flask import request
from sqlalchemy import and_
from sqlalchemy import inspect,select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from nkapp.models import Tl, engine
from nkapp.config import SECPARAMS


class SETDB:
    """  System Setting for Database """

    @staticmethod
    def deletedata():
        """  Delete all data in the table of DailyQuotes """
        seckey       = ""       # securitey for database
        secret_daily = ""       # password data
        stmt         = None
        db_name      = ""
        asetckbox01  = False
        asetckbox02  = False
        asetckbox03  = False
        asetckbox04  = False
        asetckbox05  = False
        asetckbox06  = False
        asetckbox07  = False

        if request.method == "POST":
            asetckbox01 = 'asetckbox01' in request.form.getlist('ckbox')    # 1.DailyQuotes
            asetckbox02 = 'asetckbox02' in request.form.getlist('ckbox')    # 2.DailyQuotesAll
            asetckbox03 = 'asetckbox03' in request.form.getlist('ckbox')    # 3.ListedInfo
            asetckbox04 = 'asetckbox04' in request.form.getlist('ckbox')    # 4.Statements
            asetckbox05 = 'asetckbox05' in request.form.getlist('ckbox')    # 5.TradingCalendar
            asetckbox06 = 'asetckbox06' in request.form.getlist('ckbox')    # 6.JQCalendar
            asetckbox07 = 'asetckbox07' in request.form.getlist('ckbox')    # 7.Announcement
            secret_daily = request.form.get("secret_daily", "")
            seckey       = SECPARAMS.seckey_database
            if secret_daily != seckey:
                flash("Incorrect secret key", "error")
                print("Incorrect secret key:")

                return redirect(url_for("set.main"))

        # daily_quotesテーブルの全レコードを削除
        with Session(engine) as db_session:
            try:
                if asetckbox01:
                    stmt = Tl.daily_table.delete()
                    db_name = "DailyQuotes"
                elif asetckbox02:
                    stmt = Tl.daily_all_table.delete()
                    db_name = "DailyQuotesAll"
                elif asetckbox03:
                    stmt = Tl.info_table.delete()
                    db_name = "ListedInfo"
                elif asetckbox04:
                    stmt = Tl.statements_table.delete()
                    db_name = "Statements"
                elif asetckbox05:
                    stmt = Tl.t_calendar.delete()
                    db_name = "TradingCalendar"
                elif asetckbox06:
                    stmt = Tl.jq_calendar.delete()
                    db_name = "JQCalendar"
                elif asetckbox07:
                    stmt = Tl.announcement_table.delete()
                    db_name = "Announcement"
                else:
                    # エラーが発生した場合はロールバック
                    db_session.rollback()
                    flash("エラーが発生しました: ", "error")
                    print("エラーが発生しました: ")

                    return redirect(url_for("set.main"))

                # 変更をコミット
                db_session.execute(stmt)
                db_session.commit()
                flash(f"Deleted !! all data in {db_name}.", "success")
                print(f">>> Deleted all data in {db_name}.")

            except SQLAlchemyError as e:
                # エラーが発生した場合はロールバック
                db_session.rollback()
                flash(f"エラーが発生しました: {e}", "error")
                print(f"エラーが発生しました: {e}")

            finally:
                # セッションを閉じる
                db_session.close()
        return redirect(url_for("set.main"))


    @staticmethod
    def dailyall_deletedata():
        """  Delete all data in the table of DailyQuotes """
        setckbox01 = False
        setckbox02 = False
        setcode = ""
        setdate = "2024-01-01"
        secret_settable = ""
        seckey       = ""

        # 選択したレコードを削除
        with Session(engine) as session:
            try:
                if request.method == "POST":
                    setckbox01 = 'setckbox01' in request.form.getlist('ckbox')
                    setckbox02 = 'setckbox02' in request.form.getlist('ckbox')
                    setcode = request.form.get("code","")
                    setdate_str = request.form.get("date","2024-01-01")
                    setdate = datetime.strptime(setdate_str, "%Y-%m-%d").date()
                    secret_daily = request.form.get("secret_settable", "")
                    seckey       = SECPARAMS.seckey_database
                    print(f"setckbox01: {setckbox01}")
                    print(f"setckbox02: {setckbox02}")
                    print(f"setcode: {setcode}")
                    print(f"setdate: {setdate}")
                    print(f"secret_settable: {secret_settable}")
                    print(f"seckey: {seckey}")
                    if setckbox01:
                        set_table = Tl.daily_table
                    elif setckbox02:
                        set_table = "Test"
                        #set_table = Tl.daily_table
                        #set_table = Tl.dailyall_table
                    else:
                        flash("Not select checkbox", "error")
                        print("Not select checkbox")
                        return redirect(url_for("set.main"))
                    if secret_daily != seckey:
                        flash("Incorrect secret key", "error")
                        print("Incorrect secret key:")
                        return redirect(url_for("set.main"))
                    # クエリを定義
                    print(f"set_table: {set_table}")
                    base_query = (
                        select(
                            set_table.c.code,
                            set_table.c.date,
                        )
                        .where(and_(set_table.c.code == setcode, set_table.c.date == setdate))
                    )
                    # 結果を確認
                    result = session.execute(base_query).fetchall()
                    if not result:
                        flash("No Data Selected.", "error")
                        print("No Data Selected.")
                    else:
                        # データが存在する場合は削除を実行
                        stmt = set_table.delete().where(
                            and_(set_table.c.code == setcode, set_table.c.date == setdate)
                        )
                        session.execute(stmt)
                        # 変更をコミット
                        session.commit()
                        flash(f"Deleted !! selected data in {set_table}:", "success")
                        print(">>> Deleted all data in DailyQuotes:")
            except SQLAlchemyError as e:
                # エラーが発生した場合はロールバック
                session.rollback()
                flash(f"エラーが発生しました: {e}", "error")
                print(f"エラーが発生しました: {e}")

            finally:
                # セッションを閉じる
                session.close()
        return redirect(url_for("set.main"))


    @staticmethod
    def table_list():
        """  データベースに接続しのテーブル・カラム確認する """
        with Session() as session:
            try:
                # インスペクターの作成
                inspector = inspect(engine)
                # データベース名の取得
                database_name = 'postgresql:nkapp_db1'
                print(f"Database Name: {database_name}\n")
                # テーブル一覧の取得
                tables = inspector.get_table_names()
                print("Table List:")
                for table in tables:
                    print(f"- {table}")
                    # 各テーブルのカラム情報を表示
                    columns = inspector.get_columns(table)
                    print("  Column:")
                    for column in columns:
                        print(f"    - {column['name']} ({column['type']})")
                    print()

            except SQLAlchemyError as e:
                print(f"データベース接続エラー: {e}")
            finally:
                # セッションを閉じる
                session.close()

            return redirect(url_for("set.main"))

