"""  nkapp.api.api_main.py  """
import json
import os
from datetime import datetime
import requests
from flask import redirect, url_for, flash, request, render_template
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session
from sqlalchemy import text  # 必要な場合にスキーマ変更用
from nkapp.models import ListedInfo, engine
from nkapp.api.config import Config

# from sqlalchemy import func
# from nkapp.models import Session, Tl

class AP:
    """API control for NKAPP"""

    @staticmethod
    def config():
        """Initial Params for Analysisparames"""
        return {
            "head_title": "API Managements for NKAPP",
            "header_title": "APIs",
            "endpoint": "api.api_main",
            "return_url": "api.api_main",
            "return_name": "API Managements",
            "home_url": "nkapp.index",
        }


    @staticmethod
    def load_config():  # config.jsonの読み込みと保存を行う関数
        """config.jsonファイルから設定を読み込む"""
        config_file = os.path.join(os.path.dirname(__file__), "config.json")
        if os.path.exists(config_file):
            with open(config_file, "r", encoding="utf-8") as file:
                return json.load(file)
        else:
            return {}


    @staticmethod
    def save_config(data):
        """設定をconfig.jsonファイルに保存する"""
        config_file = os.path.join(os.path.dirname(__file__), "config.json")
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
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    config_data = AP.load_config()
                    config_data["ID_TOKEN"] = id_token
                    config_data["ID_TOKEN_TIMESTAMP"] = timestamp
                    AP.save_config(config_data)
                else:
                    print("IDトークンがレスポンスに含まれていません")  # デバッグ用のprint文
                    raise ValueError("IDトークンがレスポンスに含まれていません")

                status_code = res.status_code
                status_message = res.json().get("message", "Success")

                return redirect(url_for("api.api_main"))

            except requests.exceptions.RequestException as e:
                status_code = res.status_code if res else "Unknown"
                status_message = res.json().get("message", str(e)) if res else str(e)
            except ValueError as e:
                status_code = res.status_code if res else "Unknown"
                status_message = res.json().get("message", str(e)) if res else str(e)
            except Exception as e:
                status_code = "Unknown"
                status_message = str(e)
            return render_template(
                "api_main.html",
                status_code=status_code,
                status_message=status_message,
            )


    @staticmethod
    def save_refresh_token():
        """
        POSTリクエストから新しいリフレッシュトークンを取得し、設定に保存する。

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
            flash("リフレッシュトークンが正常に更新されました。", "success")
        else:
            flash("リフレッシュトークンの入力が無効です。", "error")
        return redirect(url_for("api.api_main"))


    @staticmethod
    def listedinfo_request():
        """
        JQ APIから上場銘柄一覧データを取得し、データベースに保存または更新する。

        :param request: Flaskのリクエストオブジェクト
        :return: テンプレートのレンダリングまたはリダイレクトレスポンス
        """
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
        return redirect(url_for("api.api_main"))

