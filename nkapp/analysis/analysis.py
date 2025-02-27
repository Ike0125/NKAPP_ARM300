"""  nkapp.rpt.report.py  """
from math import ceil
from datetime import datetime, timedelta
from flask import request
from sqlalchemy import func, text, and_
from sqlalchemy import select, desc
from nkapp.models import Session, Tl
from nkapp.rpt.models import VT


class Analysisparams:
    """Params for listed_info"""
    def __init__(self,head_title,header_title,
        endpoint,return_url,return_name,page,
        per_page,db_data,total_records,total_pages,
        initial,company_query,filters
        ):
        self.head_title = head_title        # head_info
        self.header_title = header_title    # header_info
        self.endpoint = endpoint            # self-endpoint
        self.return_url = return_url        # return-endpoint
        self.return_name = return_name      # return_name
        self.page = page                    # page
        self.per_page = per_page            # per_page
        self.db_data = db_data              # database_data
        self.total_records = total_records  # total_counts
        self.total_pages = total_pages      # total_pages
        self.initial = initial              # initial:1
        self.companyname_query = company_query
        self.filters = filters


    @staticmethod
    def config():
        """Initial Params for Analysisparames"""
        return {
            "head_title": "Analysis: Main_Info",
            "header_title": "検索",
            "endpoint": "analysis.ana_list",
            "return_url": "analysis.main",
            "return_name": "元に戻る",
            "db_data": [],
            "total_records": 0,
            "total_pages": 0,
            "page": 1,
            "per_page": 15,
            "companyname_query": "",
            "initial": 1
        }


    @staticmethod
    def params(lists,counts,total_pages,page,per_page,filters,initial):
        """Initial Params for Analysisparames"""
        config = Analysisparams.config()
        return {
            "head_title": config["head_title"],
            "header_title": config["header_title"],
            "endpoint": config["endpoint"],
            "return_url": config["return_url"],
            "return_name": config["return_name"],
            "db_data": lists,
            "total_records": counts,
            "total_pages": total_pages,
            "page": page,
            "per_page": per_page,
            "filters": filters,
            "initial": initial
        }


    @staticmethod
    def ana_list():                 #引数：companyname,page
        """Params for listed_info"""
        config = Analysisparams.config()
        info = Tl.info_table  # table_info
        per_page = config["per_page"]
        page = request.args.get("page", 1, type=int)
        with Session() as session:  # セッション開始
            #  HTTPリクエストからcompanynameを取得
            companyname_query = request.args.get("companyname", "").strip()
            # 初期表示時は空の結果を返す
            is_initial_request = not bool(request.args.get("companyname", "").strip())
            if is_initial_request or not request.args.get("companyname", "").strip():
                lists = []
                counts = 0
                total_pages = 0
                page = 1
                initial = 1         # initial:1
            else:
                # 曖昧検索用にワイルドカードを追加
                wildcard_companyname = f"%{companyname_query}%"
                # cord_queryと一致するレコードの全columnを選択
                base_query = select(info.c).where(info.c.companyname.like(wildcard_companyname))
                print(f"SQL Query: {base_query}")
                # 総レコード数を取得
                # pylint: disable=not-callable
                count_query = select(func.count()).select_from(base_query.subquery())
                # base_queryをサブクエリとし、その結果の行数をカウント
                counts = session.execute(count_query).scalar()
                # オフセット計算
                offset = (page - 1) * per_page
                # ページネーションをオフセット値と１ページ当りのレコード数より設定
                paginated_query = base_query.offset(offset).limit(per_page)
                # sqlalchemyクエリを実行し、全レコードを取得
                lists = session.execute(paginated_query).fetchall()
                # トータルページ数の計算
                total_pages = ceil(counts / per_page)
                initial = 0
            filters = companyname_query
        # 掲示板のパラメータ
        params = Analysisparams.params(lists,counts,total_pages,page,per_page,filters,initial)
        return params


    @staticmethod
    def filter1():                 #引数：companyname,page
        """Params for listed_info"""
        config = Analysisparams.config()
        info = Tl.info_table  # table_info
        per_page = config["per_page"]
        page = request.args.get("page", 1, type=int)
        with Session() as session:  # セッション開始
            #  HTTPリクエストからcompanynameを取得
            filter_query1 = request.args.get("filter1", "").strip()
            # 初期表示時は空の結果を返す
            # print(filter_query1)
            is_initial_request = not bool(request.args.get("filter1", "").strip())
            if is_initial_request or not request.args.get("filter1", "").strip():
                lists = []
                counts = 0
                total_pages = 0
                page = 1
                initial = 1         # initial:1
            else:
                # 曖昧検索用にワイルドカードを追加
                condition1 = text(filter_query1)
                base_query = select(info.c).where(condition1)
                print(f"SQL Query: {base_query}")
                # 総レコード数を取得
                # pylint: disable=not-callable
                count_query = select(func.count()).select_from(base_query.subquery())
                # base_queryをサブクエリとし、その結果の行数をカウント
                counts = session.execute(count_query).scalar()
                # オフセット計算
                offset = (page - 1) * per_page
                # ページネーションをオフセット値と１ページ当りのレコード数より設定
                paginated_query = base_query.offset(offset).limit(per_page)
                # sqlalchemyクエリを実行し、全レコードを取得
                lists = session.execute(paginated_query).fetchall()
                # トータルページ数の計算
                total_pages = ceil(counts / per_page)
                initial = 0
            filters = filter_query1
        # 掲示板のパラメータ
        params = Analysisparams.params(lists,counts,total_pages,page,per_page,filters,initial)
        return params


    @staticmethod
    def filter2():                 #引数：companyname,page
        """Params for listed_info"""
        config = Analysisparams.config()
        endpoint = "analysis.filter2"
        marketcode_query = "0111"
        end_day = datetime.strptime("2024-6-14", "%Y-%m-%d").date()
        start_day = end_day - timedelta(days=40)
        per_page = config["per_page"]
        page = request.args.get("page", 1, type=int)
        with Session() as session:  # セッション開始
            #  HTTPリクエストからcompanynameを取得
            filter_query2 = request.args.get("filter2", "").strip()
            # 初期表示時は空の結果を返す
            print(filter_query2)
            print(f"page1: {page}")

            is_initial_request = not bool(request.args.get("filter2", "").strip())
            if is_initial_request or not request.args.get("filter2", "").strip():
                lists = []
                counts = 0
                total_pages = 0
                page = 1
                initial = 1         # initial:1
            else:
                subquery = (select(
                        Tl.company.code,
                        Tl.company.companyname,
                        Tl.company.marketcode,
                    ).where(and_(
                        Tl.company.marketcode == marketcode_query,
                    )).subquery()
                )
                subquery2 = (select(
                        Tl.daily.code,
                        Tl.daily.date,
                        Tl.daily.adjustmentclose,
                        VT.moving_average_deviation(20)[0].label('ma_20'),  # 20日移動平均を計算
                        VT.moving_average_deviation(20)[1].label('deviation_rate')
                    ).where(and_(
                        Tl.daily.date >= start_day,
                        Tl.daily.date <= end_day
                    )).subquery()
                )
                # print(f"subquery: {subquery}")
                base_query = (select(subquery.c.code, subquery.c.companyname,subquery2.c.deviation_rate)
                        .join(subquery2, subquery.c.code == subquery2.c.code)
                        .where(subquery2.c.adjustmentclose > subquery2.c.ma_20 * 1.1)
                        .where(subquery2.c.date == end_day)
                        .group_by(subquery2.c.deviation_rate)
                        .order_by(desc('deviation_rate'))
                )
                # 総レコード数を取得
                # pylint: disable=not-callable
                count_query = select(func.count()).select_from(base_query.subquery())
                # base_queryをサブクエリとし、その結果の行数をカウント
                counts = session.execute(count_query).scalar()
                # オフセット計算
                offset = (page - 1) * per_page
                # ページネーションをオフセット値と１ページ当りのレコード数より設定
                paginated_query = base_query.offset(offset).limit(per_page)
                # sqlalchemyクエリを実行し、全レコードを取得
                lists = session.execute(paginated_query).fetchall()
                # トータルページ数の計算
                total_pages = ceil(counts / per_page)
                initial = 0

            filters = filter_query2
        # 掲示板のパラメータ
        params = {
            "head_title": config["head_title"],
            "header_title": config["header_title"],
            "endpoint": endpoint,
            "return_url": config["return_url"],
            "return_name": config["return_name"],
            "db_data": lists,
            "total_records": counts,
            "total_pages": total_pages,
            "page": page,
            "per_page": per_page,
            "filters": filters,
            "initial": initial
        }

        return params


    @staticmethod
    def filtermix():
        """Params for listed_info BBS"""
        info = Tl.info_table  # table_info
        head_title = "Report:Listed_Info"  # head_info
        header_title = "上場銘柄一覧 (Listed_Info)"  # header_info
        endpoint = "rpt.info_list2"  # self-endpoint
        return_url = "rpt.main"  # return-endpoint
        return_name = "レポートに戻る"  # return_name
        page = request.args.get("page", 1, type=int)
        per_page = 15
        lists = []
        counts = 0
        total_pages = 0
        page = 1
        initial = 1         # initial:1
        companyname_query = "Company_Name"

        config_params = {
            "head_title": head_title,
            "header_title": header_title,
            "endpoint": endpoint,
            "return_url": return_url,
            "return_name": return_name,
            "db_data": lists,
            "total_records": counts,
            "total_pages": total_pages,
            "page": page,
            "per_page": per_page,
            "companyname_query": companyname_query,
            "initial": initial
        }

        return config_params


    @staticmethod
    def info_list():
        """Params for listed_info BBS"""
        info = Tl.info_table  # table_info
        head_title = "Report:Listed_Info"  # head_info
        header_title = "上場銘柄一覧 (Listed_Info)"  # header_info
        endpoint = "rpt.info_list2"  # self-endpoint
        return_url = "rpt.main"  # return-endpoint
        return_name = "レポートに戻る"  # return_name
        page = request.args.get("page", 1, type=int)
        per_page = 15
        lists = []
        counts = 0
        total_pages = 0
        page = 1
        initial = 1         # initial:1
        companyname_query = "Company_Name"

        config_params = {
            "head_title": head_title,
            "header_title": header_title,
            "endpoint": endpoint,
            "return_url": return_url,
            "return_name": return_name,
            "db_data": lists,
            "total_records": counts,
            "total_pages": total_pages,
            "page": page,
            "per_page": per_page,
            "companyname_query": companyname_query,
            "initial": initial
        }

        return config_params
