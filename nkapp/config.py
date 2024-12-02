"""  nkapp.config.py  """
import datetime
import os
import json
import pandas as pd
from sqlalchemy import func
from sqlalchemy.engine.row import Row
from flask import render_template
from .models import Session, Tl


class Mainparams:
    """Get SQL_DB Parameters"""

    @staticmethod
    def get_current_time():
        """現在の日時取得"""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

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
        db = Tl.current_db
        at_db = db.find('@')
        current_db = db[at_db:]
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


class Fileparams:
    """ファイル管理の共通初期設定値"""
    @staticmethod
    def save_csv(data, base_name, index=False, stamp=False):
        """検索結果をCSVファイルにデータを保存"""
        # initial params fot file management
        save_dir = r"C:\Users\Ichizo\OneDrive\ARM300\data\saved_data"
        os.makedirs(save_dir, exist_ok=True)  # ディレクトリが存在しない場合は作成
        encoding = 'utf-8'
        dataframe = Fileparams.ensure_dataframe(data)
        # データフレームをCSVファイルに保存する汎用メソッド。

        # Parameters:
        #    dataframe (pd.DataFrame): 保存するPandasデータフレーム
        #    base_name (str): ファイル名のベース (例: "output")
        #    index (bool, optional): インデックスを保存するかどうか (デフォルト: False)
        #    encoding (str, optional): ファイルのエンコーディング (デフォルト: 'utf-8')
        #    include_timestamp (bool, optional): タイムスタンプをファイル名に含めるかどうか (デフォルト: True)
        #    results_df = pd.DataFrame(results_data) : 辞書型をDFに変換

        # Returns:
        #    str: 保存したファイルのパス
        try:
            # タイムスタンプを追加する場合
            if stamp:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"{base_name}_{timestamp}.csv"
            else:
                file_name = f"{base_name}.csv"

            # CSVファイルを保存
            full_path = os.path.join(save_dir, file_name)
            dataframe.to_csv(full_path, index=index, encoding=encoding)

            print(f"Saved data file: {full_path}")
            return {"message" : f"CSVファイルが正常に保存されました: {file_name}",
                    "errormsg" : ""
                    }
        except Exception as e:
            print(f"CSVファイルの保存中にエラーが発生しました,{e}")
            return {"errormsg" : f"CSVファイルの保存中にエラーが発生しました: {e}",
                    "message" : ""
                    }


    @staticmethod
    def ensure_dataframe(data):
        """
        入力データをDataFrameに変換する。

        Parameters:
            data (various): チェックまたは変換するデータ。
                サポートする形式:
                - pd.DataFrame: そのまま返す。
                - list of dict: DataFrameに変換。
                - list of list: DataFrameに変換 (列名は自動生成)。
                - dict: DataFrameに変換。
        Returns:
            pd.DataFrame: 変換されたまたは元のDataFrame。
        Raises:
            ValueError: 対応していないデータ形式の場合。
        """
        if isinstance(data, pd.DataFrame):
            # すでにDataFrameの場合はそのまま返す
            return data
        elif isinstance(data, list):
            if all(isinstance(item, dict) for item in data):
                # list of dictをDataFrameに変換
                return pd.DataFrame(data)
            elif all(isinstance(item, list) for item in data):
                # list of listをDataFrameに変換
                return pd.DataFrame(data)
            elif all(isinstance(item, Row) for item in data):
                # list of Row を辞書に変換してDataFrameに変換
                return pd.DataFrame([row._asdict() for row in data])
            else:
                raise ValueError("リスト形式は辞書またはリストのリストである必要があります。")
        elif isinstance(data, dict):
            # dictをDataFrameに変換
            return pd.DataFrame([data])
        else:
            raise ValueError("DataFrameに変換できないデータ形式です。")


    @staticmethod
    def save_config(config_data, config_name, stamp=False):
        """指定されたJSONファイルに設定を保存

        Args:
            file_name (str): 保存するファイル名
            config_data (dict): 保存する設定データ
            add_timestamp (bool): ファイル名にタイムスタンプを追加するかどうか
        """
        file_name = config_name
        # 保存ディレクトリを指定
        save_dir = r"C:\Users\Ichizo\OneDrive\ARM300\data\saved_data"
        os.makedirs(save_dir, exist_ok=True)  # ディレクトリが存在しない場合は作成

        # 拡張子が .json でない場合、自動的に追加
        if not file_name.endswith(".json"):
            file_name += ".json"
        # タイムスタンプを追加する場合
        if stamp:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name, ext = os.path.splitext(file_name)
            file_name = f"{base_name}_{timestamp}{ext}"

        # ファイルパスを作成
        file_path = os.path.join(save_dir, file_name)

        try:
            # JSONファイルにデータを保存
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(config_data, file, ensure_ascii=True, indent=4)
            print(f"Saved setting params: {file_path}")
            return {
                "message" : f"設定ファイルが正常に保存されました: {file_name}",
                "errormsg" : ""
            }

        except Exception as e:
            print(f"JSONファイルの保存中にエラーが発生しました: {e}")
            return {
                "errormsg" : f"設定ファイルの保存中にエラーが発生しました: {e}",
                "message" : ""
            }
