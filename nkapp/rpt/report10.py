"""  nkapp.rpt.report.py  """
# from flask import render_template
from math import ceil
from flask import request
from sqlalchemy import select, func, desc
from sqlalchemy.orm import aliased
# from sqlalchemy.orm import Session
import pandas as pd
import numpy as np
from nkapp.config import Reportparams, Config
from nkapp.models import Session
from .models import VT,Tl


class Infoparams10:
    """Params for listed_info"""

    @staticmethod
    def tstock_query20():
        """Params for daily_quotes_info BBS"""
        # logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        # logging.basicConfig(
        #    level=logging.INFO,
        #    format='%(asctime)s - %(levelname)s - %(message)s',
        #    filename='app.log',
        #    filemode='a'
        #)
        # Params
        head_title = "Report: Daily_Quotes_Query"  # head_info
        header_title = "検索：株価四本値 (Prices/Daily_Quotes)"  # header_info
        endpoint = "rpt.tstock_query20"  # self-endpoint
        return_url = "rpt.main"  # return-endpoint
        return_name = "レポートに戻る"  # return_name
        current_time = Config.get_current_time()
        per_page = Reportparams.per_page
        page = request.args.get("page", 1, type=int)

        # Data
        with Session() as session:
            code_query = request.args.get("code", "")
            if code_query == "":  # Error処理
                raw_data = []
                counts = 0
                total_pages = 0
                page = 1
            else:
                # 検索
                filters = Tl.daily.code == code_query if code_query else None
                base_query = VT.tstock(filters)
                # 総レコード数を取得
                # pylint: disable=not-callable
                count_query = select(func.count()).select_from(base_query.subquery())
                counts = session.scalar(count_query)
                # print(base_query)
            if counts == 0:  # Error処理
                raw_data = []
                counts = 0
                total_pages = 0
                page = 1
            else:
                # Pagination
                offset = (page - 1) * per_page
                paginated_query = base_query.offset(offset).limit(per_page)
                paginated_query = paginated_query.order_by(desc('date'))
                # Execute query
                raw_data = session.execute(paginated_query).mappings().all()

        total_pages = ceil(counts / per_page)
        # データの整形
        formatted_data = []
        columns_to_format = [
            "adjustmentopen",
            "adjustmenthigh",
            "adjustmentlow",
            "adjustmentclose",
            "adjustmentvolume",
            "turnovervalue",
        ]
        for row in raw_data:
            row_dict = dict(row)
            for col in columns_to_format:
                if col in row_dict and row_dict[col] is not None:
                    row_dict[col] = f"{row_dict[col]:,}"  # 千桁区切り表示
                # if 'code' in row_dict and row_dict['code'] is not None:
                #    row_dict['code'] = str(row_dict['code'])[:-1]  # codeを４文字表示
            formatted_data.append(row_dict)
        lists = formatted_data
        # print(f"Sample data: {lists[:5]}")  # 最初の5つの要素を表示

        # for data in formatted_data[:5]:
        #    print(data)
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
        return info_params

    # def max_counter(counter):
    #     mcount = counter
    @staticmethod
    def tstock_query11():
        """Params for daily_quotes_info BBS"""
        # Params
        # info = Tl.daily_all_table  # table_info
        head_title = "Report: Daily_Quotes_Query"  # head_info
        header_title = "検索：株価四本値 (Prices/Daily_Quotes)"  # header_info
        endpoint = "rpt.tstock_query11"  # self-endpoint
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
            daily = aliased(Tl.daily_all_table)

            # cord_queryと一致するレコードを結合したテーブルの全columnを選択
            base_query = (
                select(daily, company)
                .join(daily, company.c.code == daily.c.code)
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
            paginated_query = paginated_query.order_by(desc('date'))
            # クエリを実行し、全レコードを取得
            raw_data = session.execute(paginated_query).mappings().all()
            # for data in raw_data[:5]:
            #    print(data)
            #    print(counts)
        total_pages = ceil(counts / per_page)  # トータルページ数の計算
        # データの整形
        formatted_data = []
        columns_to_format = [
            "adjustmentopen",
            "adjustmenthigh",
            "adjustmentlow",
            "adjustmentclose",
            "adjustmentvolume",
            "turnovervalue",
        ]
        for row in raw_data:
            row_dict = dict(row)
            for col in columns_to_format:
                if col in row_dict and row_dict[col] is not None:
                    row_dict[col] = f"{row_dict[col]:,}"  # 千桁区切り表示
                # if 'code' in row_dict and row_dict['code'] is not None:
                #    row_dict['code'] = str(row_dict['code'])[:-1]  # codeを４文字表示
            formatted_data.append(row_dict)
        lists = formatted_data
        # for data in formatted_data[:5]:
        #    print(data)
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

    @staticmethod
    def tstock_query10():
        """Params for daily_quotes_info BBS"""
        # Params
        head_title = "Report: Daily_Quotes_Query"
        header_title = "検索：株価四本値 (Prices/Daily_Quotes)"
        endpoint = "rpt.tstock_query10"
        return_url = "rpt.main"
        return_name = "レポートに戻る"
        current_time = Config.get_current_time()
        per_page = Reportparams.per_page
        page = request.args.get("page", 1, type=int)
        # Data
        with Session() as session:
            code_query = request.args.get("code", "")
            if code_query == "":
                raw_data = pd.DataFrame()
                counts = 0
                total_pages = 0
                page = 1
            else:
                # SQLAlchemyを使用してクエリを構築
                ma_05 = VT.moving_average(5)
                ma_20 = VT.moving_average(20)
                ma_50 = VT.moving_average(50)
                filters = Tl.daily.code == code_query if code_query else None
                base_query = VT.tstock(filters, ma_05, ma_20, ma_50)
                # base_query = VT.tstock(filters)
                                # 総レコード数を取得
                # pylint: disable=not-callable
                count_query = select(func.count()).select_from(base_query.subquery())
                counts = session.scalar(count_query)
                if counts == 0:
                    raw_data = pd.DataFrame()
                    counts = 0
                    total_pages = 0
                    page = 1
                else:
                    # SQLAlchemyクエリをSQL文字列に変換
                    # sql_query = str(
                    #    base_query.compile(compile_kwargs={"literal_binds": True})
                    # )
                    result = session.execute(base_query)
                    # Fetch all results
                    data = result.fetchall()
                    # Get column names from the result
                    columns = result.keys()
                    # Convert to pandas DataFrame
                    df = pd.DataFrame(data, columns=columns)
                    # 降順にソート
                    df = df.sort_values(by='date', ascending=False)
                    # df = pd.read_sql(sql_query, engine)
                    # Pagination
                    total_pages = ceil(counts / per_page)
                    offset = (page - 1) * per_page
                    raw_data = df.iloc[offset: offset + per_page]
        # データの整形
        columns_to_format = [
            "adjustmentopen", "adjustmenthigh", "adjustmentlow",
            "adjustmentclose", "adjustmentvolume", "turnovervalue",
            "moving_average_5", "moving_average_20", "moving_average_50"
        ]
        raw_data = raw_data.copy()  # pandasにコピーを明示
        for col in columns_to_format:
            if col in raw_data.columns:
                raw_data[col] = raw_data[col].apply(
                    lambda x: f"{x:,.1f}" if pd.notnull(x) and not np.isnan(x) else "-"
                )
        lists = raw_data.to_dict("records")
        # print(f"Sample data: {lists[:5]}")  # 最初の5つの要素を表示
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
        return info_params
