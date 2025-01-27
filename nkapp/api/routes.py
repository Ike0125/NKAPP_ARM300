""" api/route.py """
from flask import Blueprint, render_template
from flask import redirect, url_for
from nkapp.config import Mainparams
from nkapp.api.api_main import AP, APJQ                   # トークンデータ取得・保存/上場銘柄一覧データ取得
from nkapp.api.kabudb import retrieve_kabudb_request      # 株価データ取得（選択）
from nkapp.api.kabudball import JQDB                      # 株価データ取得（一括）
# from nkapp.api.kabudball_new import JQDB2               # 株価データ取得（一括）
from nkapp.api.kabudball3 import JQDB3                    # 株価データ取得（一括）
from nkapp.api.statements import JQST
from nkapp.api.announcement import JQAN

# Blueprintのインスタンスを作成し、API関連のルートを管理
bp_api = Blueprint("api", __name__, template_folder="templates")


@bp_api.route("/api_main")
def api_main():
    """
    API管理画面をレンダリングし、トークンのタイムスタンプを表示する。
    """
    main_params = Mainparams.get_main_params()
    ap_params = AP.config()

    return render_template("api_main.html", **main_params, **ap_params)


@bp_api.route("/token_action", methods=["POST"])
def token_action():
    """
    IDトークンを更新するためのアクションを処理する。
    """
    return APJQ.get_token_request()


@bp_api.route("/save_refresh_token", methods=["POST"])
def refresh_token_action():
    """
    新しいリフレッシュトークンを保存するためのアクションを処理する。
    """
    return APJQ.save_refresh_token()  # requestを引数として渡す

@bp_api.route("/listedinfo_action", methods=["POST"])
def listedinfo_action():
    """
    ListedInfoリクエストを処理し、データを取得して保存する。
    """
    return APJQ.listedinfo_request()

@bp_api.route("/kabudb_action", methods=["POST"])
def kabudb_action():
    """
    Kabudbリクエストを処理し、データを取得して保存する。
    """
    retrieve_kabudb_request(mode=1)

    return redirect(url_for("api.api_main"))


@bp_api.route("/kabudball_action", methods=["POST"])
def kabudball_action():
    """
    Kabudbリクエストを処理し、データを取得して保存する。
    """
    JQDB.retrieve_kabudball_request()
    JQDB.update_tradingcalendar()

    return redirect(url_for("api.api_main"))


@bp_api.route("/kabudball_action_new", methods=["POST"])
def kabudball_action_new():
    """
    Kabudbリクエストを処理し、データを取得して保存する。
    """
    JQDB3.retrieve_kabudball_request()
    JQDB.update_tradingcalendar()

    return redirect(url_for("api.api_main"))


@bp_api.route("/kabudball_update", methods=["POST"])
def kabudball_update():
    """
    Kabudbリクエストを処理し、データを取得して保存する。
    """
    JQDB3.retrieve_kabudball_request_update()
    JQDB.update_tradingcalendar()

    return redirect(url_for("api.api_main"))


@bp_api.route("/kabudball_update_date", methods=["POST"])
def kabudball_update_date():
    """
    Kabudbリクエストを処理し、データを取得して保存する。
    """
    JQDB3.kabudball_update_date(mode=1)
    JQDB.update_tradingcalendar()

    return redirect(url_for("api.api_main"))


@bp_api.route("/jqcalendar_update", methods=["POST"])
def jqcalendar_update():
    """
    Kabudbリクエストを処理し、データを取得して保存する。
    """
    APJQ.jqcalendar_update()

    return redirect(url_for("api.api_main"))


@bp_api.route("/get_statements", methods=["POST"])
def get_statements():
    """
    statementsリクエストを処理し、データを取得して保存する。
    """
    JQST.get_statements(mode=1)

    return redirect(url_for("api.api_main"))


@bp_api.route("/get_announcement", methods=["POST"])
def get_announcement():
    """
    annoucementリクエストを処理し、データを取得して保存する。
    """
    JQAN.get_announcement(mode=1)

    return redirect(url_for("api.api_main"))
