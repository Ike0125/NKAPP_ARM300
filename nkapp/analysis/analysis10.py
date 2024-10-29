"""  nkapp.analysis.analysis10.py  """
from math import ceil
from datetime import timedelta, datetime
import pandas as pd
from flask import request, session
from sqlalchemy import func, and_, case, literal
from sqlalchemy import select, desc, asc
from nkapp.models import Session, Tl
from nkapp.rpt.models import VT
from .config import VALUE_MAP10, VALUE_MAP20, VALUE_MAP30, VALUE_MAP40, VALUE_MAP41


class Analysisparams10:
    """ Params """

    def __init__(self):
        # for BBS
        config = self.config()
        self.head_title = config["head_title"]  # head_info
        self.header_title = config["header_title"]  # header_info
        self.endpoint = config["endpoint"]  # self-endpoint
        self.return_url = config["return_url"]  # return-privious
        self.home_url = config["home_url"]  # return_home
        self.page = config["page"]  # page
        self.per_page = config["per_page"]  # per_page
        self.db_data = config["db_data"]  # database_data
        self.total_records = config["total_records"]  # total_counts
        self.total_pages = config["total_pages"]  # total_pages
        self.initial = config["initial"]  # initial:1
        self.companyname_query = config["company_query"]  # for companyname
        self.marketcode_query = config["marketcode_query"]  # for marketcode
        self.start_day = config["start_day"]  # start_day
        self.end_day = config["end_day"]  # end_day
        self.day_gap = config["day_gap"]  # start_day=Today-day_gap
        self.column_name = config["column_name"]
        self.filters = config["filters"]

    @staticmethod
    def config():
        """Initial Params for Analysisparames"""
        return {
            "head_title": "Analysis: Query_Builder",
            "header_title": "検索",
            "endpoint": "analysis.analysis_query",
            "return_url": "javascript:history.back()",
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
        }

    @staticmethod
    def params(column_name, lists, counts, total_pages, page, per_page, initial):
        """Params for BBS"""
        config = Analysisparams10.config()
        return {
            "head_title": config["head_title"],
            "header_title": config["header_title"],
            "endpoint": config["endpoint"],
            "return_url": config["return_url"],
            "home_url": config["home_url"],
            "column_name": column_name,
            "db_data": lists,
            "total_records": counts,
            "total_pages": total_pages,
            "page": page,
            "per_page": per_page,
            "initial": initial,
        }

    @staticmethod
    def querybuilder():
        """for querybuilder"""
        # 初期設定値
        paramname21 = "移動平均日数"
        paramname31 = "何日前"
        paramname32 = "パラメータ１"
        paramquery21 = 20
        paramquery31 = 0
        paramquery32 = 0
        # 掲示板から選択値を取得し、保存
        if request.method == "POST":
            session["selected10"] = request.form.get("dropdown10")
            session["selected20"] = request.form.get("dropdown20")
            session["selected30"] = request.form.get("dropdown30")
            session["selected40"] = request.form.get("dropdown40")
            session["selected41"] = request.form.get("dropdown41")
            session["paramquery21"] = request.form.get("param21", "")
            session["paramquery31"] = request.form.get("param31", "")
            session["paramquery32"] = request.form.get("param32", "")
        # セッションに保存したデータの読み込み
        selected10 = session.get("selected10", "")
        selected20 = session.get("selected20", "")
        selected30 = session.get("selected30", "")
        selected40 = session.get("selected40", "")
        selected41 = session.get("selected41", "")
        paramquery21 = session.get("paramquery21", "")
        paramquery31 = session.get("paramquery31", "")
        paramquery32 = session.get("paramquery32", "")

        # 掲示板へのデータまとめ
        builder_params = {
            "selected10": selected10,  # 市場区分コード
            "selected20": selected20,  # 計算方法
            "selected30": selected30,  # 演算子
            "selected40": selected40,  # ソート順
            "selected41": selected41,  # KEY Column
            "VALUE_MAP10": VALUE_MAP10,  # 市場区分コードリスト
            "VALUE_MAP20": VALUE_MAP20,  # 計算方法リスト
            "VALUE_MAP30": VALUE_MAP30,  # 演算子リスト
            "VALUE_MAP40": VALUE_MAP40,  # ソート順リスト
            "VALUE_MAP41": VALUE_MAP41,  # KEY Columnリスト
            "paramname21": paramname21,  # 移動平均日数
            "paramname31": paramname31,  # 何日前
            "paramname32": paramname32,  # パラメータ１
            "paramquery21": paramquery21,  # 計算方法params
            "paramquery31": paramquery31,  # 何日前params
            "paramquery32": paramquery32,  # 計算params
        }
        print(f"builder_params: {builder_params}")
        # return builder_params
        return builder_params

    @staticmethod
    def analysis_query(builder_params):
        """Params for listed_info"""
        config = Analysisparams10.config()
        start_time = datetime.now()
        column_name = ""
        # builder = Analysisparams10.querybuilder()
        builders = builder_params
        per_page = config["per_page"]
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
                lists = []
                counts = 0
                total_pages = 0
                page = 1
                initial = 1  # initial:1
            else:
                if builders["selected20"] == "0201":
                    base_query = Analysisparams10.ana_query_ma(builders)
                    column_name = "乖離率 %"
                elif builders["selected20"] == "0202":
                    base_query = Analysisparams10.ana_query_rsi2(builders)
                    column_name = "RSI %"
                elif builders["selected20"] == "0203":
                    base_query = Analysisparams10.ana_query_macd(builders)
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
        params = Analysisparams10.params(
            column_name, lists, counts, total_pages, page, per_page, initial
        )
        end_time = datetime.now()
        query_time = end_time - start_time
        print(f"Query_time: {query_time}")
        # print(f"params: {params}")
        return params

    @staticmethod
    def ana_query_ma(builders):
        """querybuilder for moving average"""
        marketcode_query = builders["selected10"]
        operator = builders["selected30"]
        ana_sort = builders["selected40"]
        window = int(builders["paramquery21"])
        day_gap = int(builders["paramquery31"])
        ana_param32 = float(builders["paramquery32"])
        key_column = builders["selected41"]
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
                Analysisparams10.get_sort_order(
                    ana_sort, getattr(subquery2.c, key_column)
                )
            )
        )
        # print(f"base_query: {base_query}")
        return base_query

    @staticmethod
    def ana_query_rsi(builders):
        """querybuilder for RSI"""
        marketcode_query = builders["selected10"]
        operator = builders["selected30"]
        ana_sort = builders["selected40"]
        window = int(builders["paramquery21"])
        day_gap = int(builders["paramquery31"])
        ana_param32 = float(builders["paramquery32"])
        # key_column = builders["selected41"]
        key_column = f"rsi_{window}"
        with Session() as session:
            last_update = session.query(func.max(Tl.daily_table.c.date)).scalar()
            end_day = last_update - timedelta(days=day_gap)
            start_day = end_day - timedelta(days=window + 2)  # RSI用に＋２日分
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
        rsi_query = VT.rsi(window).subquery("rsi_subquery")

        # subquery2 = (
        #    select(
        #        Tl.daily.code,
        #        Tl.daily.date,
        #        Tl.daily.adjustmentclose,
        #        rsi_query.c[f"rsi_{window}"]
        #    )  # RSIを計算
        #    .where(and_(Tl.daily.date >= start_day, Tl.daily.date <= end_day))
        #    .subquery()
        # )
        # print(f"subquery2: {subquery2}")

        base_query = (
            select(
                subquery.c.code, subquery.c.companyname, rsi_query.c[f"rsi_{window}"]
            )
            .join(rsi_query, subquery.c.code == rsi_query.c.code)
            .where(
                rsi_query.c.date == end_day,
                rsi_query.c[f"rsi_{window}"].op(operator)(ana_param32),
            )
            .order_by(
                Analysisparams10.get_sort_order(
                    ana_sort, getattr(rsi_query.c, key_column)
                )
            )
        )
        # print(f"base_query: {base_query}")
        # print(f"RSI:rsi_{window}")
        return base_query

    @staticmethod
    def ana_query_macd(builders):
        """Optimized and corrected query builder for MACD."""
        # 初期設定
        marketcode_query = builders["selected10"]
        operator = builders["selected30"]
        ana_sort = builders["selected40"]
        short_window = int(builders["paramquery21"])
        long_window = int(builders["paramquery22"])
        signal_window = int(builders["paramquery23"])
        day_gap = int(builders["paramquery31"])

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
                    Analysisparams10.get_sort_order(ana_sort, final_query.c.histogram)
                )
            )
        return result_query

    @staticmethod
    def ana_query_rsi2(builders):
        """Optimized and corrected query builder for RSI."""
        marketcode_query = builders["selected10"]
        operator = builders["selected30"]
        ana_sort = builders["selected40"]
        window = int(builders["paramquery21"])
        day_gap = int(builders["paramquery31"])
        ana_param32 = float(builders["paramquery32"])
        # key_column = f"rsi_{window}"

        with Session() as session:
            last_update = session.query(func.max(Tl.daily_table.c.date)).scalar()
            end_day = last_update - timedelta(days=day_gap)
            start_day = end_day - timedelta(days=window * 2)  # 必要な期間をカバー

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
            # print(f"Number of records in base_query: {base_query}")

            # **修正ポイント1：lag値を計算するサブクエリを作成**
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
            # **修正ポイント2：lag_valueがNULLでない行を選択し、price_changeを計算**
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

            # RSIの計算（ゼロ除算を防ぐための条件分岐を追加）
            # pylint: disable=not-callable
            # rs = func.coalesce(avg_gain / func.nullif(avg_loss, 0), 0)
            # rsi_value = case(
            #    (avg_loss == 0, 100),
            #    (avg_gain == 0, 0),
            #    else_=100 - (100 / (1 + rs))
            # ).label('rsi_value')
            # rsi_final = func.coalesce(rsi_value, 50).label('rsi_final')
            # print(f"rsi_final_data: {rsi_final}")
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
                    Analysisparams10.get_sort_order(ana_sort, final_query.c.rsi_final)
                )
            )
            # print(f"result_query: {result_query}")
            print(
                f"Base query count: {session.execute(select(func.count()).select_from(base_query)).scalar()}"
            )
            print(
                f"Lag query count: {session.execute(select(func.count()).select_from(lag_query)).scalar()}"
            )
            print(
                f"RSI query count: {session.execute(select(func.count()).select_from(rsi_query)).scalar()}"
            )
            print(
                f"Final query count: {session.execute(select(func.count()).select_from(final_query)).scalar()}"
            )
            print(
                f"Result query count: {session.execute(select(func.count()).select_from(result_query)).scalar()}"
            )
            # pylint: disable=not-callable
            """
            debug_query = (
                select(
                    rsi_query.c.code,
                    rsi_query.c.date,
                    avg_gain.label('avg_gain'),
                    avg_loss.label('avg_loss'),
                    rs.label('rs'),
                    rsi_value.label('rsi_value'),
                    rsi_final.label('rsi_final')
                )
                .where(rsi_query.c.date == end_day)
                .limit(10)
            )

            debug_results = session.execute(debug_query).fetchall()
            print("Debug RSI calculations:")
            for row in debug_results:
                print(row)

            debug_query = (
                select(
                    final_query.c.code,
                    final_query.c.date,
                    final_query.c.rsi_final
                )
                .order_by(final_query.c.code, final_query.c.date)
                .limit(20)
            )

            debug_results = session.execute(debug_query).fetchall()
            print("Debug RSI calculations_Updated (final values):")
            for row in debug_results:
                print(row)

            # price_changeの分布を確認
            price_change_stats = (
                select(
                    func.min(rsi_query.c.price_change).label('min_change'),
                    func.max(rsi_query.c.price_change).label('max_change'),
                    func.avg(rsi_query.c.price_change).label('avg_change'),
                    func.sum(case((rsi_query.c.price_change < 0, 1), else_=0)).label('negative_changes'),
                    func.sum(case((rsi_query.c.price_change > 0, 1), else_=0)).label('positive_changes')
                )
            )
            stats_result = session.execute(price_change_stats).first()
            print(f"Price change stats: {stats_result}")

            price_change_debug = (
                select(
                    lag_query.c.code,
                    lag_query.c.date,
                    lag_query.c.adjustmentclose,
                    lag_query.c.lag_value,
                    (lag_query.c.adjustmentclose - lag_query.c.lag_value).label('price_change')
                )
                .order_by(lag_query.c.code, lag_query.c.date)
                .limit(20)
            )

            price_change_results = session.execute(price_change_debug).fetchall()
            print("Price change calculation:")
            for row in price_change_results:
                print(row)

            gain_loss_debug = (
                select(
                    rsi_query.c.code,
                    rsi_query.c.date,
                    rsi_query.c.price_change,
                    case((rsi_query.c.price_change > 0, rsi_query.c.price_change), else_=0).label('gain'),
                    case((rsi_query.c.price_change < 0, -rsi_query.c.price_change), else_=0).label('loss'),
                    avg_gain,
                    avg_loss
                )
                .order_by(rsi_query.c.code, rsi_query.c.date)
                .limit(20)
            )

            gain_loss_results = session.execute(gain_loss_debug).fetchall()
            print("Gain and Loss calculation:")
            for row in gain_loss_results:
                print(row)

            window_function_debug = (
                select(
                    rsi_query.c.code,
                    rsi_query.c.date,
                    func.sum(
                        case((rsi_query.c.price_change > 0, rsi_query.c.price_change), else_=0)
                    ).over(
                        partition_by=rsi_query.c.code,
                        order_by=rsi_query.c.date,
                        rows=(-(window-1), 0)
                    ).label('sum_gain'),
                    func.sum(
                        case((rsi_query.c.price_change < 0, -rsi_query.c.price_change), else_=0)
                    ).over(
                        partition_by=rsi_query.c.code,
                        order_by=rsi_query.c.date,
                        rows=(-(window-1), 0)
                    ).label('sum_loss')
                )
                .order_by(rsi_query.c.code, rsi_query.c.date)
                .limit(20)
            )

            window_function_results = session.execute(window_function_debug).fetchall()
            print("Window function operation:")
            for row in window_function_results:
                print(row)

            rsi_final_debug = (
                select(
                    rsi_query.c.code,
                    rsi_query.c.date,
                    avg_gain,
                    avg_loss,
                    rs,
                    rsi_value,
                    rsi_final,
                )
                .order_by(rsi_query.c.code, rsi_query.c.date)
                .limit(20)
            )

            rsi_final_results = session.execute(rsi_final_debug).fetchall()
            print("Final RSI calculation:")
            for row in rsi_final_results:
                print(row)

            result_sample = session.execute(result_query.limit(20)).fetchall()
            print("Sample of final result:")
            for row in result_sample:
                print(row)
            """
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
