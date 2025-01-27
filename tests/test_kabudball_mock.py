import sys
import os
import datetime
from sqlalchemy.orm import Session
from nkapp.models import DailyQuotesAll, engine

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# モックデータ作成
def generate_mock_data(start_date, end_date, batch_codes):
    """
    指定された日付範囲と銘柄コードに基づいてモックデータを生成。
    """
    mock_data = []
    current_date = start_date
    while current_date <= end_date:
        for code in batch_codes:
            mock_data.append({
                "Date": current_date.strftime("%Y-%m-%d"),
                "Code": code,
                "Open": 100.0,
                "High": 110.0,
                "Low": 90.0,
                "Close": 105.0,
                "Volume": 1000,
                "TurnoverValue": 105000.0,
                "UpperLimit": 120.0,
                "LowerLimit": 80.0,
                "AdjustmentFactor": 1.0,
                "AdjustmentOpen": 100.0,
                "AdjustmentHigh": 110.0,
                "AdjustmentLow": 90.0,
                "AdjustmentClose": 105.0,
                "AdjustmentVolume": 1000,
            })
        current_date += datetime.timedelta(days=1)
    return mock_data


@staticmethod
def mock_fetch_batch_data(batch_codes, headers):
    """
    モックデータを使用してAPIリクエストを模倣。
    """
    import datetime
    # モックデータの期間と銘柄コードを設定
    start_date = datetime.date(2024, 1, 1)
    end_date = datetime.date(2024, 1, 5)  # 例: 5日間のデータ
    mock_data = generate_mock_data(start_date, end_date, batch_codes)

    # ページング処理を模倣（1ページに最大100件）
    batch_size = 100
    pages = [mock_data[i:i + batch_size] for i in range(0, len(mock_data), batch_size)]

    # ページングキーの付加
    pagination_key = None
    if len(pages) > 1:
        pagination_key = "mock_key"

    return {
        "data": pages[0],  # 最初のページのデータ
        "pagination_key": pagination_key,
    }


def test_retrieve_kabudball_request_with_mock():
    """
    モックデータを使用したテストの実行。
    """
    print("Starting mock data retrieval test...")  # 開始メッセージを表示

    headers = {"Authorization": "Bearer MOCK_TOKEN"}
    batch_codes = ["CODE1", "CODE2", "CODE3"]
    
    with Session(engine) as session:
        response = mock_fetch_batch_data(batch_codes, headers)
        batch_data = response.get("data", [])
        print(f"Fetched mock data: {len(batch_data)} records")  # モックデータ件数を表示
        save_to_database(session, batch_data)

    print("Mock data retrieval and storage test completed.")  # 完了メッセージを表示
