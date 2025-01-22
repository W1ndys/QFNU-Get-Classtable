import tkinter as tk
from tkinter import messagebox
from main import simulate_login, get_xls_file


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("曲阜师范大学教务系统登录")
        self.root.geometry("400x250")
        self.root.configure(bg="#f0f0f0")

        # 设置字体
        label_font = ("Arial", 12)
        entry_font = ("Arial", 10)
        button_font = ("Arial", 12, "bold")

        # 创建账号输入框
        tk.Label(root, text="账号:", font=label_font, bg="#f0f0f0").grid(
            row=0, column=0, padx=10, pady=10, sticky="e"
        )
        self.account_entry = tk.Entry(root, font=entry_font)
        self.account_entry.grid(row=0, column=1, padx=10, pady=10)

        # 创建密码输入框
        tk.Label(root, text="密码:", font=label_font, bg="#f0f0f0").grid(
            row=1, column=0, padx=10, pady=10, sticky="e"
        )
        self.password_entry = tk.Entry(root, show="*", font=entry_font)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # 创建学期输入框
        tk.Label(root, text="学期:", font=label_font, bg="#f0f0f0").grid(
            row=2, column=0, padx=10, pady=10, sticky="e"
        )
        self.semester_entry = tk.Entry(root, font=entry_font)
        self.semester_entry.grid(row=2, column=1, padx=10, pady=10)

        # 创建登录按钮
        self.login_button = tk.Button(
            root,
            text="登录并获取xls",
            font=button_font,
            bg="#4CAF50",
            fg="white",
            command=self.login,
        )
        self.login_button.grid(row=3, column=0, columnspan=2, pady=20)

    def login(self):
        user_account = self.account_entry.get()
        user_password = self.password_entry.get()
        semester = self.semester_entry.get()

        if not user_account or not user_password or not semester:
            messagebox.showwarning("输入错误", "请填写所有字段")
            return

        try:
            session, cookies = simulate_login(user_account, user_password)
            xls_file = get_xls_file(session, cookies, user_account, semester)
            if xls_file:
                messagebox.showinfo("成功", f"已成功获取 {xls_file} 文件")
            else:
                messagebox.showerror(
                    "错误", "获取xls文件失败，请检查网络连接或教务系统的可用性。"
                )
        except Exception as e:
            messagebox.showerror("登录失败", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
