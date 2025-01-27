from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# データベースエンジンの設定
engine = create_engine('postgresql://postgres:karasuyama4176@localhost:5432/nkapp_db1')

# ベースクラスの定義
Base = declarative_base()

# テーブル定義のサンプル
class ExampleTable(Base):
    __tablename__ = 'example_table'
    id = Column(Integer, primary_key=True)
    name = Column(String)

# テーブルの確認
print(Base.metadata.tables.keys())
print("Currently registered tables in MetaData:")