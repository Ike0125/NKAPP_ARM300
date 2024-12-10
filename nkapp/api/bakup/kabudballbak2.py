""" kabudball.py J-QuantsとのAPIテストプログラム"""

from datetime import datetime
from time import sleep
from flask import flash, redirect, url_for
import requests
from sqlalchemy.orm import Session
from nkapp.models import ListedInfo, DailyQuotesAll, engine
from nkapp.api.config import Config
from nkapp.api.api_main import AP

@staticmethod
def retrieve_kabudball_request():
    """
    JQ APIから全銘柄の株価データを取得し、データベースに保存する。
    """
    # トークン取得
    config_data = AP.load_config()  # config.jsonを読み込む
    id_token = config_data.get("ID_TOKEN")
    headers = {"Authorization": f"Bearer {id_token}"}

    # 全銘柄リストを取得する（APIや事前に保存した銘柄リストなど）
    all_codes_response = session.query(ListedInfo.code).all()
    all_codes = [item[0] for item in all_codes_response]

    # 全銘柄のデータを取得
    for code in all_codes:
        params = {"code": code}
        try:
            response = requests.get(
                Config.JQ_Daily_URL, headers=headers, params=params, timeout=10
            )
            response.raise_for_status()  # ステータスコードがエラーなら例外を発生させる
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for code {code}: {e}")
            continue  # エラーが発生した場合は次の銘柄へ

        if response.status_code == 200:
            data = response.json()
            # データベースへの保存前に日付を変換
            for item in data["daily_quotes"]:
                date_obj = datetime.strptime(item["Date"], "%Y-%m-%d").date()
                new_quote = DailyQuotesAll(
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
                    adjustmentvolume=item["AdjustmentVolume"],
                )
                session.add(new_quote)
            session.commit()
        else:
            flash(f"{code}のデータ取得に失敗しました: {response.status_code}", "error")

        # APIのリクエスト制限を考慮して、少し待機する
        sleep(1)  # 必要に応じて調整

    flash("すべての銘柄のデータ取得と保存に成功しました", "success")
    return redirect(url_for("api.api_main"))
