""" Creating Charts / report11.py """
from datetime import datetime
import io
import base64
import pandas as pd
import mplfinance as mpf
import matplotlib
import matplotlib.pyplot as plt
from flask import request
from sqlalchemy import and_
from nkapp.models import Session
from .models import Tl, VT

matplotlib.use("Agg")
plt.rcParams["font.family"] = "MS Gothic"  # または 'IPAexGothic'


class Chartparams:
    """Create Chat Params """
    @classmethod
    def get_chart(cls,code=None):
        """株価データ取得とろうそく足グラフ作成"""
        with Session() as session:
            # リクエストからcodeを取得
            chart_range = 120  # チャートの表示期間
            chart_margin = 60  # チャート開始日のマージン
            days_range = chart_range + chart_margin  # データ取得期間
            code = request.args.get("code", "")
            if code:
                # 現在の日付を取得
                # end_date = datetime.now().date()
                end_date = datetime.strptime("2024-05-31", "%Y-%m-%d").date()
                # 指定された日数分前の日付を計算
                # start_date = end_date - timedelta(days=days_range)
                start_date = datetime.strptime("2023-10-15", "%Y-%m-%d").date()
                ma_05 = VT.moving_average(5)
                ma_20 = VT.moving_average(20)
                ma_50 = VT.moving_average(50)
                # フィルター条件に日付範囲を追加
                filters = and_(
                    Tl.daily.code == code,
                    Tl.daily.date >= start_date,
                    Tl.daily.date <= end_date,
                )
                base_query = VT.tstock(filters, ma_05, ma_20, ma_50)
                # Execute the query using the session
                result = session.execute(base_query)
                # Fetch all results
                data = result.fetchall()
                # Get column names from the result
                columns = result.keys()
                # Convert to pandas DataFrame
                df = pd.DataFrame(data, columns=columns)
                # データが存在しない場合のエラーハンドリング
                if df.empty:
                    chart_params = ({"error": "No code provided"}), 400
                    return chart_params
                # ここでグラフ作成の処理を行う
                # ろうそく足グラフの作成
                df = df.rename(
                    columns={
                        "adjustmentopen": "Open",
                        "adjustmenthigh": "High",
                        "adjustmentlow": "Low",
                        "adjustmentclose": "Close",
                        "adjustmentvolume": "Volume",
                    }
                )
                df = df.copy()      # E1137 does not support item assignment対応
                df["date"] = pd.to_datetime(df["date"])
                df.set_index("date", inplace=True)
                df = df[
                    [
                        "Open",
                        "High",
                        "Low",
                        "Close",
                        "Volume",
                        "moving_average_5",
                        "moving_average_20",
                        "moving_average_50",
                    ]
                ]

                # カスタムのFigureとAxesの作成
                _, (ax, ax_vol) = plt.subplots(
                    2,
                    1,
                    figsize=(10, 8),
                    gridspec_kw={"height_ratios": [4, 1]},
                    sharex=True,
                )

                # タイトルをメインのローソク足のAxesに設定
                ax.set_title(f"Candle Chart: {code}")
                ax_vol.set_xlabel("Date")  # 出来高グラフのX軸にラベルを設定

                # 凡例の表示
                ax.legend(loc="upper left")

                # ローソク足のX軸ラベルを非表示にする
                ax.xaxis.set_visible(False)
                # グリッドの追加（等間隔）
                ax.grid(True, which="both", linestyle="--", linewidth=0.5, color="gray")
                ax_vol.grid(
                    True, which="both", linestyle="--", linewidth=0.5, color="gray"
                )

                # 移動平均線の追加（addplotを使用）
                moving_average_plot_01 = mpf.make_addplot(
                    df["moving_average_5"],
                    ax=ax,
                    color=(0, 0, 1, 0.3),  # 青色の透明度を30%に設定
                    linestyle="-",
                    width=0.8,  # 線の太さを0.8に設定
                    label="5-day MA",
                )
                moving_average_plot_02 = mpf.make_addplot(
                    df["moving_average_20"],
                    ax=ax,
                    color=(0, 1, 0, 0.3),  # 青色の透明度を30%に設定
                    linestyle="-",
                    width=0.8,  # 線の太さを0.8に設定
                    label="20-day MA",
                )
                moving_average_plot_03 = mpf.make_addplot(
                    df["moving_average_50"],
                    ax=ax,
                    color=(1, 0, 0, 0.1),  # 青色の透明度を30%に設定
                    linestyle="-",
                    width=0.8,  # 線の太さを0.8に設定
                    label="50-day MA",
                )
                mpf.plot(
                    df,
                    type="candle",
                    style="yahoo",
                    addplot=[
                        moving_average_plot_01,
                        moving_average_plot_02,
                        moving_average_plot_03,
                    ],  # 移動平均線を追加
                    volume=ax_vol,
                    xlim=("2023-12-01", "2024-5-31"),
                    ax=ax,
                    datetime_format="%Y-%m-%d",  # 日付フォーマットを指定
                    xrotation=45  # X軸ラベルを45度回転
                )

                # グリッドの追加（等間隔）
                ax.grid(True, which="both", linestyle="--", linewidth=0.5, color="gray")
                ax_vol.grid(
                    True, which="both", linestyle="--", linewidth=0.5, color="gray"
                )

                # グラフをバイトストリームに保存
                img = io.BytesIO()
                plt.savefig(img, format="png")
                img.seek(0)

                # Base64エンコード
                graph = base64.b64encode(img.getvalue()).decode()
                # For BBS params
                chart_params = {
                    "graph": graph,  # Base64エンコードされたグラフ画像
                    "code": code,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d"),
                    "days_range": days_range,
                }
                return chart_params
            else:
                chart_params = ({"error": "No code provided"}), 400
                return chart_params
