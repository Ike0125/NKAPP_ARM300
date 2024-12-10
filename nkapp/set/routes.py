""" rpt/route.py """
from flask import render_template, Blueprint
from nkapp.config import Mainparams
from nkapp.set.daily_list import DBC
from nkapp.set.system_setting import Set
# from nkapp.rpt.report10 import Infoparams10
# from nkapp.rpt.report11 import Chartparams

#  Blueprintのインスタンス作成
bp_set = Blueprint("set", __name__, template_folder="templates")


@bp_set.route("/main")                      # Report メイン画面
def main():
    """  Routing for Report-Main BBS  """
    main_params = Mainparams.get_main_params()
    main_params2 = Set.config()
    return render_template("set_main.html", **main_params, **main_params2)
    # return render_template("set_main.html", **main_params)


@bp_set.route("/daily_printout")                      # Report メイン画面
def daily_printout():
    """  Routing for Report-Main BBS  """

    return DBC.daily_printout()
