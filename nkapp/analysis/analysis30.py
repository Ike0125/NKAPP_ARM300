"""  nkapp.analysis.analysis10.py  """
from math import ceil
from datetime import timedelta, datetime
import pandas as pd
from flask import request, session
from sqlalchemy import func, and_, case, literal
from sqlalchemy import select, desc, asc
from nkapp.config import Config
from nkapp.models import Session, Tl
from nkapp.rpt.models import VT
from .config import VALUE_MAP10, VALUE_MAP20, VALUE_MAP30, VALUE_MAP40, VALUE_MAP41
from .analysis20 import Ana

class Analysisparams30:
    """ Params """

    def __init__(self):
        # for BBS
        config = self.config()
        self.endpoint = ""                      # self-endpoint
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
        self.filters = config["filters"]

    @staticmethod
    def config():
        """Initial Params for Analysisparames"""
        return {
            "head_title": "Analysis: Query_Builder",
            "header_title": "検索",
            "endpoint": "analysis.analysis_query30",
            "return_url": "analysis.analysis_query30",
            "return_name": "To analysis30",
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
    def params(column_name, lists, counts, total_pages, page, per_page, initial,
                paramname101, paramname102, paramname103, paramname104):
        """Params for BBS"""
        config = Analysisparams30.config()
        return {
            "head_title": config["head_title"],
            "header_title": config["header_title"],
            "endpoint": config["endpoint"],
            "return_name": config["return_name"],
            "return_url": config["return_url"],
            "home_url": config["home_url"],
            "column_name": column_name,
            "db_data": lists,
            "total_records": counts,
            "total_pages": total_pages,
            "page": page,
            "per_page": per_page,
            "initial": initial,
            "paramname101": paramname101,
            "paramname102": paramname102,
            "paramname103": paramname103,
            "paramname104": paramname104,
        }

    @staticmethod
    def querybuilder():
        """for querybuilder"""
        # 初期設定値
        daygap101 = "何日前"
        daygap102 = "何日前"
        # 掲示板から選択値を取得し、保存
        if request.method == "POST":
            session["cal_select101"] = request.form.get("dropdown101")
            session["cal_select102"] = request.form.get("dropdown102")
            session["ope_select130"] = request.form.get("dropdown130")
            session["sort_select140"] = request.form.get("dropdown140")
            session["window_201"]    = request.form.get("dropdown201")
            session["paramquery101"] = request.form.get("param101", "")
            session["paramquery102"] = request.form.get("param102", "")
            session["paramquery103"] = request.form.get("param103", "")
            session["paramquery104"] = request.form.get("param104", "")
            session["gapquery101"] = request.form.get("gap101", "")
            session["gapquery102"] = request.form.get("gap102", "")
        # セッションに保存したデータの読み込み
        window_201    = int(session.get("window_201", 5))
        cal_select101 = session.get("cal_select101", "0201")
        cal_select102 = session.get("cal_select102", "0500")
        ope_select130 = session.get("ope_select130", "")
        sort_select140 = session.get("sort_select140", "02")
        paramquery101 = session.get("paramquery101", "")
        paramquery102 = session.get("paramquery102", "")
        paramquery103 = session.get("paramquery103", "")
        paramquery104 = session.get("paramquery104", "")
        gapquery101 = session.get("gapquery101", 0)
        gapquery102 = session.get("gapquery102", 0)

        # 掲示板へのデータまとめ
        ana_config = Ana.load_config("ana_config.json")
        builder_params = {
            # Market/Calculation setting
            "marketcode": ana_config.get('marketcode', None),   #市場区分コード
            "selected10": ana_config.get('selected10', None),        #市場区分
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
            "cal_select101": cal_select101,  # 計算方法A-1
            "cal_select102": cal_select102,  # 計算方法A-2
            "ope_select130": ope_select130,  # 演算子
            "sort_select140": sort_select140,  # ソート順
            "VALUE_MAP10": VALUE_MAP10,  # 市場区分コードリスト
            "VALUE_MAP20": VALUE_MAP20,  # 計算方法リスト
            "VALUE_MAP30": VALUE_MAP30,  # 演算子リスト
            "VALUE_MAP40": VALUE_MAP40,  # ソート順リスト
            "VALUE_MAP41": VALUE_MAP41,  # KEY Columnリスト
            "window_201" : window_201,  # 移動平均日数
            "daygap101"   : daygap101,  # 何日前
            "daygap102"   : daygap102,  # 何日前
            "gapquery101": gapquery101,  # 何日前params
            "gapquery102": gapquery102,  # 何日前params
            "paramquery101": paramquery101,  # 計算params
            "paramquery102": paramquery102,  # 計算params
            "paramquery103": paramquery103,  # 計算params
            "paramquery104": paramquery104,  # 計算params
        }
        return builder_params

    @staticmethod
    def analysis_query30(builder_params):
        """Params for listed_info"""
        paramname101 = "Param101"
        paramname102 = "Param102"
        paramname103 = "Param103"
        paramname104 = "Param104"
        config = Analysisparams30.config()
        start_time = datetime.now()
        column_name = ""
        builders = builder_params
        per_page = config["per_page"]
        if request.method == "POST":
            page = 1
        else:
            page = request.args.get("page", 1, type=int)
        with Session() as session:  # セッション開始
            # 初期表示時は空の結果を返す
            if request.method != "POST" and "page" not in request.args:
                print("postでないよ")
                lists = []
                counts = 0
                total_pages = 0
                page = 1
                initial = 1  # initial:1
            else:
                if builders["cal_select101"] == "0200":
                    base_query = Analysisparams30.ana_query_ma(builders)
                    column_name = "移動平均"
                elif builders["cal_select101"] == "0201":
                    base_query = Analysisparams30.ana_query_madev(builders)
                    column_name = "乖離率 %"
                    paramname103 = "定数"
                elif builders["cal_select101"] == "0202":
                    base_query = Analysisparams30.ana_query_rsi2(builders)
                    column_name = "RSI %"
                elif builders["cal_select101"] == "0203":
                    base_query = Analysisparams30.ana_query_macd(builders)
                else:
                    return {"error": "クエリの生成に失敗しました"}
                if base_query is None:
                    return {"error": "クエリの生成に失敗しました"}
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
                total_pages = ceil(counts / per_page)
                initial = 0
        # 掲示板のパラメータ
        params = Analysisparams30.params(
            column_name, lists, counts, total_pages, page, per_page, initial,
            paramname101,paramname102,paramname103,paramname104
        )
        end_time = datetime.now()
        query_time = end_time - start_time
        print(f"Query_time: {query_time}")
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
                Analysisparams30.get_sort_order(
                    ana_sort, getattr(subquery2.c, key_column)
                )
            )
        )
        return base_query

    @staticmethod
    def ana_query_madev(builders):
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
                Analysisparams30.get_sort_order(
                    ana_sort, getattr(subquery2.c, key_column)
                )
            )
        )
        return base_query


    @staticmethod
    def ana_query_rsi(builders):
        """querybuilder for RSI"""
        marketcode_query = builders["marketcode"]
        operator = builders["ope_select130"]
        ana_sort = builders["sort_select140"]
        window = int(builders["rsi_period_value"])
        day_gap = int(builders["daygap101"])
        ana_param32 = float(builders["paramquery103"])
        key_column = f"rsi_{window}"
        with Session() as session:
            last_update = session.query(func.max(Tl.daily_table.c.date)).scalar()
            end_day = last_update - timedelta(days=day_gap)
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
        rsi_query = VT.rsi(window).subquery("rsi_subquery")

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
                Analysisparams30.get_sort_order(
                    ana_sort, getattr(rsi_query.c, key_column)
                )
            )
        )
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
        # print(f"marketcode_query: {marketcode_query}")
        # print(f"ana_sort: {ana_sort}")
        # print(f"day_gap: {day_gap}")
        # print(f"short_window: {short_window}")
        # print(f"long_window: {long_window}")
        # print(f"signal_window: {signal_window}")

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
                    Analysisparams30.get_sort_order(ana_sort, final_query.c.histogram)
                )
            )
        return result_query

    @staticmethod
    def ana_query_rsi2(builders):
        """Optimized and corrected query builder for RSI."""
        marketcode_query = builders["marketcode"]
        operator = builders["ope_select130"]
        ana_sort = builders["sort_select140"]
        window = int(builders["rsi_period_value"])
        day_gap = int(builders["gapquery101"])
        ana_param32 = float(builders["paramquery103"])
        # key_column = f"rsi_{window}"
        # print(f"marketcode_query: {marketcode_query}")
        # print(f"operator: {operator}")
        # print(f"ana_sort: {ana_sort}")
        # print(f"window: {window}")
        # print(f"day_gap: {day_gap}")
        # print(f"ana_param32: {ana_param32}")

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

            rs = case((avg_loss != 0, avg_gain / avg_loss), else_=0).label("rs")
            rsi_final = 100 - (100 / (1 + rs))

            # 最終的なクエリ
            final_query = select(
                rsi_query.c.code,
                rsi_query.c.companyname,
                rsi_query.c.date,
                rsi_final.label("rsi_final"),
            ).subquery()
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
                    Analysisparams30.get_sort_order(ana_sort, final_query.c.rsi_final)
                )
            )
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
