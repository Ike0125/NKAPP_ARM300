""" models.py """
from sqlalchemy import select
from sqlalchemy import func, case, Numeric, cast
from nkapp.models import Tl


class VT:
    """Combined table with daily_quotes_all and listed_info"""
    def __init__(self, date, daily_code, adjustmentopen, adjustmenthigh,
               adjustmentlow, adjustmentclose, adjustmentvolume,
               turnovervalue, upperlimit, lowerlimit, companyname,
               company_code
               ):
        self.date = date
        self.code = daily_code
        self.adjustmentopen = adjustmentopen
        self.adjustmenthigh = adjustmenthigh
        self.adjustmentlow = adjustmentlow
        self.adjustmentclose = adjustmentclose
        self.adjustmentvolume = adjustmentvolume
        self.turnovervalue = turnovervalue
        self.upperlimit = upperlimit
        self.lowerlimit = lowerlimit
        self.companyname = companyname
        self.companycode = company_code

    @classmethod
    def tstock(cls, filters=None, *derived_columns):
        """Query for Combining tables"""
        # print(f"Filters: {filters}")  # デバッグ出力
        base_columns = [
            Tl.daily.date,
            Tl.daily.code.label('daily_code'),
            Tl.daily.adjustmentopen,
            Tl.daily.adjustmenthigh,
            Tl.daily.adjustmentlow,
            Tl.daily.adjustmentclose,
            Tl.daily.adjustmentvolume,
            Tl.daily.turnovervalue,
            Tl.daily.upperlimit,
            Tl.daily.lowerlimit,
            Tl.company.code.label('company_code'),
            Tl.company.companyname,
            Tl.company.marketcode
        ]
        query = select(*(base_columns + list(derived_columns)))
        query = query.join(Tl.company, Tl.daily.code == Tl.company.code)
        if filters is not None:
        #    query = query.where(filters).order_by(desc(Tl.daily.date))
            query = query.where(filters)
        # print(query.compile(compile_kwargs={"literal_binds": True}))
        return query

    @staticmethod
    def moving_average(window):
        """移動平均を計算する関数を返す"""
        return func.avg(Tl.daily.adjustmentclose).over(
            partition_by=Tl.daily.code,
            order_by=Tl.daily.date,
            rows=(-(window-1), 0)
        ).label(f'moving_average_{window}')


    @staticmethod
    def deviation_rate(price_column, ma_column):
        """乖離率を計算する関数を返す。0除算の場合はNULLを返す"""
        return case(
            (ma_column == 0, None),  # 移動平均が0の場合はNULL
            else_=(
                cast(
                    (price_column - ma_column) / ma_column * 100,
                    Numeric(10, 2)
                )
            )
        ).label('deviation_rate')

    @staticmethod
    def moving_average_deviation(window):
        """移動平均と乖離率を計算する関数を返す"""
        ma = VT.moving_average(window)
        return (
            ma,
            VT.deviation_rate(Tl.daily.adjustmentclose, ma)
        )


    @staticmethod
    def rsi(period=14):
        """RSIを計算する関数を返す"""
        # サブクエリ1：price_changeを計算
        subquery1 = select(
            Tl.daily.code.label('code'),
            Tl.daily.date.label('date'),
            Tl.daily.adjustmentclose.label('adjustmentclose'),
            (
                Tl.daily.adjustmentclose - func.lag(Tl.daily.adjustmentclose).over(
                    partition_by=Tl.daily.code,
                    order_by=Tl.daily.date
                )
            ).label('price_change')
        ).subquery('subquery1')
        # print(f"subquery1: {subquery1}")
        # サブクエリ2：gainとlossを計算
        subquery2 = select(
            subquery1.c.code,
            subquery1.c.date,
            subquery1.c.adjustmentclose,
            case(
                (subquery1.c.price_change > 0, subquery1.c.price_change),
                else_=0
            ).label('gain'),
            func.abs(
                case(
                    (subquery1.c.price_change < 0, subquery1.c.price_change),
                    else_=0
                )
            ).label('loss')
        ).subquery('subquery2')
        # print(f"subquery2: {subquery2}")
        # サブクエリ3：avg_gainとavg_lossを計算
        subquery3 = select(
            subquery2.c.code,
            subquery2.c.date,
            subquery2.c.adjustmentclose,
            subquery2.c.gain,
            subquery2.c.loss,
            func.avg(subquery2.c.gain).over(
                partition_by=subquery2.c.code,
                order_by=subquery2.c.date,
                rows=(-(period - 1), 0)
            ).label('avg_gain'),
            func.avg(subquery2.c.loss).over(
                partition_by=subquery2.c.code,
                order_by=subquery2.c.date,
                rows=(-(period - 1), 0)
            ).label('avg_loss')
        ).subquery('subquery3')
        # print(f"subquery3: {subquery3}")
        # 最終クエリ：RSとRSIを計算
        rs = case(
            (subquery3.c.avg_loss != 0, subquery3.c.avg_gain / subquery3.c.avg_loss),
            else_=0
        ).label('rs')

        rsi = (100 - (100 / (1 + rs))).label(f'rsi_{period}')

        final_query = select(
            subquery3.c.code,
            subquery3.c.date,
            subquery3.c.adjustmentclose,
            rsi
        ).select_from(subquery3)
        # print(f"final_query: {final_query}")
        return final_query


    @staticmethod
    def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
        """Calculate MACD, Signal line and Histogram"""
        # Calculate short-term and long-term EMAs
        short_ema = data['adjustmentclose'].ewm(span=short_window, adjust=False).mean()
        long_ema = data['adjustmentclose'].ewm(span=long_window, adjust=False).mean()

        # Calculate MACD line
        macd_line = short_ema - long_ema

        # Calculate Signal line
        signal_line = macd_line.ewm(span=signal_window, adjust=False).mean()

        # Calculate Histogram
        histogram = macd_line - signal_line

        return macd_line, signal_line, histogram

    @classmethod
    def tstock30(cls, *derived_columns, filters=None):
        """Query for Combining tables"""
        # print(f"Filters: {filters}")  # デバッグ出力
        base_columns = [
            Tl.daily.date,
            Tl.daily.code.label('daily_code'),
            Tl.daily.adjustmentopen,
            Tl.daily.adjustmenthigh,
            Tl.daily.adjustmentlow,
            Tl.daily.adjustmentclose,
            Tl.daily.adjustmentvolume,
            Tl.daily.turnovervalue,
            Tl.daily.upperlimit,
            Tl.daily.lowerlimit,
            Tl.company.code.label('company_code'),
            Tl.company.companyname,
        ]
        query = select(*(base_columns + list(derived_columns)))
        query = query.join(Tl.company, Tl.daily.code == Tl.company.code)
        if filters is not None:
            query = query.where(filters)
        # print(query.compile(compile_kwargs={"literal_binds": True}))
        return query

