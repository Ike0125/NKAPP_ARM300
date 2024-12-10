""" listedinfo.py """
from datetime import datetime
from flask import flash, redirect, url_for
import requests
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session
from nkapp.api.models import ListedInfo, engine
from nkapp.api.config import Config
from nkapp.api.jq_main import APJQ


def listedinfo_request(request):
    """
    JQ APIから上場銘柄一覧データを取得し、データベースに保存または更新する。

    :param request: Flaskのリクエストオブジェクト
    :return: テンプレートのレンダリングまたはリダイレクトレスポンス
    """
    # トークン取得
    config_data = APJQ.load_config()  # config.jsonを読み込む
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
                        index_elements=["code"],  # 一意制約に基づいて更新
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
    return redirect(url_for("api.jq_main"))
