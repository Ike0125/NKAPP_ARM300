"""  test_stocksdb_structure.py  stocksdbのテーブルとカラムを表示"""
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError


def check_database_connection(db_url):
    """  データベースに接続しのテーブル・カラム確認する """
    try:
        # データベースエンジンの作成
        # db_url = "sqlite:///data/stocks.db"  # あなたのデータベースURLに置き換えてください

        engine = create_engine(db_url)

        # インスペクターの作成
        inspector = inspect(engine)

        # データベース接続のテスト
        with engine.connect() as connection:
            # テーブル一覧の取得
            tables = inspector.get_table_names()
            print("データベース接続成功!")
            print("テーブル一覧:")
            for table in tables:
                print(f"- {table}")
                # 各テーブルのカラム情報を表示
                columns = inspector.get_columns(table)
                print("  カラム:")
                for column in columns:
                    print(f"    - {column['name']} ({column['type']})")
                print()

    except SQLAlchemyError as e:
        print(f"データベース接続エラー: {e}")


if __name__ == "__main__":
    db_url = "sqlite:///data/stocks.db"  # あなたのデータベースURLに置き換えてください
    check_database_connection(db_url)