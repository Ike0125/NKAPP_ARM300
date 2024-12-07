""" rpt/route.py """
from flask import Blueprint
from flask import render_template
from nkapp.config import Mainparams
from .analysis import Analysisparams
from .analysis10 import Analysisparams10
from .analysis20 import Marketparams, Formulaparams, Ana
from .analysis30 import Analysisparams30
from .analysis31 import A31
from .testview import Tst2, FR

#  Blueprintのインスタンス作成
bp_analysis = Blueprint("analysis", __name__, template_folder="templates")


@bp_analysis.route("/builder", methods=['Get','post']) # Formula Setting
def builder():
    """  Routing for Treeview BBS  """
    main_params = Mainparams.get_main_params()
    config_builder = Ana.builder()
    return render_template('ana_builder.html', **main_params, **config_builder)


@bp_analysis.route("/query_builder2", methods=["GET","POST"])
def query_builder2():
    """  Routing for Treeview BBS  """
    main_params = Mainparams.get_main_params()
    builder_params = A31.query_builder2()
    config_params = A31.config()
    return render_template("ana_query31.html", **main_params, **builder_params, **config_params)


@bp_analysis.route("/analysis_query31", methods=['GET','POST']) # クエリー1
def analysis_query31():
    """  Report BBS: Listed_Info_list   """
    main_params = Mainparams.get_main_params()
    builder_params = A31.query_builder2()
    main_params2 = A31.analysis_query31(builder_params)
    return render_template("ana_query31.html", **main_params, **main_params2)


@bp_analysis.route("/register_option", methods=['Post'])
def register_option():
    """  Routing for Treeview BBS  """
    return A31.register_option()


@bp_analysis.route("/reset_option", methods=['Post'])
def reset_option():
    """  Routing for Treeview BBS  """
    return A31.reset_option()


@bp_analysis.route("/register_ma", methods=['Post'])
def register_ma():
    """  Routing for Treeview BBS  """
    return Formulaparams.register_ma()


@bp_analysis.route("/register_rsi", methods=['Post'])
def register_rsi():
    """  Routing for Treeview BBS  """
    return Formulaparams.register_rsi()


@bp_analysis.route("/register_macd", methods=['Post'])
def register_macd():
    """  Routing for Treeview BBS  """
    return Formulaparams.register_macd()


@bp_analysis.route("/reg_marketcode", methods=['Post'])
def reg_marketcode():
    """  Routing for Treeview BBS  """
    return Marketparams.reg_marketcode()


@bp_analysis.route("/select_csv", methods=["POST"])
def select_csv():
    """  Selecting CSV file """
    return Marketparams.select_csv()


@bp_analysis.route("/reset_csv", methods=['Post'])
def reset_csv():
    """  Routing for Treeview BBS  """
    return Marketparams.reset_csv()


@bp_analysis.route("/test_select", methods=["GET","POST"])
def test_select():
    """  Routing for Treeview BBS  """
    print("Post_されました")
    config_builder = Tst2.test_select()
    main_params = FR.select_file()
    return render_template('test_select.html', **config_builder, **main_params)


@bp_analysis.route("/select_file", methods=["POST"])
def select_file():
    """  Selecting CSV file """
    config_builder = Tst2.test_select()
    main_params = FR.select_file()
    return render_template('test_select.html', **config_builder, **main_params)


@bp_analysis.route("/test_fileread", methods=["POST"])
def test_fileread():
    """  Reading CSV file """
    config_builder = Tst2.test_select()
    main_params = FR.test_fileread()
    return render_template('test_select.html', **config_builder, **main_params)


@bp_analysis.route("/reset_option_t", methods=['Post'])
def reset_option_t():
    """  Routing for Treeview BBS  """
    return FR.reset_option_t()


@bp_analysis.route("/main")                      # Analysis メイン画面
def main():                                     # 現在使用していない
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
def filtermix():                                  # 現在使用していない
    """  Report BBS: Listed_Info_all   """
    main_params = Analysisparams.filtermix()
    return render_template("info_list.html", **main_params)


@bp_analysis.route("/analysis_query", methods=['GET','POST']) # クエリー1
def analysis_query():                           # 現在使用していない
    """  Report BBS: Listed_Info_list   """
    main_params = Mainparams.get_main_params()
    builder_params = Analysisparams10.querybuilder()
    main_params2 = Analysisparams10.analysis_query(builder_params)
    return render_template("ana_query.html", **main_params, **main_params2, **builder_params)


@bp_analysis.route("/analysis_query30", methods=['GET','POST']) # クエリー1
def analysis_query30():                             # 現在使用していない
    """  Report BBS: Listed_Info_list   """
    main_params = Mainparams.get_main_params()
    builder_params = Analysisparams30.querybuilder()
    main_params2 = Analysisparams30.analysis_query30(builder_params)
    return render_template("ana_query30.html", **main_params, **main_params2, **builder_params)
