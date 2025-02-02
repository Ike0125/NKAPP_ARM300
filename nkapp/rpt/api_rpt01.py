"""  nkapp.rpt.api_rpt01.py  """
from math import ceil
from flask import request
from sqlalchemy import select, func
from nkapp.config import Reportparams, Config
from nkapp.models import Session
from .models import Tl

class ApiRpt:
    """Params for API-Announcement"""
    @staticmethod
    def config():
        """Initial Params for apt_rpt01.py """
        return {
            "head_title": "NKAPP MAIN",
            "header_title": "Main",
            "endpoint": "nkapp.index",
            "return_url": "nkapp.index",
            "return_name": "Nkapp Main",
            "home_url": "nkapp.index",
        }


    @staticmethod
    def rpt01_config():
        """Initial Params for Announcement"""
        current_time = Config.get_current_time()
        return {
            "head_title": "Report: Annoucement",
            "header_title": "決算発表予定日 (fins/announcement)",
            "endpoint": "rpt.api_rpt01",
            "return_url": "nkapp.index",
            "return_name": "index",
            "home_url": "nkapp.index",
            "current_time": current_time,
        }


    @staticmethod
    def api_rpt01(mode=1):
        """Params for Announcement BBS"""
        # Params
        per_page = Reportparams.per_page
        page = request.args.get("page", 1, type=int)
        ann = Tl.announcement
        minimum_no = 5      #　ミニマム取得数
        counts = 0
        raw_data ={}

        with Session() as db_session:
            base_query = (
                db_session.query(
                    ann.Date,
                    ann.Code,
                    ann.CompanyName,
                    ann.FiscalYear,
                    ann.SectorName,
                    ann.FiscalQuarter,
                    ann.Section
                )
                .order_by(func.to_date(ann.Date, 'YYYY-MM-DD').desc())
            )
            if mode == 1:
                # 総レコード数を取得
                # pylint: disable=not-callable
                count_query = select(func.count()).select_from(base_query.subquery())
                # base_queryをサブクエリとし、その結果の行数をカウント
                counts = db_session.execute(count_query).scalar()
                # オフセット計算
                offset = (page - 1) * per_page
                # ページネーションをオフセット値と１ページ当りのレコード数より設定
                paginated_query = base_query.offset(offset).limit(per_page)
                # クエリを実行し、全レコードを取得
                raw_data = db_session.execute(paginated_query).mappings().all()
                # print(f"raw data: {raw_data}")
            elif mode == 2:
                minimum_query = base_query.limit(minimum_no)
                raw_data = db_session.execute(minimum_query).mappings().all()

        total_pages = ceil(counts / per_page)  # トータルページ数の計算
        # print(f"raw data: {raw_data[:5]}")

        info_params = {
            "db_data": raw_data,
            "total_records": counts,
            "total_pages": total_pages,
            "page": page,
            "per_page": per_page,
        }

        return info_params
