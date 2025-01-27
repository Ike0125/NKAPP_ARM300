""" kabudb.py J-QuantsとのAPIプログラム """
from datetime import datetime
from time import time
from flask import flash, redirect, url_for, request
import requests
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from nkapp.models import DailyQuotes, engine
from nkapp.api.config import Config
from nkapp.api.api_main import AP


@staticmethod
def retrieve_kabudb_request():
    """
    JQ APIから株価データを取得し、データベースに保存または更新する。
    """
    start_time = time()  # 全体の処理時間計測開始
    print("Starting data retrieval process...")
    # トークン取得
    config_data = AP.load_config()  # config.jsonを読み込む
    id_token = config_data.get("ID_TOKEN")
    headers = {"Authorization": f"Bearer {id_token}"}

    # ユーザーが入力したコードを取得
    code = request.form.get("code", "72030")  # デフォルト値は '72030'

    # APIリクエスト
    params = {"code": code}
    response = requests.get(
        Config.JQ_Daily_URL, headers=headers, params=params, timeout=10
    )

    try:
        if response.status_code == 200:
            data = response.json()
            with Session(engine) as session:  # SQLAlchemy 2.x の構文を使用
                with session.no_autoflush:  # 自動フラッシュを一時的に無効化
                    for item in data.get("daily_quotes", []):  # データが存在しない場合に空リストを使う
                        try:
                            date_obj = datetime.strptime(item["Date"], "%Y-%m-%d").date()
                        except KeyError:
                            flash("データ形式が正しくありません", "error")
                            continue

                        # INSERTまたはUPDATE
                        stmt = insert(DailyQuotes).values(
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
                        # `stmt`を初期化した後で`stmt.excluded`を使用
                        stmt = stmt.on_conflict_do_update(
                            index_elements=["date", "code"],  # 一意制約に基づく更新
                            set_={
                                "open": stmt.excluded.open,
                                "high": stmt.excluded.high,
                                "low": stmt.excluded.low,
                                "close": stmt.excluded.close,
                                "upperlimit": stmt.excluded.upperlimit,
                                "lowerlimit": stmt.excluded.lowerlimit,
                                "volume": stmt.excluded.volume,
                                "turnovervalue": stmt.excluded.turnovervalue,
                                "adjustmentfactor": stmt.excluded.adjustmentfactor,
                                "adjustmentopen": stmt.excluded.adjustmentopen,
                                "adjustmenthigh": stmt.excluded.adjustmenthigh,
                                "adjustmentlow": stmt.excluded.adjustmentlow,
                                "adjustmentclose": stmt.excluded.adjustmentclose,
                                "adjustmentvolume": stmt.excluded.adjustmentvolume,
                            },
                        )
                        session.execute(stmt)
                session.commit()
            flash("データの取得と保存に成功しました", "success")
        else:
            flash(f"データの取得に失敗しました: {response.status_code}", "error")
    except Exception as e:
        flash(f"エラーが発生しました: {str(e)}", "error")
        raise
    print(f"Total process time: {time() - start_time:.2f} seconds")

    return redirect(url_for("api.api_main"))
