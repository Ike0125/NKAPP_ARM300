"""  __init__.py  """
from flask import Flask
# from nkapp.tests.testdb import create_books_table
# from .models import create_sql_table
from .routes import bp_nkapp        # nkappのblueprint
from .rpt.routes import bp_rpt      # reportのblueprint
# from .api.routes import bp_api      # apiのblueprint
# from .tests.routes import bp_tests  # testsのblueprint
from .analysis.routes import bp_analysis  # testsのblueprint


def create_nkapp():
    """  nkapp initialization  """
    nkapp = Flask(__name__)
    nkapp.secret_key = 'arm200_secret_key'  #dropdownlist用
    # create_books_table()
    # テスト用DB,book作成
    # create_sql_table()
    # SQL_DB用接続、作成
    # Blueprint registration
    nkapp.register_blueprint(bp_nkapp, url_prefix='/nkapp')         # Main
    nkapp.register_blueprint(bp_rpt, url_prefix='/nkapp/rpt')       # Report
    nkapp.register_blueprint(bp_analysis, url_prefix='/nkapp/analysis')       # Report
    # nkapp.register_blueprint(bp_api, url_prefix='/nkapp/api')       # api
    # nkapp.register_blueprint(bp_tests, url_prefix='/nkapp/tests')   # tests

    return nkapp
