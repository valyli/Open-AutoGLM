# 桌面环境配置指南

本文档介绍如何在 macOS、Windows 和 Linux 上配置和使用 Open-AutoGLM 的桌面自动化功能。

## 概述

Open-AutoGLM 现在支持桌面自动化，可以控制 Windows、macOS 和 Linux 系统上的桌面应用程序。通过视觉语言模型理解屏幕内容，自动执行点击、输入、滑动等操作。

## 环境准备

### 1. Python 环境

建议使用 Python 3.10 及以上版本。

### 2. 安装桌面依赖

```bash
# 安装桌面自动化依赖
pip install -r requirements_desktop.txt

# 或者手动安装
pip install pyautogui mss pygetwindow pillow
```

### 3. 系统权限配置

#### macOS

1. **辅助功能权限**：
   - 打开 `系统偏好设置` > `安全性与隐私` > `隐私` > `辅助功能`
   - 添加你的终端应用（Terminal、iTerm2 等）和 Python
   - 确保这些应用已被勾选启用

2. **屏幕录制权限**：
   - 打开 `系统偏好设置` > `安全性与隐私` > `隐私` > `屏幕录制`
   - 添加你的终端应用和 Python
   - 确保这些应用已被勾选启用

#### Windows

1. **UAC 设置**：
   - 建议以管理员权限运行命令提示符或 PowerShell
   - 或者降低 UAC 级别以减少权限提示

2. **防病毒软件**：
   - 某些防病毒软件可能会阻止自动化操作
   - 将 Python 和项目目录添加到白名单

#### Linux

1. **X11 权限**：
   - 确保有 X11 显示权限
   - 可能需要运行 `xhost +local:` 来允许本地连接

2. **依赖包**：
   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3-tk python3-dev scrot

   # CentOS/RHEL
   sudo yum install tkinter python3-devel
   ```

## 多屏幕支持

### 问题描述

在多屏幕环境中，AutoGLM 需要截图来分析屏幕内容，但默认只截取主显示器。如果目标应用在其他屏幕上，AI 将无法找到相应的按钮和界面元素。

### 解决方案

桌面版本提供了多种截图模式来解决多屏幕问题：

#### 1. 自动模式（推荐）

```bash
# 默认模式，自动检测活动窗口所在的屏幕
python main.py --device-type desktop --screenshot-mode auto "打开Safari"
```

#### 2. 全屏模式

```bash
# 截取所有屏幕的组合图像
python main.py --device-type desktop --screenshot-mode all "打开Safari"
```

#### 3. 指定屏幕模式

```bash
# 强制使用主屏幕
python main.py --device-type desktop --screenshot-mode primary "打开Safari"

# 强制使用第一个屏幕
python main.py --device-type desktop --screenshot-mode monitor_1 "打开Safari"

# 强制使用第二个屏幕
python main.py --device-type desktop --screenshot-mode monitor_2 "打开Safari"
```

#### 4. 环境变量配置

```bash
# 设置默认截图模式
export PHONE_AGENT_SCREENSHOT_MODE=all
python main.py --device-type desktop "打开Safari"
```

### 屏幕检测工具

```python
# 查看所有屏幕信息
from phone_agent.desktop.screenshot import list_monitors
list_monitors()
# 输出：
# Monitor 1: 1920x1080 at (0, 0)
# Monitor 2: 1512x982 at (168, 1080)

# 测试不同截图模式
from phone_agent.desktop.config import set_screenshot_mode, ScreenshotMode
from phone_agent.desktop import get_screenshot

# 全屏模式
set_screenshot_mode(ScreenshotMode.ALL)
s = get_screenshot()
print(f'全屏截图: {s.width}x{s.height}')

# 主屏模式
set_screenshot_mode(ScreenshotMode.PRIMARY)
s = get_screenshot()
print(f'主屏截图: {s.width}x{s.height}')
```

### 推荐配置

1. **开发调试时**：使用 `--screenshot-mode all` 确保能看到所有屏幕内容
2. **生产使用时**：使用 `--screenshot-mode auto` 让系统自动选择最合适的屏幕
3. **固定应用场景**：如果应用总是在特定屏幕，使用 `--screenshot-mode monitor_1` 或 `monitor_2`



桌面版本支持以下类型的应用程序：

### 浏览器
- Chrome/谷歌浏览器
- Edge/浏览器
- Firefox/火狐浏览器

### Office 套件
- Microsoft Word
- Microsoft Excel
- Microsoft PowerPoint
- Microsoft Outlook

### 系统应用
- 记事本/Notepad
- 计算器/Calculator
- 画图/Paint
- 资源管理器/Explorer

### 通讯软件
- 微信/WeChat
- QQ

### 开发工具
- VS Code/Visual Studio Code
- 命令提示符/CMD
- PowerShell

### 自定义应用

你可以在 `phone_agent/config/apps_desktop.py` 中添加更多应用：

```python
APP_PACKAGES_DESKTOP = {
    "应用名称": "应用程序路径或命令",
    "Chrome": "chrome.exe",  # Windows
    "Chrome": "open -a 'Google Chrome'",  # macOS
    "Chrome": "google-chrome",  # Linux
}
```

## 使用方法

### 1. 命令行使用

```bash
# 桌面模式 - 交互模式
python main.py --device-type desktop --base-url http://localhost:8000/v1 --model "autoglm-phone-9b"

# 桌面模式 - 指定任务
python main.py --device-type desktop --base-url http://localhost:8000/v1 "打开Chrome浏览器搜索Python教程"

# 使用第三方模型服务
python main.py --device-type desktop --base-url https://open.bigmodel.cn/api/paas/v4 --model "autoglm-phone" --apikey "your-api-key" "打开记事本写一段文字"

# 列出支持的桌面应用
python main.py --device-type desktop --list-apps
```

### 2. Python API 使用

```python
from phone_agent import PhoneAgent
from phone_agent.model import ModelConfig
from phone_agent.agent import AgentConfig
from phone_agent.device_factory import DeviceType, set_device_type

# 设置设备类型为桌面
set_device_type(DeviceType.DESKTOP)

# 配置模型
model_config = ModelConfig(
    base_url="http://localhost:8000/v1",
    model_name="autoglm-phone-9b",
)

# 配置 Agent
agent_config = AgentConfig(
    max_steps=50,
    verbose=True,
    lang="cn",
)

# 创建 Agent
agent = PhoneAgent(
    model_config=model_config,
    agent_config=agent_config,
)

# 执行任务
result = agent.run("打开浏览器搜索天气预报")
print(result)
```

## 支持的操作

桌面版本支持以下操作：

| 操作 | 描述 | 实现方式 |
|------|------|----------|
| `Launch` | 启动应用程序 | subprocess.Popen() |
| `Tap` | 单击坐标 | pyautogui.click() |
| `Double Tap` | 双击坐标 | pyautogui.doubleClick() |
| `Long Press` | 右键点击（模拟长按） | pyautogui.rightClick() |
| `Swipe` | 拖拽操作 | pyautogui.drag() |
| `Type` | 输入文本 | pyautogui.write() |
| `Back` | 浏览器后退 | Alt+Left |
| `Home` | 显示桌面/开始菜单 | Windows/Cmd 键 |
| `Wait` | 等待 | time.sleep() |

## 测试部署

使用测试脚本验证桌面环境是否正确配置：

```bash
python scripts/test_desktop.py
```

预期输出：
```
============================================================
Desktop Module Test Suite
============================================================
Testing desktop module imports... ✅ All imports successful

Testing screenshot capture... ✅ Screenshot captured: 1920x1080

Testing current app detection... ✅ Current app: Terminal

Testing device listing... ✅ Found 1 device(s)
   - local: macOS 14.0

Testing DeviceFactory integration... ✅ DeviceFactory works: 1920x1080, app=Terminal

============================================================
Results: 5/5 tests passed
✅ All tests passed!
```

## 常见问题

### 1. 权限被拒绝

**macOS**：
- 检查辅助功能和屏幕录制权限
- 重启终端应用后重试

**Windows**：
- 以管理员权限运行
- 检查防病毒软件设置

### 2. 截图失败

```bash
# 检查屏幕录制权限
python -c "from phone_agent.desktop import get_screenshot; print(get_screenshot().width)"
```

### 3. 应用启动失败

- 检查应用路径是否正确
- 更新 `apps_desktop.py` 中的应用配置
- 确保应用已安装

### 4. 坐标点击不准确

- 检查屏幕缩放设置
- 确保使用主显示器
- 调整 pyautogui 的安全设置

## 性能优化

### 1. 截图优化

```python
# 在 screenshot.py 中可以调整截图区域
monitor = sct.monitors[1]  # 主显示器
# 或指定区域：{"top": 0, "left": 0, "width": 1920, "height": 1080}
```

### 2. 操作延迟

```python
# 在 device.py 中调整操作间隔
pyautogui.PAUSE = 0.1  # 每次操作后暂停时间
```

### 3. 失效保护

```python
# 禁用鼠标移动到角落停止脚本的功能
pyautogui.FAILSAFE = False
```

## 安全注意事项

1. **权限控制**：只授予必要的系统权限
2. **应用白名单**：只配置信任的应用程序路径
3. **网络安全**：使用 HTTPS 连接模型服务
4. **数据隐私**：避免在敏感应用中使用自动化

## 扩展开发

### 添加新的操作类型

在 `phone_agent/desktop/device.py` 中添加新函数：

```python
def new_action(param1, param2, device_id=None, delay=None):
    """新的操作类型"""
    # 实现操作逻辑
    pyautogui.some_action(param1, param2)
    if delay:
        time.sleep(delay)
```

### 支持新的应用类型

在 `phone_agent/config/apps_desktop.py` 中添加：

```python
APP_PACKAGES_DESKTOP.update({
    "新应用": "应用路径或命令",
})
```

## 故障排除

### 调试模式

```bash
# 启用详细输出
python main.py --device-type desktop --verbose "测试任务"
```

### 日志记录

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 手动测试

```python
# 测试截图
from phone_agent.desktop import get_screenshot
screenshot = get_screenshot()
print(f"Screenshot: {screenshot.width}x{screenshot.height}")

# 测试点击
from phone_agent.desktop import tap
tap(100, 100)  # 点击坐标 (100, 100)
```

---

通过以上配置，你就可以在桌面环境中使用 Open-AutoGLM 进行自动化操作了。如有问题，请参考故障排除部分或提交 Issue。