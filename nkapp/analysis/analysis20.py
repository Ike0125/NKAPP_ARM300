"""  nkapp.analysis.analysis20.py  """
import json
import os
# from math import ceil
# from datetime import timedelta, datetime
# import pandas as pd
from flask import request, redirect, url_for, session
# from sqlalchemy import func, and_, case, literal
# from sqlalchemy import select, desc, asc
# from nkapp.models import Session, Tl
# from nkapp.rpt.models import VT
# from .config import VALUE_MAP10, VALUE_MAP20, VALUE_MAP30, VALUE_MAP40, VALUE_MAP41


class Ana:
    """Params for save/load """
    @staticmethod
    def load_config(file_name):
        """指定されたJSONファイルから設定を読み込み"""
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        else:
            return {}  # ファイルが存在しない場合、空の辞書を返す

    @staticmethod
    def save_config(file_name, config_data):
        """指定されたJSONファイルに設定を保存"""
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(config_data, file, indent=4)
                print(f"{file_path} にデータが保存されました。")
        except Exception as e:
            print(f"JSONファイルの保存中にエラーが発生しました: {e}")


class Formulaparams:
    """Params for Calculation Formula """

    def __init__(self):
        # for initializing params
        config = self.config()
        self.ma_value01 = config["ma_value01"]
        self.ma_value02 = config["ma_value02"]
        self.ma_value03 = config["ma_value03"]
        self.ma_value04 = config["ma_value04"]
        self.ma_value05 = config["ma_value05"]
        self.rsi_period_value = config["rsi_period_value"]
        self.macd_short_value = config["macd_short_value"]
        self.macd_long_value  = config["macd_long_value"]
        self.macd_signal_value= config["macd_signal_value"]


    @staticmethod
    def config():
        """Config Params"""
        return{
            "ma_value01" : 5,
            "ma_value02" : 20,
            "ma_value03" : 50,
            "ma_value04" : 100,
            "ma_value05" : 200,
            "rsi_period_value" : 14,
            "macd_short_value" : 7,
            "macd_long_value"  : 14,
            "macd_signal_value": 9
        }


    @staticmethod
    def register_ma():
        """Registration ma_config_params"""
        if request.method == "POST":
            config_ma = {
                "ma_value01": int(request.form.get("ma_value01", 5)),
                "ma_value02": int(request.form.get("ma_value02", 20)),
                "ma_value03": int(request.form.get("ma_value03", 50)),
                "ma_value04": int(request.form.get("ma_value04", 100)),
                "ma_value05": int(request.form.get("ma_value05", 200)),
            }
            print(f"config_ma: {config_ma}")
            config_formula = Ana.load_config("ana_config.json")
            config_formula.update(config_ma)
            Ana.save_config("ana_config.json",config_formula)
            return config_formula
        else:
            print("ma_Postではありません")
        return


    @staticmethod
    def register_rsi():
        """Registration ma_config_params"""
        if request.method == "POST":
            config_rsi = {
                "rsi_period_value": int(request.form.get("rsi_period_value","14")),
            }
            print(f"config_rsi: {config_rsi}")
            config_formula = Ana.load_config("ana_config.json")
            config_formula.update(config_rsi)
            Ana.save_config("ana_config.json",config_formula)
            return config_formula
        else:
            print("Post_RSIではありません")
        return


    @staticmethod
    def register_macd():
        """Registration ma_config_params"""
        if request.method == "POST":
            # 既存の設定を読み込み
            config_macd = {
                "macd_short_value"    : int(request.form.get("macd_short_value", 7)),
                "macd_long_value"     : int(request.form.get("macd_long_value", 14)),
                "macd_signal_value"   : int(request.form.get("macd_signal_value", 9))
            }
            print(f"config_macd: {config_macd}")
            Ana.save_config("config_macd.json",config_macd)
            config_formula = Ana.load_config("ana_config.json")
            config_formula.update(config_macd)
            Ana.save_config("ana_config.json",config_formula)

            return config_formula
        return
