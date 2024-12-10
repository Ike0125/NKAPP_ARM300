""" token.py    """
from datetime import datetime
import requests
from flask import redirect, url_for, flash, request, render_template
from nkapp.api.config import Config
from nkapp.api.jq_main import APJQ


#  config = load_config()
#  save_config(config)


def get_token_request(request):
    """
    POSTリクエストからリフレッシュトークンを使用してIDトークンを取得し、ヘッダーを返す。

    :param request: Flaskのリクエストオブジェクト
    :return: 認証ヘッダーまたはリダイレクトレスポンス
    """
    if request.method == "POST":
        try:
            # JQ APIにリクエストを送信してIDトークンを取得
            config_data = APJQ.load_config()  # config.jsonを読み込む
            refresh_token = config_data.get("REFRESH_TOKEN")
            res = requests.post(
                f"{Config.JQ_Token_URL}?refreshtoken={refresh_token}",
                timeout=10,
            )
            print(f"リクエストが送信されました。ステータスコード: {res.status_code}")
            res.raise_for_status()  # ステータスコードのチェックを追加
            id_token = res.json().get("idToken")

            if id_token:
                # IDトークンと取得日時をconfig.jsonに保存
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                config_data = APJQ.load_config()
                config_data["ID_TOKEN"] = id_token
                config_data["ID_TOKEN_TIMESTAMP"] = timestamp
                APJQ.save_config(config_data)
            else:
                print("IDトークンがレスポンスに含まれていません")  # デバッグ用のprint文
                raise ValueError("IDトークンがレスポンスに含まれていません")

            status_code = res.status_code
            status_message = res.json().get("message", "Success")

            return redirect(url_for("api.jq_main"))

        except requests.exceptions.RequestException as e:
            status_code = res.status_code if res else "Unknown"
            status_message = res.json().get("message", str(e)) if res else str(e)
        except ValueError as e:
            status_code = res.status_code if res else "Unknown"
            status_message = res.json().get("message", str(e)) if res else str(e)
        except Exception as e:
            status_code = "Unknown"
            status_message = str(e)
        return render_template(
            "jq_main.html",
            status_code=status_code,
            status_message=status_message,
        )


def save_refresh_token():
    """
    POSTリクエストから新しいリフレッシュトークンを取得し、設定に保存する。

    :return: リダイレクトレスポンス
    """
    new_refresh_token = request.form.get("refresh_token")
    if new_refresh_token:
        config_data = load_config()
        config_data["REFRESH_TOKEN"] = new_refresh_token
        config_data["REFRESH_TOKEN_TIMESTAMP"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        save_config(config_data)
        flash("リフレッシュトークンが正常に更新されました。", "success")
    else:
        flash("リフレッシュトークンの入力が無効です。", "error")
    return redirect(url_for("api.jq_main"))
