""" api/route.py """
from flask import Blueprint, render_template
from nkapp.config import Mainparams
from nkapp.api.api_main import AP, APJQ                         # トークンデータ取得・保存/上場銘柄一覧データ取得
from nkapp.api.kabudb import retrieve_kabudb_request            # 株価データ取得（選択）
from nkapp.api.kabudball import retrieve_kabudball_request      # 株価データ取得（一括）


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


# @bp_api.route("/jq_main")
# def jq_main():
#    """
#    JQ管理画面をレンダリングし、トークンのタイムスタンプを表示する。
#    """
#    jq_params = APJQ.jq_main()
#
#    return render_template("jq_main.html", **jq_params)


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
    return retrieve_kabudb_request()


@bp_api.route("/kabudball_action", methods=["POST"])
def kabudball_action():
    """
    Kabudbリクエストを処理し、データを取得して保存する。
    """
    return retrieve_kabudball_request()
