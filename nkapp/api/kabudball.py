"""  nkapp.api.kabudball.py  """
from datetime import datetime
from time import sleep, time
import requests
from flask import flash
from sqlalchemy import select
from sqlalchemy import func, text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from nkapp.models import ListedInfo, DailyQuotesAll, DailyQuotes
from nkapp.models import TradingCalendar, Tl, engine
from nkapp.api.config import Config
from nkapp.api.api_main import AP
from nkapp.set.mockjq_main import MK


class JQDB:
    """Updating Trading Calendar"""

    @staticmethod
    def retrieve_kabudball_request(mode=1):
        """
        JQ APIから全銘柄の株価データを取得し、データベースに新しいデータを追加する。
        """
        # 全体の処理時間計測開始
        start_time = time()
        print("Starting data retrieval process...")

        # トークン取得
        step_start = time()
        config_data = AP.load_config()  # config.jsonを読み込む
        id_token = config_data.get("ID_TOKEN")
        headers = {"Authorization": f"Bearer {id_token}"}
        print(f"Token retrieval time: {time() - step_start:.2f} seconds")

        with Session(engine) as session:
            # 全銘柄リストを取得する
            step_start = time()
            listed_info_stmt = select(ListedInfo.code)
            all_codes_response = session.execute(listed_info_stmt).scalars().all()
            all_codes = list(all_codes_response)
            print(f"New codes processing time: {time() - step_start:.2f} seconds")
            # APIで新しい銘柄リストを取得
            step_start = time()
            new_codes = []  # 実際には適切なAPI呼び出しまたはデータ取得を行う
            all_codes.extend(new_codes)
            # print(f"new codes:{new_codes}")
            print(f"New codes processing time: {time() - step_start:.2f} seconds")
            # 各銘柄ごとにデータ取得と保存

            # **変更箇所：全データを一時リストに格納**
            new_quotes = []  # 全ての新規データを一時保存するリスト

            for code in all_codes:
                step_start = time()
                params = {"code": code}
                try:
                    if mode == 9:    # mock test
                        # APIリクエスト(モックテスト)
                        response = MK.mock_jquants_api(
                            Config.JQ_Daily_URL, headers=headers, params=params, timeout=10
                        )
                    elif mode == 1:
                        # APIリクエスト
                        response = requests.get(
                            Config.JQ_Daily_URL, headers=headers, params=params, timeout=10
                        )
                    else:
                        print("Modeが設定されていません")
                        raise ValueError("mode isn't set.")
                    response.raise_for_status()  # ステータスコードがエラーなら例外を発生させる
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching data for code {code}: {e}")
                    flash(f"Error fetching data for code {code}: {e}", "error")
                    #return redirect(url_for("api.api_main"))
                    # continue  # エラーが発生した場合は次の銘柄へ
                    return

                if response.status_code == 200:
                    data = response.json()
                    print(f"API request for {code} time: {time() - step_start:.2f} seconds")
                    if mode == 1:
                        for item in data["daily_quotes"]:
                            date_obj = datetime.strptime(item["Date"], "%Y-%m-%d").date()
                            # 新しいデータのみ追加
                            existing_data_stmt = select(DailyQuotesAll).where(
                                (DailyQuotesAll.code == item["Code"]) &
                                (DailyQuotesAll.date == date_obj)
                            )
                            existing_data = session.execute(existing_data_stmt).first()

                            if not existing_data:
                                new_quotes.append(DailyQuotesAll(
                                    date=date_obj,
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
                                    adjustmentvolume=item["AdjustmentVolume"],)
                                )
                                #session.add(new_quote)
                        #session.commit()  # データを確定
                    elif mode == 9:
                        for item in data["daily_quotes"]:
                            date_obj = datetime.strptime(item["Date"], "%Y-%m-%d").date()
                            # 新しいデータのみ追加
                            existing_data_stmt = select(DailyQuotes).where(
                                (DailyQuotes.code == item["Code"]) &
                                (DailyQuotes.date == date_obj)
                            )
                            existing_data = session.execute(existing_data_stmt).first()

                            if not existing_data:
                                new_quotes.append(DailyQuotes(
                                    date=date_obj,
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
                                    adjustmentvolume=item["AdjustmentVolume"],)
                                )
                                # session.add(new_quote)
                        # session.commit()  # データを確定
                else:
                    flash(f"{code}のデータ取得に失敗しました: {response.status_code}", "error")

                # APIのリクエスト制限を考慮して少し待機
                sleep(0.2)  # 必要に応じて調整
                print(f"Processing time for code {code}: {time() - step_start:.2f} seconds")

            # **変更箇所：一括でデータベースに保存**
            try:
                session.add_all(new_quotes)
                session.commit()
                print("All data committed successfully.")
            except SQLAlchemyError as e:
                print(f"Error committing data: {e}")
                flash("データベースへの保存中にエラーが発生しました", "error")
                session.rollback()
        print(f"Total process time: {time() - start_time:.2f} seconds")
        flash("すべての銘柄のデータ取得と保存に成功しました", "success")
        # return redirect(url_for("api.api_main"))
        return


    @staticmethod
    def update_tradingcalendar():
        """Updating Trading Calendar"""
        # Tl.daily_table から最新の日付を取得
        with Session(engine) as db_session:
            try:
                daily      = Tl.daily         # DailyQuotesAll
                t_calendar = Tl.t_calendar  # TradingCalendar

                max_trade_date_no = db_session.query(func.max(TradingCalendar.trade_date_no)).scalar()
                seq_current_value = db_session.execute(text("SELECT last_value FROM trade_date_no_seq")).scalar()

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
                d_date = db_session.query(func.max(daily.date)).scalar()
                t_date = db_session.query(func.max(t_calendar.c.tradingdate)).scalar()

                if not d_date:
                    flash("No dates found in DailyQuotesAll. Aborting update.", "error")
                    return

                if t_date is None:
                    # TradingCalendar が空の場合、初期データを挿入
                    flash("TradingCalendar is empty. Rebuilding with initial data.", "message")
                    JQDB._initialize_trading_calendar(db_session, daily, d_date)
                    return

                # 更新が必要か確認
                if t_date >= d_date:  # t_date >= d_date は更新不要
                    flash("Trading calendar is already up-to-date.", "message")
                    return

                # TradingCalendar に追加する営業日を取得
                trading_dates = (
                    db_session.query(daily.date)
                    .filter(daily.date > t_date, daily.date <= d_date)
                    .distinct()
                    .order_by(daily.date)
                    .all()
                )

                # TradingCalendar にデータを追加
                for date in trading_dates:
                    new_entry = TradingCalendar(tradingdate=date[0])
                    db_session.add(new_entry)

                # コミットして変更を保存
                db_session.commit()
                flash("Trading calendar has been updated to match daily_table.", "success")

            except SQLAlchemyError as e:
                # ロールバックしてエラーを処理
                db_session.rollback()
                flash(f"Database Connecting Error: {e}", "error")
            except ValueError as e:
                print(f"Error: {e}")
                flash(f"{e}:", "error")
            finally:
                # セッションを閉じる
                db_session.close()

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

