"""setup_db.py"""
from sqlalchemy import create_engine, text

# データベース接続設定
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:karasuyama4176@localhost:5432/nkapp_db1'

engine = create_engine(SQLALCHEMY_DATABASE_URI)

def add_unique_constraint():
    """Set unique on database"""
    with engine.connect() as connection:
        # 一意制約を追加
        connection.execute(
            text(
                """
                ALTER TABLE daily_quotes
                ADD CONSTRAINT unique_date_code UNIQUE (date, code);
                """
            )
        )
    print("一意制約が追加されました。")

# このスクリプトを実行すると制約が追加される
if __name__ == "__main__":
    add_unique_constraint()
