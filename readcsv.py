import pandas as pd
from tkinter import Tk, filedialog

# ファイル選択ダイアログを開く
root = Tk()
root.withdraw()  # Tkinterウィンドウを非表示にする
file_path = filedialog.askopenfilename(title="CSVファイルを選択してください", filetypes=[("CSVファイル", "*.csv")])

# ファイルが選択されなかった場合の処理
if not file_path:
    print("ファイルが選択されませんでした。")
else:
    # CSVファイルを読み込む
    data = pd.read_csv(file_path)

    # 先頭10行を出力
    print(data.head(10))
