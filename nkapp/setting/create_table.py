from sqlalchemy import create_engine
from add_models import Base

# データベース接続情報を記載
DATABASE_URL = 'postgresql://postgres:karasuyama4176@localhost:5432/nkapp_db1'


# データベースエンジンを作成
engine = create_engine(DATABASE_URL)

# テーブルを作成
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("テーブルが作成されました。")
