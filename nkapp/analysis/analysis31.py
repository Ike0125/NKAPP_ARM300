"""  nkapp.analysis.testview.py  """
# import os
from decimal import Decimal
from math import ceil
from datetime import timedelta, datetime
import pandas as pd
from flask import request, session
from flask import redirect, url_for
from sqlalchemy import func, and_, case, literal
from sqlalchemy import select, desc, asc
from sqlalchemy.orm import aliased
# from sqlalchemy.engine.row import Row
from nkapp.config import Fileparams, TD
from nkapp.models import Session, Tl
from nkapp.rpt.models import VT
from .config import VALUE_MAP10, VALUE_MAP20, VALUE_MAP30
from .config import VALUE_MAP40, VALUE_MAP41, VALUE_MAP50
from .analysis20 import Ana


class A31:
    """Params"""
    @staticmethod
    def register_option():
        """Register Params for Save Option"""
        if request.method == "POST":
            # 既存の設定を読み込み
            ckbox511   = "ckbox511" in request.form
            ckbox512   = "ckbox512" in request.form
            ckbox521   = "ckbox521" in request.form
            ckbox531   = "ckbox531" in request.form
            data521    = request.form.get("data521", "")
            conf531    = request.form.get("conf531", "")
            print(f"ckxbox511: {ckbox511}")
            print(f"ckxbox512: {ckbox512}")
            reset_config = {
                "ckbox511" : ckbox511,
                "ckbox512" : ckbox512,
                "ckbox521" : ckbox521,
                "ckbox531" : ckbox531,
                "data521"  : data521,
                "conf531"  : conf531,
            }
            # print(f"config_macd: {config_macd}")
            config_data = Ana.load_config("ana_config.json")
            config_data.update(reset_config)
            Ana.save_config("ana_config.json",config_data)
        else:
            print("Register Error/register_option/47")
        return redirect(url_for('analysis.query_builder2'))


    @staticmethod
    def reset_option():
        """Reset Params for Save Option"""
        if request.method == "POST":
            # 初期設定値を保存
            reset_config = {
                "ckbox511"    : False,
                "ckbox512"    : False,
                "ckbox521"    : False,
                "ckbox531"    : False,
                "data521"     : "nkapp_df",
                "conf531"     : "nkapp_conf",
                "subject541"  : "",
                "comment541"  : ""
            }
            # print(f"config_macd: {config_macd}")
            config_data = Ana.load_config("ana_config.json")
            config_data.update(reset_config)
            Ana.save_config("ana_config.json",config_data)
        else:
            print("Reset Error/reset_option/68")
        return redirect(url_for('analysis.query_builder2'))


    @staticmethod
    def errormessage(errormsg):
        """Error messages for BBS"""
        params = A31.query_builder2()
        lists = []
        counts = 0
        total_pages = 0
        per_page = 20
        page = 1
        initial = 1  # initial:1
        params.update(
            {
                "db_data": lists,
                "total_records": counts,
                "total_pages": total_pages,
                "page": page,
                "per_page": per_page,
                "initial": initial,
                "error" : errormsg
            }
        )
        return params

    @staticmethod
    def config():
        """Initial Params for Analysisparames"""
        return {
            "db_data": [],
            "total_records": 0,
            "total_pages": 0,
            "page": 1,
            "per_page": 15,
            "initial": 1,
        }


    @staticmethod
    def query_builder2():
        """for display_settings"""
        ana_config = Ana.load_config("ana_config.json")
        errormsg =""
        column_name = ""
        comment102 = ana_config.get("comment102", "式もしくは設定したパラメータ")
        paramname121 = ana_config.get("paramname121", "Param-A1")  # Param-A1
        paramname122 = ana_config.get("paramname122", "Param-A2")  # Param-A2
        paramname221 = ana_config.get("paramname221", "Param-B1")  # Param-B1
        paramname222 = ana_config.get("paramname222", "Param-B2")  # Param-B2
        subject123 = ana_config.get("subject123", "A123")
        subject124 = ana_config.get("subject124", "A124")
        subject125 = ana_config.get("subject125", "A125")
        comment123 = ana_config.get("comment123", "A123_comment")
        comment124 = ana_config.get("comment124", "A124_comment")
        comment125 = ana_config.get("comment125", "A125_comment")
        comment202 = ana_config.get("comment202", "固定値")
        subject223 = ana_config.get("subject223", "B223")
        subject224 = ana_config.get("subject224", "B224")
        subject225 = ana_config.get("subject225", "B225")
        comment223 = ana_config.get("comment223", "B223_comment")
        comment224 = ana_config.get("comment224", "B224_comment")
        comment225 = ana_config.get("comment225", "B225_comment")
        comment502 = ana_config.get("comment502", "E502_comment")
        data521    = "nkapp_df"
        conf531    = "nkapp_conf"
        subject541 = ana_config.get("subject541", "E541")
        comment541 = ana_config.get("comment541", "E541_comment")

        if request.method == "POST":
            # 掲示板から選択値を取得し、セッションに保存
            # Selection
            dropdown_value = request.form.get("dropdown001")
            if dropdown_value is not None:
                session["condition001"] = dropdown_value
            # Gropu A
            session["window101"] = request.form.get("dropdown101", 5)
            session["gapquery111"] = request.form.get("gap111", 0)
            session["paramquery121"] = request.form.get("param121", 1)
            session["paramquery122"] = request.form.get("param122", 1)
            # Operator
            session["ope_select131"] = request.form.get("dropdown131", ">")
            # Group B
            session["window201"] = request.form.get("dropdown201", 20)
            session["gapquery211"] = request.form.get("gap211", 0)
            session["paramquery221"] = request.form.get("param221", 1)
            session["paramquery222"] = request.form.get("param222", 1)
            # Group E
            session["sort_select501"] = request.form.get("dropdown501", "02")
            #session["ckbox511"]   = "ckbox511" in request.form
            #session["ckbox512"]   = "ckbox512" in request.form
            #session["ckbox521"]   = "ckbox521" in request.form
            #session["ckbox531"]   = "ckbox531" in request.form
            #session["data521"] = request.form.get("data521", "")
            #session["conf531"] = request.form.get("conf531", "")
        else:
            # 保存したデータの読み込み
            session["condition001"] = ana_config.get("condition001")
            session["window101"] = ana_config.get("window101", 5)
            session["gapquery111"] = ana_config.get("gapquery111", 0)
            session["paramquery121"] = ana_config.get("paramquery121", 1)
            session["paramquery122"] = ana_config.get("paramquery122", 1)
            session["ope_select131"] = ana_config.get("ope_select131", ">")
            session["window201"] = ana_config.get("window201", 20)
            session["gapquery211"] = ana_config.get("gapquery211", 0)
            session["paramquery221"] = ana_config.get("paramquery221", 1)
            session["paramquery222"] = ana_config.get("paramquery222", 1)
            session["sort_select501"] = ana_config.get("sort_select501", "02")

        # セッションに保存したデータの読み込み
        condition001 = session.get("condition001", None)
        if condition001     == "0501":
            column_name     = "乖離率 %"
            paramname221    = "定数(%)"
            comment202      = "固定値"
            comment502      = f"{column_name}"
        elif condition001   == "0502":
            window_period   = session["window201"]
            column_name     = f"dev_{window_period}%"
            comment502      = f"{column_name}"
        elif condition001   == "0503":
            window_period   = session["window201"]
            column_name     = f"dev_{window_period}%"
            comment502      = f"{column_name}"
        elif condition001   == "0504":
            column_name     = "乖離率 %"
            comment202      = "daygap=MA"
            comment502      = "deviation rate"
        elif condition001   == "0511":
            column_name     = "RSI %"
            paramname221    = "RSI %"
            rsi_period      = ana_config.get("rsi_period_value", None)
            comment102      = f"RSI={rsi_period}"
            comment502      = f"{column_name}"
        elif condition001   == "0521":
            column_name     = "histgram"
            macd_short      = ana_config.get("macd_short_value", 7)
            macd_long       = ana_config.get("macd_long_value", 14)
            # macd_signal     = ana_config.get("macd_signal_value", 9)
            comment102      = "MACD-GC"
            subject123      = "Short"
            subject223      = "Long"
            comment123      = f"EMA={macd_short}"
            comment223      = f"EMA={macd_long}"
            comment502      = "histgram"
        elif condition001   == "0599":
            column_name     = "Close"
            comment102      = "No fiter"
            comment202      = "No fiter"
            comment502      = "Code"

        else:
            errormsg = ">>Params Error/query_builder2/174<<"
        # Group A
        window101      = int(session.get("window101", 5))
        gapquery111    = int(session.get("gapquery111", 0))
        paramquery121  = session.get("paramquery121", 1)
        paramquery122  = session.get("paramquery122", 1)
        # Operator
        ope_select131  = session.get("ope_select131", "")
        # Group B
        window201      = int(session.get("window201", 20))
        gapquery211    = int(session.get("gapquery211", 0))
        paramquery221  = session.get("paramquery221", 1)
        paramquery222  = session.get("paramquery222", 1)
        sort_select501 = session.get("sort_select501", "")

        ckbox511     = ana_config.get("ckbox511",False)
        ckbox512     = ana_config.get("ckbox512",False)
        ckbox521     = ana_config.get("ckbox521",False)
        ckbox531     = ana_config.get("ckbox531",False)
        data521      = ana_config.get("data521", "nkapp_df.csv")
        conf531      = ana_config.get("conf531", "nkapp_conf.json")
        file_path      = ana_config.get("file_path","")
        print(f"ckxbox511-2: {ckbox511}")
        # ckbox512       = session.get("ckbox512",False)
        # ckbox521       = session.get("ckbox521",False)
        # ckbox531       = session.get("ckbox531",False)
        # data521        = session.get("data521", "")
        # conf531        = session.get("conf531", "")

        # 掲示板へのデータまとめ
        builder_params = {
            # Market/Calculation setting
            "marketcategory" : ana_config.get("marketcategory", None),
            "categorydetail": ana_config.get("categorydetail", None),
            "marketcode": ana_config.get("marketcode", None),  # 市場区分コード
            "selected10": ana_config.get("selected10", None),  # 市場区分
            "ma_value01": ana_config.get("ma_value01", None),  # 移動平均１
            "ma_value02": ana_config.get("ma_value02", None),  # 移動平均２
            "ma_value03": ana_config.get("ma_value03", None),  # 移動平均３
            "ma_value04": ana_config.get("ma_value04", None),  # 移動平均４
            "ma_value05": ana_config.get("ma_value05", None),  # 移動平均５
            "rsi_period_value": ana_config.get("rsi_period_value", None),  # RSI期間
            "macd_short_value": ana_config.get("macd_short_value", 7),  # MACDshort
            "macd_long_value": ana_config.get("macd_long_value", 14),  # MACDlong
            "macd_signal_value": ana_config.get(
                "macd_signal_value", 9
            ),  # MACDsignal
            # Query Setting
            "daygapname111": "何日前",
            "daygapname211": "何日前",
            "VALUE_MAP10": VALUE_MAP10,  # 市場区分コードリスト
            "VALUE_MAP20": VALUE_MAP20,  # 計算方法リスト
            "VALUE_MAP30": VALUE_MAP30,  # 演算子リスト
            "VALUE_MAP40": VALUE_MAP40,  # ソート順リスト
            "VALUE_MAP41": VALUE_MAP41,  # KEY Columnリスト
            "VALUE_MAP50": VALUE_MAP50,  # Query Conditionリスト
            # "condition"     : condition,
            "condition001": condition001,
            "window101": window101,
            "gapquery111": gapquery111,
            "paramquery121": paramquery121,
            "paramquery122": paramquery122,
            "ope_select131": ope_select131,
            "window201": window201,
            "gapquery211": gapquery211,
            "paramquery221": paramquery221,
            "paramquery222": paramquery222,
            "sort_select501": sort_select501,
            # BBS setteing
            "comment102": comment102,
            "paramname121": paramname121,  # Param-A1
            "paramname122": paramname122,  # Param-A2
            "paramname221": paramname221,  # Param-B1
            "paramname222": paramname222,  # Param-B2
            "subject123"  : subject123,
            "subject124"  : subject124,
            "subject125"  : subject125,
            "comment123"  : comment123,
            "comment124"  : comment124,
            "comment125"  : comment125,
            "comment202"  : comment202,
            "subject223"  : subject223,
            "subject224"  : subject224,
            "subject225"  : subject225,
            "comment223"  : comment223,
            "comment224"  : comment224,
            "comment225"  : comment225,
            "comment502"  : comment502,
            "column_name" : column_name,
            "ckbox511"    : ckbox511,
            "ckbox512"    : ckbox512,
            "ckbox521"    : ckbox521,
            "ckbox531"    : ckbox531,
            "data521"     : data521,
            "conf531"     : conf531,
            "subject541"  : subject541,
            "comment541"  : comment541,
            # Base BBS setting
            "head_title": "Analysis: Query_Builder",
            "header_title": "検索",
            "endpoint": "analysis.analysis_query31",
            "return_url": "analysis.analysis_query31",
            "return_name": "To analysis31",
            "home_url": "nkapp.index",
            "marketcode_query": "",
            "companyname_query": "",
            "file_path": file_path,
            "error" : errormsg
        }
        # print(f"builder_params: {builder_params}")
        # データの保存
        config_formula = Ana.load_config("ana_config.json")
        config_formula.update(builder_params)
        Ana.save_config("ana_config.json", config_formula)

        return builder_params

    @staticmethod
    def analysis_query31(builder_params):
        """Params for listed_info"""
        params = builder_params
        config31 = A31.config()
        start_time = datetime.now()
        lists = []
        subquery    = ""
        errormsg    = ""
        subject541  = ""
        comment541  = ""
        # base_name   = ""
        stamp = True
        index = False
        ana_config = Ana.load_config("ana_config.json")
        per_page = config31["per_page"]
        if request.method == "POST":
            page = 1
        else:
            page = request.args.get("page", 1, type=int)
        with Session() as session:  # セッション開始
            if request.method != "POST" and "page" not in request.args:
                counts = 0
                total_pages = 0
                page = 0
                initial = 1  # initial:1
            else:
                condition001 = ana_config.get("condition001")
                if condition001 == "0501":
                    base_query = A31.ana_query_madev()
                elif condition001 == "0502":
                    gcdc = "gc"
                    base_query = A31.ana_query_magcdc(gcdc)
                elif condition001 == "0503":
                    gcdc = "dc"
                    base_query = A31.ana_query_magcdc(gcdc)
                elif condition001 == "0504":
                    base_query = A31.ana_query_mamt()
                elif condition001 == "0511":
                    base_query = A31.ana_query_rsi2()
                elif condition001 == "0521":
                    macd_params = A31.ana_query_macd_gcdc(page)
                    base_query = macd_params["lists"]
                elif condition001 == "0599":
                    base_query = A31.ana_query_mkt()
                else:
                    errormsg = ">>Query Error/analysis_query31/313<"
                    params = A31.errormessage(errormsg)
                    print(f"Error Message: {errormsg}")
                    return params
                if condition001 == "0521":
                    macd_params = A31.ana_query_macd_gcdc(page)
                    lists = base_query                          #queried data
                    # print(f"lists: {lists}")
                    counts = macd_params["counts"]              # total counts
                    total_pages = macd_params["total_pages"]    # total_pages
                    page = macd_params["page"]                  # Current Page Number
                    initial = 0
                else:
                    # 総レコード数を取得
                    # pylint: disable=not-callable
                    count_query = select(func.count()).select_from(base_query.subquery())
                    # base_queryをサブクエリとし、その結果の行数をカウント
                    counts = session.execute(count_query).scalar()
                    # オフセット計算
                    # print(f"counts: {counts}")
                    offset = (page - 1) * per_page
                    # print(f"offset: {offset}")
                    # ページネーションをオフセット値と１ページ当りのレコード数より設定
                    paginated_query = base_query.offset(offset).limit(per_page)
                    # sqlalchemyクエリを実行し、全レコードを取得
                    lists = session.execute(paginated_query).fetchall()
                    # トータルページ数の計算
                    total_pages = ceil(counts / per_page)
                    initial = 0
                    # print(f"lists: {lists}")

        # 掲示板のパラメータ
        end_time = datetime.now()
        query_time = end_time - start_time
        params.update(
            {
                "db_data"    : lists,
                "total_records": counts,
                "total_pages": total_pages,
                "page"       : page,
                "per_page"   : per_page,
                "initial"    : initial,
                "query_time" : query_time,
                "error"      : errormsg,
                "subject541" : subject541,
                "comment541" : comment541
            }
        )
        # 検索データ保存
        ckbox511 =ana_config.get("ckbox511",False)
        ckbox512 =ana_config.get("ckbox512",False)
        ckbox521 =ana_config.get("ckbox521",False)
        ckbox531 =ana_config.get("ckbox531",False)
        conf531  =ana_config.get("conf531",False)
        base_name =ana_config.get("data521",False)

        if ckbox511 and ckbox521 and page == 1:
            #　データ保存プロセス
            subquery = base_query.subquery()
            aliased_subquery = aliased(subquery)
            #Timestampの入力判断
            if ckbox512 is True:
                stamp = True
            else:
                stamp = False
            # Data取得
            data = session.query(aliased_subquery).all()
            # Data保存
            Fileparams.save_csv(data, base_name, index ,stamp)
            # メッセージ読み出し
            result = Fileparams.save_csv(data, base_name, index ,stamp)
            subject541 = result["message"]
            errormsg = result["errormsg"]

        # configデータ保存
        if ckbox511 and ckbox531 and page == 1:
            #Timestampの入力判断
            if ckbox512 is True:
                stamp = True
            else:
                stamp = False
            config_data = Ana.load_config("ana_config.json")
            config_name = conf531
            Fileparams.save_config(config_data, config_name , stamp)
            # メッセージ読み出し
            result_config = Fileparams.save_config(config_data, config_name , stamp)
            comment541 = result_config["message"]
            errormsg = result_config["errormsg"]
        params.update(
            {
                "error"      : errormsg,
                "comment541" : comment541
            }
        )
        return params


    @staticmethod
    def ana_query_mkt():
        """querybuilder for moving average"""
        df_custom_data = {}
        marketcode_condition = ""
        status      = ""
        errormsg    = ""
        file_path   = ""

        ana_config = Ana.load_config("ana_config.json")
        marketcategory       = ana_config.get("marketcategory")
        marketcode_query     = ana_config.get("marketcode")
        sector17code_query   = ana_config.get('sector17code')
        sector33code_query   = ana_config.get('sector33code')
        scalecategory_query  = ana_config.get('scalecategory')
        customcategory_query  = ana_config.get('customcategory')
        ana_sort = ana_config.get("sort_select501")
        day_gap = 0
        key_column = "code"

        with Session() as session:
            # 取引カレンダーから最新の取引日を取得
            last_trade_date = session.query(
                func.max(Tl.daily_table.c.date)
            ).scalar()

            # 取引日番号を使って取引日を計算
            t_date = last_trade_date
            end_day_no = TD.date_tno(t_date) - day_gap

            # end_day_no = session.query(
            #    Tl.t_calendar.c.trade_date_no
            # ).filter(Tl.t_calendar.c.tradingdate == last_trade_date).scalar() - day_gap

            # 取引日カレンダーから具体的な取引日を取得
            t_no = end_day_no
            end_day = TD.tno_tdate(t_no)

            #end_day = session.query(
            #    Tl.t_calendar.c.tradingdate
            #).filter(Tl.t_calendar.c.trade_date_no == end_day_no).scalar()

            print(f"last_trade_date : {last_trade_date}")
            print(f"end_day_no     : {end_day_no}")
            print(f"trading_date: {end_day}")
            print(type(end_day))
            print(f"day_gap     : {day_gap}")

            if marketcategory == "Market Code":
                marketcode_condition = (Tl.company.marketcode == marketcode_query)
            elif marketcategory == "Sector17Code":
                marketcode_condition = (Tl.company.sector17code == sector17code_query)
            elif marketcategory == "Sector33Code":
                marketcode_condition = (Tl.company.sector33code == sector33code_query)
            elif marketcategory == "Scale Category":
                marketcode_condition = (Tl.company.scalecategory.contains(scalecategory_query))
            elif marketcategory == "Custom Category":
                if customcategory_query == "1001":
                    custom_a    = Fileparams.fileread_csv()
                    status      = custom_a.get("status","")
                    df_custom_data = custom_a.get("data",{})
                    errormsg    = custom_a.get("errormsg","")
                    print(f"custom_data: {df_custom_data}")
                    print(f"status: {status}")
                    print(f"file_path: {file_path}")
                    print(f"Error Message: {errormsg}")
                    custom_code = df_custom_data["code"].astype(str).tolist()  # 数値を文字列に変換
                    marketcode_condition = Tl.company.code.in_(custom_code)  # SQLAlchemyのin_演算子を使用
                else:
                    params={
                        status   : "Notice",
                        errormsg : ">>Not provided yet<<"
                    }
                    return params
            elif marketcategory == "All":
                marketcode_condition = True
            else:
                errormsg = ">>Query Error/ana_querymkt/444<<"
                params = A31.errormessage(errormsg)
                print(f"Error Message: {errormsg}")
                return params
            base_query = (
                select(
                    Tl.company.code,
                    Tl.company.companyname,
                    Tl.daily.adjustmentclose,
                    Tl.daily.date,
                    Tl.company.marketcode,
                    Tl.company.sector17code,
                    Tl.company.sector33code,
                    Tl.company.scalecategory
                )
                .join(Tl.company, Tl.company.code == Tl.daily.code)
                .where(marketcode_condition)
                .where(Tl.daily.date == end_day)
                .order_by(A31.get_sort_order(
                    ana_sort, getattr(Tl.company, key_column)))
            )
        # print(f"base_query: {base_query}")
        return base_query


    @staticmethod
    def ana_query_macd_gcdc(page):
        """MACDのゴールデンクロスで銘柄を抽出（データ検証用に結果を保存）"""
        ana_config = Ana.load_config("ana_config.json")
        config31 = A31.config()
        per_page = config31["per_page"]
        # marketcode_query = ana_config.get("marketcode")
        # ana_sort = ana_config.get("sort_select501")
        day_gap_A = 0
        key_column = "histogram"

        short_window = int(ana_config.get("macd_short_value"))   # 短期EMA期間
        long_window = int(ana_config.get("macd_long_value"))     # 長期EMA期間
        signal_window = int(ana_config.get("macd_signal_value"))  # シグナルライン期間

        with Session() as session:
            # 最新の取引日を取得
            last_trade_date = session.query(
                func.max(Tl.t_calendar.c.tradingdate)
            ).scalar()

            # 取引日番号を計算
            end_day_A_no = session.query(
                Tl.t_calendar.c.trade_date_no
            ).filter(Tl.t_calendar.c.tradingdate == last_trade_date).scalar() - day_gap_A

            # 必要なデータ期間を計算（十分な過去データを取得）
            start_day_no = end_day_A_no -((long_window*2) + signal_window)

            # 実際の取引日を取得
            end_day_A = session.query(
                Tl.t_calendar.c.tradingdate
            ).filter(Tl.t_calendar.c.trade_date_no == end_day_A_no).scalar()

            start_day = session.query(
                Tl.t_calendar.c.tradingdate
            ).filter(Tl.t_calendar.c.trade_date_no == start_day_no).scalar()

            print(f"last_trade_date : {last_trade_date}")
            print(f"end_day_A_no    : {end_day_A_no}")
            print(f"start_day_no    : {start_day_no}")
            print(f"end_day_A       : {end_day_A}")
            print(f"start_day       : {start_day}")

            # marketcodeの条件を設定
            subquery = A31.ana_query_mkt().subquery()
            aliased_subquery = aliased(subquery)

            # marketcode_condition = case(
            #    (literal(marketcode_query) == "0100", True),
            #    else_=Tl.company.marketcode == marketcode_query,
            #)

            # 銘柄コードと会社名を取得
            companies = session.execute(
                select(
                    aliased_subquery.c.code,
                    Tl.company.code,
                    Tl.company.companyname
                ).join(aliased_subquery, aliased_subquery.c.code == Tl.company.code)
            ).fetchall()

            # companies = session.execute(
            #    select(
            #        Tl.company.code,
            #        Tl.company.companyname
            #    ).where(marketcode_condition)
            #).fetchall()

            # 銘柄コードのリストを作成
            codes = [company.code for company in companies]

            # データを取得
            price_data = session.execute(
                select(
                    Tl.daily.code,
                    Tl.daily.date,
                    Tl.daily.adjustmentclose
                ).where(
                    and_(
                        Tl.daily.code.in_(codes),
                        Tl.daily.date >= start_day,
                        Tl.daily.date <= end_day_A
                    )
                )
            ).fetchall()

            # データをDataFrameに変換
            df = pd.DataFrame(price_data, columns=['code', 'date', 'adjustmentclose'])

            if df.empty:
                print("データが取得できませんでした。")
                return None

            # 日付でソート
            df.sort_values(by=['code', 'date'], inplace=True)

            # 結果を保存するリスト
            results_list = []       # for Analysis
            lists        = []       # for BBS
            # 銘柄ごとに処理
            grouped = df.groupby('code')

            for code, group in grouped:
                # 必要なデータが揃っているか確認
                if len(group) < long_window + signal_window:
                    continue  # データが足りない場合はスキップ

                # MACDを計算
                macd_line, signal_line, histogram = VT.calculate_macd(group, short_window, long_window, signal_window)

                group = group.assign(
                    macd_line=macd_line.values,
                    signal_line=signal_line.values,
                    histogram=histogram.values
                )

                # ゴールデンクロスを検出
                group['macd_line_prev'] = group['macd_line'].shift(1)
                group['signal_line_prev'] = group['signal_line'].shift(1)

                latest_data = group[group['date'] == end_day_A]

                if latest_data.empty:
                    continue  # 最新の日付のデータがない場合はスキップ

                latest_row = latest_data.iloc[0]

                if pd.notnull(latest_row['macd_line_prev']) and pd.notnull(latest_row['signal_line_prev']):
                    if latest_row['macd_line_prev'] < latest_row['signal_line_prev'] and latest_row['macd_line'] >= latest_row['signal_line']:
                        # ゴールデンクロスが発生
                        company_name = next((company.companyname for company in companies if company.code == code), None)
                        results_list.append({
                            'code': code,
                            'companyname': company_name,
                            'macd_line': latest_row['macd_line'],
                            'signal_line': latest_row['signal_line'],
                            'macd_line_prev': latest_row['macd_line_prev'],
                            'signal_line_prev': latest_row['signal_line_prev'],
                            'date': latest_row['date'],
                            'histogram': latest_row['histogram'],
                            'adjustmentclose': latest_row['adjustmentclose']
                        })
                        lists.append((
                            code, company_name,
                            round(Decimal(latest_row['histogram']),2)
                        ))
            # 結果をDataFrameに変換
            results_df = pd.DataFrame(results_list)

            if results_df.empty:
                print("ゴールデンクロスが検出されませんでした。")
                return None

            # ソート（必要に応じてソート条件を設定）
            results_df.sort_values(by=key_column, ascending=False, inplace=True)
            # ページング処理
            total_counts = len(results_df)
            total_pages = (total_counts + per_page - 1) // per_page
            offset = (page - 1) * per_page
            paged_results = lists[offset:offset + per_page]
            macd_params={
            "lists": paged_results,
            "counts": total_counts,
            "total_pages": total_pages,
            "page": page,
            "per_page": per_page,
            }
            return macd_params



    @staticmethod
    def ana_query_ma():
        """querybuilder for moving average"""
        ana_config = Ana.load_config("ana_config.json")
        marketcode_query = ana_config.get("marketcode")
        operator = ana_config.get("ope_select130")
        ana_sort = ana_config.get("sort_select140")
        window = int(ana_config.get("window_201"))
        day_gap = int(ana_config.get("gapquery101"), 0)
        ana_param32 = float(ana_config.get("paramquery103"))
        key_column = "deviation_rate"
        print(f"marketcode_query: {marketcode_query}")
        print(f"operator: {operator}")
        print(f"ana_sort: {ana_sort}")
        print(f"window: {window}")
        print(f"day_gap: {day_gap}")
        print(f"ana_param32: {ana_param32}")
        with Session() as session:
            last_update = session.query(func.max(Tl.daily_table.c.date)).scalar()
            end_day = last_update - timedelta(days=day_gap)
            start_day = end_day - timedelta(days=window * 2)
            # marketcodeの条件を動的に設定
            marketcode_condition = case(
                (literal(marketcode_query) == "0100", True),  # "0100"の場合は常にTrue
                else_=Tl.company.marketcode == marketcode_query,  # それ以外は通常の条件
            )

            subquery = (
                select(
                    Tl.company.code,
                    Tl.company.companyname,
                    Tl.company.marketcode,
                )
                .where(marketcode_condition)
                .subquery()
            )
        # print(f"subquery: {subquery}")

        subquery2 = (
            select(
                Tl.daily.code,
                Tl.daily.date,
                Tl.daily.adjustmentclose,
                VT.moving_average_deviation(window)[0].label(
                    f"ma_{window}"
                ),  # 20日移動平均を計算
                VT.moving_average_deviation(window)[1].label("deviation_rate"),
            )
            .where(and_(Tl.daily.date >= start_day, Tl.daily.date <= end_day))
            .subquery()
        )
        # print(f"subquery2: {subquery2}")

        base_query = (
            select(subquery.c.code, subquery.c.companyname, subquery2.c.deviation_rate)
            .join(subquery2, subquery.c.code == subquery2.c.code)
            .where(
                subquery2.c.adjustmentclose.op(operator)(
                    subquery2.c[f"ma_{window}"] * ana_param32
                )
            )
            .where(subquery2.c.date == end_day)
            .group_by(
                subquery.c.code, subquery.c.companyname, subquery2.c.deviation_rate
            )
            .order_by(A31.get_sort_order(ana_sort, getattr(subquery2.c, key_column)))
        )
        # print(f"base_query: {base_query}")
        return base_query


    @staticmethod
    def ana_query_madev():
        """querybuilder for moving average"""
        ana_config = Ana.load_config("ana_config.json")
        # marketcode_query = ana_config.get("marketcode")
        operator = ana_config.get("ope_select131")
        ana_sort = ana_config.get("sort_select501")
        window = int(ana_config.get("window101"))
        day_gap = int(ana_config.get("gapquery111"))
        ana_param32 = float(ana_config.get("paramquery221"))
        key_column = "deviation_rate"
        with Session() as session:
            last_trade_date = session.query(func.max(Tl.daily_table.c.date)).scalar()

            t_date = last_trade_date
            end_day_no = TD.date_tno(t_date) - day_gap

            t_no = end_day_no
            end_day = TD.tno_tdate(t_no)

            start_day_no = end_day_no-(window *2)
            t_no = start_day_no
            start_day = TD.tno_tdate(t_no)
            # end_day = last_update - timedelta(days=day_gap)
            # start_day = end_day - timedelta(days=window * 2)
            print(f"last_trade_date : {last_trade_date}")
            print(f"end_day_no      : {end_day_no}")
            print(f"end_day         : {end_day}")
            print(f"start_day       : {start_day}")
            print(f"day_gap         : {day_gap}")
            print(f"window          : {window}")

            subquery = A31.ana_query_mkt().subquery()
            aliased_subquery = aliased(subquery)

            print(f"type of subquery : {type(subquery)}")
            print(f"culumn keys of subquery : {subquery.columns.keys()}")

            subquery2 = (
                select(
                    aliased_subquery.c.code,
                    Tl.daily.date,
                    Tl.daily.adjustmentclose,
                    VT.moving_average_deviation(window)[0].label(f"ma_{window}"),
                    VT.moving_average_deviation(window)[1].label("deviation_rate"),
                )
                .join(aliased_subquery, aliased_subquery.c.code == Tl.daily.code)
                .where(and_(Tl.daily.date >= start_day, Tl.daily.date <= end_day))
                .subquery()
            )

            # marketcodeの条件を動的に設定
            #marketcode_condition = case(
            #    (literal(marketcode_query) == "0100", True),  # "0100"の場合は常にTrue
            #    else_=Tl.company.marketcode == marketcode_query,  # それ以外は通常の条件
            #)

            #subquery = (
            #    select(
            #        Tl.company.code,
            #        Tl.company.companyname,
            #        Tl.company.marketcode,
            #    )
            #    .where(marketcode_condition)
            #    .subquery()
            #)
        # print(f"subquery: {subquery}")

        #subquery2 = (
        #    select(
        #        Tl.daily.code,
        #        Tl.daily.date,
        #        Tl.daily.adjustmentclose,
        #        VT.moving_average_deviation(window)[0].label(
        #            f"ma_{window}"
        #        ),  # 20日移動平均を計算
        #        VT.moving_average_deviation(window)[1].label("deviation_rate"),
        #    )
        #    .where(and_(Tl.daily.date >= start_day, Tl.daily.date <= end_day))
        #    .subquery()
        #)
        # print(f"subquery2: {subquery2}")

        base_query = (
            select(subquery.c.code, subquery.c.companyname, subquery2.c.deviation_rate)
            .join(subquery2, subquery.c.code == subquery2.c.code)
            .where(
                subquery2.c.adjustmentclose.op(operator)(
                    subquery2.c[f"ma_{window}"] * (1 + ana_param32 / 100)
                )
            )
            .where(subquery2.c.date == end_day)
            .group_by(
                subquery.c.code, subquery.c.companyname, subquery2.c.deviation_rate
            )
            .order_by(A31.get_sort_order(ana_sort, getattr(subquery2.c, key_column)))
        )
        # print(f"base_query: {base_query}")
        return base_query


    @staticmethod
    def ana_query_macd():
        """Optimized and corrected query builder for MACD."""
        # 初期設定
        ana_config = Ana.load_config("ana_config.json")
        marketcode_query = ana_config.get("marketcode")
        ana_sort = ana_config.get("sort_select140")
        day_gap = int(ana_config.get("gapquery101"))
        short_window = int(ana_config.get("macd_short_value"))
        long_window = int(ana_config.get("macd_long_value"))
        signal_window = int(ana_config.get("macd_signal_value"))
        print(f"marketcode_query: {marketcode_query}")
        print(f"ana_sort: {ana_sort}")
        print(f"day_gap: {day_gap}")
        print(f"short_window: {short_window}")
        print(f"long_window: {long_window}")
        print(f"signal_window: {signal_window}")

        with Session() as session:
            # データ取得期間計算
            last_update = session.query(func.max(Tl.daily_table.c.date)).scalar()
            end_day = last_update - timedelta(days=day_gap)
            start_day = end_day - timedelta(days=long_window * 2)  # 必要な期間をカバー

            print(f"End day for analysis: {end_day}")
            print(f"start day: {start_day}")

            # marketcodeの条件設定
            if marketcode_query == "0100":
                marketcode_condition = True  # 全市場対象
            else:
                marketcode_condition = Tl.company.marketcode == marketcode_query

            # Tl.companyとTl.dailyを結合し、必要なデータを取得
            base_query = (
                select(
                    Tl.daily.code,
                    Tl.company.companyname,
                    Tl.daily.date,
                    Tl.daily.adjustmentclose,
                )
                .join(Tl.company, Tl.company.code == Tl.daily.code)
                .where(
                    marketcode_condition,
                    Tl.daily.date >= start_day,
                    Tl.daily.date <= end_day,
                )
                .subquery()
            )

            # Fetch data and calculate MACD
            data_df = pd.read_sql(base_query, session.bind)
            macd_line, signal_line, histogram = VT.calculate_macd(
                data_df, short_window, long_window, signal_window
            )

            data_df["macd"] = macd_line
            data_df["signal"] = signal_line
            data_df["histogram"] = histogram

            # 最終的なクエリ
            final_query = select(
                base_query.c.code,
                base_query.c.companyname,
                base_query.c.date,
                data_df["macd"].label("macd"),
                data_df["signal"].label("signal"),
                data_df["histogram"].label("histogram"),
            ).subquery()

            # フィルタリングとソート
            result_query = (
                select(
                    final_query.c.code,
                    final_query.c.companyname,
                    final_query.c.macd,
                    final_query.c.signal,
                    final_query.c.histogram,
                )
                .where(final_query.c.date == end_day)
                .order_by(A31.get_sort_order(ana_sort, final_query.c.histogram))
            )
        return result_query


    @staticmethod
    def ana_query_rsi2():
        """Optimized and corrected query builder for RSI."""
        ana_config = Ana.load_config("ana_config.json")
        # marketcode_query = ana_config.get("marketcode")
        operator = ana_config.get("ope_select131")
        ana_sort = ana_config.get("sort_select501")
        window = int(ana_config.get("window101"))
        day_gap = int(ana_config.get("gapquery111", 0))
        ana_param32 = float(ana_config.get("paramquery221"))

        with Session() as session:
            last_trade_date = session.query(func.max(Tl.daily_table.c.date)).scalar()
            end_day_no = TD.date_tno(last_trade_date) - day_gap
            end_day = TD.tno_tdate(end_day_no)
            start_day_no = end_day_no-(window *2)
            start_day = TD.tno_tdate(start_day_no)
            # last_update = session.query(func.max(Tl.daily_table.c.date)).scalar()
            # end_day = last_update - timedelta(days=day_gap)
            # start_day = end_day - timedelta(days=window * 2)  # 必要な期間をカバー
            # print(f"End day for analysis: {end_day}")
            # print(f"start day: {start_day}")
            # marketcodeの条件設定
            subquery = A31.ana_query_mkt().subquery()
            aliased_subquery = aliased(subquery)


            #if marketcode_query == "0100":
            #    marketcode_condition = True  # 全市場対象
            #else:
            #    marketcode_condition = Tl.company.marketcode == marketcode_query
            # Tl.companyとTl.dailyを結合し、必要なデータを取得
            base_query = (
                select(
                    aliased_subquery.c.code,
                    Tl.company.code,
                    Tl.daily.code,
                    Tl.company.companyname,
                    Tl.daily.date,
                    Tl.daily.adjustmentclose,
                )
                .join(aliased_subquery, aliased_subquery.c.code == Tl.daily.code)
                .join(Tl.company, Tl.company.code == Tl.daily.code)
                .where(Tl.daily.date >= start_day, Tl.daily.date <= end_day)
                .subquery()
            )
            # print(f"Number of records in base_query: {base_query}")
            # lag値を計算するサブクエリを作成
            lag_query = select(
                base_query.c.code,
                base_query.c.companyname,
                base_query.c.date,
                base_query.c.adjustmentclose,
                func.lag(base_query.c.adjustmentclose)
                .over(partition_by=base_query.c.code, order_by=base_query.c.date)
                .label("lag_value"),
            ).subquery()
            # print(f"lag_query: {lag_query}")
            # lag_valueがNULLでない行を選択し、price_changeを計算
            rsi_query = (
                select(
                    lag_query.c.code,
                    lag_query.c.companyname,
                    lag_query.c.date,
                    (lag_query.c.adjustmentclose - lag_query.c.lag_value).label(
                        "price_change"
                    ),
                )
                .where(lag_query.c.lag_value.isnot(None))
                .subquery()
            )
            # 平均gainと平均lossの計算
            # pylint: disable=not-callable
            avg_gain = func.avg(
                case((rsi_query.c.price_change > 0, rsi_query.c.price_change), else_=0)
            ).over(
                partition_by=rsi_query.c.code,
                order_by=rsi_query.c.date,
                rows=(-(window - 1), 0),
            )
            avg_loss = func.avg(
                case((rsi_query.c.price_change < 0, -rsi_query.c.price_change), else_=0)
            ).over(
                partition_by=rsi_query.c.code,
                order_by=rsi_query.c.date,
                rows=(-(window - 1), 0),
            )
            rs = case((avg_loss != 0, avg_gain / avg_loss), else_=0).label("rs")
            rsi_final = 100 - (100 / (1 + rs))
            # 最終的なクエリ
            final_query = select(
                rsi_query.c.code,
                rsi_query.c.companyname,
                rsi_query.c.date,
                rsi_final.label("rsi_final"),
            ).subquery()
            # print(f"final_query: {final_query}")
            # フィルタリングとソート
            result_query = (
                select(
                    final_query.c.code,
                    final_query.c.companyname,
                    final_query.c.rsi_final,
                )
                .where(final_query.c.date == end_day)
                .where(final_query.c.rsi_final.op(operator)(ana_param32))
                .order_by(A31.get_sort_order(ana_sort, final_query.c.rsi_final))
            )
            # print(f"result_query: {result_query}")
            # print(f"Base query count: {session.execute(select(func.count()).select_from(base_query)).scalar()}")
            # print(f"Lag query count: {session.execute(select(func.count()).select_from(lag_query)).scalar()}")
            # print(f"RSI query count: {session.execute(select(func.count()).select_from(rsi_query)).scalar()}")
            # print(f"Final query count: {session.execute(select(func.count()).select_from(final_query)).scalar()}")
            # print(f"Result query count: {session.execute(select(func.count()).select_from(result_query)).scalar()}")
        return result_query

    @staticmethod
    def ana_query_magcdc(gcdc):
        """querybuilder for moving average Golden Cross"""
        ana_config = Ana.load_config("ana_config.json")
        # marketcode_query = ana_config.get("marketcode")
        ana_sort = ana_config.get("sort_select501")
        short_window = int(
            ana_config.get("window101", 5)
        )  # 短期移動平均の日数（デフォルト5日）
        long_window = int(
            ana_config.get("window201", 25)
        )  # 長期移動平均の日数（デフォルト25日）
        day_gap = int(ana_config.get("gapquery111", 0))  # 日付のギャップ
        with Session() as session:
            # 取引カレンダーを使って取引日を計算する
            last_trade_date = session.query(func.max(Tl.daily_table.c.date)).scalar()
            end_day_no = TD.date_tno(last_trade_date) - day_gap
            end_day = TD.tno_tdate(end_day_no)
            start_day_no = end_day_no-(long_window *2)
            start_day = TD.tno_tdate(start_day_no)

            print(f"last_trade_date : {last_trade_date}")
            print(f"end_day_no      : {end_day_no}")
            print(f"end_day         : {end_day}")
            print(f"start_day       : {start_day}")
            print(f"day_gap         : {day_gap}")
            print(f"window          : {long_window}")

            subquery = A31.ana_query_mkt().subquery()
            aliased_subquery = aliased(subquery)

            # print(f"type of subquery : {type(subquery)}")
            # print(f"culumn keys of subquery : {subquery.columns.keys()}")

            # last_update = session.query(func.max(Tl.daily_table.c.date)).scalar()
            # end_day = last_update - timedelta(days=day_gap)
            # start_day = end_day - timedelta(days=long_window * 2)

            # marketcodeの条件を動的に設定
            #marketcode_condition = case(
            #    (literal(marketcode_query) == "0100", True),  # "0100"の場合は常にTrue
            #    else_=Tl.company.marketcode == marketcode_query,  # それ以外は通常の条件
            #)

            #subquery = (
            #    select(
            #        Tl.company.code,
            #        Tl.company.companyname,
            #        Tl.company.marketcode,
            #    )
            #    .where(marketcode_condition)
            #    .subquery()
            #)

            # 移動平均の計算
            subquery2 = (
                select(
                    aliased_subquery.c.code,
                    # Tl.daily.code,
                    Tl.daily.date,
                    Tl.daily.adjustmentclose,
                    func.avg(Tl.daily.adjustmentclose)
                    .over(
                        partition_by=Tl.daily.code,
                        order_by=Tl.daily.date.asc(),
                        rows=(-(short_window - 1), 0),
                    )
                    .label("short_ma"),
                    func.avg(Tl.daily.adjustmentclose)
                    .over(
                        partition_by=Tl.daily.code,
                        order_by=Tl.daily.date.asc(),
                        rows=(-(long_window - 1), 0),
                    )
                    .label("long_ma"),
                )
                .join(aliased_subquery, aliased_subquery.c.code == Tl.daily.code)   #追加
                .where(and_(Tl.daily.date >= start_day, Tl.daily.date <= end_day))
                .subquery()
            )

            # 今日のデータ
            today_query = (
                select(
                    subquery2.c.code,
                    subquery2.c.adjustmentclose.label("adjustmentclose_today"),
                    subquery2.c.short_ma.label("short_ma_today"),
                    subquery2.c.long_ma.label("long_ma_today"),
                )
                .where(subquery2.c.date == end_day)
                .subquery()
            )

            # 昨日のデータ
            yesterday_query = (
                select(
                    subquery2.c.code,
                    subquery2.c.short_ma.label("short_ma_yesterday"),
                    subquery2.c.long_ma.label("long_ma_yesterday"),
                )
                .where(subquery2.c.date == end_day - timedelta(days=1))
                .subquery()
            )

            # ゴールデンクロスの条件を適用
            deviation_rate = (
                (
                    (today_query.c.adjustmentclose_today - today_query.c.long_ma_today)
                    / today_query.c.long_ma_today
                    * 100
                )).label("deviation_rate")

            if gcdc == "gc":
                base_query = (
                    select(
                        subquery.c.code,
                        subquery.c.companyname,
                        deviation_rate,
                        today_query.c.short_ma_today,
                        today_query.c.long_ma_today,
                        yesterday_query.c.short_ma_yesterday,
                        yesterday_query.c.long_ma_yesterday,
                    )
                    .join(today_query, subquery.c.code == today_query.c.code)
                    .join(yesterday_query, subquery.c.code == yesterday_query.c.code)
                    .where(
                        yesterday_query.c.short_ma_yesterday
                        <= yesterday_query.c.long_ma_yesterday,
                        today_query.c.short_ma_today > today_query.c.long_ma_today,
                    )
                    .order_by(
                        A31.get_sort_order(
                            ana_sort,deviation_rate,
                        )
                    )
                )
            elif gcdc == "dc":
                # デッドクロスの条件を適用
                base_query = (
                    select(
                        subquery.c.code,
                        subquery.c.companyname,
                        deviation_rate,
                        today_query.c.short_ma_today,
                        today_query.c.long_ma_today,
                        yesterday_query.c.short_ma_yesterday,
                        yesterday_query.c.long_ma_yesterday,
                    )
                    .join(today_query, subquery.c.code == today_query.c.code)
                    .join(yesterday_query, subquery.c.code == yesterday_query.c.code)
                    .where(
                        yesterday_query.c.short_ma_yesterday
                        >= yesterday_query.c.long_ma_yesterday,
                        today_query.c.short_ma_today < today_query.c.long_ma_today,
                    )
                    .order_by(A31.get_sort_order(ana_sort, deviation_rate))
                )
            else:
                return {"error": "gcdc生成に失敗しました"}

        return base_query


    @staticmethod
    def ana_query_mamt():
        """移動平均のモーメント"""
        ana_config = Ana.load_config("ana_config.json")
        marketcode_query = ana_config.get("marketcode")
        operator = ana_config.get("ope_select131")
        ana_sort = ana_config.get("sort_select501")
        window = int(ana_config.get("window101"))
        day_gap_A = int(ana_config.get("gapquery111"))
        day_gap_B = int(ana_config.get("gapquery211"))
        key_column = "deviation_rate"

        with Session() as session:
            # 取引カレンダーから最新の取引日を取得
            last_trade_date = session.query(
                func.max(Tl.t_calendar.c.tradingdate)
            ).scalar()

            # 取引日番号を使って取引日を計算
            end_day_A_no = session.query(
                Tl.t_calendar.c.trade_date_no
            ).filter(Tl.t_calendar.c.tradingdate == last_trade_date).scalar() - day_gap_A

            end_day_B_no = end_day_A_no - window - day_gap_B
            start_day_no = end_day_A_no - (window * 2)

            # 取引日カレンダーから具体的な取引日を取得
            end_day_A = session.query(
                Tl.t_calendar.c.tradingdate
            ).filter(Tl.t_calendar.c.trade_date_no == end_day_A_no).scalar()

            end_day_B = session.query(
                Tl.t_calendar.c.tradingdate
            ).filter(Tl.t_calendar.c.trade_date_no == end_day_B_no).scalar()

            start_day = session.query(
                Tl.t_calendar.c.tradingdate
            ).filter(Tl.t_calendar.c.trade_date_no == start_day_no).scalar()

            # print(f"last_trade_date : {last_trade_date}")
            # print(f"end_day_A       : {end_day_A}")
            # print(f"end_day_B       : {end_day_B}")
            # print(f"start_day       : {start_day}")
            # print(f"window          : {window}")

            subquery = A31.ana_query_mkt().subquery()
            aliased_subquery = aliased(subquery)

            # marketcodeの条件を動的に設定
            #marketcode_condition = case(
            #    (literal(marketcode_query) == "0100", True),  # "0100"の場合は常にTrue
            #    else_=Tl.company.marketcode == marketcode_query,  # それ以外は通常の条件
            #)

            #subquery = (
            #    select(
            #        Tl.company.code,
            #        Tl.company.companyname,
            #        Tl.company.marketcode,
            #    )
            #    .where(marketcode_condition)
            #    .subquery()
            #)
            subquery_data = session.execute(select(subquery)).fetchall()
            print(f"subquery rows: {len(subquery_data)}")

            subquery2 = (
                select(
                    aliased_subquery.c.code,
                    Tl.daily.date,
                    Tl.daily.adjustmentclose,
                    func.avg(Tl.daily.adjustmentclose)
                    .over(
                        partition_by=Tl.daily.code,
                        order_by=Tl.daily.date.asc(),
                        rows=(-(window - 1), 0),
                    ).label("calc_ma"),
                    VT.moving_average_deviation(window)[1].label("deviation_rate"),
                )
                .join(aliased_subquery, aliased_subquery.c.code == Tl.daily.code)
                #.join(
                #    subquery,  # subqueryと結合
                #    subquery.c.code == Tl.daily.code
                #)
                .where(and_(Tl.daily.date >= start_day, Tl.daily.date <= end_day_A))
                .subquery()
            )
            subquery2_data = session.execute(select(subquery2)).fetchall()
            print(f"subquery2 rows: {len(subquery2_data)}")

            day_a_result = (
                select(
                    subquery2.c.code,
                    subquery2.c.date,
                    subquery2.c.adjustmentclose,
                    subquery2.c.deviation_rate,
                    subquery2.c.calc_ma.label("ma_day_A"),
                )
                .where(subquery2.c.date == end_day_A)
                .subquery()
            )

            day_b_result = (
                select(
                    subquery2.c.code,
                    subquery2.c.date,
                    subquery2.c.calc_ma.label("ma_day_B"),
                )
                .where(subquery2.c.date == end_day_B)
                .subquery()
            )

            day_a_data = session.execute(select(day_a_result)).fetchall()
            print(f"day_a_result rows: {len(day_a_data)}")

            day_b_data = session.execute(select(day_b_result)).fetchall()
            print(f"day_b_result rows: {len(day_b_data)}")
            # print(f"Operator: {operator}")

            base_query = (
                select(
                    day_a_result.c.code,
                    Tl.company.companyname,
                    subquery2.c.deviation_rate,
                    day_a_result.c.ma_day_A,
                    day_b_result.c.ma_day_B,
                )
                .join(day_b_result, day_a_result.c.code == day_b_result.c.code,)
                .join(
                    subquery2,
                    and_(
                        day_a_result.c.code == subquery2.c.code,
                        subquery2.c.date == end_day_A  # 日付条件を追加
                    )
                )
                .join(Tl.company, day_a_result.c.code == Tl.company.code,)
                .where(
                    day_a_result.c.ma_day_A.op(operator)(day_b_result.c.ma_day_B)
                )
                .group_by(
                    day_a_result.c.code,
                    Tl.company.companyname,
                    subquery2.c.deviation_rate,
                    day_a_result.c.ma_day_A,
                    day_b_result.c.ma_day_B,
                )
                .order_by(A31.get_sort_order(ana_sort, getattr(subquery2.c, key_column)))
            )
            # results = session.execute(base_query).fetchall()
            # count = 0
            # for row in results:
            #    if count >= 20:  # 20行出力したらループを終了
            #        break
            #    print(f"Code: {row.code}, MA Day A: {row.ma_day_A}, MA Day B: {row.ma_day_B}")
            #    count += 1
            return base_query


    @staticmethod
    def get_sort_order(sort_value, column):
        """ana_sortの値に基づいてソート順を決定する関数"""
        if sort_value == "01":
            return asc(column)
        elif sort_value == "02":
            return desc(column)
        else:
            # デフォルトの挙動（例：昇順）または例外を投げる
            return asc(column)
