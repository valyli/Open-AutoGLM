# Windows 平台使用指南

本文档介绍如何在 Windows 平台上使用 AutoGLM 控制 Windows 应用程序。

## 功能特性

- ✅ 自动截取 Windows 屏幕
- ✅ 识别当前活动窗口
- ✅ 模拟鼠标点击、拖拽
- ✅ 模拟键盘输入（支持中英文）
- ✅ 启动 Windows 应用程序
- ✅ 与 Android/HarmonyOS/iOS 模式共存

## 环境准备

### 1. Python 环境

建议使用 Python 3.10 及以上版本。

### 2. 安装依赖

```bash
# 安装基础依赖
pip install -r requirements.txt
pip install -e .

# 安装 Windows 特定依赖
pip install -r requirements_windows.txt
```

或者手动安装：

```bash
pip install pyautogui mss pygetwindow pillow
```

### 3. 权限设置

Windows 10/11 可能需要：
- 关闭 UAC（用户账户控制）或以管理员身份运行
- 允许 Python 访问屏幕录制权限

## 使用方法

### 命令行模式

```bash
# 交互模式
python main.py --device-type windows --base-url http://localhost:8000/v1

# 单次任务
python main.py --device-type windows --base-url http://localhost:8000/v1 "打开记事本，输入Hello World"

# 使用第三方 API
python main.py --device-type windows --base-url https://open.bigmodel.cn/api/paas/v4 --model "autoglm-phone" --apikey "your-api-key" "打开Chrome浏览器"

# 查看支持的应用
python main.py --device-type windows --list-apps
```

### Python API

```python
from phone_agent import PhoneAgent
from phone_agent.agent import AgentConfig
from phone_agent.device_factory import DeviceType, set_device_type
from phone_agent.model import ModelConfig

# 设置为 Windows 模式
set_device_type(DeviceType.WINDOWS)

# 配置模型
model_config = ModelConfig(
    base_url="http://localhost:8000/v1",
    model_name="autoglm-phone-9b",
)

# 配置 Agent
agent_config = AgentConfig(
    max_steps=50,
    lang="cn",
    verbose=True,
)

# 创建 Agent
agent = PhoneAgent(
    model_config=model_config,
    agent_config=agent_config,
)

# 执行任务
result = agent.run("打开记事本，输入Hello Windows")
print(result)
```

## 支持的应用

默认支持以下 Windows 应用（可在 `phone_agent/config/apps_windows.py` 中自定义）：

### 浏览器
- Chrome / 谷歌浏览器
- Edge / 浏览器
- Firefox / 火狐浏览器

### Office 套件
- Word
- Excel
- PowerPoint
- Outlook

### 系统应用
- 记事本 / Notepad
- 计算器 / Calculator
- 画图 / Paint
- 资源管理器 / Explorer

### 通讯工具
- 微信 / WeChat
- QQ

### 开发工具
- VS Code / Visual Studio Code
- CMD / 命令提示符
- PowerShell

## 自定义应用路径

编辑 `phone_agent/config/apps_windows.py`：

```python
APP_PACKAGES_WINDOWS = {
    "你的应用": r"C:\Path\To\Your\App.exe",
    # 或使用命令（如果在 PATH 中）
    "Chrome": "chrome.exe",
}
```

## 可用操作

| 操作 | 说明 | Windows 实现 |
|------|------|-------------|
| `Launch` | 启动应用 | `subprocess.Popen()` |
| `Tap` | 点击 | `pyautogui.click()` |
| `Double Tap` | 双击 | `pyautogui.doubleClick()` |
| `Long Press` | 长按（右键） | `pyautogui.rightClick()` |
| `Swipe` | 滑动 | `pyautogui.drag()` |
| `Type` | 输入文本 | `pyautogui.write()` |
| `Back` | 后退 | `Alt+Left` |
| `Home` | 主页 | `Win` 键 |

## 常见问题

### 1. 鼠标/键盘操作不生效

**原因**：某些应用（如游戏、管理员权限应用）可能阻止自动化操作。

**解决方案**：
- 以管理员身份运行 Python
- 检查应用是否有反自动化保护

### 2. 中文输入乱码

**原因**：pyautogui 默认使用英文键盘布局。

**解决方案**：
- 确保系统输入法为中文
- 或修改 `windows/input.py` 使用剪贴板输入

### 3. 截图为黑屏

**原因**：某些应用使用硬件加速或 DRM 保护。

**解决方案**：
- 在应用设置中关闭硬件加速
- 使用窗口模式而非全屏

### 4. 找不到应用

**原因**：应用路径未配置或不在 PATH 中。

**解决方案**：
- 在 `apps_windows.py` 中添加完整路径
- 或将应用目录添加到系统 PATH

## 与其他平台切换

```bash
# Android
python main.py --device-type adb "打开微信"

# HarmonyOS
python main.py --device-type hdc "打开微信"

# iOS
python main.py --device-type ios "打开微信"

# Windows
python main.py --device-type windows "打开微信"
```

## 示例任务

```bash
# 办公自动化
python main.py --device-type windows "打开Word，新建文档，输入'会议纪要'"

# 浏览器操作
python main.py --device-type windows "打开Chrome，搜索Python教程"

# 文件管理
python main.py --device-type windows "打开资源管理器，进入下载文件夹"

# 系统操作
python main.py --device-type windows "打开计算器，计算123+456"
```

## 注意事项

1. **屏幕分辨率**：模型返回的坐标基于当前屏幕分辨率，切换显示器可能需要重新训练
2. **多显示器**：默认使用主显示器，多显示器支持需要额外配置
3. **安全性**：避免在敏感操作（如支付、密码输入）时使用自动化
4. **性能**：Windows 截图速度比 ADB 快，但 GUI 响应可能有延迟

## 技术架构

```
用户指令
    ↓
PhoneAgent (agent.py)
    ↓
DeviceFactory (device_factory.py)
    ↓
Windows 模块 (phone_agent/windows/)
    ├── screenshot.py  → mss (截图)
    ├── device.py      → pyautogui (鼠标/键盘)
    ├── input.py       → pyautogui (文本输入)
    └── connection.py  → 本地连接
```

## 贡献

欢迎提交 PR 添加更多 Windows 应用支持或改进功能！
