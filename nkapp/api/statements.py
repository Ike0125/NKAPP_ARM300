""" statements.py """
import time
from datetime import datetime, timedelta
from time import sleep
import requests
from flask import flash, request, session
from flask import redirect, url_for
from sqlalchemy.orm import Session
from nkapp.config import Mainparams
from nkapp.models import Statements
from nkapp.models import engine
from nkapp.api.config import Config
from nkapp.api.api_main import AP
from nkapp.set.mockjq_main import MK


class JQST:
    """ Updating Statements Information """
    @staticmethod
    def get_statements(mode):
        """
        指定した日付の株価データを取得し、ページング管理を含めて保存する。
        APIで取得したデータをデータベースに保存。
        mode 1 : statements, data check なし
        mode 9 : Mock Tests
        """
        # トークン取得
        config_data = AP.load_config()
        id_token = config_data.get("ID_TOKEN")
        headers = {"Authorization": f"Bearer {id_token}"}
        base_url = Config.JQ_Statements_URL
        main_params = Mainparams.get_main_params()
        current_day  = datetime.now().date()
        update_gap = 0

        if request.method == "POST":
            st_date_start = request.form.get("st_date1","2024-01-01")
            st_date_end = request.form.get("st_date2","2024-01-01")
            session["st_date_start"] = st_date_start
            session["st_date_end"] = st_date_end

            try:
                date_start_obj = datetime.strptime(st_date_start, "%Y-%m-%d").date()
                date_end_obj   = datetime.strptime(st_date_end, "%Y-%m-%d").date()
                last_update_statements   = main_params["last_update_statements"]
                start_statements         = main_params["start_statements"]
                last_update_statements = datetime.strptime(last_update_statements, "%Y-%m-%d").date()
                start_statements = datetime.strptime(start_statements, "%Y-%m-%d").date()
                #start_statements = None
                if start_statements is None:
                    last_update_statements = current_day-timedelta(days=update_gap)
                    start_statements = last_update_statements-timedelta(days=(5*365))
                else:
                    if (date_start_obj <= last_update_statements) and (date_end_obj >= start_statements):
                        flash(f"Input Date for mode 8or 9 between {date_start_obj} & {date_end_obj} is out of range.", "error" )
                        return redirect(url_for("api.api_main"))

            except ValueError:
                flash("Invalid date format. Please use YYYY-MM-DD.", "error")
                return None
            date_obj = date_start_obj
            start_time = time.time()
            print(f"Starting data retrieval process...:{start_time}")

            while date_obj <= date_end_obj:
                date_obj_str = date_obj.strftime("%Y-%m-%d")
                params = {"date": date_obj_str}
                print(f"date_obj:{date_obj}")
                print(f"date_end_obj:{date_end_obj}")
                start_time2 = time.time()
                # データ取得
                response = JQST.fetch_statements(base_url, headers, params, mode, max_retries=1, retry_delay=3)
                if response is None:
                    return redirect(url_for("api.api_main"))  # 処理停止し掲示板に戻る
                # データ保存
                db_commit = JQST.save_to_db_statements(response)

                if db_commit is False:
                    return redirect(url_for("api.api_main"))  # 処理停止し掲示板に戻る

                date_obj = date_obj + timedelta(days=1)
                elapsed_time2 = time.time() - start_time2
                print(f"Data retrieval and storage : {date_obj} in {elapsed_time2:.2f} seconds.")
                # APIのリクエスト制限を考慮して少し待機
                sleep(0.1)  # 必要に応じて調整
            elapsed_time = time.time() - start_time
            print(f"Data retrieval and storage completed successfully in {elapsed_time:.2f} seconds.")
            flash(f"Updated {date_start_obj} to {date_end_obj} in {elapsed_time:.2f} seconds.", "success")


    @staticmethod
    def fetch_statements(base_url, headers, params, mode, max_retries=2, retry_delay=3):
        """
        指定された銘柄コードリストに基づいてデータを取得。
        APIで取得したデータをデータベースに保存。
        mode 1 : statements, data check なし
        mode 9 : Mock Tests
        """
        retries = 0

        while retries <= max_retries:
            try:
                response_data = []  # 全データを格納するリスト
                while True:
                    if mode == 9:    # mock test
                        # APIリクエスト(モックテスト)
                        r_get = MK.mock_jquants_api(
                            base_url, headers=headers, params=params, timeout=10,
                        )
                        print(f"r_get:{r_get.json()}")

                    elif mode == 1:
                        # APIリクエスト
                        # print(f"params: {params}")
                        r_get = requests.get(base_url, headers=headers, params=params, timeout=10)
                        response = r_get.json()
                        response_data += response.get("statements", [])
                        while "pagination_key" in response_data:
                            pagination_key = response_data["pagination_key"]
                            params["pagination_key"] = pagination_key
                            r_get = requests.get(base_url, headers=headers, params=params, timeout=10)
                            next_page_data = r_get.json()
                            response_data += next_page_data["statements",[]]
                            print(f"pagination_key{pagination_key}")

                    else:
                        print("Modeが設定されていません")
                        raise Exception

                    if r_get.status_code == 200:
                        print(f"status:{r_get.status_code}")
                        # print(f"response_data:{response_data}")
                        return response_data  # JSON全体を返す（ページングキーも含む）
                    elif r_get.status_code in [400, 401, 403, 413]:
                        flash(f"{r_get.status_code}: {r_get.json().get('message', 'Unknown Error')}", "error")
                        return None  # 処理を終了させるため None を返す
                    elif r_get.status_code >= 500:
                        print(f"Server Error {r_get.status_code}: Retrying...")
                        retries += 1
                        if retries > max_retries:
                            flash(f"Server error after {retries} retries: {r_get.status_code}", "error")
                            return None
                        time.sleep(retry_delay)
                        continue
            except Exception as e:  # 不明なエラーを包括的に処理
                flash(f"Unknown error: {str(e)}", "error")
                return


    @staticmethod
    def save_to_db_statements(response):
        """
        APIで取得したデータをデータベースに保存。
        """
        db_commit = False
        with Session(engine) as db_session:
            try:
                for item in response:
                    new_statement = Statements(
                            DisclosedDate   = item["DisclosedDate"],
                            DisclosedTime   = item["DisclosedTime"],
                            LocalCode       = item["LocalCode"],
                            DisclosureNumber  = item["DisclosureNumber"],
                            TypeOfDocument          = item["TypeOfDocument"],
                            TypeOfCurrentPeriod     = item["TypeOfCurrentPeriod"],
                            CurrentPeriodStartDate  = item["CurrentPeriodStartDate"],
                            CurrentPeriodEndDate    = item["CurrentPeriodEndDate"],
                            CurrentFiscalYearStartDate  = item["CurrentFiscalYearStartDate"],
                            CurrentFiscalYearEndDate    = item["CurrentFiscalYearEndDate"],
                            NextFiscalYearStartDate     = item["NextFiscalYearStartDate"],
                            NextFiscalYearEndDate       = item["NextFiscalYearEndDate"],
                            NetSales                = item["NetSales"],
                            OperatingProfit         = item["OperatingProfit"],
                            OrdinaryProfit          = item["OrdinaryProfit"],
                            Profit                  = item["Profit"],
                            EarningsPerShare        = item["EarningsPerShare"],
                            DilutedEarningsPerShare = item["DilutedEarningsPerShare"],
                            TotalAssets             = item["TotalAssets"],
                            Equity                  = item["Equity"],
                            EquityToAssetRatio      = item["EquityToAssetRatio"],
                            BookValuePerShare       = item["BookValuePerShare"],
                            CashFlowsFromOperatingActivities = item["CashFlowsFromOperatingActivities"],
                            CashFlowsFromInvestingActivities = item["CashFlowsFromInvestingActivities"],
                            CashFlowsFromFinancingActivities = item["CashFlowsFromFinancingActivities"],
                            CashAndEquivalents               = item["CashAndEquivalents"],
                            ResultDividendPerShare1stQuarter = item["ResultDividendPerShare1stQuarter"],
                            ResultDividendPerShare2ndQuarter = item["ResultDividendPerShare2ndQuarter"],
                            ResultDividendPerShare3rdQuarter = item["ResultDividendPerShare3rdQuarter"],
                            ResultDividendPerShareFiscalYearEnd= item["ResultDividendPerShareFiscalYearEnd"],
                            ResultDividendPerShareAnnual     = item["ResultDividendPerShareAnnual"],
                            DistributionsPerUnit_REIT       = item["DistributionsPerUnit(REIT)"],
                            ResultTotalDividendPaidAnnual    = item["ResultTotalDividendPaidAnnual"],
                            ResultPayoutRatioAnnual          = item["ResultPayoutRatioAnnual"],
                            ForecastDividendPerShare1stQuarter    = item["ForecastDividendPerShare1stQuarter"],
                            ForecastDividendPerShare2ndQuarter    = item["ForecastDividendPerShare2ndQuarter"],
                            ForecastDividendPerShare3rdQuarter    = item["ForecastDividendPerShare3rdQuarter"],
                            ForecastDividendPerShareFiscalYearEnd = item["ForecastDividendPerShareFiscalYearEnd"],
                            ForecastDividendPerShareAnnual        = item["ForecastDividendPerShareAnnual"],
                            ForecastDistributionsPerUnit_REIT     = item["ForecastDistributionsPerUnit(REIT)"],
                            ForecastTotalDividendPaidAnnual       = item["ForecastTotalDividendPaidAnnual"],
                            ForecastPayoutRatioAnnual             = item["ForecastPayoutRatioAnnual"],
                            NextYearForecastDividendPerShare1stQuarter      = item["NextYearForecastDividendPerShare1stQuarter"],
                            NextYearForecastDividendPerShare2ndQuarter      = item["NextYearForecastDividendPerShare2ndQuarter"],
                            NextYearForecastDividendPerShare3rdQuarter      = item["NextYearForecastDividendPerShare3rdQuarter"],
                            NextYearForecastDividendPerShareFiscalYearEnd   = item["NextYearForecastDividendPerShareFiscalYearEnd"],
                            NextYearForecastDividendPerShareAnnual          = item["NextYearForecastDividendPerShareAnnual"],
                            NextYearForecastDistributionsPerUnit_REIT      = item["NextYearForecastDistributionsPerUnit(REIT)"],
                            NextYearForecastPayoutRatioAnnual   = item["NextYearForecastPayoutRatioAnnual"],
                            ForecastNetSales2ndQuarter          = item["ForecastNetSales2ndQuarter"],
                            ForecastOperatingProfit2ndQuarter   = item["ForecastOperatingProfit2ndQuarter"],
                            ForecastOrdinaryProfit2ndQuarter    = item["ForecastOrdinaryProfit2ndQuarter"],
                            ForecastProfit2ndQuarter            = item["ForecastProfit2ndQuarter"],
                            ForecastEarningsPerShare2ndQuarter  = item["ForecastEarningsPerShare2ndQuarter"],
                            NextYearForecastNetSales2ndQuarter  = item["NextYearForecastNetSales2ndQuarter"],
                            NextYearForecastOperatingProfit2ndQuarter   = item["NextYearForecastOperatingProfit2ndQuarter"],
                            NextYearForecastOrdinaryProfit2ndQuarter    = item["NextYearForecastOrdinaryProfit2ndQuarter"],
                            NextYearForecastProfit2ndQuarter            = item["NextYearForecastProfit2ndQuarter"],
                            NextYearForecastEarningsPerShare2ndQuarter  = item["NextYearForecastEarningsPerShare2ndQuarter"],
                            ForecastNetSales            = item["ForecastNetSales"],
                            ForecastOperatingProfit     = item["ForecastOperatingProfit"],
                            ForecastOrdinaryProfit      = item["ForecastOrdinaryProfit"],
                            ForecastProfit              = item["ForecastProfit"],
                            ForecastEarningsPerShare    = item["ForecastEarningsPerShare"],
                            NextYearForecastNetSales    = item["NextYearForecastNetSales"],
                            NextYearForecastOperatingProfit     = item["NextYearForecastOperatingProfit"],
                            NextYearForecastOrdinaryProfit      = item["NextYearForecastOrdinaryProfit"],
                            NextYearForecastProfit              = item["NextYearForecastProfit"],
                            NextYearForecastEarningsPerShare    = item["NextYearForecastEarningsPerShare"],
                            MaterialChangesInSubsidiaries       = item["MaterialChangesInSubsidiaries"],
                            SignificantChangesInTheScopeOfConsolidation = item["SignificantChangesInTheScopeOfConsolidation"],
                            ChangesBasedOnRevisionsOfAccountingStandard = item["ChangesBasedOnRevisionsOfAccountingStandard"],
                            ChangesOtherThanOnesBasedOnRevisionsOfAccountingStandard    = item["ChangesOtherThanOnesBasedOnRevisionsOfAccountingStandard"],
                            ChangesInAccountingEstimates    = item["ChangesInAccountingEstimates"],
                            RetrospectiveRestatement        = item["RetrospectiveRestatement"],
                            NumberOfIssuedAndOutstandingSharesAtTheEndOfFiscalYearIncludingTreasuryStock = item["NumberOfIssuedAndOutstandingSharesAtTheEndOfFiscalYearIncludingTreasuryStock"],
                            NumberOfTreasuryStockAtTheEndOfFiscalYear   = item["NumberOfTreasuryStockAtTheEndOfFiscalYear"],
                            AverageNumberOfShares                       = item["AverageNumberOfShares"],
                            NonConsolidatedNetSales                     = item["NonConsolidatedNetSales"],
                            NonConsolidatedOperatingProfit              = item["NonConsolidatedOperatingProfit"],
                            NonConsolidatedOrdinaryProfit               = item["NonConsolidatedOrdinaryProfit"],
                            NonConsolidatedProfit                       = item["NonConsolidatedProfit"],
                            NonConsolidatedEarningsPerShare             = item["NonConsolidatedEarningsPerShare"],
                            NonConsolidatedTotalAssets                  = item["NonConsolidatedTotalAssets"],
                            NonConsolidatedEquity                       = item["NonConsolidatedEquity"],
                            NonConsolidatedEquityToAssetRatio           = item["NonConsolidatedEquityToAssetRatio"],
                            NonConsolidatedBookValuePerShare            = item["NonConsolidatedBookValuePerShare"],
                            ForecastNonConsolidatedNetSales2ndQuarter   = item["ForecastNonConsolidatedNetSales2ndQuarter"],
                            ForecastNonConsolidatedOperatingProfit2ndQuarter    = item["ForecastNonConsolidatedOperatingProfit2ndQuarter"],
                            ForecastNonConsolidatedOrdinaryProfit2ndQuarter     = item["ForecastNonConsolidatedOrdinaryProfit2ndQuarter"],
                            ForecastNonConsolidatedProfit2ndQuarter             = item["ForecastNonConsolidatedProfit2ndQuarter"],
                            ForecastNonConsolidatedEarningsPerShare2ndQuarter   = item["ForecastNonConsolidatedEarningsPerShare2ndQuarter"],
                            NextYearForecastNonConsolidatedNetSales2ndQuarter   = item["NextYearForecastNonConsolidatedNetSales2ndQuarter"],
                            NextYearForecastNonConsolidatedOperatingProfit2ndQuarter    = item["NextYearForecastNonConsolidatedOperatingProfit2ndQuarter"],
                            NextYearForecastNonConsolidatedOrdinaryProfit2ndQuarter     = item["NextYearForecastNonConsolidatedOrdinaryProfit2ndQuarter"],
                            NextYearForecastNonConsolidatedProfit2ndQuarter             = item["NextYearForecastNonConsolidatedProfit2ndQuarter"],
                            NextYearForecastNonConsolidatedEarningsPerShare2ndQuarter   = item["NextYearForecastNonConsolidatedEarningsPerShare2ndQuarter"],
                            ForecastNonConsolidatedNetSales             = item["ForecastNonConsolidatedNetSales"],
                            ForecastNonConsolidatedOperatingProfit      = item["ForecastNonConsolidatedOperatingProfit"],
                            ForecastNonConsolidatedOrdinaryProfit       = item["ForecastNonConsolidatedOrdinaryProfit"],
                            ForecastNonConsolidatedProfit               = item["ForecastNonConsolidatedProfit"],
                            ForecastNonConsolidatedEarningsPerShare     = item["ForecastNonConsolidatedEarningsPerShare"],
                            NextYearForecastNonConsolidatedNetSales     = item["NextYearForecastNonConsolidatedNetSales"],
                            NextYearForecastNonConsolidatedOperatingProfit  = item["NextYearForecastNonConsolidatedOperatingProfit"],
                            NextYearForecastNonConsolidatedOrdinaryProfit   = item["NextYearForecastNonConsolidatedOrdinaryProfit"],
                            NextYearForecastNonConsolidatedProfit           = item["NextYearForecastNonConsolidatedProfit"],
                            NextYearForecastNonConsolidatedEarningsPerShare = item["NextYearForecastNonConsolidatedEarningsPerShare"],
                    )
                    db_session.add(new_statement)
                db_session.commit()
                db_commit = True
                return db_commit

            except ValueError as e:
                flash(f"{str(e)}","error")
