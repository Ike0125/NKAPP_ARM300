"""   ARM300/Run.py   """
from nkapp import create_nkapp

# ロギング設定
# logging.basicConfig(
#    filename='logs/sqlalchemy.log',
#    level=logging.INFO,
#    format='%(asctime)s %(levelname)s %(message)s',
#    datefmt='%Y-%m-%d %H:%M:%S',
#    filemode='w'  # 'a'=ログの追加モード,'w'=上書き保存モード
# )
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
#  Option1: level(DEBUG,INFO,WARNING,ERROR,CRITICAL)
#  exp.: logging.basicconfig(level=logging.WARNING) default=WARNING
#  Option2: format,%(asctime)s:ログ日時,%(levelname):ログレベル,%(message):メッセージ

# アプリケーションの作成と起動
nkapp = create_nkapp()
if __name__ == "__main__":
    nkapp.run(debug=True)
    #  debug mode:True, normal mode:False
