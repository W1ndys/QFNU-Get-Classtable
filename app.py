from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os
from main import simulate_login, get_xls_file
import threading
import time

app = Flask(__name__)
app.secret_key = "your_secret_key"


def delete_file_after_delay(filename, delay):
    """在指定延迟后删除文件"""
    time.sleep(delay)
    try:
        os.remove(filename)
        print(f"文件 {filename} 已被删除")
    except Exception as e:
        print(f"删除文件 {filename} 时出错: {e}")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_account = request.form.get("user_account")
        user_password = request.form.get("user_password")
        semester = request.form.get("semester")

        try:
            session, cookies = simulate_login(user_account, user_password)
            xls_file = get_xls_file(session, cookies, user_account, semester)
            if xls_file:
                flash(f"已成功获取 {xls_file} 文件，文件将在五分钟后删除。", "success")
                # 启动后台线程在五分钟后删除文件
                threading.Thread(
                    target=delete_file_after_delay, args=(xls_file, 5)
                ).start()

                return redirect(url_for("download_file", filename=xls_file))
            else:
                flash("获取xls文件失败，请检查网络连接或教务系统的可用性。", "danger")
        except Exception as e:
            flash(str(e), "danger")

        return redirect(url_for("index"))

    return render_template("index.html")


@app.route("/download/<filename>")
def download_file(filename):
    flash("文件下载成功！", "success")
    return send_file(filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
