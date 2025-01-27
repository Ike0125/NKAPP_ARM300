"""  __init__.py  """
from datetime import timedelta
from flask import Flask
from .routes import bp_nkapp        # nkappのblueprint
from .rpt.routes import bp_rpt      # reportのblueprint
from .api.routes import bp_api      # apiのblueprint
from .analysis.routes import bp_analysis  # testsのblueprint
from .set.routes import bp_set      # setのblueprint
# from nkapp.tests.testdb import create_books_table
# from .models import create_sql_table
# from .tests.routes import bp_tests  # testsのblueprint


def create_nkapp():
    """  nkapp initialization  """
    nkapp = Flask(__name__)
    # セッション用の秘密鍵を設定
    nkapp.secret_key = 'arm300_secret_key'  #dropdownlist用
    # セッションの永続性を有効化
    nkapp.config['SESSION_PERMANENT'] = True
    # セッションの有効期限を1週間に設定
    nkapp.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

    # テーブル作成
    # create_sql_table()
    # Blueprint registration
    nkapp.register_blueprint(bp_nkapp, url_prefix='/nkapp')               # Main
    nkapp.register_blueprint(bp_rpt, url_prefix='/nkapp/rpt')             # Report
    nkapp.register_blueprint(bp_analysis, url_prefix='/nkapp/analysis')   # Report
    nkapp.register_blueprint(bp_api, url_prefix='/nkapp/api')             # api
    nkapp.register_blueprint(bp_set, url_prefix='/nkapp/set')             # setting
    # nkapp.register_blueprint(bp_tests, url_prefix='/nkapp/tests')       # tests

    return nkapp
