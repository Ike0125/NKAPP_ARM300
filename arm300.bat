@echo off
cd C:\Users\Ichizo\OneDrive\ARM300

rem 仮想環境をActivateするためのバッチファイルを起動
call C:\Users\Ichizo\OneDrive\ARM300\env\Scripts\activate.bat

rem python.exeでスクリプトを実行
python C:\Users\Ichizo\OneDrive\ARM300\run.py

rem コマンドプロンプトの画面を残す場合
pause