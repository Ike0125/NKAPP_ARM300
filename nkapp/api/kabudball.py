from datetime import datetime
from time import sleep, time
from flask import flash, redirect, url_for
import requests
from sqlalchemy.orm import Session
#from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from nkapp.models import ListedInfo, DailyQuotesAll, engine
from nkapp.api.config import Config
from nkapp.api.api_main import AP


@staticmethod
def retrieve_kabudball_request():
    """
    JQ APIから全銘柄の株価データを取得し、データベースに新しいデータを追加する。
    """
    start_time = time()  # 全体の処理時間計測開始
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
        # APIで新規銘柄リストを取得（仮定として別APIまたはデータで取得）
        step_start = time()
        new_codes = []  # 実際には適切なAPI呼び出しまたはデータ取得を行う
        all_codes.extend(new_codes)
        print(f"New codes processing time: {time() - step_start:.2f} seconds")
        # 各銘柄ごとにデータ取得と保存
        for code in all_codes:
            step_start = time()
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
                print(f"API request for {code} time: {time() - step_start:.2f} seconds")
                for item in data["daily_quotes"]:
                    date_obj = datetime.strptime(item["Date"], "%Y-%m-%d").date()
                    # 新しいデータのみ追加
                    existing_data_stmt = select(DailyQuotesAll).where(
                        (DailyQuotesAll.code == item["Code"]) &
                        (DailyQuotesAll.date == date_obj)
                    )
                    existing_data = session.execute(existing_data_stmt).first()

                    if not existing_data:
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
                session.commit()  # データを確定
            else:
                flash(f"{code}のデータ取得に失敗しました: {response.status_code}", "error")

            # APIのリクエスト制限を考慮して少し待機
            sleep(1)  # 必要に応じて調整
            print(f"Processing time for code {code}: {time() - step_start:.2f} seconds")

    print(f"Total process time: {time() - start_time:.2f} seconds")
    flash("すべての銘柄のデータ取得と保存に成功しました", "success")
    return redirect(url_for("api.api_main"))
