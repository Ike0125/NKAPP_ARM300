#  from datetime import datetime
import json
import os
#  import requests
#  from flask import redirect, url_for, flash, request, render_template
#  from .config import Config


def load_config():  # config.jsonの読み込みと保存を行う関数
    """config.jsonファイルから設定を読み込む"""
    config_file = os.path.join(os.path.dirname(__file__), "config.json")
    if os.path.exists(config_file):
        with open(config_file, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        return {}


def save_config(data):
    """設定をconfig.jsonファイルに保存する"""
    config_file = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)