""" announcement.py """
import time
from datetime import datetime
from time import sleep
import requests
from flask import flash, request
from flask import redirect, url_for
from sqlalchemy import select
from sqlalchemy.orm import Session
from nkapp.models import Announcement
from nkapp.models import engine
from nkapp.api.config import Config
from nkapp.api.api_main import AP
from nkapp.set.mockjq_main import MK


class JQAN:
    """ Updating Announcement Information """
    @staticmethod
    def get_announcement(mode):
        """
        指定した日付の株価データを取得し、ページング管理を含めて保存する。
        APIで取得したデータをデータベースに保存。
        mode 1 : announcement, data check なし
        mode 9 : Mock Tests
        """
        # トークン取得
        config_data = AP.load_config()
        id_token = config_data.get("ID_TOKEN")
        headers = {"Authorization": f"Bearer {id_token}"}
        base_url = Config.JQ_Announcement_URL
        if request.method == "POST":
            start_time = time.time()
            print(f"Starting data retrieval process...:{start_time}")
            params ={}
            # データ取得
            response = JQAN.fetch_announcement(base_url, headers, params, mode, max_retries=1, retry_delay=3)
            if response is None:
                return redirect(url_for("api.api_main"))  # 処理停止し掲示板に戻る
            # データ保存
            db_commit = JQAN.save_to_db_announcement(response)

            if db_commit is False:
                return redirect(url_for("api.api_main"))  # 処理停止し掲示板に戻る

            sleep(0.1)  # 必要に応じて調整
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            config_data["ANNOUNCEMENT_TIMESTAMP"] = timestamp
            AP.save_config(config_data)
            elapsed_time = time.time() - start_time
            print(f"Data retrieval and storage completed successfully in {elapsed_time:.2f} seconds.")
            flash(f"Updated on {timestamp} in {elapsed_time:.2f} seconds.", "success")


    @staticmethod
    def fetch_announcement(base_url, headers, params, mode, max_retries=2, retry_delay=3):
        """
        指定された銘柄コードリストに基づいてデータを取得。
        APIで取得したデータをデータベースに保存。
        mode 1 : announcement, data check なし
        mode 9 : Mock Tests
        """
        retries = 0

        while retries <= max_retries:
            try:
                response_data = []  # 全データを格納するリスト
                while True:
                    if mode == 9:    # mock test
                        # APIリクエスト(モックテスト)
                        r_get = MK.mock_jquants_api(
                            base_url, headers=headers, params=params, timeout=10,
                        )
                        print(f"r_get:{r_get.json()}")

                    elif mode == 1:
                        # APIリクエスト
                        r_get = requests.get(base_url, headers=headers, params=params, timeout=10)
                        response = r_get.json()
                        response_data += response.get("announcement", [])
                        while "pagination_key" in response_data:
                            pagination_key = response_data["pagination_key"]
                            params["pagination_key"] = pagination_key
                            r_get = requests.get(base_url, headers=headers, params=params, timeout=10)
                            next_page_data = r_get.json()
                            response_data += next_page_data["announcement",[]]
                            print(f"pagination_key{pagination_key}")

                    else:
                        print("Modeが設定されていません")
                        raise Exception

                    if r_get.status_code == 200:
                        print(f"status:{r_get.status_code}")
                        # print(f"response_data: {response_data}")

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
                flash(f"Unknown error: {str(e)}", "error")
                return


    @staticmethod
    def save_to_db_announcement(response):
        """
        APIで取得したデータをデータベースに保存。
        """
        db_commit = False
        with Session(engine) as db_session:
            # print(f"response:{response}")
            try:
                for item in response:
                    existing_data_stmt = select(Announcement).where(
                        (Announcement.Date == item["Date"]) &
                        (Announcement.Code == item["Code"])
                    )
                    existing_data = db_session.execute(existing_data_stmt).first()
                    if not existing_data:
                        new_announcement = Announcement(
                                Date          = item["Date"],
                                Code          = item["Code"],
                                CompanyName   = item["CompanyName"],
                                FiscalYear    = item["FiscalYear"],
                                SectorName    = item["SectorName"],
                                FiscalQuarter = item["FiscalQuarter"],
                                Section       = item["Section"],
                        )
                        db_session.add(new_announcement)
                db_session.commit()
                db_commit = True
                return db_commit

            except ValueError as e:
                flash(f"{str(e)}","error")
