"""  nkapp.api.api_main.py  """
import json
import os
import time
# from time import sleep
from datetime import datetime, timedelta
# from time import time
import requests
from flask import redirect, url_for, flash
from flask import session,request
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session
from sqlalchemy import text
from nkapp.models import ListedInfo, engine
from nkapp.models import JqTradingCalendar
from nkapp.api.config import Config
from nkapp.config import Mainparams

class AP:
    """API control for NKAPP"""

    @staticmethod
    def config():
        """Initial Params for Analysisparames"""
        config_data = AP.load_config()  # config.jsonを読み込む
        id_token_timestamp = config_data.get("ID_TOKEN_TIMESTAMP","")
        refresh_token_timestamp = config_data.get("REFRESH_TOKEN_TIMESTAMP","")
        announcement_timestamp = config_data.get("ANNOUNCEMENT_TIMESTAMP","")
        # 更新日のギャップ：
        update_gap =84
        # 現在の時間を取得
        current_time = datetime.now()
        current_day  = datetime.now().date()
        mp = Mainparams.get_main_params()
        data1 = mp.get("last_update_all") + timedelta(days=1)

        last_update_statements = mp.get("last_update_statements")
        last_update_statements = datetime.strptime(last_update_statements, "%Y-%m-%d").date()
        st_data1 = last_update_statements + timedelta(days=1)
        st_data1 = st_data1.strftime("%Y-%m-%d")
        next_update_info = current_day - timedelta(days=update_gap)
        jqcd1 = mp.get("last_update_jqcalendar") + timedelta(days=1)
        jqcd2 = current_day - timedelta(days=update_gap)
        jqcd1_data = jqcd1.strftime("%Y-%m-%d")
        jqcd2_data = jqcd2.strftime("%Y-%m-%d")
        date1_value = session.get("date_start", data1)
        date2_value = session.get("date_end", jqcd2_data)
        jqcd1_value = session.get("jqcd_start",jqcd1_data)
        jqcd2_value = session.get("jqcd_end", jqcd2_data)
        st_date1_value = session.get("st_date_start",st_data1)
        st_date2_value   = session.get("st_date_end",jqcd2_data)

        # id_token_timestamp の有効期限チェック
        if id_token_timestamp:
            try:
                id_token_time = datetime.fromisoformat(id_token_timestamp)
                if current_time - id_token_time > timedelta(hours=20):
                    flash("ID_TOKEN_TIMESTAMP is needed to update.", "error")
            except ValueError:
                flash("Invalid format for ID_TOKEN_TIMESTAMP.", "error")

        # refresh_token_timestamp の有効期限チェック
        if refresh_token_timestamp:
            try:
                refresh_token_time = datetime.fromisoformat(refresh_token_timestamp)
                if current_time - refresh_token_time > timedelta(days=6):
                    flash("REFRESH_TOKEN_TIMESTAMP is needed to update.", "error")
            except ValueError:
                flash("Invalid format for REFRESH_TOKEN_TIMESTAMP.", "error")

        return {
            "id_token_timestamp": id_token_timestamp,
            "refresh_token_timestamp": refresh_token_timestamp,
            "head_title": "API Managements for NKAPP",
            "header_title": "APIs",
            "endpoint": "api.api_main",
            "return_url": "api.api_main",
            "return_name": "API Managements",
            "home_url": "nkapp.index",
            "next_update_info"       : next_update_info,
            "date1_value"            : date1_value,
            "date2_value"            : date2_value,
            "jqcd1_value"            : jqcd1_value,
            "jqcd2_value"            : jqcd2_value,
            "st_date1_value"         : st_date1_value,
            "st_date2_value"         : st_date2_value,
            "announcement_timestamp" : announcement_timestamp
        }


    @staticmethod
    def load_config():  # config.jsonの読み込みと保存を行う関数
        """config.jsonファイルから設定を読み込む"""
        config_file = os.path.join(os.path.dirname(__file__), "api_config.json")
        if os.path.exists(config_file):
            with open(config_file, "r", encoding="utf-8") as file:
                return json.load(file)
        else:
            return {}


    @staticmethod
    def save_config(data):
        """設定をconfig.jsonファイルに保存する"""
        config_file = os.path.join(os.path.dirname(__file__), "api_config.json")
        with open(config_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)


class APJQ:
    """Token control for J-Quonts"""
    @staticmethod
    def get_token_request():
        """
        POSTリクエストからリフレッシュトークンを使用してIDトークンを取得し、ヘッダーを返す。

        :param request: Flaskのリクエストオブジェクト
        :return: 認証ヘッダーまたはリダイレクトレスポンス
        """
        if request.method == "POST":
            try:
                # JQ APIにリクエストを送信してIDトークンを取得
                config_data = AP.load_config()  # config.jsonを読み込む
                refresh_token = config_data.get("REFRESH_TOKEN")
                res = requests.post(
                    f"{Config.JQ_Token_URL}?refreshtoken={refresh_token}",
                    timeout=10,
                )
                print(f"リクエストが送信されました。ステータスコード: {res.status_code}")
                res.raise_for_status()  # ステータスコードのチェックを追加
                id_token = res.json().get("idToken")

                if id_token:
                    # IDトークンと取得日時をconfig.jsonに保存
                    config_data = AP.load_config()
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    # print(f"timestamp: {timestamp}")

                    config_data["ID_TOKEN"] = id_token
                    config_data["ID_TOKEN_TIMESTAMP"] = timestamp
                    AP.save_config(config_data)
                    status_code = res.status_code
                    status_message = res.json().get("message")
                    flash(f"Status:{status_code}-{status_message}","success")
                else:
                    print("IDトークンがレスポンスに含まれていません")  # デバッグ用のprint文
                    raise ValueError("IDトークンがレスポンスに含まれていません")

                return redirect(url_for("api.api_main"))

            except requests.exceptions.RequestException as e:
                status_code = res.status_code if res else "Unknown"
                status_message = res.json().get("message", str(e)) if res else str(e)
                flash(f"Status:{status_code}-{status_message}","error")
            except ValueError as e:
                status_code = res.status_code if res else "Unknown"
                status_message = res.json().get("message", str(e)) if res else str(e)
                flash(f"Status:{status_code}-{status_message}","error")
            except Exception as e:
                status_code = "Unknown"
                status_message = str(e)
                flash(f"Status:{status_code}-{status_message}","error")
            return redirect(url_for("api.api_main"))


    @staticmethod
    def save_refresh_token():
        """
        手動で新しいリフレッシュトークンを取得し、設定に保存する。

        :return: リダイレクトレスポンス
        """
        new_refresh_token = request.form.get("refresh_token")
        if new_refresh_token:
            config_data = AP.load_config()
            config_data["REFRESH_TOKEN"] = new_refresh_token
            config_data["REFRESH_TOKEN_TIMESTAMP"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            AP.save_config(config_data)
            flash("Updated Refresh-Token.", "success")
        else:
            flash("Invalid Refresh-Token.", "error")
        return redirect(url_for("api.api_main"))


    @staticmethod
    def listedinfo_request():
        """
        JQ APIから上場銘柄一覧データを取得し、データベースに保存または更新する。

        :param request: Flaskのリクエストオブジェクト
        :return: テンプレートのレンダリングまたはリダイレクトレスポンス
        """
        start_time = time.time()  # 全体の処理時間計測開始
        print("Starting data retrieval process...")
        # トークン取得
        config_data = AP.load_config()  # config.jsonを読み込む
        id_token = config_data.get("ID_TOKEN")
        headers = {"Authorization": f"Bearer {id_token}"}

        # ユーザーが入力した日付を取得
        date = request.form.get("date", "2024-05-26")  # デフォルト値

        # APIリクエスト
        params = {"date": date}
        response = requests.get(
            Config.JQ_Listed_URL, headers=headers, params=params, timeout=10
        )
        try:
            if response.status_code == 200:
                data = response.json()
                with Session(engine) as session:  # SQLAlchemy 2.x 構文を使用
                    # 制約が存在するかチェックしてから追加
                    constraint_check_query = text(
                        """
                        SELECT COUNT(*)
                        FROM information_schema.table_constraints
                        WHERE table_name = 'listed_info'
                        AND constraint_name = 'unique_code';
                        """
                    )
                    result = session.execute(constraint_check_query).scalar()
                    if result == 0:  # 制約が存在しない場合のみ追加
                        session.execute(
                            text(
                                """
                                ALTER TABLE listed_info
                                ADD CONSTRAINT unique_code UNIQUE (code);
                                """
                            )
                        )
                        session.commit()
                    for item in data["info"]:
                        date_obj = datetime.strptime(item["Date"], "%Y-%m-%d").date()

                        # INSERTまたはUPDATE
                        stmt = insert(ListedInfo).values(
                            date=date_obj,
                            code=item["Code"],
                            companyname=item["CompanyName"],
                            companynameenglish=item["CompanyNameEnglish"],
                            sector17code=item["Sector17Code"],
                            sector17codename=item["Sector17CodeName"],
                            sector33code=item["Sector33Code"],
                            sector33codename=item["Sector33CodeName"],
                            scalecategory=item["ScaleCategory"],
                            marketcode=item["MarketCode"],
                            marketcodename=item["MarketCodeName"],
                        )
                        stmt = stmt.on_conflict_do_update(
                            index_elements=["code"],  # 一意性制約に基づいて更新
                            set_=dict(
                                date=stmt.excluded.date,
                                companyname=stmt.excluded.companyname,
                                companynameenglish=stmt.excluded.companynameenglish,
                                sector17code=stmt.excluded.sector17code,
                                sector17codename=stmt.excluded.sector17codename,
                                sector33code=stmt.excluded.sector33code,
                                sector33codename=stmt.excluded.sector33codename,
                                scalecategory=stmt.excluded.scalecategory,
                                marketcode=stmt.excluded.marketcode,
                                marketcodename=stmt.excluded.marketcodename,
                            ),
                        )
                        session.execute(stmt)
                    session.commit()
                flash("データの取得と保存に成功しました", "success")
            else:
                flash(f"データの取得に失敗しました: {response.status_code}", "error")
        except Exception as e:
            flash(f"エラーが発生しました: {str(e)}", "error")
            raise
        print(f"Total process time: {time.time() - start_time:.2f} seconds")
        return redirect(url_for("api.api_main"))


    @staticmethod
    def jqcalendar_update():
        """
        東証およびOSEにおける営業日、休業日、ならびにOSEにおける祝日取引の有無の情報
        """
        # トークン取得
        config_data = AP.load_config()
        id_token = config_data.get("ID_TOKEN")
        headers = {"Authorization": f"Bearer {id_token}"}
        base_url = Config.JQ_Calendar_URL
        max_retries = 2
        retry_delay = 3

        if request.method == "POST":
            # フォームデータの取得とバリデーション
            jqcd_start = request.form.get("jqcd1", "2024-01-01")
            jqcd_end = request.form.get("jqcd2", "2024-01-01")
            #session["jqcd_start"] = jqcd_start
            #session["jqcd_end"] = jqcd_end
            try:
                jqcd_start = datetime.strptime(jqcd_start, "%Y-%m-%d").date()
                jqcd_end = datetime.strptime(jqcd_end, "%Y-%m-%d").date()
            except ValueError:
                flash("Invalid date format. Please use YYYY-MM-DD.", "error")
                return None
            params = {"from": jqcd_start.strftime("%Y-%m-%d"), "to": jqcd_end.strftime("%Y-%m-%d")}

            retries = 0
            while retries <= max_retries:
                try:
                    r_get = requests.get(base_url, headers=headers, params=params, timeout=10)
                    if r_get.status_code == 200:
                        try:
                            response_data = r_get.json()
                            print("Response Data:", response_data)
                        except ValueError:
                            flash("Invalid response format from API.", "error")
                            print("Raw Response Text:", r_get.text)
                            return None

                        with Session(engine) as db_session:
                            trading_calendar = response_data["trading_calendar"]
                            for item in trading_calendar:
                                date = datetime.strptime(item["Date"], "%Y-%m-%d").date()
                                existing = db_session.query(JqTradingCalendar).filter_by(date=date).first()
                                if not existing:
                                    new_data = JqTradingCalendar(
                                        date=date,
                                        holidaydivision=item["HolidayDivision"],
                                    )
                                    db_session.add(new_data)
                            db_session.commit()
                        flash("Data retrieval and storage completed successfully.", "success")
                        return

                    elif r_get.status_code in [400, 401, 403, 413]:
                        flash(f"{r_get.status_code}: {r_get.json().get('message', 'Unknown Error')}", "error")
                        return None
                    elif r_get.status_code >= 500:
                        raise requests.exceptions.RequestException(f"Server Error {r_get.status_code}")
                except requests.exceptions.RequestException as e:
                    retries += 1
                    if retries > max_retries:
                        flash(f"Server error after {retries} tries: {e}", "error")
                        return None
                    time.sleep(retry_delay)
                    continue


