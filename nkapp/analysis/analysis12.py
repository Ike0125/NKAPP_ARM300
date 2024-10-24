"""  nkapp.rpt.report.py  """
from math import ceil
from datetime import timedelta, datetime
from flask import request, session
from sqlalchemy import func, and_, case, literal
from sqlalchemy import select, desc, asc
from nkapp.models import Session, Tl
from nkapp.rpt.models import VT
from .config import VALUE_MAP10, VALUE_MAP20, VALUE_MAP30, VALUE_MAP40, VALUE_MAP41


class Analysisparams10:
    """Params for listed_info"""

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
        # print(f"builder_params: {builder_params}")
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
                    base_query = Analysisparams10.ana_query_rsi(builders)
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
    def ana_query_rsi(builders):
        """Optimized and integrated query builder for RSI."""
        marketcode_query = builders["selected10"]
        operator = builders["selected30"]
        ana_sort = builders["selected40"]
        window = int(builders["paramquery21"])
        day_gap = int(builders["paramquery31"])
        ana_param32 = float(builders["paramquery32"])
        key_column = f"rsi_{window}"

        with Session() as session:
            last_update = session.query(
                func.max(Tl.daily_table.c.date)
            ).scalar()
            end_day = last_update - timedelta(days=day_gap)
            start_day = end_day - timedelta(days=window * 2)  # 必要な期間をカバー

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
                    Tl.daily.adjustmentclose
                )
                .join(Tl.company, Tl.company.code == Tl.daily.code)
                .where(
                    marketcode_condition,
                    Tl.daily.date >= start_day,
                    Tl.daily.date <= end_day
                )
                .subquery()
            )

            # 価格変化、gain、loss、平均gain、平均lossを一度に計算
            rsi_query = (
                select(
                    base_query.c.code,
                    base_query.c.companyname,
                    base_query.c.date,
                    (base_query.c.adjustmentclose - func.lag(base_query.c.adjustmentclose).over(
                        partition_by=base_query.c.code,
                        order_by=base_query.c.date
                    )).label('price_change'),
                )
                .subquery()
            )

            # RSIの計算
            final_query = (
                select(
                    rsi_query.c.code,
                    rsi_query.c.companyname,
                    (100 - 100 / (1 + (
                        func.avg(case(
                            (rsi_query.c.price_change > 0, rsi_query.c.price_change),
                            else_=0
                        )).over(
                            partition_by=rsi_query.c.code,
                            order_by=rsi_query.c.date,
                            rows=window - 1
                        ) /
                        func.avg(case(
                            (rsi_query.c.price_change < 0, -rsi_query.c.price_change),
                            else_=0
                        )).over(
                            partition_by=rsi_query.c.code,
                            order_by=rsi_query.c.date,
                            rows=window - 1
                        )
                    ))).label(key_column)
                )
                .where(rsi_query.c.date == end_day)
                .subquery()
            )

            # フィルタリングとソート
            result_query = (
                select(final_query.c.code, final_query.c.companyname, getattr(final_query.c, key_column))
                .where(
                    getattr(final_query.c, key_column).op(operator)(ana_param32)
                )
                .order_by(
                    Analysisparams10.get_sort_order(
                        ana_sort, getattr(final_query.c, key_column)
                    )
                )
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

