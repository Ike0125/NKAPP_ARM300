"""  nkapp.rpt.fin01.py  """
# import datetime
from math import ceil
from datetime import datetime, timedelta, date
from flask import request
from sqlalchemy import select, func
from sqlalchemy import and_
from sqlalchemy import cast, Float
# from sqlalchemy import case, literal
from sqlalchemy.orm import aliased
from nkapp.config import Config, Reportparams
from nkapp.models import Session
from nkapp.analysis.analysis20 import Ana
from nkapp.analysis.analysis31 import A31
from .models import Tl

class FinRpt:
    """Params for Financial Statements"""

    @staticmethod
    def fin01_config():
        """Initial Params for fin01_config_parames"""
        current_time = Config.get_current_time()
        return {
            "head_title"    : "Report: Statements",
            "endpoint"      : "rpt.fin_rpt01",
            "return_url"    : "rpt.main",
            "return_name"   : "rpt.main",
            "home_url"      : "nkapp.index",
            "current_time"  : current_time,
        }


    @staticmethod
    def fin_rpt01():
        """Params for statement BBS card"""
        per_page = 1
        fin = Tl.statements
        company = Tl.company
        counts = 0
        raw_data ={}
        base_query = {}
        companyname = ""
        header_title = "財務情報"

        with Session() as db_session:  # セッション開始
            if request.method == "POST":
                stcode = request.form.get("stcode","72030")
                page   = int(request.form.get("page", 1))
                # print(f"page  : {page}")
                # 会社名
                companyname = db_session.query(company.companyname).filter(company.code == stcode).scalar()
                header_title = f"財務情報 :{stcode} -{companyname[:20]}"

                base_query = (
                    select(
                        fin.DisclosedDate,
                        fin.DisclosedTime,
                        fin.LocalCode,
                        fin.DisclosureNumber,
                        fin.TypeOfDocument,
                        fin.TypeOfCurrentPeriod,
                        fin.CurrentPeriodStartDate,
                        fin.CurrentPeriodEndDate,
                        fin.NetSales,
                        fin.OperatingProfit,
                        fin.OrdinaryProfit,
                        fin.Profit,
                        fin.EarningsPerShare,
                        fin.DilutedEarningsPerShare,
                        fin.TotalAssets,
                        fin.Equity,
                        fin.EquityToAssetRatio,
                        fin.BookValuePerShare,
                        fin.CashFlowsFromOperatingActivities,
                        fin.CashFlowsFromOperatingActivities,
                        fin.CashFlowsFromFinancingActivities,
                        fin.CashAndEquivalents,
                        fin.ForecastNetSales,
                        fin.ForecastOperatingProfit,
                        fin.ForecastOrdinaryProfit,
                        fin.ForecastProfit,
                        fin.ForecastEarningsPerShare
                    )
                    .filter(fin.LocalCode == stcode)
                    .order_by(func.to_date(fin.DisclosedDate, 'YYYY-MM-DD').desc())
                )
            # 総レコード数を取得
            # pylint: disable=not-callable
            count_query = select(func.count()).select_from(base_query.subquery())
            # base_queryをサブクエリとし、その結果の行数をカウント
            counts = db_session.execute(count_query).scalar()
            # オフセット計算
            offset = (page - 1) * per_page
            # ページネーションをオフセット値と１ページ当りのレコード数より設定
            paginated_query = base_query.offset(offset).limit(per_page)
            # クエリを実行し、全レコードを取得
            raw_data = db_session.execute(paginated_query).mappings().all()
            # print(f"stcode  : {stcode}")
            # print(f"raw data: {raw_data[:5]}")

        total_pages = ceil(counts / per_page)  # トータルページ数の計算
        info_params = {
            "db_data"       : raw_data,
            "total_records" : counts,
            "total_pages"   : total_pages,
            "page"          : page,
            "per_page"      : per_page,
            "stcode"        : stcode,
            "companyname"   : companyname,
            "header_title"  : header_title
        }
        return info_params


    @staticmethod
    def fin_rpt05():
        """Params for statement BBS list"""
        per_page = Reportparams.per_page
        fin = Tl.statements
        company = Tl.company
        counts = 0
        page = 1
        raw_data ={}
        base_query = {}
        header_title = "財務情報"
        stdate1 = ""
        stdate2 = ""
        ana_config = Ana.load_config("ana_config.json")

        with Session() as db_session:  # セッション開始

            if request.method == "POST":
                stdate1 = request.form.get("stdate1","")
                stdate2 = request.form.get("stdate2","")
                page   = int(request.form.get("page", 1))
            elif request.method == "GET":
                last_update_statements = db_session.query(func.max(Tl.statements.DisclosedDate)).scalar()
                if last_update_statements is None:
                    last_update_statements = date.today()
                    last_update_statements = last_update_statements.strftime("%Y-%m-%d")

                statements_value = datetime.strptime(last_update_statements, "%Y-%m-%d").date()
                st1_value = statements_value - timedelta(days=10)

                stdate1 = st1_value.strftime("%Y-%m-%d")
                stdate2 = last_update_statements

            header_title = f"財務情報 :{stdate1} to {stdate2}"
            subquery = A31.ana_query_mkt().subquery()
            aliased_subquery = aliased(subquery)

            base_query = (
                select(
                    fin.DisclosedDate,
                    fin.DisclosedTime,
                    fin.LocalCode,
                    fin.DisclosureNumber,
                    fin.TypeOfDocument,
                    fin.TypeOfCurrentPeriod,
                    fin.CurrentPeriodStartDate,
                    fin.CurrentPeriodEndDate,
                    fin.NetSales,
                    fin.OperatingProfit,
                    fin.OrdinaryProfit,
                    fin.Profit,
                    fin.EarningsPerShare,
                    fin.DilutedEarningsPerShare,
                    fin.TotalAssets,
                    fin.Equity,
                    fin.EquityToAssetRatio,
                    fin.BookValuePerShare,
                    fin.CashFlowsFromOperatingActivities,
                    fin.CashFlowsFromOperatingActivities,
                    fin.CashFlowsFromFinancingActivities,
                    fin.CashAndEquivalents,
                    fin.ForecastNetSales,
                    fin.ForecastOperatingProfit,
                    fin.ForecastOrdinaryProfit,
                    fin.ForecastProfit,
                    fin.ForecastEarningsPerShare,
                    aliased_subquery.c.code,
                    aliased_subquery.c.companyname,
                    # company.companyname
                )
                # .join(company, company.code == fin.LocalCode)
                .join(aliased_subquery, fin.LocalCode == aliased_subquery.c.code )
                .where(
                        and_(
                            func.to_date(fin.DisclosedDate, 'YYYY-MM-DD') >= func.to_date(stdate1, 'YYYY-MM-DD'),
                            func.to_date(fin.DisclosedDate, 'YYYY-MM-DD') <= func.to_date(stdate2, 'YYYY-MM-DD')
                        )
                    )
                .order_by(cast(func.nullif(fin.ForecastEarningsPerShare, ''), Float).desc().nulls_last())
                .order_by(func.to_date(fin.DisclosedDate, 'YYYY-MM-DD').desc())
            )
            # 総レコード数を取得
            # pylint: disable=not-callable
            count_query = select(func.count()).select_from(base_query.subquery())
            # base_queryをサブクエリとし、その結果の行数をカウント
            counts = db_session.execute(count_query).scalar()
            # オフセット計算
            offset = (page - 1) * per_page
            # ページネーションをオフセット値と１ページ当りのレコード数より設定
            paginated_query = base_query.offset(offset).limit(per_page)
            # クエリを実行し、全レコードを取得
            raw_data = db_session.execute(paginated_query).mappings().all()
            # print(f"raw data: {raw_data[:5]}")

        total_pages = ceil(counts / per_page)  # トータルページ数の計算
        info_params = {
            "db_data"       : raw_data,
            "total_records" : counts,
            "total_pages"   : total_pages,
            "page"          : page,
            "per_page"      : per_page,
            "stdate1"       : stdate1,
            "stdate2"       : stdate2,
            "header_title"  : header_title
        }
        return info_params


    @staticmethod
    def fin_rpt06():
        """Params for statement BBS list on Nkapp-main"""
        fin = Tl.statements
        company = Tl.company
        minimum_no = 5      #　ミニマム取得数
        raw_data ={}
        base_query = {}
        stdate1 = ""
        stdate2 = ""

        with Session() as db_session:  # セッション開始
            if request.method == "POST":
                stdate1 = request.form.get("stdate1","")
                stdate2 = request.form.get("stdate2","")
            elif request.method == "GET":
                last_update_statements = db_session.query(func.max(Tl.statements.DisclosedDate)).scalar()
                if last_update_statements is None:
                    last_update_statements = date.today()
                    last_update_statements = last_update_statements.strftime("%Y-%m-%d")

                statements_value = datetime.strptime(last_update_statements, "%Y-%m-%d").date()
                st1_value = statements_value - timedelta(days=3)

                stdate1 = st1_value.strftime("%Y-%m-%d")
                stdate2 = last_update_statements
                # print(f"stdate1_value:{type(stdate1)}")
                # print(f"stdate2_value:{type(stdate2)}")

            base_query = (
                select(
                    fin.DisclosedDate,
                    fin.DisclosedTime,
                    fin.LocalCode,
                    fin.DisclosureNumber,
                    fin.TypeOfDocument,
                    fin.TypeOfCurrentPeriod,
                    fin.CurrentPeriodStartDate,
                    fin.CurrentPeriodEndDate,
                    fin.NetSales,
                    fin.OperatingProfit,
                    fin.OrdinaryProfit,
                    fin.Profit,
                    fin.EarningsPerShare,
                    fin.DilutedEarningsPerShare,
                    fin.TotalAssets,
                    fin.Equity,
                    fin.EquityToAssetRatio,
                    fin.BookValuePerShare,
                    fin.CashFlowsFromOperatingActivities,
                    fin.CashFlowsFromOperatingActivities,
                    fin.CashFlowsFromFinancingActivities,
                    fin.CashAndEquivalents,
                    fin.ForecastNetSales,
                    fin.ForecastOperatingProfit,
                    fin.ForecastOrdinaryProfit,
                    fin.ForecastProfit,
                    fin.ForecastEarningsPerShare,
                    company.companyname
                )
                .join(company, company.code == fin.LocalCode)
                .where(
                        and_(
                            func.to_date(fin.DisclosedDate, 'YYYY-MM-DD') >= func.to_date(stdate1, 'YYYY-MM-DD'),
                            func.to_date(fin.DisclosedDate, 'YYYY-MM-DD') <= func.to_date(stdate2, 'YYYY-MM-DD')
                        )
                    )
                .order_by(func.to_date(fin.DisclosedDate, 'YYYY-MM-DD').desc())
                .order_by(cast(func.nullif(fin.ForecastEarningsPerShare, ''), Float).desc().nulls_last())
            )
            minimum_query = base_query.limit(minimum_no)
            raw_data = db_session.execute(minimum_query).mappings().all()
        info_params = {
            "db_data2"      : raw_data,
            "stdate1"       : stdate1,
            "stdate2"       : stdate2,
        }
        return info_params
