"""  nkapp.config.py  """

from datetime import datetime
from sqlalchemy import func
from flask import render_template
from .models import Session, Tl


class Mainparams:
    """Get SQL_DB Parameters"""

    @staticmethod
    def get_current_time():
        """現在の日時取得"""
        return datetime.now().strftime("%Y-%m-%d %H:%M")

    @staticmethod
    def get_main_params():
        """main process"""
        with Session() as session:
            with session.begin():
                record_count_info = f"{session.query(Tl.info_table).count():,}"
                # listed_info 総レコード数
                record_count = f"{session.query(Tl.daily_table).count():,}"
                # daily_quotes総レコード数
                record_count_all = f"{session.query(Tl.daily_all_table).count():,}"
                # daily_quotes_all総レコード数
                last_update_info = session.query(
                    func.max(Tl.info_table.c.date)
                ).scalar()  # listed_info 最終更新日
                last_update = session.query(
                    func.max(Tl.daily_table.c.date)
                ).scalar()  # daily_quotes最終更新日
                last_update_all = session.query(
                    func.max(Tl.daily_all_table.c.date)
                ).scalar()  # daily_quotes最終更新日
        current_time = Mainparams.get_current_time()
        current_db = Tl.current_db
        main_params = {
            "record_count_info": record_count_info,
            "record_count": record_count,
            "record_count_all": record_count_all,
            "last_update_info": last_update_info,
            "last_update": last_update,
            "last_update_all": last_update_all,
            "current_time": current_time,
            "current_db": current_db,
        }
        # print(record_count_all)
        return main_params


class Config:
    """各掲示板の共通初期設定値"""

    @staticmethod
    def get_current_time():
        """現在の日時取得"""
        return datetime.now().strftime("%Y-%m-%d %H:%M")

    @staticmethod
    def render_analysis_template():
        """analysis.htmlへの各初期パラメータの取得・転送"""
        current_time = Mainparams.get_current_time()

        return render_template(
            "analysis.html",
            current_time=current_time,
        )


class Reportparams():
    """各掲示板の共通初期設定値"""
    per_page = 50   # 1ページ当たりの表示件数

