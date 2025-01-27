"""  test_stocksdb_structure.py  stocksdbのテーブルとカラムを表示"""
from flask import redirect, url_for
from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError
from nkapp.models import Session
# from sqlalchemy import create_engine
# from nkapp.models import Tl


def table_list():
    """  データベースに接続しのテーブル・カラム確認する """
    with Session() as session:
        try:
            # データベースエンジンの作成
            # db_url = "sqlite:///data/stocks.db"  # あなたのデータベースURLに置き換えてください
            #engine = create_engine(db_url)
            # インスペクターの作成
            inspector = inspect()
            # データベース接続のテスト
            #with engine.connect() as connection:
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
        finally:
            # セッションを閉じる
            session.close()

        return redirect(url_for("set.main"))



# if __name__ == "__main__":
#    db_url = "sqlite:///data/stocks.db"  # あなたのデータベースURLに置き換えてください
#    check_database_connection(db_url)