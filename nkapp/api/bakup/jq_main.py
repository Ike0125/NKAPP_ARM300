""" from datetime import datetime """
import json
import os
from sqlalchemy import func
from nkapp.models import Session, Tl

#  import requests
#  from flask import redirect, url_for, flash, request, render_template
#  from .config import Config


class APJQ:
    """ API_params """
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


    @staticmethod
    def jq_main():
        """API初期画面jq_main.html用パラメータ"""
        config_data = APJQ.load_config()

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

        id_token_timestamp      = config_data.get("ID_TOKEN_TIMESTAMP")
        refresh_token_timestamp = config_data.get("REFRESH_TOKEN_TIMESTAMP")
        jq_params = {
            "id_token_timestamp" : id_token_timestamp,
            "refresh_token_timestamp" : refresh_token_timestamp,
            "record_count_info" : record_count_info,
            "record_count"      : record_count,
            "record_count_all"  : record_count_all,
            "last_update_info"  : last_update_info,
            "last_update_all"   : last_update_all,
            "last_update"       : last_update,
        }

        return jq_params
