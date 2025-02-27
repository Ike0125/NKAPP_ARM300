""" rpt/route.py """
from flask import render_template, Blueprint
from flask import redirect, url_for
from nkapp.config import Mainparams
from nkapp.set.set_dbprint import DBC
from nkapp.set.system_setting import Set
from nkapp.set.set_database import SETDB
from nkapp.set.mockjq_main import MK
from nkapp.api.kabudball import JQDB
from nkapp.api.kabudball3 import JQDB3
from nkapp.api.kabudb import retrieve_kabudb_request
from nkapp.api.statements import JQST
from nkapp.set.set_print_statements import SETPR

#  Blueprintのインスタンス作成
bp_set = Blueprint("set", __name__, template_folder="templates")


@bp_set.route("/main")                      # System Setting メイン画面
def main():
    """  Routing for Report-Main BBS  """
    main_params = Mainparams.get_main_params()
    main_params2 = Set.config()
    mockparams = MK.config()
    # print(f"mockparams:{mockparams}")
    return render_template("set_main.html", **main_params, **main_params2, **mockparams)


@bp_set.route("/daily_printout", methods=['post'])            # Database Structure
def daily_printout():
    """  Database Management fRouting for Report-Main BBS  """

    return DBC.daily_printout()


@bp_set.route("/calendar_printout")            # Database Structure
def calendar_printout():
    """  Database Management fRouting for Report-Main BBS  """

    return DBC.calendar_printout()


@bp_set.route("/jq_calendar_printout")            # Database Structure
def jq_calendar_printout():
    """  Database Management fRouting for Report-Main BBS  """

    return DBC.jq_calendar_printout()


@bp_set.route("/update_tradingcalendar", methods=['post'])            # Database Structure
def update_tradingcalendar():
    """  Database Management fRouting for Report-Main BBS  """
    JQDB.update_tradingcalendar()
    return redirect(url_for("set.main"))


@bp_set.route("/deletedata", methods=['post'])  # Database Settings
def deletedata():
    """  Routing for Report-Main BBS  """

    return SETDB.deletedata()


@bp_set.route("/dailyall_deletedata", methods=['post'])  # Database Settings
def dailyall_deletedata():
    """  Routing for Report-Main BBS  """

    return SETDB.dailyall_deletedata()


@bp_set.route("/table_list")  # Database Settings
def table_list():
    """  Routing for Report-Main BBS  """

    return SETDB.table_list()


@bp_set.route("/mock_kabudb_action", methods=["POST"])
def mock_kabudb_action():
    """
    Kabudbリクエストを処理し、データを取得して保存する。
    """
    retrieve_kabudb_request(mode=1)

    return redirect(url_for("set.main"))


@bp_set.route("/mock_kabudball_action", methods=["POST"])
def mock_kabudball_action():
    """
    Kabudbリクエストを処理し、データを取得して保存する。
    """
    JQDB3.retrieve_kabudball_request(mode=9)

    return redirect(url_for("set.main"))


@bp_set.route("/mock_statements_action", methods=["POST"])
def mock_statements_action():
    """
    statementsリクエストのモックテスト。
    """
    JQST.get_statements(mode=9)

    return redirect(url_for("set.main"))


@bp_set.route("/set_print_statement1")
def set_print_statement1():
    """
    statementsのprint処理
    """

    return SETPR.set_print_statement1()


@bp_set.route("/set_print_statement2")
def set_print_statement2():
    """
    statementsのprint処理
    """
    SETPR.set_print_statement2()

    return redirect(url_for("set.main"))


@bp_set.route("/set_print_statement3")
def set_print_statement3():
    """
    statementsのprint処理
    """
    SETPR.set_print_statement3()

    return redirect(url_for("set.main"))


@bp_set.route("/set_print_statement4")
def set_print_statement4():
    """
    statementsのprint処理
    """
    SETPR.set_print_statement4()

    return redirect(url_for("set.main"))


@bp_set.route("/set_print_statement5")
def set_print_statement5():
    """
    statementsのprint処理
    """
    SETPR.set_print_statement5()

    return redirect(url_for("set.main"))
