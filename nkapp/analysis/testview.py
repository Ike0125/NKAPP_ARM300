"""  nkapp.analysis.testview.py  """
from flask import request, session
from .config import VALUE_MAP10, VALUE_MAP20, VALUE_MAP30
from .config import VALUE_MAP40, VALUE_MAP41, VALUE_MAP50
from .analysis20 import Ana


class Tst:
    """ Params """
    @staticmethod
    def test():
        """for querybuilder"""
        daygap101 = "何日前"
        daygap102 = "何日前"
        if request.method == "POST":
            session["cal_select101"] = request.form.get("dropdown101")
            session["cal_select102"] = request.form.get("dropdown102")
            session["cal_select121"] = request.form.get("dropdown121")
            session["paramquery101"] = request.form.get("param101", "")
            session["paramquery102"] = request.form.get("param102", "")
            session["paramquery103"] = request.form.get("param103", "")
            session["paramquery104"] = request.form.get("param104", "")
            session["paramquery201"] = request.form.get("param201", "")
            session["paramquery202"] = request.form.get("param202", "")
            session["gapquery101"] = request.form.get("gap101", "")
            session["gapquery102"] = request.form.get("gap102", "")
            session["gapquery103"] = request.form.get("gap103", "")
        # セッションに保存したデータの読み込み
        cal_select101 = session.get("cal_select101", "0201")
        cal_select102 = session.get("cal_select102", "0220")
        cal_select121 = session.get("cal_select121", "0500")
        paramquery101 = session.get("paramquery101", "")
        paramquery102 = session.get("paramquery102", "")
        paramquery103 = session.get("paramquery103", "")
        paramquery104 = session.get("paramquery104", "")
        paramquery201 = session.get("paramquery201", "")
        paramquery202 = session.get("paramquery202", "")
        daygap101 = session.get("gapquery101", 0)
        daygap102 = session.get("gapquery102", 0)
        daygap103 = session.get("gapquery103", 0)

        # 掲示板へのデータまとめ
        builder_params = {
            "cal_select101": cal_select101,  # 計算方法A-1
            "cal_select102": cal_select102,  # 計算方法A-2
            "cal_select121": cal_select121,  # 計算方法A-2
            "daygap101"   : daygap101,  # 何日前
            "daygap102"   : daygap102,  # 何日前
            "daygap103"   : daygap103,  # 何日前
            "paramquery101": paramquery101,  # 計算params
            "paramquery102": paramquery102,  # 計算params
            "paramquery103": paramquery103,  # 計算params
            "paramquery104": paramquery104,  # 計算params
            "paramquery201": paramquery201,  # 計算params
            "paramquery202": paramquery202,  # 計算params
        }
        # print(f"builder_params: {builder_params}")
        return builder_params


class Tst2:
    """ Params """
    @staticmethod
    def test_select():
        """for display_settings"""
        if request.method == "POST":
            value02_selected = 'value02' in request.form.getlist('value')
            value02a_selected = 'value02a' in request.form.getlist('value')
            value02b_selected = 'value02b' in request.form.getlist('value')
            print(f"value02_selected: {value02_selected}")
            print(f"value02a_selected: {value02a_selected}")
            print(f"value02b_selected: {value02b_selected}")
            session["condition"] = request.form.get("condition")
            session["value01"]   = request.form.get("value01")
            session["value02"]   = value02_selected
            session["value02a"]   = value02a_selected
            session["value02b"]   = value02b_selected
            session["value03"]   = request.form.get("value03")
            session["value04"]   = request.form.get("value04")
        condition = session.get("condition", None)
        value01  = session.get("value01", None)
        value02  = session.get("value02", False)
        value02a = session.get("value02a", False)
        value02b = session.get("value02b", False)
        value03  = session.get("value03", None)
        value04  = session.get("value04", None)

        builder_params = {
            "condition": condition,
            "value01": value01,
            "value02": value02,
            "value02a": value02a,
            "value02b": value02b,
            "value03": value03,
            "value04": value04,
        }
        print(f"builder_params: {builder_params}")

        return builder_params


class Tst3:
    """ Params """
    @staticmethod
    def query_builder2():
        """for display_settings"""
        if request.method == "POST":
            # 掲示板から選択値を取得し、セッションに保存
            session["condition"] = request.form.get("condition")
            # Selection
            session["condition001"] = request.form.get("dropdown001")
            # Gropu A
            session["window101"] = request.form.get("dropdown101")
            session["gapquery111"] = request.form.get("gap111")
            session["paramquery121"] = request.form.get("param121")
            session["paramquery122"] = request.form.get("param122")
            # Operator
            session["ope_select131"] = request.form.get("dropdown131")
            # Group B
            session["window201"] = request.form.get("dropdown201")
            session["gapquery211"] = request.form.get("gap211")
            session["paramquery221"] = request.form.get("param221")
            session["paramquery222"] = request.form.get("param222")
            # Sort
            session["sort_select501"] = request.form.get("dropdown501")
        else:
            # 保存したデータの読み込み
            ana_config = Ana.load_config("ana_config.json")
            session["condition"]      = ana_config["condition"]
            session["condition001"]   = ana_config["condition001"]
            session["window101"]      = ana_config["window101"]
            session["gapquery111"]    = ana_config["gapquery111"]
            session["paramquery121"]  = ana_config["paramquery121"]
            session["paramquery122"]  = ana_config["paramquery122"]
            session["ope_select131"]  = ana_config["ope_select131"]
            session["gapquery211"]    = ana_config["gapquery211"]
            session["paramquery221"]  = ana_config["paramquery221"]
            session["paramquery222"]  = ana_config["paramquery222"]
            session["sort_select501"] = ana_config["sort_select501"]
        # セッションに保存したデータの読み込み
        # Selection
        condition = session.get("condition", None)
        condition001 = session.get("condition001", None)
        # Group A
        window101 = int(session.get("window101",5))
        gapquery111 = session.get("gapquery111","")
        paramquery121 = session.get("paramquery121","")
        paramquery122 = session.get("paramquery122","")
        # Operator
        ope_select131 = session.get("ope_select131","")
        # Group B
        window201 = int(session.get("window201",5))
        gapquery211 = session.get("gapquery211","")
        paramquery221 = session.get("paramquery221","")
        paramquery222 = session.get("paramquery222","")
        sort_select501 = session.get("sort_select501","")
        # 掲示板へのデータまとめ
        ana_config = Ana.load_config("ana_config.json")
        builder_params = {
            # Market/Calculation setting
            "marketcode": ana_config.get('marketcode', None),   #市場区分コード
            "selected10": ana_config.get('selected10', None),   #市場区分
            "ma_value01": ana_config.get('ma_value01', None),   #移動平均１
            "ma_value02": ana_config.get('ma_value02', None),   #移動平均２
            "ma_value03": ana_config.get('ma_value03', None),   #移動平均３
            "ma_value04": ana_config.get('ma_value04', None),   #移動平均４
            "ma_value05": ana_config.get('ma_value05', None),   #移動平均５
            "rsi_period_value": ana_config.get('rsi_period_value', None),   #RSI期間
            "macd_short_value": ana_config.get('macd_short_value', None),   #MACDshort
            "macd_long_value": ana_config.get('macd_long_value', None),     #MACDlong
            "macd_signal_value": ana_config.get('macd_signal_value', None), #MACDsignal
            # Query Setting
            "daygapname111"    : "何日前",
            "paramname121"   : "Param-A1",
            "paramname122"   : "Param-A2",
            "daygapname211"    : "何日前",
            "paramname221"   : "Param-B1",
            "paramname222"   : "Param-B2",
            "VALUE_MAP10"   : VALUE_MAP10,  # 市場区分コードリスト
            "VALUE_MAP20"   : VALUE_MAP20,  # 計算方法リスト
            "VALUE_MAP30"   : VALUE_MAP30,  # 演算子リスト
            "VALUE_MAP40"   : VALUE_MAP40,  # ソート順リスト
            "VALUE_MAP41"   : VALUE_MAP41,  # KEY Columnリスト
            "VALUE_MAP50"   : VALUE_MAP50,  # Query Conditionリスト
            "condition"     : condition,
            "condition001"  : condition001,
            "window101"     : window101,
            "gapquery111"   : gapquery111,
            "paramquery121" : paramquery121,
            "paramquery122" : paramquery122,
            "ope_select131" : ope_select131,
            "window201"     : window201,
            "gapquery211"   : gapquery211,
            "paramquery221" : paramquery221,
            "paramquery222" : paramquery222,
            "sort_select501": sort_select501,
            "comment102"    : "式もしくは設定したパラメータ",      #以下は各計算メソッドから戻すこと
            "subject123"    : "A123",
            "subject124"    : "A124",
            "subject125"    : "A125",
            "comment123"    : "A123_comment",
            "comment124"    : "A124_comment",
            "comment125"    : "A125_comment",
            "comment202"    : "固定値",
            "subject223"    : "B223",
            "subject224"    : "B224",
            "subject225"    : "B225",
            "comment223"    : "B223_comment",
            "comment224"    : "B224_comment",
            "comment225"    : "B225_comment",
        }
        # print(f"builder_params: {builder_params}")
        # データの保存
        config_formula = Ana.load_config("ana_config.json")
        config_formula.update(builder_params)
        Ana.save_config("ana_config.json",builder_params)

        return builder_params
    