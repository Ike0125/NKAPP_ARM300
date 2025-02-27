"""  nkapp.route.py  """
from flask import render_template, Blueprint
from nkapp.config import Mainparams
from nkapp.rpt.api_rpt01 import ApiRpt
from nkapp.rpt.rpt_fin01 import FinRpt


# Blueprintの設定
bp_nkapp = Blueprint('nkapp', __name__)


# ダッシュボード関連
@bp_nkapp.route('/')                        # メイン画面
def index():
    """  Routing for Main BBS  """
    main_params = Mainparams.get_main_params()  # DB用
    main_params2 = ApiRpt.config()              # Announcement初期設定
    main_params3 = ApiRpt.api_rpt01(mode=2)     # Announcementデータ
    main_params4 = FinRpt.fin_rpt06()           # Statement初期設定,データ
    # print(f"main_params2:{main_params2}")
    # print(f"main_params3:{main_params3}")
    # print(f"main_params4:{main_params4}")
    return render_template(
        'nkapp_main.html', **main_params, **main_params2, **main_params3, **main_params4
    )


@bp_nkapp.route('/setting')                 # 設定関連
def setting():
    """  Routing for Setting BBS  """
    return render_template('setting.html')


@bp_nkapp.route('/api')                     # API関連
def api():
    """  Routing for API BBS  """
    return render_template('api.html')


@bp_nkapp.route('/report')                  # レポート関連
def report():
    """  Routing for Report BBS  """
    return render_template('report.html')


@bp_nkapp.route('/analysis')                # 分析関連
def analysis():
    """  Routing for Analysis BBS  """
    return render_template('analysis.html')


# @bp_nkapp.route('/tests')                   # テスト関連
# def tests():
#    """  Routing for Test BBS  """
#    return render_template('test.html')
