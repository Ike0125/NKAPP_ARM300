"""  nkapp.route.py  """
#  from datetime import datetime
from flask import render_template, Blueprint
# from nkapp.config import Config

# Blueprintの設定

bp_nkapp = Blueprint('nkapp', __name__)

# ダッシュボード関連


@bp_nkapp.route('/')                        # メイン画面
def index():
    """  Routing for Main BBS  """
    return render_template('index.html')


# @bp_nkapp.route('/setting')                 # 設定関連
# def setting():
#    """  Routing for Setting BBS  """
#    return render_template('setting.html')


# @bp_nkapp.route('/api')                     # API関連
# def api():
#    """  Routing for API BBS  """
#    return render_template('api.html')


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
