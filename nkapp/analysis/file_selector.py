import tkinter as tk
from tkinter import filedialog

def open_file_dialog():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="CSVファイルを選択してください", filetypes=[("CSVファイル", "*.csv")])
    root.destroy()
    if file_path:
        print(file_path)
    else:
        print("ファイルが選択されませんでした。")

if __name__ == "__main__":
    open_file_dialog()
