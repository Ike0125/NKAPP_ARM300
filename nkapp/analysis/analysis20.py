"""  nkapp.analysis.analysis20.py  """
import json
import os
from tkinter import Tk, filedialog
from flask import request, redirect, url_for
# from nkapp.config import Config
from .config import VALUE_MAP10, VALUE_MAP11, VALUE_MAP12, VALUE_MAP13, VALUE_MAP14


class Ana:
    """Params for save/load """
    @staticmethod
    def builder():
        """initial params for "ana_builder.html"""
        ana_config = Ana.load_config("ana_config.json")
        config_builder = {
            # "current_time" : Config.get_current_time(),
            "endpoint": "analysis.analysis_query31",
            "return_url": "analysis.analysis_query31",
            "return_name": "To analysis31",
            "home_url": "nkapp.index",
            "VALUE_MAP10": VALUE_MAP10,
            "VALUE_MAP11": VALUE_MAP11,
            "VALUE_MAP12": VALUE_MAP12,
            "VALUE_MAP13": VALUE_MAP13,
            "VALUE_MAP14": VALUE_MAP14,
            "marketcategory" : ana_config.get('marketcategory', None),
            "categorydetail" : ana_config.get('categorydetail', None),
            "marketcode"     : ana_config.get('marketcode', None),
            "sector17code"   : ana_config.get('sector17code', None),
            "sector33code"   : ana_config.get('sector33code', None),
            "scalecategory"  : ana_config.get('scalecategory', None),
            "customcategory" : ana_config.get('customcategory', None),
            "selected10": ana_config.get('selected10', None),
            "selected11": ana_config.get('selected11', None),
            "selected12": ana_config.get('selected12', None),
            "selected13": ana_config.get('selected13', None),
            "selected14": ana_config.get('selected14', None),
            "ckbox10": ana_config.get('ckbox10_selected', None),
            "ckbox11": ana_config.get('ckbox11_selected', None),
            "ckbox12": ana_config.get('ckbox12_selected', None),
            "ckbox13": ana_config.get('ckbox13_selected', None),
            "ckbox14": ana_config.get('ckbox14_selected', None),
            "ckbox19": ana_config.get('ckbox19_selected', None),
            "ma_value01": ana_config.get('ma_value01', None),
            "ma_value02": ana_config.get('ma_value02', None),
            "ma_value03": ana_config.get('ma_value03', None),
            "ma_value04": ana_config.get('ma_value04', None),
            "ma_value05": ana_config.get('ma_value05', None),
            "rsi_period_value": ana_config.get('rsi_period_value', None),
            "macd_short_value": ana_config.get('macd_short_value', None),
            "macd_long_value": ana_config.get('macd_long_value', None),
            "macd_signal_value": ana_config.get('macd_signal_value', None),
            "file_path" : ana_config.get('file_path', None),
            "status"    : request.args.get('status',""),
            "comment"   : request.args.get('comment',""),
            "errormsg"  : request.args.get('errormsg',""),
        }
        return config_builder


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
        """指定されたJSONファイルに設定を保存
        Args:
            file_name (str): 保存するファイル名
            config_data (dict): 保存する設定データ
        """
        # 保存ディレクトリを現在のファイルと同じディレクトリに設定
        save_dir = os.path.dirname(__file__)
        # 拡張子が .json でない場合、自動的に追加
        if not file_name.endswith(".json"):
            file_name += ".json"
        # ファイルパスを作成
        file_path = os.path.join(save_dir, file_name)
        # バックアップファイル名を生成
        backup_file_name = file_name.replace(".json", "_backup.json")
        backup_file_path = os.path.join(save_dir, backup_file_name)
        try:
            # JSONファイルにデータを保存
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(config_data, file, ensure_ascii=True, indent=4)

            # バックアップファイルを作成
            with open(backup_file_path, "w", encoding="utf-8") as backup_file:
                json.dump(config_data, backup_file, ensure_ascii=True, indent=4)

            print(f"Saved setting file: {file_path}")
            print(f"Saved backup file: {backup_file_path}")
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
        """Initial Params"""
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
            # print(f"config_ma: {config_ma}")
            config_formula = Ana.load_config("ana_config.json")
            config_formula.update(config_ma)
            Ana.save_config("ana_config.json",config_formula)
        else:
            print("ma_Postではありません")
        return redirect(url_for('analysis.builder'))


    @staticmethod
    def register_rsi():
        """Registration rsi_config_params"""
        status    = ""
        comment   = ""
        errormsg  = ""
        msg_params = {}
        if request.method == "POST":
            config_rsi = {
                "rsi_period_value": int(request.form.get("rsi_period_value","14")),
            }
            # print(f"config_rsi: {config_rsi}")
            config_formula = Ana.load_config("ana_config.json")
            config_formula.update(config_rsi)
            Ana.save_config("ana_config.json",config_formula)
            status = "Success-Registring"
        else:
            print("Post_RSIではありません")
        msg_params={"status": status,"comment": comment,"errormsg": errormsg}
        return redirect(url_for('analysis.builder', **msg_params))


    @staticmethod
    def register_macd():
        """Registration macd_config_params"""
        status    = ""
        comment   = ""
        errormsg  = ""
        msg_params = {}
        config_formula = Ana.load_config("ana_config.json")
        if request.method == "POST":
            # 既存の設定を読み込み
            config_macd = {
                "macd_short_value"    : int(request.form.get("macd_short_value", 7)),
                "macd_long_value"     : int(request.form.get("macd_long_value", 14)),
                "macd_signal_value"   : int(request.form.get("macd_signal_value", 9)),
                "file_path"           : None,
            }
            status ="Success-Register"

            # print(f"config_macd: {config_macd}")
            config_formula.update(config_macd)
            Ana.save_config("ana_config.json",config_formula)
        else:
            config_macd = {
                "file_path"           : None,
            }
            config_formula.update(config_macd)
            Ana.save_config("ana_config.json",config_formula)
        msg_params={"status": status,"comment": comment,"errormsg": errormsg}
        return redirect(url_for('analysis.builder', **msg_params))


class Marketparams:
    """ Market Params """
    @staticmethod
    def reg_marketcode():
        """Registration ma_config_params"""
        status    = ""
        comment   = ""
        errormsg  = ""
        msg_params = {}
        marketcategory = ""
        categorydetail = ""
        if request.method == "POST":
            marketcode = request.form.get("dropdown10","")
            sector17code = request.form.get("dropdown11","")
            sector33code = request.form.get("dropdown12","")
            scalecategory = request.form.get("dropdown13","")
            customcategory = request.form.get("dropdown14","")
            ckbox10_selected = 'ckbox10' in request.form.getlist('ckbox')
            ckbox11_selected = 'ckbox11' in request.form.getlist('ckbox')
            ckbox12_selected = 'ckbox12' in request.form.getlist('ckbox')
            ckbox13_selected = 'ckbox13' in request.form.getlist('ckbox')
            ckbox14_selected = 'ckbox14' in request.form.getlist('ckbox')
            ckbox19_selected = 'ckbox19' in request.form.getlist('ckbox')
            selected10 = VALUE_MAP10.get(marketcode,"")
            selected11 = VALUE_MAP11.get(sector17code,"")
            selected12 = VALUE_MAP12.get(sector33code,"")
            selected13 = VALUE_MAP13.get(scalecategory,"")
            selected14 = VALUE_MAP14.get(customcategory,"")

            if ckbox10_selected is True :
                marketcategory = "Market Code"
                categorydetail = selected10
            elif ckbox11_selected is True :
                marketcategory = "Sector17Code"
                categorydetail = selected11
            elif ckbox12_selected is True :
                marketcategory = "Sector33Code"
                categorydetail = selected12
            elif ckbox13_selected is True :
                marketcategory = "Scale Category"
                categorydetail = selected13
            elif ckbox14_selected is True :
                marketcategory = "Custom Category"
                categorydetail = selected14
            elif ckbox19_selected is True :
                marketcategory = "All"
                categorydetail = "---------"
            else:
                marketcategory = "---------"
                categorydetail = "---------"
            config_marketcode = {
                "marketcategory" : marketcategory,
                "categorydetail" : categorydetail,
                "selected10": selected10,
                "selected11": selected11,
                "selected12": selected12,
                "selected13": selected13,
                "selected14": selected14,
                "marketcode"    : marketcode,
                "sector17code"  : sector17code,
                "sector33code"  : sector33code,
                "scalecategory" : scalecategory,
                "customcategory": customcategory,
                "ckbox10_selected": ckbox10_selected,
                "ckbox11_selected": ckbox11_selected,
                "ckbox12_selected": ckbox12_selected,
                "ckbox13_selected": ckbox13_selected,
                "ckbox14_selected": ckbox14_selected,
                "ckbox19_selected": ckbox19_selected,
            }
            print(f"config_marketcode: {config_marketcode}")
            config_market = Ana.load_config("ana_config.json")
            config_market.update(config_marketcode)
            Ana.save_config("ana_config.json",config_market)
        else:
            print("Post_Marketcodeではありません")
        msg_params={"status": status,"comment": comment,"errormsg": errormsg}

        return redirect(url_for('analysis.builder', **msg_params))


    @staticmethod
    def select_csv():
        """  Reading CSV file with Windows """
        file_path = None
        status    = ""
        errormsg  = ""
        ana_config = Ana.load_config("ana_config.json")
        if request.method == "POST":
            root = Tk()
            root.withdraw()  # Tkinterウィンドウを非表示にする
            try:
                file_path = filedialog.askopenfilename(title="CSVファイルを選択してください", filetypes=[("CSVファイル", "*.csv")])
                if file_path:
                    print(file_path)
                    status = "success-selecting"
                else:
                    print("ファイルが選択されませんでした。")
                    status = "notice"
                    errormsg = "ファイルが選択されませんでした。"
            except Exception as e:
                status = "error",
                errormsg = str(e),
            finally:
                root.destroy()  # リソース解放を確実に行う
        else:
            file_path = ana_config.get("file_path")
        config_marketcode = {
            "file_path" : file_path,
            "status"    : status,
            "errormsg"  : errormsg
        }
        print(f"config_marketcode: {config_marketcode}")
        config_market = Ana.load_config("ana_config.json")
        config_market.update(config_marketcode)
        Ana.save_config("ana_config.json",config_market)
        msg_params = {
            "status"    : status,
            "errormsg"  : errormsg
        }

        return redirect(url_for('analysis.builder', **msg_params))


    @staticmethod
    def reset_csv():
        """Reset Params for Save Option"""
        if request.method == "POST":
            # 既存の設定を読み込み
            reset_config = {
                "file_path": None,
                "status"    : "",
                "errormsg"  : "",
                "comment"   : ""
            }
            # print(f"config_macd: {config_macd}")
            config_data = Ana.load_config("ana_config.json")
            config_data.update(reset_config)
            Ana.save_config("ana_config.json",config_data)
        else:
            print("Reset Error/reset_option/57")
        return redirect(url_for('analysis.builder'))
