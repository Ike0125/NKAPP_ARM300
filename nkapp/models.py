""" models.py """
from sqlalchemy import Column, Float, Date
from sqlalchemy import Table, Index, Integer, String, MetaData
from sqlalchemy import create_engine, Sequence, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, aliased

# PostgreSQLの接続情報
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:karasuyama4176@localhost:5432/nkapp_db1'

# エンジンの作成
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)

Base = declarative_base()
metadata = MetaData()

def create_sql_table():
    """テーブルの作成"""
    with Session() as session:
        with session.begin():
            Base.metadata.create_all(engine)

class ListedInfo(Base):
    """上場銘柄一覧テーブルの定義"""

    __tablename__ = "listed_info"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date = Column(Date, nullable=False)
    code = Column(String, primary_key=True, nullable=False)
    companyname = Column(String, nullable=True)
    companynameenglish = Column(String, nullable=True)
    sector17code = Column(String, nullable=True)
    sector17codename = Column(String, nullable=True)
    sector33code = Column(String, nullable=True)
    sector33codename = Column(String, nullable=True)
    scalecategory = Column(String, nullable=True)
    marketcode = Column(String, nullable=True)
    marketcodename = Column(String, nullable=True)

    __table_args__ = (
        Index('idx_listed_info_code_marketcode', 'code', 'marketcode'),
        {'extend_existing': True}
    )


class DailyQuotes(Base):
    """株価4本値テーブルの定義（選択）"""

    __tablename__ = "daily_quotes"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date = Column(Date, nullable=False)
    code = Column(String, nullable=False)
    open = Column(Float, nullable=True, default=0.0)
    high = Column(Float, nullable=True, default=0.0)
    low = Column(Float, nullable=True, default=0.0)
    close = Column(Float, nullable=True, default=0.0)
    upperlimit = Column(String, nullable=True, default="0")
    lowerlimit = Column(String, nullable=True, default="0")
    volume = Column(Float, nullable=True, default=0.0)
    turnovervalue = Column(Float, nullable=True, default=0.0)
    adjustmentfactor = Column(Float, nullable=True, default=1.0)
    adjustmentopen = Column(Float, nullable=True, default=0.0)
    adjustmenthigh = Column(Float, nullable=True, default=0.0)
    adjustmentlow = Column(Float, nullable=True, default=0.0)
    adjustmentclose = Column(Float, nullable=True, default=0.0)
    adjustmentvolume = Column(Float, nullable=True, default=0.0)

    __table_args__ = (
        UniqueConstraint('date', 'code', name='unique_date_code'),
    )


class DailyQuotesAll(Base):
    """株価4本値テーブルの定義（一括）"""

    __tablename__ = "daily_quotes_all"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date = Column(Date, nullable=False)
    code = Column(String, nullable=False)
    open = Column(Float, nullable=True, default=0.0)
    high = Column(Float, nullable=True, default=0.0)
    low = Column(Float, nullable=True, default=0.0)
    close = Column(Float, nullable=True, default=0.0)
    upperlimit = Column(String, nullable=True, default="0")
    lowerlimit = Column(String, nullable=True, default="0")
    volume = Column(Float, nullable=True, default=0.0)
    turnovervalue = Column(Float, nullable=True, default=0.0)
    adjustmentfactor = Column(Float, nullable=True, default=1.0)
    adjustmentopen = Column(Float, nullable=True, default=0.0)
    adjustmenthigh = Column(Float, nullable=True, default=0.0)
    adjustmentlow = Column(Float, nullable=True, default=0.0)
    adjustmentclose = Column(Float, nullable=True, default=0.0)
    adjustmentvolume = Column(Float, nullable=True, default=0.0)

    __table_args__ = (
        Index('idx_daily_quotes_all_code_date', 'code', 'date'),
        {'extend_existing': True}
    )


# シーケンスを定義し、開始値を10000に設定
trade_date_no_seq = Sequence('trade_date_no_seq', start=10000)
class TradingCalendar(Base):
    """計算用取引カレンダー"""

    __tablename__ = "trading_calendar"

    id            = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    tradingdate   = Column(Date, nullable=False)
    trade_date_no = Column(Integer, trade_date_no_seq, server_default=trade_date_no_seq.next_value())


class JqTradingCalendar(Base):
    """J-Quants 取引カレンダー"""

    __tablename__ = "jq_trading_calendar"

    id              = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date            = Column(Date, nullable=False)
    holidaydivision = Column(String, nullable=False)


class Statements(Base):
    """ J-Quants 財務情報 """

    __tablename__ = "statements"
    id                      = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    DisclosedDate           = Column(String, nullable=False)
    DisclosedTime           = Column(String, nullable=False)
    LocalCode               = Column(String, nullable=False)
    DisclosureNumber        = Column(String, nullable=False)
    TypeOfDocument          = Column(String, nullable=False)
    TypeOfCurrentPeriod     = Column(String, nullable=False)
    CurrentPeriodStartDate  = Column(String, nullable=False)
    CurrentPeriodEndDate    = Column(String, nullable=False)
    CurrentFiscalYearStartDate  = Column(String, nullable=False)
    CurrentFiscalYearEndDate    = Column(String, nullable=False)
    NextFiscalYearStartDate     = Column(String, nullable=False)
    NextFiscalYearEndDate       = Column(String, nullable=False)
    NetSales                = Column(String, nullable=False)
    OperatingProfit         = Column(String, nullable=False)
    OrdinaryProfit          = Column(String, nullable=False)
    Profit                  = Column(String, nullable=False)
    EarningsPerShare        = Column(String, nullable=False)
    DilutedEarningsPerShare = Column(String, nullable=False)
    TotalAssets             = Column(String, nullable=False)
    Equity                  = Column(String, nullable=False)
    EquityToAssetRatio      = Column(String, nullable=False)
    BookValuePerShare       = Column(String, nullable=False)
    CashFlowsFromOperatingActivities = Column(String, nullable=False)
    CashFlowsFromInvestingActivities = Column(String, nullable=False)
    CashFlowsFromFinancingActivities = Column(String, nullable=False)
    CashAndEquivalents               = Column(String, nullable=False)
    ResultDividendPerShare1stQuarter = Column(String, nullable=False)
    ResultDividendPerShare2ndQuarter = Column(String, nullable=False)
    ResultDividendPerShare3rdQuarter = Column(String, nullable=False)
    ResultDividendPerShareFiscalYearEnd= Column(String, nullable=False)
    ResultDividendPerShareAnnual     = Column(String, nullable=False)
    DistributionsPerUnit_REIT       = Column(String, nullable=False)
    ResultTotalDividendPaidAnnual    = Column(String, nullable=False)
    ResultPayoutRatioAnnual          = Column(String, nullable=False)
    ForecastDividendPerShare1stQuarter    = Column(String, nullable=False)
    ForecastDividendPerShare2ndQuarter    = Column(String, nullable=False)
    ForecastDividendPerShare3rdQuarter    = Column(String, nullable=False)
    ForecastDividendPerShareFiscalYearEnd = Column(String, nullable=False)
    ForecastDividendPerShareAnnual        = Column(String, nullable=False)
    ForecastDistributionsPerUnit_REIT    = Column(String, nullable=False)
    ForecastTotalDividendPaidAnnual       = Column(String, nullable=False)
    ForecastPayoutRatioAnnual             = Column(String, nullable=False)
    NextYearForecastDividendPerShare1stQuarter      = Column(String, nullable=False)
    NextYearForecastDividendPerShare2ndQuarter      = Column(String, nullable=False)
    NextYearForecastDividendPerShare3rdQuarter      = Column(String, nullable=False)
    NextYearForecastDividendPerShareFiscalYearEnd   = Column(String, nullable=False)
    NextYearForecastDividendPerShareAnnual          = Column(String, nullable=False)
    NextYearForecastDistributionsPerUnit_REIT      = Column(String, nullable=False)
    NextYearForecastPayoutRatioAnnual   = Column(String, nullable=False)
    ForecastNetSales2ndQuarter          = Column(String, nullable=False)
    ForecastOperatingProfit2ndQuarter   = Column(String, nullable=False)
    ForecastOrdinaryProfit2ndQuarter    = Column(String, nullable=False)
    ForecastProfit2ndQuarter            = Column(String, nullable=False)
    ForecastEarningsPerShare2ndQuarter  = Column(String, nullable=False)
    NextYearForecastNetSales2ndQuarter  = Column(String, nullable=False)
    NextYearForecastOperatingProfit2ndQuarter   = Column(String, nullable=False)
    NextYearForecastOrdinaryProfit2ndQuarter    = Column(String, nullable=False)
    NextYearForecastProfit2ndQuarter            = Column(String, nullable=False)
    NextYearForecastEarningsPerShare2ndQuarter  = Column(String, nullable=False)
    ForecastNetSales            = Column(String, nullable=False)
    ForecastOperatingProfit     = Column(String, nullable=False)
    ForecastOrdinaryProfit      = Column(String, nullable=False)
    ForecastProfit              = Column(String, nullable=False)
    ForecastEarningsPerShare    = Column(String, nullable=False)
    NextYearForecastNetSales    = Column(String, nullable=False)
    NextYearForecastOperatingProfit     = Column(String, nullable=False)
    NextYearForecastOrdinaryProfit      = Column(String, nullable=False)
    NextYearForecastProfit              = Column(String, nullable=False)
    NextYearForecastEarningsPerShare    = Column(String, nullable=False)
    MaterialChangesInSubsidiaries       = Column(String, nullable=False)
    SignificantChangesInTheScopeOfConsolidation = Column(String, nullable=False)
    ChangesBasedOnRevisionsOfAccountingStandard = Column(String, nullable=False)
    ChangesOtherThanOnesBasedOnRevisionsOfAccountingStandard    = Column(String, nullable=False)
    ChangesInAccountingEstimates    = Column(String, nullable=False)
    RetrospectiveRestatement        = Column(String, nullable=False)
    NumberOfIssuedAndOutstandingSharesAtTheEndOfFiscalYearIncludingTreasuryStock    = Column(String, nullable=False)
    NumberOfTreasuryStockAtTheEndOfFiscalYear   = Column(String, nullable=False)
    AverageNumberOfShares                       = Column(String, nullable=False)
    NonConsolidatedNetSales                     = Column(String, nullable=False)
    NonConsolidatedOperatingProfit              = Column(String, nullable=False)
    NonConsolidatedOrdinaryProfit               = Column(String, nullable=False)
    NonConsolidatedProfit                       = Column(String, nullable=False)
    NonConsolidatedEarningsPerShare             = Column(String, nullable=False)
    NonConsolidatedTotalAssets                  = Column(String, nullable=False)
    NonConsolidatedEquity                       = Column(String, nullable=False)
    NonConsolidatedEquityToAssetRatio           = Column(String, nullable=False)
    NonConsolidatedBookValuePerShare            = Column(String, nullable=False)
    ForecastNonConsolidatedNetSales2ndQuarter   = Column(String, nullable=False)
    ForecastNonConsolidatedOperatingProfit2ndQuarter    = Column(String, nullable=False)
    ForecastNonConsolidatedOrdinaryProfit2ndQuarter     = Column(String, nullable=False)
    ForecastNonConsolidatedProfit2ndQuarter             = Column(String, nullable=False)
    ForecastNonConsolidatedEarningsPerShare2ndQuarter   = Column(String, nullable=False)
    NextYearForecastNonConsolidatedNetSales2ndQuarter   = Column(String, nullable=False)
    NextYearForecastNonConsolidatedOperatingProfit2ndQuarter    = Column(String, nullable=False)
    NextYearForecastNonConsolidatedOrdinaryProfit2ndQuarter     = Column(String, nullable=False)
    NextYearForecastNonConsolidatedProfit2ndQuarter             = Column(String, nullable=False)
    NextYearForecastNonConsolidatedEarningsPerShare2ndQuarter   = Column(String, nullable=False)
    ForecastNonConsolidatedNetSales             = Column(String, nullable=False)
    ForecastNonConsolidatedOperatingProfit      = Column(String, nullable=False)
    ForecastNonConsolidatedOrdinaryProfit       = Column(String, nullable=False)
    ForecastNonConsolidatedProfit               = Column(String, nullable=False)
    ForecastNonConsolidatedEarningsPerShare     = Column(String, nullable=False)
    NextYearForecastNonConsolidatedNetSales     = Column(String, nullable=False)
    NextYearForecastNonConsolidatedOperatingProfit  = Column(String, nullable=False)
    NextYearForecastNonConsolidatedOrdinaryProfit   = Column(String, nullable=False)
    NextYearForecastNonConsolidatedProfit           = Column(String, nullable=False)
    NextYearForecastNonConsolidatedEarningsPerShare = Column(String, nullable=False)


class Announcement(Base):
    """ J-Quants 決算発表予定日 """

    __tablename__ = "announcement"

    id            = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    Date          = Column(String, nullable=False)
    Code          = Column(String, nullable=False)
    CompanyName   = Column(String, nullable=False)
    FiscalYear    = Column(String, nullable=False)
    SectorName    = Column(String, nullable=False)
    FiscalQuarter = Column(String, nullable=False)
    Section       = Column(String, nullable=False)


class Tl:
    """Table Lists"""

    info_table = Table("listed_info", metadata, autoload_with=engine)
    daily_table = Table("daily_quotes", metadata, autoload_with=engine)
    daily_all_table = Table("daily_quotes_all", metadata, autoload_with=engine)
    t_calendar = Table("trading_calendar", metadata, autoload_with=engine)
    jq_calendar = Table("jq_trading_calendar", metadata, autoload_with=engine)
    statements_table = Table("statements", metadata, autoload_with=engine)
    announcement_table = Table("announcement", metadata, autoload_with=engine)

    current_db = SQLALCHEMY_DATABASE_URI
    company = aliased(ListedInfo)
    daily = aliased(DailyQuotesAll)
    dailyquotes = aliased(DailyQuotes)
    tcalendar = aliased(TradingCalendar)
    jqcalendar = aliased(JqTradingCalendar)
    announcement = aliased(Announcement)
    statements = aliased(Statements)
