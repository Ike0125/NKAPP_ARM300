"""  nkapp.api.kabudball.py  """
import time
from datetime import datetime, timedelta
from time import sleep
import requests
from flask import flash, request, session
from flask import redirect, url_for
from sqlalchemy import select
from sqlalchemy import func, text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from nkapp.config import Mainparams
from nkapp.models import ListedInfo, DailyQuotesAll, DailyQuotes
from nkapp.models import TradingCalendar, Tl, engine
from nkapp.api.config import Config
from nkapp.api.api_main import AP
from nkapp.set.mockjq_main import MK


class JQDB3:
    """ Updating All Stock Data """

    @staticmethod
    def retrieve_kabudball_request(mode=1):
        """
        全銘柄の株価データを取得し、ページング管理を含めて保存する。
        """
        # トークン取得
        config_data = AP.load_config()
        id_token = config_data.get("ID_TOKEN")
        headers = {"Authorization": f"Bearer {id_token}"}

        start_time = time.time()
        print(f"Starting data retrieval process...:{start_time}")
        with Session(engine) as session:
            # 全銘柄リスト取得
            listed_info_stmt = select(ListedInfo.code)
            all_codes = session.execute(listed_info_stmt).scalars().all()
            print(f"Fetched {len(all_codes)} codes.")
            for code in all_codes:
                # データ取得
                start_time2 = time.time()
                response = JQDB3.fetch_batch_data([code], headers, mode, max_retries=1, retry_delay=3)
                if response is None:
                    return redirect(url_for("set.main"))  # 処理停止し掲示板に戻る
                # データ保存
                JQDB3.save_to_database(session, response, mode=9)
                elapsed_time2 = time.time() - start_time2
                print(f"Data retrieval and storage : {code} in {elapsed_time2:.2f} seconds.")
                # APIのリクエスト制限を考慮して少し待機
                sleep(0.1)  # 必要に応じて調整
        elapsed_time = time.time() - start_time
        print(f"Data retrieval and storage completed successfully in {elapsed_time:.2f} seconds.")


    @staticmethod
    def fetch_batch_data(kabu_code, headers, mode, max_retries=2, retry_delay=3):
        """
        指定された銘柄コードリストに基づいてデータを取得。
        """
        base_url = Config.JQ_Daily_URL
        params = {"code": ",".join(kabu_code)}
        retries = 0
        # print(f"mode2:{mode}")
        while retries <= max_retries:
            try:
                all_data = []  # 全データを格納するリスト
                while True:
                    # print(f"params:{params}")
                    if mode == 9:    # mock test
                        # APIリクエスト(モックテスト)
                        r_get = MK.mock_jquants_api(
                            base_url, headers=headers, params=params, timeout=10,
                        )
                        print(f"r_get:{r_get.json()}")
                    elif mode == 1:
                        # APIリクエスト
                        r_get = requests.get(base_url, headers=headers, params=params, timeout=10)
                        # print(f"Request URL: {r_get.url}")
                    else:
                        print("Modeが設定されていません")
                        raise Exception

                    if r_get.status_code == 200:
                        response_data = r_get.json()
                        all_data.extend(response_data.get("daily_quotes", []))  # データを追加
                        # pagination_keyが含まれる場合、次のリクエストを実行
                        pagination_data = response_data.get("pagination_key",[])
                        print(f"pagination_data:{pagination_data}")
                        if "pagination_key" in response_data:
                            params["pagination_key"] = response_data["pagination_key"]
                        sleep(0.1)  # 必要に応じて調整
                        return all_data  # JSON全体を返す（ページングキーも含む）
                    elif r_get.status_code in [400, 401, 403, 413]:
                        flash(f"{r_get.status_code}: {r_get.json().get('message', 'Unknown Error')}", "error")
                        return None  # 処理を終了させるため None を返す
                    elif r_get.status_code >= 500:
                        print(f"Server Error {r_get.status_code}: Retrying...")
                        raise requests.exceptions.RequestException(f"Server Error {r_get.status_code}")

            except requests.exceptions.RequestException as e:
                retries += 1
                print(f"Retry {retries}/{max_retries} for batch due to error: {e}")
                if retries > max_retries:
                    print(f"Exceeded maximum retries ({max_retries}). Redirecting to error page.")
                    flash(f"Server error after {retries} tries: {e}", "error")
                    return None
                time.sleep(retry_delay)
                continue  # 自動的に try ブロックに戻る

            except Exception as e:  # 不明なエラーを包括的に処理
                flash(f"Unknown error occurred: {str(e)}", "error")
                return


    @staticmethod
    def save_to_database(session, response, mode=9):
        """
        APIで取得した新規データをデータベースに保存。
        """
        try:
            if mode == 1:    # mock test
                for item in response:
                    new_quote = DailyQuotesAll(
                        date=datetime.strptime(item["Date"], "%Y-%m-%d").date(),
                        code=item["Code"],
                        open=item["Open"],
                        high=item["High"],
                        low=item["Low"],
                        close=item["Close"],
                        upperlimit=item["UpperLimit"],
                        lowerlimit=item["LowerLimit"],
                        volume=item["Volume"],
                        turnovervalue=item["TurnoverValue"],
                        adjustmentfactor=item["AdjustmentFactor"],
                        adjustmentopen=item["AdjustmentOpen"],
                        adjustmenthigh=item["AdjustmentHigh"],
                        adjustmentlow=item["AdjustmentLow"],
                        adjustmentclose=item["AdjustmentClose"],
                        adjustmentvolume=item["AdjustmentVolume"],
                    )
                    session.add(new_quote)
            elif mode == 9:    # mock test
                for item in response:
                    new_quote = DailyQuotes(
                        date=datetime.strptime(item["Date"], "%Y-%m-%d").date(),
                        code=item["Code"],
                        open=item["Open"],
                        high=item["High"],
                        low=item["Low"],
                        close=item["Close"],
                        upperlimit=item["UpperLimit"],
                        lowerlimit=item["LowerLimit"],
                        volume=item["Volume"],
                        turnovervalue=item["TurnoverValue"],
                        adjustmentfactor=item["AdjustmentFactor"],
                        adjustmentopen=item["AdjustmentOpen"],
                        adjustmenthigh=item["AdjustmentHigh"],
                        adjustmentlow=item["AdjustmentLow"],
                        adjustmentclose=item["AdjustmentClose"],
                        adjustmentvolume=item["AdjustmentVolume"],
                    )
                    session.add(new_quote)
            else:
                print("Modeが設定されていません")
                raise ValueError("mode isn't set.")
            session.commit()  # 全データを一括でコミット
        except ValueError as e:
            session.rollback()
            flash(f"{str(e)}","error")


    @staticmethod
    def retrieve_kabudball_request_update(mode=1):
        """
        全銘柄の株価データを取得し、ページング管理を含めて保存する。
        """
        # トークン取得
        config_data = AP.load_config()
        id_token = config_data.get("ID_TOKEN")
        headers = {"Authorization": f"Bearer {id_token}"}

        start_time = time.time()
        print(f"Starting data retrieval process...:{start_time}")
        with Session(engine) as session:
            # 全銘柄リスト取得
            listed_info_stmt = select(ListedInfo.code)
            all_codes = session.execute(listed_info_stmt).scalars().all()
            print(f"Fetched {len(all_codes)} codes.")
            for code in all_codes:
                # データ取得
                start_time2 = time.time()
                response = JQDB3.fetch_batch_data([code], headers, mode, max_retries=1, retry_delay=3)
                if response is None:
                    return redirect(url_for("set.main"))  # 処理停止し掲示板に戻る
                # データ保存
                JQDB3.save_to_database_update(session, response, mode=1)
                elapsed_time2 = time.time() - start_time2
                print(f"Data retrieval and storage : {code} in {elapsed_time2:.2f} seconds.")
                sleep(0.1)  # 必要に応じて調整
        elapsed_time = time.time() - start_time
        print(f"Data retrieval and storage completed successfully in {elapsed_time:.2f} seconds.")


    @staticmethod
    def save_to_database_update(session, response, mode=1):
        """
        APIで取得したデータをデータベースに保存。
        """
        try:
            if mode == 1:    # mock test
                for item in response:
                    # 新規データのみ保存
                    existing_data_stmt = select(DailyQuotesAll).where(
                        (DailyQuotesAll.code == item["Code"]) &
                        (DailyQuotesAll.date == datetime.strptime(item["Date"], "%Y-%m-%d").date())
                    )

                    if not session.execute(existing_data_stmt).first():
                        new_quote = DailyQuotesAll(
                            date=datetime.strptime(item["Date"], "%Y-%m-%d").date(),
                            code=item["Code"],
                            open=item["Open"],
                            high=item["High"],
                            low=item["Low"],
                            close=item["Close"],
                            upperlimit=item["UpperLimit"],
                            lowerlimit=item["LowerLimit"],
                            volume=item["Volume"],
                            turnovervalue=item["TurnoverValue"],
                            adjustmentfactor=item["AdjustmentFactor"],
                            adjustmentopen=item["AdjustmentOpen"],
                            adjustmenthigh=item["AdjustmentHigh"],
                            adjustmentlow=item["AdjustmentLow"],
                            adjustmentclose=item["AdjustmentClose"],
                            adjustmentvolume=item["AdjustmentVolume"],
                        )
                        session.add(new_quote)
                    else:
                        break
            elif mode == 9:    # mock test
                for item in response:
                    # 新規データのみ保存
                    date_obj = datetime.strptime(item["Date"], "%Y-%m-%d").date()
                    # 新しいデータのみ追加
                    existing_data_stmt = select(DailyQuotes).where(
                        (DailyQuotes.code == item["Code"]) &
                        (DailyQuotes.date == date_obj)
                    )
                    existing_data = session.execute(existing_data_stmt).first()
                    if not existing_data:
                        new_quote = DailyQuotes(
                            date=datetime.strptime(item["Date"], "%Y-%m-%d").date(),
                            code=item["Code"],
                            open=item["Open"],
                            high=item["High"],
                            low=item["Low"],
                            close=item["Close"],
                            upperlimit=item["UpperLimit"],
                            lowerlimit=item["LowerLimit"],
                            volume=item["Volume"],
                            turnovervalue=item["TurnoverValue"],
                            adjustmentfactor=item["AdjustmentFactor"],
                            adjustmentopen=item["AdjustmentOpen"],
                            adjustmenthigh=item["AdjustmentHigh"],
                            adjustmentlow=item["AdjustmentLow"],
                            adjustmentclose=item["AdjustmentClose"],
                            adjustmentvolume=item["AdjustmentVolume"],
                        )
                        session.add(new_quote)
                    else:
                        break
            else:
                print("Modeが設定されていません")
                raise ValueError("mode isn't set.")
            session.commit()  # 全データを一括でコミット
        except ValueError as e:
            flash(f"{str(e)}","error")

    @staticmethod
    def update_tradingcalendar():
        """Updating Trading Calendar"""
        # Tl.daily_table から最新の日付を取得
        with Session(engine) as session:
            try:
                daily      = Tl.daily         # DailyQuotesAll
                #daily = Tl.dailyquotes  # DailyQuotes
                t_calendar = Tl.t_calendar  # TradingCalendar

                max_trade_date_no = session.query(func.max(TradingCalendar.trade_date_no)).scalar()
                seq_current_value = session.execute(text("SELECT last_value FROM trade_date_no_seq")).scalar()

                if max_trade_date_no is None:
                    max_trade_date_no = 0  # テーブルが空の場合
                else:
                # シーケンスとtrade_date_noの整合性の確認
                    if seq_current_value != max_trade_date_no:
                        flash(
                            f"Sequence value ({seq_current_value}) and max trade_date_no ({max_trade_date_no}) are inconsistent.",
                            "error",
                        )
                        #raise ValueError("Sequence and trade_date_no are not synchronized. Please fix the sequence.")
                        raise ValueError(
                                f"Sequence value ({seq_current_value}) and max trade_date_no ({max_trade_date_no}) are inconsistent. "
                                f"Please manually reset the sequence to {max_trade_date_no + 1}."
                        )
                # daily の最新日付を取得
                d_date = session.query(func.max(daily.date)).scalar()
                t_date = session.query(func.max(t_calendar.c.tradingdate)).scalar()

                if not d_date:
                    flash("No dates found in DailyQuotesAll. Aborting update.", "error")
                    return

                if t_date is None:
                    # TradingCalendar が空の場合、初期データを挿入
                    flash("TradingCalendar is empty. Rebuilding with initial data.", "message")
                    JQDB3._initialize_trading_calendar(session, daily, d_date)
                    return

                # 更新が必要か確認
                if t_date >= d_date:  # t_date >= d_date は更新不要
                    flash("Trading calendar is already up-to-date.", "message")
                    return

                # TradingCalendar に追加する営業日を取得
                trading_dates = (
                    session.query(daily.date)
                    .filter(daily.date > t_date, daily.date <= d_date)
                    .distinct()
                    .order_by(daily.date)
                    .all()
                )

                # TradingCalendar にデータを追加
                for date in trading_dates:
                    new_entry = TradingCalendar(tradingdate=date[0])
                    session.add(new_entry)

                # コミットして変更を保存
                session.commit()
                flash("Trading calendar has been updated to match daily_table.", "success")

            except SQLAlchemyError as e:
                # ロールバックしてエラーを処理
                session.rollback()
                flash(f"Database Connecting Error: {e}", "error")
            except ValueError as e:
                print(f"Error: {e}")
                flash(f"{e}:", "error")
            finally:
                # セッションを閉じる
                session.close()

        return


    @staticmethod
    def _initialize_trading_calendar(session, daily, d_date):
        """Initialize Trading Calendar with data from DailyQuotesAll."""
        try:
            # `DailyQuotesAll` の営業日を取得
            trading_dates = (
                session.query(daily.date)
                .filter(daily.date <= d_date)
                .distinct()  # ユニークな日付のみ
                .order_by(daily.date)
                .all()
            )

            if not trading_dates:
                raise ValueError("No dates found in DailyQuotesAll for initialization.")

            # 初期データを TradingCalendar に挿入
            for date in trading_dates:
                new_entry = TradingCalendar(tradingdate=date[0])  # trade_date_no は自動生成
                session.add(new_entry)

            # データベースに変更を保存
            session.commit()
            flash("TradingCalendar has been initialized.", "success")

        except SQLAlchemyError as e:
            session.rollback()
            raise RuntimeError(f"Error initializing TradingCalendar: {e}") from e


    @staticmethod
    def kabudball_update_date(mode):
        """
        指定した日付の株価データを取得し、ページング管理を含めて保存する。
        APIで取得したデータをデータベースに保存。
        mode 1 : DailyQuotesAll, data check あり
        mode 2 : DailyQuotesAll, data check なし
        mode 8 : DailyQuotes   , data check なし
        mode 9 : DailyQuotes   , data check あり
        """
        # トークン取得
        config_data = AP.load_config()
        id_token = config_data.get("ID_TOKEN")
        headers = {"Authorization": f"Bearer {id_token}"}
        base_url = Config.JQ_Daily_URL
        main_params = Mainparams.get_main_params()
        current_day  = datetime.now().date()
        update_gap =83

        if request.method == "POST":
            date_start = request.form.get("date1","2024-01-01")
            date_end = request.form.get("date2","2024-01-01")

            try:
                date_start_obj = datetime.strptime(date_start, "%Y-%m-%d").date()
                date_end_obj   = datetime.strptime(date_end, "%Y-%m-%d").date()
                session["input_start_obj"] = date_start_obj
                session["input_end_obj"] = date_end_obj
                last_update     = main_params["last_update"]
                start_daily     = main_params["start_daily"]
                last_update_all = main_params["last_update_all"]
                start_daily_all = main_params["start_daily_all"]
                print(f"date_start_obj:{date_start_obj}")
                print(f"last_update:{last_update}")
                print(f"date_end_obj:{date_end_obj}")
                print(f"start_daily:{start_daily}")

                if start_daily is None:
                    last_update = current_day-timedelta(days=update_gap)
                    start_daily = last_update-timedelta(days=(2*365))
                else:
                    if mode in [8,9]:
                        if (date_start_obj <= last_update) and (date_end_obj >= start_daily):
                            flash(f"Input Date for mode 8or 9 between {date_start_obj} & {date_end_obj} is out of range.", "error" )
                            return redirect(url_for("api.api_main"))
                if start_daily_all is None:
                    last_update_all = current_day-timedelta(days=update_gap)
                    start_daily_all = last_update-timedelta(days=(2*365))
                else:
                    if mode in [1,2]:
                        if (date_start_obj <= last_update_all) and (date_end_obj >= start_daily_all):
                            flash(f"Input Date between {date_start_obj} & {date_end_obj} is out of range.", "error" )
                            return redirect(url_for("api.api_main"))
                print(f"date_start_obj:{date_start_obj}")
                print(f"last_update:{last_update}")
                print(f"date_end_obj:{date_end_obj}")
                print(f"start_daily:{start_daily}")

            except ValueError:
                flash("Invalid date format. Please use YYYY-MM-DD.", "error")
                return None
            date_obj = date_start_obj
            start_time = time.time()
            print(f"Starting data retrieval process...:{start_time}")

            while date_obj <= date_end_obj:
                date_obj_str = date_obj.strftime("%Y-%m-%d")
                params = {"date": date_obj_str}
                # params = {"code":"72030","date": date_obj_str}
                print(f"params:{params}")
                print(f"date_obj:{date_obj}")
                print(f"date_end_obj:{date_end_obj}")
                start_time2 = time.time()
                # データ取得
                response = JQDB3.fetch_data(base_url, headers, params, mode, max_retries=1, retry_delay=3)
                if response is None:
                    return redirect(url_for("api.api_main"))  # 処理停止し掲示板に戻る
                # データ保存
                # print(f"response:{response}")
                #JQDB3.save_to_db_update(response, mode)
                db_commit = JQDB3.save_to_db_update(response, mode)
                print(f"db_commit2:{db_commit}")

                if db_commit is False:
                    print(f"db_commit3:{db_commit}")
                    return redirect(url_for("api.api_main"))  # 処理停止し掲示板に戻る

                date_obj = date_obj + timedelta(days=1)
                elapsed_time2 = time.time() - start_time2
                print(f"Data retrieval and storage : {date_obj} in {elapsed_time2:.2f} seconds.")
                # APIのリクエスト制限を考慮して少し待機
                sleep(0.1)  # 必要に応じて調整
            elapsed_time = time.time() - start_time
            print(f"Data retrieval and storage completed successfully in {elapsed_time:.2f} seconds.")
            flash(f"Updated {date_start_obj} to {date_end_obj} in {elapsed_time:.2f} seconds.", "success")


    @staticmethod
    def fetch_data(base_url, headers, params, mode, max_retries=2, retry_delay=3):
        """
        指定された銘柄コードリストに基づいてデータを取得。
        APIで取得したデータをデータベースに保存。
        mode 1 : DailyQuotesAll, data check あり
        mode 2 : DailyQuotesAll, data check なし
        mode 8 : DailyQuotes   , data check なし
        mode 9 : DailyQuotes   , data check あり
        """
        retries = 0
        # print(f"mode2:{mode}")
        while retries <= max_retries:
            try:
                response_data = []  # 全データを格納するリスト
                while True:
                    # print(f"params:{params}")
                    if mode == 9:    # mock test
                        # APIリクエスト(モックテスト)
                        r_get = MK.mock_jquants_api(
                            base_url, headers=headers, params=params, timeout=10,
                        )
                        print(f"r_get:{r_get.json()}")
                    elif mode in [1,2,8]:
                        # APIリクエスト
                        # print(f"params: {params}")
                        r_get = requests.get(base_url, headers=headers, params=params, timeout=10)
                        response = r_get.json()
                        response_data += response.get("daily_quotes", [])
                        while "pagination_key" in response_data:
                            pagination_key = response_data["pagination_key"]
                            params["pagination_key"] = pagination_key
                            r_get = requests.get(base_url, headers=headers, params=params, timeout=10)
                            next_page_data = r_get.json()
                            response_data += next_page_data["daily_quotes",[]]
                            print(f"pagination_key{pagination_key}")
                    else:
                        print("Modeが設定されていません")
                        raise Exception

                    if r_get.status_code == 200:
                        print(f"status:{r_get.status_code}")
                        return response_data  # JSON全体を返す（ページングキーも含む）
                    elif r_get.status_code in [400, 401, 403, 413]:
                        flash(f"{r_get.status_code}: {r_get.json().get('message', 'Unknown Error')}", "error")
                        return None  # 処理を終了させるため None を返す
                    elif r_get.status_code >= 500:
                        print(f"Server Error {r_get.status_code}: Retrying...")
                        retries += 1
                        if retries > max_retries:
                            flash(f"Server error after {retries} retries: {r_get.status_code}", "error")
                            return None
                        time.sleep(retry_delay)
                        continue
            except Exception as e:  # 不明なエラーを包括的に処理
                flash(f"Unknown error occurred: {str(e)}", "error")
                return


    @staticmethod
    def save_to_db_update(response, mode=8):
        """
        APIで取得したデータをデータベースに保存。
        mode 1 : DailyQuotesAll, data check あり
        mode 2 : DailyQuotesAll, data check なし
        mode 8 : DailyQuotes   , data check なし
        mode 9 : DailyQuotes   , data check あり
        """
        db_commit = False
        with Session(engine) as db_session:
            try:
                if mode == 1:    # DailyQuotesAll, data check あり
                    for item in response:
                        # 新規データのみ保存
                        existing_data_stmt = select(DailyQuotesAll).where(
                            (DailyQuotesAll.code == item["Code"]) &
                            (DailyQuotesAll.date == datetime.strptime(item["Date"], "%Y-%m-%d").date())
                        )

                        if not db_session.execute(existing_data_stmt).first():
                            new_quote = DailyQuotesAll(
                                date=datetime.strptime(item["Date"], "%Y-%m-%d").date(),
                                code=item["Code"],
                                open=item["Open"],
                                high=item["High"],
                                low=item["Low"],
                                close=item["Close"],
                                upperlimit=item["UpperLimit"],
                                lowerlimit=item["LowerLimit"],
                                volume=item["Volume"],
                                turnovervalue=item["TurnoverValue"],
                                adjustmentfactor=item["AdjustmentFactor"],
                                adjustmentopen=item["AdjustmentOpen"],
                                adjustmenthigh=item["AdjustmentHigh"],
                                adjustmentlow=item["AdjustmentLow"],
                                adjustmentclose=item["AdjustmentClose"],
                                adjustmentvolume=item["AdjustmentVolume"],
                            )
                            db_session.add(new_quote)
                            db_session.commit()
                        else:
                            break
                elif mode == 2:       # DailyQuotesAll, data check なし
                    for item in response:
                        # 新規データのみ保存

                        new_quote = DailyQuotesAll(
                            date=datetime.strptime(item["Date"], "%Y-%m-%d").date(),
                            code=item["Code"],
                            open=item["Open"],
                            high=item["High"],
                            low=item["Low"],
                            close=item["Close"],
                            upperlimit=item["UpperLimit"],
                            lowerlimit=item["LowerLimit"],
                            volume=item["Volume"],
                            turnovervalue=item["TurnoverValue"],
                            adjustmentfactor=item["AdjustmentFactor"],
                            adjustmentopen=item["AdjustmentOpen"],
                            adjustmenthigh=item["AdjustmentHigh"],
                            adjustmentlow=item["AdjustmentLow"],
                            adjustmentclose=item["AdjustmentClose"],
                            adjustmentvolume=item["AdjustmentVolume"],
                        )
                        db_session.add(new_quote)
                    db_session.commit()

                elif mode == 8:    # DailyQuotes   , data check なし
                    # print(f"response:{response}")
                    for item in response:
                        new_quote = DailyQuotes(
                            date=datetime.strptime(item["Date"], "%Y-%m-%d").date(),
                            code=item["Code"],
                            open=item["Open"],
                            high=item["High"],
                            low=item["Low"],
                            close=item["Close"],
                            upperlimit=item["UpperLimit"],
                            lowerlimit=item["LowerLimit"],
                            volume=item["Volume"],
                            turnovervalue=item["TurnoverValue"],
                            adjustmentfactor=item["AdjustmentFactor"],
                            adjustmentopen=item["AdjustmentOpen"],
                            adjustmenthigh=item["AdjustmentHigh"],
                            adjustmentlow=item["AdjustmentLow"],
                            adjustmentclose=item["AdjustmentClose"],
                            adjustmentvolume=item["AdjustmentVolume"],
                        )
                        db_session.add(new_quote)
                    db_session.commit()

                elif mode == 9:    # DailyQuotes   , data check あり

                    for item in response:
                        # 新規データのみ保存
                        date_obj = datetime.strptime(item["Date"], "%Y-%m-%d").date()
                        # 新しいデータのみ追加
                        existing_data_stmt = select(DailyQuotes).where(
                            (DailyQuotes.code == item["Code"]) &
                            (DailyQuotes.date == date_obj)
                        )
                        existing_data = db_session.execute(existing_data_stmt).first()
                        if not existing_data:
                            new_quote = DailyQuotes(
                                date=datetime.strptime(item["Date"], "%Y-%m-%d").date(),
                                code=item["Code"],
                                open=item["Open"],
                                high=item["High"],
                                low=item["Low"],
                                close=item["Close"],
                                upperlimit=item["UpperLimit"],
                                lowerlimit=item["LowerLimit"],
                                volume=item["Volume"],
                                turnovervalue=item["TurnoverValue"],
                                adjustmentfactor=item["AdjustmentFactor"],
                                adjustmentopen=item["AdjustmentOpen"],
                                adjustmenthigh=item["AdjustmentHigh"],
                                adjustmentlow=item["AdjustmentLow"],
                                adjustmentclose=item["AdjustmentClose"],
                                adjustmentvolume=item["AdjustmentVolume"],
                            )
                            db_session.add(new_quote)
                        db_session.commit()
                else:
                    print("Modeが設定されていません")
                    raise ValueError("mode isn't set.")
                db_commit = True
                return db_commit

            except ValueError as e:
                flash(f"{str(e)}","error")
