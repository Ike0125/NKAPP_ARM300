"""  nkapp.analysis.testview.py  """
from math import ceil
from datetime import timedelta, datetime
import pandas as pd
from flask import request, session
from sqlalchemy import func, and_, case, literal
from sqlalchemy import select, desc, asc
# from nkapp.config import Config
from nkapp.models import Session, Tl
from nkapp.rpt.models import VT
from .config import VALUE_MAP10, VALUE_MAP20, VALUE_MAP30
from .config import VALUE_MAP40, VALUE_MAP41, VALUE_MAP50
from .analysis20 import Ana


class A31:
    """ Params """

    def __init__(self):
        # for BBS
        config = self.config()
        self.error = config["error"]       # error message
        self.endpoint = "endpoint"         # self-endpoint
        self.return_url = config["return_url"]  # return-privious
        self.home_url = config["home_url"]      # return_home
        self.page = config["page"]              # page
        self.per_page = config["per_page"]      # per_page
        self.db_data = config["db_data"]        # database_data
        self.total_records = config["total_records"]  # total_counts
        self.total_pages = config["total_pages"]  # total_pages
        self.initial = config["initial"]        # initial:1
        self.companyname_query = config["company_query"]  # for companyname
        self.marketcode_query = config["marketcode_query"]  # for marketcode
        self.start_day = config["start_day"]  # start_day
        self.end_day = config["end_day"]  # end_day
        self.day_gap = config["day_gap"]  # start_day=Today-day_gap
        self.column_name = config["column_name"]
        self.comment102 = config["comment102"]
        self.paramname121 = config["paramname121"]
        self.paramname122 = config["paramname122"]
        self.paramname221 = config["paramname221"]
        self.paramname222 = config["paramname222"]
        self.subject123 = config["subject123"]
        self.subject124 = config["subject124"]
        self.subject125 = config["subject125"]
        self.comment123 = config["comment123"]
        self.comment124 = config["comment124"]
        self.comment125 = config["comment125"]
        self.comment202 = config["comment202"]
        self.subject223 = config["subject223"]
        self.subject224 = config["subject224"]
        self.subject225 = config["subject225"]
        self.comment223 = config["comment223"]
        self.comment224 = config["comment224"]
        self.comment225 = config["comment225"]


    @staticmethod
    def config():
        """Initial Params for Analysisparames"""
        return {
            "error": "Error Message:",
            "head_title": "Analysis: Query_Builder",
            "header_title": "検索",
            "endpoint": "analysis.analysis_query31",
            "return_url": "analysis.analysis_query31",
            "return_name": "To analysis31",
            "home_url": "nkapp.index",
            "db_data": [],
            "total_records": 0,
            "total_pages": 0,
            "page": 1,
            "per_page": 15,
            "marketcode_query": "",
            "companyname_query": "",
            "column_name": "乖離率/%",
            "initial": 1,
            "comment102"    : "式もしくは設定したパラメータ",      #以下は各計算メソッドから戻すこと
            "paramname121"   : "Param-A1",              # Param-A1
            "paramname122"   : "Param-A2",              # Param-A2
            "paramname221"   : "Param-B1",              # Param-B1
            "paramname222"   : "Param-B2",              # Param-B2
            "subject123"    : "A123",
            "subject124"    : "A124",
            "subject125"    : "A125",
            "comment123"    : "A123_comment",
            "comment124"    : "A124_comment",
            "comment125"    : "A125_comment",
            "comment202"    : "固定値",
            "subject223"    : "B223",
            "subject224"    : "B224",
            "subject225"    : "B225",
            "comment223"    : "B223_comment",
            "comment224"    : "B224_comment",
            "comment225"    : "B225_comment",
        }


    @staticmethod
    def query_builder2():
        """for display_settings"""
        if request.method == "POST":
            # 掲示板から選択値を取得し、セッションに保存
            session["condition"] = request.form.get("condition")
            # Selection
            session["condition001"] = request.form.get("dropdown001")
            # Gropu A
            session["window101"] = request.form.get("dropdown101")
            session["gapquery111"] = request.form.get("gap111")
            session["paramquery121"] = request.form.get("param121")
            session["paramquery122"] = request.form.get("param122")
            # Operator
            session["ope_select131"] = request.form.get("dropdown131")
            # Group B
            session["window201"] = request.form.get("dropdown201")
            session["gapquery211"] = request.form.get("gap211")
            session["paramquery221"] = request.form.get("param221")
            session["paramquery222"] = request.form.get("param222")
            # Sort
            session["sort_select501"] = request.form.get("dropdown501")
        else:
            # 保存したデータの読み込み
            ana_config = Ana.load_config("ana_config.json")
            session["condition"]      = ana_config["condition"]
            session["condition001"]   = ana_config["condition001"]
            session["window101"]      = ana_config["window101"]
            session["gapquery111"]    = ana_config["gapquery111"]
            session["paramquery121"]  = ana_config["paramquery121"]
            session["paramquery122"]  = ana_config["paramquery122"]
            session["ope_select131"]  = ana_config["ope_select131"]
            session["gapquery211"]    = ana_config["gapquery211"]
            session["paramquery221"]  = ana_config["paramquery221"]
            session["paramquery222"]  = ana_config["paramquery222"]
            session["sort_select501"] = ana_config["sort_select501"]
        # セッションに保存したデータの読み込み
        # Selection
        condition = session.get("condition", None)
        condition001 = session.get("condition001", None)
        # Group A
        window101 = int(session.get("window101",5))
        gapquery111 = session.get("gapquery111","")
        paramquery121 = session.get("paramquery121","")
        paramquery122 = session.get("paramquery122","")
        # Operator
        ope_select131 = session.get("ope_select131","")
        # Group B
        window201 = int(session.get("window201",5))
        gapquery211 = session.get("gapquery211","")
        paramquery221 = session.get("paramquery221","")
        paramquery222 = session.get("paramquery222","")
        sort_select501 = session.get("sort_select501","")
        # 掲示板へのデータまとめ
        ana_config = Ana.load_config("ana_config.json")
        builder_params = {
            # Market/Calculation setting
            "marketcode": ana_config.get('marketcode', None),   #市場区分コード
            "selected10": ana_config.get('selected10', None),   #市場区分
            "ma_value01": ana_config.get('ma_value01', None),   #移動平均１
            "ma_value02": ana_config.get('ma_value02', None),   #移動平均２
            "ma_value03": ana_config.get('ma_value03', None),   #移動平均３
            "ma_value04": ana_config.get('ma_value04', None),   #移動平均４
            "ma_value05": ana_config.get('ma_value05', None),   #移動平均５
            "rsi_period_value": ana_config.get('rsi_period_value', None),   #RSI期間
            "macd_short_value": ana_config.get('macd_short_value', None),   #MACDshort
            "macd_long_value": ana_config.get('macd_long_value', None),     #MACDlong
            "macd_signal_value": ana_config.get('macd_signal_value', None), #MACDsignal
            # Query Setting
            "daygapname111"    : "何日前",
            "daygapname211"    : "何日前",
            "VALUE_MAP10"   : VALUE_MAP10,  # 市場区分コードリスト
            "VALUE_MAP20"   : VALUE_MAP20,  # 計算方法リスト
            "VALUE_MAP30"   : VALUE_MAP30,  # 演算子リスト
            "VALUE_MAP40"   : VALUE_MAP40,  # ソート順リスト
            "VALUE_MAP41"   : VALUE_MAP41,  # KEY Columnリスト
            "VALUE_MAP50"   : VALUE_MAP50,  # Query Conditionリスト
            "condition"     : condition,
            "condition001"  : condition001,
            "window101"     : window101,
            "gapquery111"   : gapquery111,
            "paramquery121" : paramquery121,
            "paramquery122" : paramquery122,
            "ope_select131" : ope_select131,
            "window201"     : window201,
            "gapquery211"   : gapquery211,
            "paramquery221" : paramquery221,
            "paramquery222" : paramquery222,
            "sort_select501": sort_select501,
        }
        # print(f"builder_params: {builder_params}")
        # データの保存
        config_formula = Ana.load_config("ana_config.json")
        config_formula.update(builder_params)
        Ana.save_config("ana_config.json",builder_params)

        return builder_params

    @staticmethod
    def analysis_query31(builder_params):
        """Params for listed_info"""
        params = A31.config()
        start_time = datetime.now()
        # builder = Analysisparams10.querybuilder()
        builders = builder_params
        per_page = params["per_page"]
        if request.method == "POST":
            page = 1
        else:
            page = request.args.get("page", 1, type=int)
        # print(f"builder_params: {builders}")
        with Session() as session:  # セッション開始
            # 初期表示時は空の結果を返す
            # is_initial_request = not bool(request.args.get("filter2", "").strip())
            # if is_initial_request or not request.args.get("filter2", "").strip():
            print(f"page1: {page}")
            # if request.method != "POST":
            if request.method != "POST" and "page" not in request.args:
                print("postでないよ")
                lists = []
                counts = 0
                total_pages = 0
                page = 1
                initial = 1  # initial:1
            else:
                if builders["condition001"] == "0500":
                    base_query = A31.ana_query_ma(builders)
                    params["column_name"] = "移動平均"
                elif builders["condition001"] == "0501":
                    base_query = A31.ana_query_madev(builders)
                    params["column_name"] = "乖離率 %"
                    params["paramname221"] = "定数(%)"
                elif builders["condition001"] == "0511":
                    base_query = A31.ana_query_rsi2(builders)
                    params["column_name"] = "RSI %"
                    params["paramname221"] = "RSI %"
                    rsi_period = builders["rsi_period_value"]
                    params["comment102"] = f"RSI={rsi_period}"
                elif builders["condition001"] == "0521":
                    base_query = A31.ana_query_macd(builders)
                else:
                    return {"error": "クエリの生成に失敗しました"}
                if base_query is None:
                    return {"error": "クエリの生成に失敗しました"}
                # print(f"base_query: {base_query}")
                # 総レコード数を取得
                # pylint: disable=not-callable
                count_query = select(func.count()).select_from(base_query.subquery())
                # base_queryをサブクエリとし、その結果の行数をカウント
                counts = session.execute(count_query).scalar()
                # オフセット計算
                print(f"counts: {counts}")
                offset = (page - 1) * per_page
                print(f"offset: {offset}")
                # ページネーションをオフセット値と１ページ当りのレコード数より設定
                paginated_query = base_query.offset(offset).limit(per_page)
                # sqlalchemyクエリを実行し、全レコードを取得
                lists = session.execute(paginated_query).fetchall()
                # トータルページ数の計算
                # print(f"db_data: {lists}")
                total_pages = ceil(counts / per_page)
                initial = 0
                # print(f"page2: {page}")
                # print(f"lists: {lists}")
        # 掲示板のパラメータ
        params.update({
            "db_data" : lists,
            "total_records" : counts,
            "total_pages" : total_pages,
            "page" : page,
            "per_page": per_page,
            "initial" : initial
        })
        end_time = datetime.now()
        query_time = end_time - start_time
        print(f"Query_time: {query_time}")
        print(f"params: {params}")
        return params

    @staticmethod
    def ana_query_ma(builders):
        """querybuilder for moving average"""
        marketcode_query = builders["marketcode"]
        operator = builders["ope_select130"]
        ana_sort = builders["sort_select140"]
        window = int(builders["window_201"])
        day_gap = int(builders["gapquery101"], 0)
        ana_param32 = float(builders["paramquery103"])
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
            .order_by(
                A31.get_sort_order(
                    ana_sort, getattr(subquery2.c, key_column)
                )
            )
        )
        # print(f"base_query: {base_query}")
        return base_query

    @staticmethod
    def ana_query_madev(builders):
        """querybuilder for moving average"""
        marketcode_query = builders["marketcode"]
        operator = builders["ope_select131"]
        ana_sort = builders["sort_select501"]
        window = int(builders["window101"])
        day_gap = int(builders["gapquery111"], 0)
        ana_param32 = float(builders["paramquery221"])
        key_column = "deviation_rate"
        #print(f"marketcode_query: {marketcode_query}")
        #print(f"operator: {operator}")
        #print(f"ana_sort: {ana_sort}")
        #print(f"window: {window}")
        #print(f"day_gap: {day_gap}")
        #print(f"ana_param32: {ana_param32}")
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
                    subquery2.c[f"ma_{window}"] * (1+ana_param32/100)
                )
            )
            .where(subquery2.c.date == end_day)
            .group_by(
                subquery.c.code, subquery.c.companyname, subquery2.c.deviation_rate
            )
            .order_by(
                A31.get_sort_order(
                    ana_sort, getattr(subquery2.c, key_column)
                )
            )
        )
        # print(f"base_query: {base_query}")
        return base_query


    @staticmethod
    def ana_query_macd(builders):
        """Optimized and corrected query builder for MACD."""
        # 初期設定
        marketcode_query = builders["marketcode"]
        ana_sort = builders["sort_select140"]
        day_gap = int(builders["gapquery101"])
        short_window = int(builders["macd_short_value"])
        long_window = int(builders["macd_long_value"])
        signal_window = int(builders["macd_signal_value"])
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
                .order_by(
                    A31.get_sort_order(ana_sort, final_query.c.histogram)
                )
            )
        return result_query

    @staticmethod
    def ana_query_rsi2(builders):
        """Optimized and corrected query builder for RSI."""
        marketcode_query = builders["marketcode"]
        operator = builders["ope_select131"]
        ana_sort = builders["sort_select501"]
        window = int(builders["window101"])
        day_gap = int(builders["gapquery111"], 0)
        ana_param32 = float(builders["paramquery221"])
        # key_column = f"rsi_{window}"
        print(f"marketcode_query: {marketcode_query}")
        print(f"operator: {operator}")
        # print(f"ana_sort: {ana_sort}")
        print(f"window: {window}")
        print(f"day_gap: {day_gap}")
        print(f"ana_param32: {ana_param32}")

        with Session() as session:
            last_update = session.query(func.max(Tl.daily_table.c.date)).scalar()
            end_day = last_update - timedelta(days=day_gap)
            start_day = end_day - timedelta(days=window * 2)  # 必要な期間をカバー
            #print(f"End day for analysis: {end_day}")
            #print(f"start day: {start_day}")
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
                .order_by(
                    A31.get_sort_order(ana_sort, final_query.c.rsi_final)
                )
            )
            #print(f"result_query: {result_query}")
            #print(f"Base query count: {session.execute(select(func.count()).select_from(base_query)).scalar()}")
            #print(f"Lag query count: {session.execute(select(func.count()).select_from(lag_query)).scalar()}")
            #print(f"RSI query count: {session.execute(select(func.count()).select_from(rsi_query)).scalar()}")
            #print(f"Final query count: {session.execute(select(func.count()).select_from(final_query)).scalar()}")
            #print(f"Result query count: {session.execute(select(func.count()).select_from(result_query)).scalar()}")
        return result_query


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
