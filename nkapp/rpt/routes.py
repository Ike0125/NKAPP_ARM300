""" rpt/route.py """
from flask import render_template, Blueprint
from nkapp.config import Mainparams
from nkapp.rpt.report import Infoparams
from nkapp.rpt.report10 import Infoparams10
from nkapp.rpt.report11 import Chartparams

#  Blueprintのインスタンス作成
bp_rpt = Blueprint("rpt", __name__, template_folder="templates")


@bp_rpt.route("/main")                      # Report メイン画面
def main():
    """  Routing for Report-Main BBS  """
    main_params = Mainparams.get_main_params()
    main_params2 = Infoparams.info_list2()
    return render_template("main.html", **main_params, **main_params2)


@bp_rpt.route("/info_all")                  # 上場銘柄一覧画面
def info_all():
    """  Report BBS: Listed_Info_all   """
    main_params = Infoparams.info_all()
    return render_template("info_all.html", **main_params)


@bp_rpt.route("/info_card")                 # 上場銘柄個別画面
def info_card():
    """  Report BBS: Listed_Info_all   """
    main_params = Infoparams.info_card()
    main_params2 = Chartparams.get_chart()
    return render_template("info_card2.html", **main_params, **main_params2)
    # return render_template("info_card2.html", **main_params)


@bp_rpt.route("/info_list")                 # 上場銘柄検索画面
def info_list():                            # 現在使用していない
    """  Report BBS: Listed_Info_list   """
    main_params = Infoparams.info_list()
    return render_template("info_list.html", **main_params)


@bp_rpt.route("/info_list2")                # 上場銘柄検索画面
def info_list2():
    """  Report BBS: Listed_Info_list   """
    main_params = Mainparams.get_main_params()
    main_params2 = Infoparams.info_list2()
    return render_template("main.html", **main_params, **main_params2)


@bp_rpt.route("/daily")                     # 株価関連-個別画面
def daily():
    """  Report BBS: Daily Quotes/ Prices """
    main_params = Infoparams.daily()
    return render_template("daily.html", **main_params)


@bp_rpt.route("/daily_query")               # 株価関連-全数画面
def daily_query():
    """  Report BBS: Daily Quotes/ Prices """
    main_params = Infoparams.daily_query()
    return render_template("daily_query.html", **main_params)


@bp_rpt.route("/tstock_query10")              # 株価/上場銘柄複合画面
def tstock_query10():                         # 移動平均データ付き
    """  Report BBS: Daily Quotes/ Prices """
    main_params = Infoparams10.tstock_query10()
    # print("DEBUG: main_params =", main_params)
    return render_template("tstock_query10.html", **main_params)


@bp_rpt.route("/tstock_query20")              # 株価/上場銘柄複合画面
def tstock_query20():                         # テスト用
    """  Report BBS: Daily Quotes/ Prices """
    main_params = Infoparams10.tstock_query20()
    return render_template("tstock_query10.html", **main_params)


@bp_rpt.route("/tstock_query11")            # 株価/上場銘柄複合画面
def tstock_query11():
    """  Report BBS: Daily Quotes/ Prices """
    main_params = Infoparams10.tstock_query11()
    return render_template("tstock_query11.html", **main_params)


@bp_rpt.route("/get_chart")  # グラフ画面
def get_chart():                                # 出力は、rpt.main.htmlへ
    """  Report BBS: Daily Quotes/ Prices """
    main_params = Chartparams.get_chart()
    # print(main_params)
    return render_template("chart_test.html", **main_params)
