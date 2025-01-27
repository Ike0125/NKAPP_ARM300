"""  test_daily_print_list.py  """
from flask import redirect, url_for
from flask import flash, request, session
from flask import render_template_string
# from nkapp.models import Session
from nkapp.config import Fileparams
from nkapp.models import Tl


dailyquotes    = Tl.dailyquotes
dailyquotesall = Tl.daily
listedinfo     = Tl.company
calendar       = Tl.t_calendar

class MK:
    """  mockjq_main.py  """
    @staticmethod
    def config():
        """config prams for mock test"""
        mock_dailyquotes    = session.get("mock_dailyquotes", None)
        mockbox_c_e400  = session.get("mockbox_c_e400", None)
        mockbox_c_e401  = session.get("mockbox_c_e401", None)
        mockbox_c_e403  = session.get("mockbox_c_e403", None)
        mockbox_c_e413  = session.get("mockbox_c_e413", None)
        mockbox_c_e500  = session.get("mockbox_c_e500", None)
        mock_dailyquotesall = session.get("mock_dailyquotesall", None)
        mockbox_d_e400  = session.get("mockbox_d_e400", None)
        mockbox_d_e401  = session.get("mockbox_d_e401", None)
        mockbox_d_e403  = session.get("mockbox_d_e403", None)
        mockbox_d_e413  = session.get("mockbox_d_e413", None)
        mockbox_d_e500  = session.get("mockbox_d_e500", None)
        mock_statements = session.get("mock_statements", None)
        mockbox_f_e400  = session.get("mockbox_f_e400", None)
        mockbox_f_e401  = session.get("mockbox_f_e401", None)
        mockbox_f_e403  = session.get("mockbox_f_e403", None)
        mockbox_f_e413  = session.get("mockbox_f_e413", None)
        mockbox_f_e500  = session.get("mockbox_f_e500", None)
        print(f"mock_statements:{mock_statements}")
        print(f"mock_f_e400:{mockbox_f_e400}")
        mockparams={
            "mockbox_c"     : mock_dailyquotes,
            "mockbox_c_e400"  : mockbox_c_e400,
            "mockbox_c_e401"  : mockbox_c_e401,
            "mockbox_c_e403"  : mockbox_c_e403,
            "mockbox_c_e413"  : mockbox_c_e413,
            "mockbox_c_e500"  : mockbox_c_e500,
            "mockbox_d"     : mock_dailyquotesall,
            "mockbox_d_e400"  : mockbox_d_e400,
            "mockbox_d_e401"  : mockbox_d_e401,
            "mockbox_d_e403"  : mockbox_d_e403,
            "mockbox_d_e413"  : mockbox_d_e413,
            "mockbox_d_e500"  : mockbox_d_e500,
            "mockbox_f"     : mock_statements,
            "mockbox_f_e400"  : mockbox_f_e400,
            "mockbox_f_e401"  : mockbox_f_e401,
            "mockbox_f_e403"  : mockbox_f_e403,
            "mockbox_f_e413"  : mockbox_f_e413,
            "mockbox_f_e500"  : mockbox_f_e500,
        }
        return mockparams


    @staticmethod
    def mock_jquants_api(url, headers=None, params=None, timeout=None):
        """ mock_test for kabudb.py """
        status_code = None
        MOCK_API_RESPONSE = {}
        # mock_config = Fileparams.load_config("mock_config.json")

        class MockResponse:
            """ mock response """
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                """ mock response """
                return self.json_data
        print ("mock_requests_dailyquonts: Recieved params")
        if url:                                 # url: リクエスト先のURL
            print(f"URL: {url}")
        if headers:                             # headers: HTTPヘッダー情報
            print(f"Headers: {headers}")
        if params:                              # params: クエリパラメータ
            print(f"Params: {params}")
        if timeout:                             # timeout: タイムアウト設定
            print(f"Timeout: {timeout}")
        # モックデータを定義
        if request.method == "POST":
            session["mock_dailyquotes"]     = 'mockbox_c' in request.form.getlist('ckbox')
            session["mockbox_c_e400"]  = 'mockbox_c_e400' in request.form.getlist('ckbox')
            session["mockbox_c_e401"]  = 'mockbox_c_e401' in request.form.getlist('ckbox')
            session["mockbox_c_e403"]  = 'mockbox_c_e403' in request.form.getlist('ckbox')
            session["mockbox_c_e413"]  = 'mockbox_c_e413' in request.form.getlist('ckbox')
            session["mockbox_c_e500"]  = 'mockbox_c_e500' in request.form.getlist('ckbox')

            session["mock_dailyquotesall"]  = 'mockbox_d' in request.form.getlist('ckbox')
            session["mockbox_d_e400"]  = 'mockbox_d_e400' in request.form.getlist('ckbox')
            session["mockbox_d_e401"]  = 'mockbox_d_e401' in request.form.getlist('ckbox')
            session["mockbox_d_e403"]  = 'mockbox_d_e403' in request.form.getlist('ckbox')
            session["mockbox_d_e413"]  = 'mockbox_d_e413' in request.form.getlist('ckbox')
            session["mockbox_d_e500"]  = 'mockbox_d_e500' in request.form.getlist('ckbox')

            session["mock_statements"]  = 'mockbox_f' in request.form.getlist('ckbox')
            session["mockbox_f_e400"]  = 'mockbox_f_e400' in request.form.getlist('ckbox')
            session["mockbox_f_e401"]  = 'mockbox_f_e401' in request.form.getlist('ckbox')
            session["mockbox_f_e403"]  = 'mockbox_f_e403' in request.form.getlist('ckbox')
            session["mockbox_f_e413"]  = 'mockbox_f_e413' in request.form.getlist('ckbox')
            session["mockbox_f_e500"]  = 'mockbox_f_e500' in request.form.getlist('ckbox')

        mock_dailyquotes    = session.get("mock_dailyquotes",None)
        mockbox_c_e400  = session.get("mockbox_c_e400",None)
        mockbox_c_e401  = session.get("mockbox_c_e401",None)
        mockbox_c_e403  = session.get("mockbox_c_e403",None)
        mockbox_c_e413  = session.get("mockbox_c_e413",None)
        mockbox_c_e500  = session.get("mockbox_c_e500",None)

        mock_dailyquotesall = session.get("mock_dailyquotesall",None)
        mockbox_d_e400  = session.get("mockbox_d_e400",None)
        mockbox_d_e401  = session.get("mockbox_d_e401",None)
        mockbox_d_e403  = session.get("mockbox_d_e403",None)
        mockbox_d_e413  = session.get("mockbox_d_e413",None)
        mockbox_d_e500  = session.get("mockbox_d_e500",None)

        mock_statements = session.get("mock_statements",None)
        mockbox_f_e400  = session.get("mockbox_f_e400",None)
        mockbox_f_e401  = session.get("mockbox_f_e401",None)
        mockbox_f_e403  = session.get("mockbox_f_e403",None)
        mockbox_f_e413  = session.get("mockbox_f_e413",None)
        mockbox_f_e500  = session.get("mockbox_f_e500",None)

        if mock_dailyquotes:
            MOCK_API_RESPONSE = MK.mockdata_dailyquotes()
            status_code = 200
            # print(f"status_code:{status_code}")
            flash(f"status_code:{status_code}","success")
        elif mock_dailyquotesall:
            MOCK_API_RESPONSE = MK.mockdata_dailyquotes()
            status_code = 200
            flash(f"status_code:{status_code}","success")
        elif mock_statements:
            MOCK_API_RESPONSE = MK.mockdata_statements()
            status_code = 200
            flash(f"status_code:{status_code}","success")
            print(f"{MOCK_API_RESPONSE}")
        elif mockbox_c_e400 or mockbox_d_e400 or mockbox_f_e400:
            status_code = 400
            MOCK_API_RESPONSE = {"message": "Bad Request"}
            print(f"status_code:{status_code},{MOCK_API_RESPONSE}")
            flash(f"status_code:{status_code},{MOCK_API_RESPONSE}","error")
        elif mockbox_c_e401 or mockbox_d_e401 or mockbox_f_e401:
            status_code = 401
            MOCK_API_RESPONSE = {"message": "Unauthorized/The incoming token is invalid or expired."}
            print(f"status_code:{status_code}")
            flash(f"status_code:{status_code},{MOCK_API_RESPONSE}","error")
        elif mockbox_c_e403 or mockbox_d_e403 or mockbox_f_e403:
            status_code = 403
            MOCK_API_RESPONSE = {"message": "Forbidden/Missing Authentication Token. The method or resources may not be supported."}
            print(f"status_code:{status_code}")
            flash(f"status_code:{status_code},{MOCK_API_RESPONSE}","error")
        elif mockbox_c_e413 or mockbox_d_e413 or mockbox_f_e413:
            status_code = 413
            MOCK_API_RESPONSE = {"message": ": Playload too large/Response data is too large. Specify parameters to reduce the acquired data range."}
            print(f"status_code:{status_code}")
            flash(f"status_code:{status_code},{MOCK_API_RESPONSE}","error")
        elif mockbox_c_e500 or mockbox_d_e500 or mockbox_f_e500:
            status_code = 500
            MOCK_API_RESPONSE = {"message": "Internal Server Error/Unexpected error. Please try again later."}
            print(f"status_code:{status_code}")
            flash(f"status_code:{status_code},{MOCK_API_RESPONSE}","error")
        else:
            status_code = 400
            MOCK_API_RESPONSE = {"message": "else/Bad Request"}
            print(f"status_code:{status_code}")
            flash(f"status_code:{status_code},{MOCK_API_RESPONSE}","error")
        # モックデータを返す
        return MockResponse(MOCK_API_RESPONSE, status_code)


    @staticmethod
    def mockdata_dailyquotes():
        API_RESPONSE = {
            "daily_quotes": [
                {
                    "Date": "2024-06-19",
                    "Code": "tst012",
                    "Open": 3860.0,
                    "High": 3865.0,
                    "Low": 3820.0,
                    "Close": 3865.0,
                    "UpperLimit": 0,
                    "LowerLimit": 0,
                    "Volume": 42900.0,
                    "TurnoverValue": 165224000.0,
                    "AdjustmentFactor": 1.0,
                    "AdjustmentOpen": 3860.0,
                    "AdjustmentHigh": 3865.0,
                    "AdjustmentLow": 3820.0,
                    "AdjustmentClose": 3865.0,
                    "AdjustmentVolume": 42900.0,
                }
            ]
        }
        return API_RESPONSE


    @staticmethod
    def mockdata_statements():
        API_RESPONSE = {
            "statements": [
                {
                    "DisclosedDate": "2023-01-30",
                    "DisclosedTime": "12:00:00",
                    "LocalCode": "86970",
                    "DisclosureNumber": "20230127594871",
                    "TypeOfDocument": "3QFinancialStatements_Consolidated_IFRS",
                    "TypeOfCurrentPeriod": "3Q",
                    "CurrentPeriodStartDate": "2022-04-01",
                    "CurrentPeriodEndDate": "2022-12-31",
                    "CurrentFiscalYearStartDate": "2022-04-01",
                    "CurrentFiscalYearEndDate": "2023-03-31",
                    "NextFiscalYearStartDate": "",
                    "NextFiscalYearEndDate": "",
                    "NetSales": "100529000000",
                    "OperatingProfit": "51765000000",
                    "OrdinaryProfit": "",
                    "Profit": "35175000000",
                    "EarningsPerShare": "66.76",
                    "DilutedEarningsPerShare": "",
                    "TotalAssets": "79205861000000",
                    "Equity": "320021000000",
                    "EquityToAssetRatio": "0.004",
                    "BookValuePerShare": "",
                    "CashFlowsFromOperatingActivities": "",
                    "CashFlowsFromInvestingActivities": "",
                    "CashFlowsFromFinancingActivities": "",
                    "CashAndEquivalents": "91135000000",
                    "ResultDividendPerShare1stQuarter": "",
                    "ResultDividendPerShare2ndQuarter": "26.0",
                    "ResultDividendPerShare3rdQuarter": "",
                    "ResultDividendPerShareFiscalYearEnd": "",
                    "ResultDividendPerShareAnnual": "",
                    "DistributionsPerUnit(REIT)": "",
                    "ResultTotalDividendPaidAnnual": "",
                    "ResultPayoutRatioAnnual": "",
                    "ForecastDividendPerShare1stQuarter": "",
                    "ForecastDividendPerShare2ndQuarter": "",
                    "ForecastDividendPerShare3rdQuarter": "",
                    "ForecastDividendPerShareFiscalYearEnd": "36.0",
                    "ForecastDividendPerShareAnnual": "62.0",
                    "ForecastDistributionsPerUnit(REIT)": "",
                    "ForecastTotalDividendPaidAnnual": "",
                    "ForecastPayoutRatioAnnual": "",
                    "NextYearForecastDividendPerShare1stQuarter": "",
                    "NextYearForecastDividendPerShare2ndQuarter": "",
                    "NextYearForecastDividendPerShare3rdQuarter": "",
                    "NextYearForecastDividendPerShareFiscalYearEnd": "",
                    "NextYearForecastDividendPerShareAnnual": "",
                    "NextYearForecastDistributionsPerUnit(REIT)": "",
                    "NextYearForecastPayoutRatioAnnual": "",
                    "ForecastNetSales2ndQuarter": "",
                    "ForecastOperatingProfit2ndQuarter": "",
                    "ForecastOrdinaryProfit2ndQuarter": "",
                    "ForecastProfit2ndQuarter": "",
                    "ForecastEarningsPerShare2ndQuarter": "",
                    "NextYearForecastNetSales2ndQuarter": "",
                    "NextYearForecastOperatingProfit2ndQuarter": "",
                    "NextYearForecastOrdinaryProfit2ndQuarter": "",
                    "NextYearForecastProfit2ndQuarter": "",
                    "NextYearForecastEarningsPerShare2ndQuarter": "",
                    "ForecastNetSales": "132500000000",
                    "ForecastOperatingProfit": "65500000000",
                    "ForecastOrdinaryProfit": "",
                    "ForecastProfit": "45000000000",
                    "ForecastEarningsPerShare": "85.42",
                    "NextYearForecastNetSales": "",
                    "NextYearForecastOperatingProfit": "",
                    "NextYearForecastOrdinaryProfit": "",
                    "NextYearForecastProfit": "",
                    "NextYearForecastEarningsPerShare": "",
                    "MaterialChangesInSubsidiaries": "false",
                    "SignificantChangesInTheScopeOfConsolidation": "",
                    "ChangesBasedOnRevisionsOfAccountingStandard": "false",
                    "ChangesOtherThanOnesBasedOnRevisionsOfAccountingStandard": "false",
                    "ChangesInAccountingEstimates": "true",
                    "RetrospectiveRestatement": "",
                    "NumberOfIssuedAndOutstandingSharesAtTheEndOfFiscalYearIncludingTreasuryStock": "528578441",
                    "NumberOfTreasuryStockAtTheEndOfFiscalYear": "1861043",
                    "AverageNumberOfShares": "526874759",
                    "NonConsolidatedNetSales": "",
                    "NonConsolidatedOperatingProfit": "",
                    "NonConsolidatedOrdinaryProfit": "",
                    "NonConsolidatedProfit": "",
                    "NonConsolidatedEarningsPerShare": "",
                    "NonConsolidatedTotalAssets": "",
                    "NonConsolidatedEquity": "",
                    "NonConsolidatedEquityToAssetRatio": "",
                    "NonConsolidatedBookValuePerShare": "",
                    "ForecastNonConsolidatedNetSales2ndQuarter": "",
                    "ForecastNonConsolidatedOperatingProfit2ndQuarter": "",
                    "ForecastNonConsolidatedOrdinaryProfit2ndQuarter": "",
                    "ForecastNonConsolidatedProfit2ndQuarter": "",
                    "ForecastNonConsolidatedEarningsPerShare2ndQuarter": "",
                    "NextYearForecastNonConsolidatedNetSales2ndQuarter": "",
                    "NextYearForecastNonConsolidatedOperatingProfit2ndQuarter": "",
                    "NextYearForecastNonConsolidatedOrdinaryProfit2ndQuarter": "",
                    "NextYearForecastNonConsolidatedProfit2ndQuarter": "",
                    "NextYearForecastNonConsolidatedEarningsPerShare2ndQuarter": "",
                    "ForecastNonConsolidatedNetSales": "",
                    "ForecastNonConsolidatedOperatingProfit": "",
                    "ForecastNonConsolidatedOrdinaryProfit": "",
                    "ForecastNonConsolidatedProfit": "",
                    "ForecastNonConsolidatedEarningsPerShare": "",
                    "NextYearForecastNonConsolidatedNetSales": "",
                    "NextYearForecastNonConsolidatedOperatingProfit": "",
                    "NextYearForecastNonConsolidatedOrdinaryProfit": "",
                    "NextYearForecastNonConsolidatedProfit": "",
                    "NextYearForecastNonConsolidatedEarningsPerShare": ""
                }
            ],
            "pagination_key": "value1.value2."
        }
        return API_RESPONSE
