from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.text import LabelBase
from kivy.uix.image import Image
import requests
from PIL import Image as PILImage
from io import BytesIO
from captcha_ocr import get_ocr_res
import os
from dotenv import load_dotenv

load_dotenv()

RandCodeUrl = "http://zhjw.qfnu.edu.cn/verifycode.servlet"
loginUrl = "http://zhjw.qfnu.edu.cn/Logon.do?method=logonLdap"
dataStrUrl = "http://zhjw.qfnu.edu.cn/Logon.do?method=logon&flag=sess"

# 注册字体
LabelBase.register(name="SimHei", fn_regular="SimHei.ttf")


class MyGridLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyGridLayout, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 10
        self.background_color = (0.9, 0.9, 0.9, 1)  # 更亮的背景色

        self.label = Label(
            text="欢迎使用成绩查询系统",
            font_size=28,
            font_name="SimHei",
            size_hint=(1, 0.2),
            color=(0.3, 0.3, 0.3, 1),  # 更亮的字体颜色
        )
        self.add_widget(self.label)

        grid = GridLayout(cols=2, spacing=10, size_hint=(1, 0.6))

        grid.add_widget(
            Label(text="账号", font_name="SimHei", color=(0.3, 0.3, 0.3, 1))
        )
        self.account_input = TextInput(
            hint_text="请输入账号",
            multiline=False,
            font_name="SimHei",
            background_color=(1, 1, 1, 1),
        )
        grid.add_widget(self.account_input)

        grid.add_widget(
            Label(text="密码", font_name="SimHei", color=(0.3, 0.3, 0.3, 1))
        )
        self.password_input = TextInput(
            hint_text="请输入密码",
            multiline=False,
            password=True,
            font_name="SimHei",
            background_color=(1, 1, 1, 1),
        )
        grid.add_widget(self.password_input)

        grid.add_widget(
            Label(text="学期", font_name="SimHei", color=(0.3, 0.3, 0.3, 1))
        )
        self.semester_input = TextInput(
            hint_text="例如：2024-2025-1",
            multiline=False,
            font_name="SimHei",
            background_color=(1, 1, 1, 1),
        )
        grid.add_widget(self.semester_input)

        self.add_widget(grid)

        self.button = Button(
            text="登录并获取文件",
            size_hint=(1, 0.2),
            font_name="SimHei",
            background_color=(0.3, 0.7, 0.9, 1),  # 明亮的按钮颜色
            color=(1, 1, 1, 1),  # 白色字体
        )
        self.button.bind(on_press=self.on_button_click)
        self.add_widget(self.button)

        # 添加版权信息
        self.copyright_label = Label(
            text="2025 W1ndys. All rights reserved.",
            font_size=12,
            font_name="SimHei",
            size_hint=(1, 0.1),
            color=(0.3, 0.3, 0.3, 1),
        )
        self.add_widget(self.copyright_label)

    def on_button_click(self, instance):
        user_account = self.account_input.text
        user_password = self.password_input.text
        semester = self.semester_input.text

        if not user_account or not user_password:
            self.show_popup("错误", "请输入账号和密码")
            return

        try:
            session, cookies = self.simulate_login(user_account, user_password)
            if session and cookies:
                xls_file = self.get_xls_file(session, cookies, user_account, semester)
                if xls_file:
                    self.show_popup("成功", f"已成功获取 {xls_file} 文件")
                else:
                    self.show_popup(
                        "错误", "获取xls文件失败，请检查网络连接或教务系统的可用性。"
                    )
        except Exception as e:
            self.show_popup("错误", str(e))

    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message, font_name="SimHei"),
            size_hint=(0.8, 0.4),
        )
        popup.open()

    def get_initial_session(self):
        session = requests.session()
        response = session.get(dataStrUrl, timeout=1000)
        cookies = session.cookies.get_dict()
        return session, cookies, response.text

    def handle_captcha(self, session, cookies):
        response = session.get(RandCodeUrl, cookies=cookies)
        if response.status_code != 200:
            self.show_popup("错误", f"请求验证码失败，状态码: {response.status_code}")
            return None

        try:
            image = PILImage.open(BytesIO(response.content))
        except Exception as e:
            self.show_popup("错误", f"无法识别图像文件: {e}")
            return None

        return get_ocr_res(image)

    def generate_encoded_string(self, data_str, user_account, user_password):
        res = data_str.split("#")
        code, sxh = res[0], res[1]
        data = f"{user_account}%%%{user_password}"
        encoded = ""
        b = 0

        for a in range(len(code)):
            if a < 20:
                encoded += data[a]
                for _ in range(int(sxh[a])):
                    encoded += code[b]
                    b += 1
            else:
                encoded += data[a:]
                break
        return encoded

    def login(
        self, session, cookies, user_account, user_password, random_code, encoded
    ):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
            "Origin": "http://zhjw.qfnu.edu.cn",
            "Referer": "http://zhjw.qfnu.edu.cn/",
            "Upgrade-Insecure-Requests": "1",
        }

        data = {
            "userAccount": user_account,
            "userPassword": user_password,
            "RANDOMCODE": random_code,
            "encoded": encoded,
        }

        return session.post(
            loginUrl, headers=headers, data=data, cookies=cookies, timeout=1000
        )

    def simulate_login(self, user_account, user_password):
        session, cookies, data_str = self.get_initial_session()

        for attempt in range(3):
            random_code = self.handle_captcha(session, cookies)
            if not random_code:
                continue
            encoded = self.generate_encoded_string(
                data_str, user_account, user_password
            )
            response = self.login(
                session, cookies, user_account, user_password, random_code, encoded
            )

            if response.status_code == 200:
                if "验证码错误!!" in response.text:
                    self.show_popup("错误", f"验证码识别错误，重试第 {attempt + 1} 次")
                    continue
                if "密码错误" in response.text:
                    raise Exception("用户名或密码错误")
                return session, cookies
            else:
                raise Exception("登录失败")

        raise Exception("验证码识别错误，请重试")

    def get_xls_file(self, session, cookies, user_account, semester):
        url = f"http://zhjw.qfnu.edu.cn/jsxsd/xskb/xskb_print.do?xnxq01id={semester}"
        response = session.get(url, cookies=cookies, timeout=1000)
        if response.status_code != 200:
            self.show_popup(
                "错误",
                f"获取xls文件失败，状态码: {response.status_code}，错误信息: {response.text}",
            )
            return None
        file_path = f"{user_account}-{semester}.xls"
        with open(file_path, "wb") as f:
            f.write(response.content)
        return file_path


class MyApp(App):
    def build(self):
        self.title = "教务系统成绩查询 by W1ndys | QQ2769731875"  # 设置程序名称
        return MyGridLayout()


if __name__ == "__main__":
    MyApp().run()
