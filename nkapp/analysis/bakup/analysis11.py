from flask_query_builder.querying import QueryBuilder
from flask_query_builder.filters import AllowedFilter
from flask_query_builder.sorts import AllowedSort

class MADeviationFilterSet(BaseFilterSet):
    marketcode = AllowedFilter.exact('marketcode')
    date_range = AllowedFilter.custom('date_range', DateRangeFilter())
    ma_deviation = AllowedFilter.custom('ma_deviation', MADeviationFilter())
    deviation_rate = AllowedSort('deviation_rate')

class DateRangeFilter(Filter):
    def filter(self, query, model, filter_name, values):
        start_date, end_date = values
        return query.filter(and_(
            model.date >= start_date,
            model.date <= end_date
        ))

class MADeviationFilter(Filter):
    def filter(self, query, model, filter_name, values):
        window, operator, ana_param32 = values
        return query.filter(
            model.adjustmentclose.op(operator)(
                getattr(model, f"ma_{window}") * ana_param32
            )
        )

@staticmethod
def ana_query_ma(builders):
    marketcode_query = builders["selected10"]
    operator = builders["selected30"]
    ana_sort = builders["selected40"]
    window = int(builders["paramquery21"])
    day_gap = int(builders["paramquery31"])
    ana_param32 = float(builders["paramquery32"])
    key_column = builders["selected41"]

    with Session() as session:
        last_update = session.query(func.max(Tl.daily_table.c.date)).scalar()
        end_day = last_update - timedelta(days=day_gap)
        start_day = end_day - timedelta(days=window * 2)

        query = (
            QueryBuilder(Tl.daily)
            .join(Tl.company)
            .allowed_filters([
                AllowedFilter.exact('marketcode'),
                AllowedFilter.custom('date_range', DateRangeFilter()),
                AllowedFilter.custom('ma_deviation', MADeviationFilter())
            ])
            .allowed_sorts([
                AllowedSort('deviation_rate')
            ])
            .query
        )

        filter_params = {
            'marketcode': marketcode_query,
            'date_range': (start_day, end_day),
            'ma_deviation': (window, operator, ana_param32)
        }

        sort_params = [f"{'-' if ana_sort == 'desc' else ''}{key_column}"]

        filtered_query = MADeviationFilterSet(query).filter_query(filter_params)
        sorted_query = filtered_query.sort_query(sort_params)

        return sorted_query
    