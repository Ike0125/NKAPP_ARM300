""" kabudb.py J-QuantsとのAPIプログラム """
from datetime import datetime
from time import time
from flask import flash, request
import requests
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from nkapp.models import DailyQuotes, engine
from nkapp.api.config import Config
from nkapp.api.api_main import AP
from nkapp.set.mockjq_main import MK


# モックデータを定義（プログラムの冒頭に記載）
MOCK_API_RESPONSE = {
    "daily_quotes": [
        {
            "Date": "2024-06-19",
            "Code": "13010",
            "Open": 3860.0,
            "High": 3865.0,
            "Low": 3820.0,
            "Close": 3865.0,
            "UpperLimit": 0,
            "LowerLimit": 0,
            "Volume": 42900.0,
            "TurnoverValue": 165224000.0,
            "AdjustmentFactor": 1.0,
            "AdjustmentOpen": 3860.0,
            "AdjustmentHigh": 3865.0,
            "AdjustmentLow": 3820.0,
            "AdjustmentClose": 3865.0,
            "AdjustmentVolume": 42900.0,
        }
    ]
}


# モック関数を定義
def mock_requests_get(url, headers=None, params=None, timeout=None):
    """ mock_test for kabudb.py """
    class MockResponse:
        """ mock response """
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            """ mock response """
            return self.json_data
    # 引数を無視する場合
    _ = url
    _ = headers
    _ = params
    _ = timeout

    # モックデータを返す
    return MockResponse(MOCK_API_RESPONSE, 200)


@staticmethod
def retrieve_kabudb_request(mode=1):
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

    params = {"code": code}

    if mode == 9:    # mock test
        # APIリクエスト(モックテスト)
        response = MK.mock_jquants_api(
            Config.JQ_Daily_URL, headers=headers, params=params, timeout=10
        )
        print(f"response:{response.json()}")
    elif mode == 1:
        # APIリクエスト
        response = requests.get(
            Config.JQ_Daily_URL, headers=headers, params=params, timeout=10
        )
    else:
        print("Modeが設定されていません")
        raise ValueError("mode isn't set.")
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
            flash(f"{response.status_code}:Updated. ", "success")
        else:
            message =response.json().get('message')
            flash(f"{response.status_code}:{message}", "error")
    except ValueError as e:
        flash(f"{str(e)}","error")
    except Exception as e:
        flash(f"エラーが発生しました: {str(e)}", "error")
    print(f"Total process time: {time() - start_time:.2f} seconds")

    return
