"""
框架配置文件
"""
import os
import sys
from pathlib import Path

# 项目根目录 - 支持 PyInstaller 打包
if getattr(sys, 'frozen', False):
    # 打包后运行，使用 exe 所在目录
    BASE_DIR = Path(sys.executable).parent
else:
    # 开发环境，使用脚本所在目录
    BASE_DIR = Path(__file__).parent

# LLOneBot 连接配置
LLONEBOT_WS_URL = "ws://127.0.0.1:3888"
LLONEBOT_HTTP_URL = "http://127.0.0.1:3889"
LLONEBOT_TOKEN = ""  # 如果设置了 token，在这里填写

# 框架配置
FRAMEWORK_NAME = "LL_XTCAT_Bot"
FRAMEWORK_VERSION = "1.0.0"

# 目录配置
PLUGINS_DIR = BASE_DIR / "plugins"
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
CONFIG_DIR = DATA_DIR / "config"
DATABASE_DIR = DATA_DIR / "database"

# 日志配置
LOG_LEVEL = "DEBUG"  # DEBUG, INFO, WARNING, ERROR
LOG_ROTATION = "10 MB"  # 日志文件大小
LOG_RETENTION = "7 days"  # 日志保留时间

# 插件配置
PLUGIN_AUTO_RELOAD = False  # 是否自动重载插件
PLUGIN_LOAD_TIMEOUT = 10  # 插件加载超时时间（秒）

# UI 配置
UI_THEME = "dark"  # dark, light
UI_COLOR_THEME = "blue"  # blue, green, dark-blue

# 创建必要的目录
for directory in [DATA_DIR, LOGS_DIR, CONFIG_DIR, DATABASE_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
