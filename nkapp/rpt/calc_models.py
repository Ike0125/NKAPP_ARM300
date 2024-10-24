""" calc_models.py """
from sqlalchemy import select
import pandas as pd

class 
def calculate_moving_average():
    stmt = select(StockPrice)
    data = session.scalars(stmt).all()
    df = pd.DataFrame([{'date': row.date, 'close': row.close} for row in data])
    df = df.sort_values(by='date')
    df['ma_5'] = df['close'].rolling(window=5).mean()
    df['ma_10'] = df['close'].rolling(window=10).mean()

    for index, row in df.iterrows():
        stock = session.get(StockPrice, row['date'])
        stock.ma_5 = row['ma_5']
        stock.ma_10 = row['ma_10']
    session.commit()
