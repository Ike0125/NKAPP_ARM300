""" rpt/route.py """
from flask import render_template, Blueprint
from nkapp.config import Mainparams
from .analysis import Analysisparams
from .analysis10 import Analysisparams10
from .analysis20 import Formulaparams, Ana

#  Blueprintのインスタンス作成
bp_analysis = Blueprint("analysis", __name__, template_folder="templates")


@bp_analysis.route("/main")                      # Analysis メイン画面
def main():
    """  Routing for Report-Main BBS  """
    main_params = Mainparams.get_main_params()
    main_params2 = Analysisparams.ana_list()
    return render_template("ana_main.html", **main_params, **main_params2)


@bp_analysis.route("/ana_list")                    # 上場銘柄検索画面
def ana_list():                                    # 現在使用していない
    """  Report BBS: Listed_Info_list   """
    main_params = Mainparams.get_main_params()
    main_params2 = Analysisparams.ana_list()
    return render_template("ana_main.html", **main_params, **main_params2)


@bp_analysis.route("/filter1")                    # 上場銘柄検索画面
def filter1():                                    # 現在使用していない
    """  Report BBS: Listed_Info_list   """
    main_params = Analysisparams.filter1()
    return render_template("info_list.html", **main_params)


@bp_analysis.route("/filter2")                    # 上場銘柄検索画面
def filter2():                                    # 現在使用していない
    """  Report BBS: Listed_Info_list   """
    main_params = Mainparams.get_main_params()
    main_params2 = Analysisparams.filter2()
    return render_template("ana_main.html", **main_params, **main_params2)


@bp_analysis.route("/filtermix")                  # 上場銘柄一覧画面
def filtermix():
    """  Report BBS: Listed_Info_all   """
    main_params = Analysisparams.filtermix()
    return render_template("info_list.html", **main_params)


@bp_analysis.route("/analysis_query", methods=['GET','POST']) # クエリー1
# テスト用
def analysis_query():
    """  Report BBS: Listed_Info_list   """
    main_params = Mainparams.get_main_params()
    builder_params = Analysisparams10.querybuilder()
    main_params2 = Analysisparams10.analysis_query(builder_params)
    # print(f"main_params2: {main_params2}")
    return render_template("ana_query.html", **main_params, **main_params2, **builder_params)


@bp_analysis.route("/builder", methods=['Get']) # Formula Setting
def builder():
    """  Routing for Treeview BBS  """
    formula_params = Ana.load_config("ana_config.json")
    return render_template('ana_builder.html', **formula_params)


@bp_analysis.route("/register_ma", methods=['Post'])
def register_ma():
    """  Routing for Treeview BBS  """
    formula_params = Formulaparams.register_ma()
    return render_template('ana_builder.html', **formula_params)


@bp_analysis.route("/register_rsi", methods=['Post'])
def register_rsi():
    """  Routing for Treeview BBS  """
    formula_params = Formulaparams.register_rsi()
    return render_template('ana_builder.html', **formula_params)
    # return render_template('ana_builder.html')


@bp_analysis.route("/register_macd", methods=['Post'])
def register_macd():
    """  Routing for Treeview BBS  """
    formula_params = Formulaparams.register_macd()
    return render_template('ana_builder.html', **formula_params)
