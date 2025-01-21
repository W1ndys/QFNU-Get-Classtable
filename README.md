# QFNUGetClasstable

曲阜师范大学课表绕过学期限制xls导出脚本

旧版脚本：[QFNUGetClasstable v1](https://github.com/W1ndys/QFNUGetClasstable/tree/main/v1)

新版脚本使用了 [QFNULogin](https://github.com/W1ndys/QFNULogin) 的模拟登录

## 功能介绍

QFNUGetClasstable 是一个用于从曲阜师范大学教务系统下载课程表的脚本工具。通过模拟登录，用户可以越过学期限制，下载指定学期的课程表。

## 安装步骤

1. 克隆本项目到本地：

   ```bash
   git clone https://github.com/W1ndys/QFNUGetClasstable.git
   cd QFNUGetClasstable
   ```

2. 安装所需的 Python 库：

   ```bash
   pip install -r requirements.txt
   ```

3. 配置环境变量：
   - 在项目根目录下创建一个`.env`文件。
   - 添加以下内容并填写你的账号和密码：
     ```
     USER_ACCOUNT=你的账号
     USER_PASSWORD=你的密码
     ```

## 使用方法

1. 运行脚本：

   ```bash
   python main.py
   ```

2. 按照提示输入学期信息，例如：`2024-2025-1`。

3. 脚本将自动下载并保存课程表为 xls 文件。

## 快速创建和激活虚拟环境

本项目提供了用于快速创建和激活虚拟环境的脚本：

- **Windows:**

  - `create_venv_windows.bat`: 创建并激活虚拟环境，同时安装`requirements.txt`中的依赖。
  - `open_venv_terminal_windows.bat`: 打开一个新的命令提示符窗口并激活虚拟环境。

- **Linux:**
  - `create_venv_linux.sh`: 创建并激活虚拟环境，同时安装`requirements.txt`中的依赖。
  - `open_venv_terminal_linux.sh`: 打开一个新的终端窗口并激活虚拟环境。

## 注意事项

- 请确保你的账号和密码正确无误。
- 如果验证码识别错误，请重试。
- 确保网络连接正常，以便访问教务系统。

## 贡献

欢迎贡献代码！如果你有任何改进建议或发现了 bug，请提交 issue 或 pull request。

## 许可证

本项目采用 [GPL-3.0 许可证](LICENSE)。

## 联系方式

如有任何问题，请联系 [W1ndys](https://github.com/W1ndys)。
