"""  nkapp.rpt.report.py  """
# from flask import render_template
from math import ceil
from datetime import datetime, timedelta
from flask import request
from sqlalchemy import select, func
from sqlalchemy.orm import aliased
from nkapp.models import Session, Tl
from nkapp.config import Reportparams, Config


class Infoparams:
    """Params for listed_info"""
    @staticmethod
    def info_all():
        """Params for listed_info BBS"""
        # Params
        info = Tl.info_table  # table_info
        head_title = "Report:Listed_Info"  # head_info
        header_title = "上場銘柄一覧 (Listed_Info)"  # header_info
        endpoint = "rpt.info_all"  # self-endpoint
        return_url = "rpt.main"  # return-endpoint
        return_name = "レポートに戻る"  # return_name
        home_url = "nkapp.index"  # home-url
        current_time = Config.get_current_time()
        page = request.args.get("page", 1, type=int)
        per_page = Reportparams.per_page
        with Session() as session:
            counts = session.query(info).count()
            offset = (page - 1) * per_page
            stmt = select(info.c).offset(offset).limit(per_page)
            # pylint: disable=not-callable
            lists = session.execute(stmt).fetchall()
        total_pages = ceil(counts / per_page)
        info_params = {
            "head_title": head_title,
            "header_title": header_title,
            "endpoint": endpoint,
            "return_url": return_url,
            "return_name": return_name,
            "home_url": home_url,
            "db_data": lists,
            "total_records": counts,
            "total_pages": total_pages,
            "page": page,
            "per_page": per_page,
            "current_time": current_time,
        }
        # print(lists)
        return info_params

    @staticmethod
    def info_card():
        """Params for listed_info BBS"""
        # Params
        info = Tl.info_table  # table_info
        head_title = "Report:Listed_Info"  # head_info
        header_title = "上場銘柄カード (Listed_Info)"  # header_info
        endpoint = "rpt.info_card"  # self-endpoint
        return_url = "rpt.main"  # return-endpoint
        return_name = "レポートに戻る"  # return_name
        current_time = Config.get_current_time()
        page = request.args.get("page", 1, type=int)
        per_page = 1
        page = request.args.get("page", 1, type=int)
        # Data
        with Session() as session:  # セッション開始
            #  HTTPリクエストからcodeを取得
            code_query = request.args.get("code", "")
            # code_query = "15700"
            # cord_queryと一致するレコードの全columnを選択
            base_query = select(info.c).where(info.c.code == code_query)
            # 総レコード数を取得
            # pylint: disable=not-callable
            count_query = select(func.count()).select_from(base_query.subquery())
            # base_queryをサブクエリとし、その結果の行数をカウント
            counts = session.execute(count_query).scalar()
            # オフセット計算
            offset = (page - 1) * per_page
            # ページネーションをオフセット値と１ページ当りのレコード数より設定
            paginated_query = base_query.offset(offset).limit(per_page)
            # クエリを実行し、全レコードを取得
            lists = session.execute(paginated_query).fetchall()
            # トータルページ数の計算
        total_pages = ceil(counts / per_page)
        # Params for rpt.daily
        info_params = {
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
            "current_time": current_time,
        }
        # print(lists)
        return info_params

    def info_list():
        """Params for listed_info BBS"""
        info = Tl.info_table  # table_info
        head_title = "Report:Listed_Info"  # head_info
        header_title = "上場銘柄一覧 (Listed_Info)"  # header_info
        endpoint = "rpt.info_list"  # self-endpoint
        return_url = "rpt.main"  # return-endpoint
        return_name = "レポートに戻る"  # return_name
        current_time = Config.get_current_time()
        page = request.args.get("page", 1, type=int)
        per_page = Reportparams.per_page
        with Session() as session:  # セッション開始
            #  HTTPリクエストからcompanynameを取得
            companyname_query = request.args.get("companyname", "")
            # print(f"Searching for companyname: {companyname_query}")
            # 曖昧検索用にワイルドカードを追加
            wildcard_companyname = f"%{companyname_query}%"
            # cord_queryと一致するレコードの全columnを選択
            base_query = select(info.c).where(info.c.companyname.like(wildcard_companyname))
            # 総レコード数を取得
            # pylint: disable=not-callable
            count_query = select(func.count()).select_from(base_query.subquery())
            # base_queryをサブクエリとし、その結果の行数をカウント
            counts = session.execute(count_query).scalar()
            # オフセット計算
            offset = (page - 1) * per_page
            # ページネーションをオフセット値と１ページ当りのレコード数より設定
            paginated_query = base_query.offset(offset).limit(per_page)
            # クエリを実行し、全レコードを取得
            lists = session.execute(paginated_query).fetchall()
            # トータルページ数の計算
        total_pages = ceil(counts / per_page)
        info_params = {
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
            "current_time": current_time,
        }
        # print(f"Searching for companyname: {companyname_query}")
        # print(f"SQL Query: {base_query}")
        # print(f"Total count: {counts}")
        # print(f"db_data: {lists}")
        # print(f"page: {page}")
        return info_params

    def info_list2():
        """Params for listed_info BBS"""
        info = Tl.info_table  # table_info
        head_title = "Report:Listed_Info"  # head_info
        header_title = "上場銘柄一覧 (Listed_Info)"  # header_info
        endpoint = "rpt.info_list2"  # self-endpoint
        return_url = "rpt.main"  # return-endpoint
        home_url = "nkapp.index"  # home-url
        return_name = "レポートに戻る"  # return_name
        page = request.args.get("page", 1, type=int)
        per_page = 15
        with Session() as session:  # セッション開始
            #  HTTPリクエストからcompanynameを取得
            companyname_query = request.args.get("companyname", "").strip()
            # 初期表示時は空の結果を返す
            is_initial_request = not bool(request.args.get("companyname", "").strip())
            last_update_statements = session.query(func.max(Tl.statements.DisclosedDate)).scalar()
            statements_value = datetime.strptime(last_update_statements, "%Y-%m-%d").date()
            st1_value = statements_value - timedelta(days=3)

            stdate1_value = st1_value.strftime("%Y-%m-%d")
            stdate2_value = last_update_statements
            print(f"stdate1_value:{stdate1_value}")
            print(f"stdate2_value:{stdate2_value}")

            # print(f"Searching for initial_request: {is_initial_request}")
            # print(f"Request args: {request.args}")
            # print(f"Initial parameter: {request.args.get('initial')}")
            # print(f"Companyname query: '{request.args.get('companyname', '')}'")
            # print(f"Is initial request: {is_initial_request}")
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
                # 総レコード数を取得
                # pylint: disable=not-callable
                count_query = select(func.count()).select_from(base_query.subquery())
                # base_queryをサブクエリとし、その結果の行数をカウント
                counts = session.execute(count_query).scalar()
                # オフセット計算
                offset = (page - 1) * per_page
                # ページネーションをオフセット値と１ページ当りのレコード数より設定
                paginated_query = base_query.offset(offset).limit(per_page)
                # クエリを実行し、全レコードを取得
                lists = session.execute(paginated_query).fetchall()
                # トータルページ数の計算
                total_pages = ceil(counts / per_page)
                initial = 0
            info_params = {
                "head_title": head_title,
                "header_title": header_title,
                "endpoint": endpoint,
                "return_url": return_url,
                "return_name": return_name,
                "home_url": home_url,
                "db_data": lists,
                "total_records": counts,
                "total_pages": total_pages,
                "page": page,
                "per_page": per_page,
                "companyname_query": companyname_query,
                "initial": initial,
                "stdate1_value" : stdate1_value,
                "stdate2_value" : stdate2_value
            }
        # print(f"Searching for companyname: {companyname_query}")
        # print(f"SQL Query: {base_query}")
        # print(f"Total count: {counts}")
        # print(f"db_data: {lists}")
        # print(f"page: {page}")

        return info_params

    @staticmethod
    def daily():
        """Params for daily_quotes_info BBS"""
        # Params
        info = Tl.daily_table  # table_info
        head_title = "Report: Daily_Quotes"  # head_info
        header_title = "株価四本値 (Prices/Daily_Quotes)"  # header_info
        endpoint = "rpt.daily"  # self-endpoint
        return_url = "rpt.main"  # return-endpoint
        return_name = "レポートに戻る"  # return_name
        current_time = Config.get_current_time()
        page = request.args.get("page", 1, type=int)
        per_page = Reportparams.per_page
        # Data
        with Session() as session:
            counts = session.query(info).count()
            offset = (page - 1) * per_page
            stmt = select(info.c).offset(offset).limit(per_page)
            # pylint: disable=not-callable
            lists = session.execute(stmt).fetchall()
        total_pages = ceil(counts / per_page)
        # Params for rpt.daily
        info_params = {
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
            "current_time": current_time,
        }
        # print(lists)
        return info_params

    @staticmethod
    def daily_query():
        """Params for daily_quotes_info BBS"""
        # Params
        info = Tl.daily_all_table  # table_info
        head_title = "Report: Daily_Quotes_Query"  # head_info
        header_title = "検索：株価四本値 (Prices/Daily_Quotes)"  # header_info
        endpoint = "rpt.daily_query"  # self-endpoint
        return_url = "rpt.main"  # return-endpoint
        return_name = "レポートに戻る"  # return_name
        current_time = Config.get_current_time()
        per_page = Reportparams.per_page
        page = request.args.get("page", 1, type=int)
        # Data
        with Session() as session:  # セッション開始
            #  HTTPリクエストからcodeを取得
            code_query = request.args.get("code", "")
            # code_query = "15700"
            # cord_queryと一致するレコードの全columnを選択
            base_query = select(info.c).where(info.c.code == code_query)
            # 総レコード数を取得
            # pylint: disable=not-callable
            count_query = select(func.count()).select_from(base_query.subquery())
            # base_queryをサブクエリとし、その結果の行数をカウント
            counts = session.execute(count_query).scalar()
            # オフセット計算
            offset = (page - 1) * per_page
            # ページネーションをオフセット値と１ページ当りのレコード数より設定
            paginated_query = base_query.offset(offset).limit(per_page)
            # クエリを実行し、全レコードを取得
            lists = session.execute(paginated_query).fetchall()
            # トータルページ数の計算
        total_pages = ceil(counts / per_page)
        # Params for rpt.daily
        info_params = {
            "head_title": head_title,
            "header_title": header_title,
            "code_query": code_query,
            "endpoint": endpoint,
            "return_url": return_url,
            "return_name": return_name,
            "db_data": lists,
            "total_records": counts,
            "total_pages": total_pages,
            "page": page,
            "per_page": per_page,
            "current_time": current_time,
        }
        # クエリエラーはレコード数０をHTMLに送りHTML側で処理
        # print(f"Searching for code: {code_query}")
        # print(f"SQL Query: {base_query}")
        # print(f"Total count: {counts}")
        # print(f"db_data: {lists}")
        # print(f"page: {page}")
        return info_params

    @staticmethod
    def tstock_query():
        """Params for daily_quotes_info BBS"""
        # Params
        # info = Tl.daily_all_table  # table_info
        head_title = "Report: Daily_Quotes_Query"  # head_info
        header_title = "検索：株価四本値 (Prices/Daily_Quotes)"  # header_info
        endpoint = "rpt.tstock_query"  # self-endpoint
        return_url = "rpt.main"  # return-endpoint
        return_name = "レポートに戻る"  # return_name
        current_time = Config.get_current_time()
        per_page = Reportparams.per_page
        page = request.args.get("page", 1, type=int)
        # Data
        with Session() as session:  # セッション開始
            #  HTTPリクエストからcodeを取得
            code_query = request.args.get("code", "")
            # print(f"Searching for code: {code_query}")
            company = aliased(Tl.info_table)
            db = aliased(Tl.daily_all_table)

            # cord_queryと一致するレコードを結合したテーブルの全columnを選択
            base_query = (
                select(db, company)
                .join(db, company.c.code == db.c.code)
                .where(company.c.code == code_query)
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
            # クエリを実行し、全レコードを取得
            lists = session.execute(paginated_query).fetchall()
            # トータルページ数の計算
        total_pages = ceil(counts / per_page)
        # Params for rpt.daily
        info_params = {
            "head_title": head_title,
            "header_title": header_title,
            "code_query": code_query,
            "endpoint": endpoint,
            "return_url": return_url,
            "return_name": return_name,
            "db_data": lists,
            "total_records": counts,
            "total_pages": total_pages,
            "page": page,
            "per_page": per_page,
            "current_time": current_time,
        }
        # クエリエラーはレコード数０をHTMLに送りHTML側で処理
        # print(f"Sample data: {lists[:5]}")  # 最初の5つの要素を表示
        # print(f"Number of columns: {len(lists[0]) if lists else 0}")
        # print(f"Searching for code: {code_query}")
        # print(f"SQL Query: {base_query}")
        # print(f"Total count: {counts}")
        # print(f"db_data: {lists}")
        # print(f"page: {page}")
        return info_params
