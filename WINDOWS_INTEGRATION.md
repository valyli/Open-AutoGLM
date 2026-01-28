# Windows 平台集成完成

## 已完成的工作

### 1. 核心模块创建

已创建 `phone_agent/windows/` 目录，包含以下模块：

- **`__init__.py`** - 模块导出和兼容性函数
- **`screenshot.py`** - 使用 mss 库截取 Windows 屏幕
- **`device.py`** - 使用 pyautogui 模拟鼠标和键盘操作
- **`input.py`** - 使用 pyautogui 进行文本输入
- **`connection.py`** - Windows 连接管理（本地模式）

### 2. 配置文件

- **`phone_agent/config/apps_windows.py`** - Windows 应用程序映射配置
  - 支持浏览器（Chrome、Edge、Firefox）
  - 支持 Office 套件（Word、Excel、PowerPoint）
  - 支持系统应用（记事本、计算器、画图等）
  - 支持通讯工具（微信、QQ）
  - 支持开发工具（VS Code、CMD、PowerShell）

### 3. 核心框架集成

- **`phone_agent/device_factory.py`** - 添加 `DeviceType.WINDOWS` 支持
- **`main.py`** - 添加 `--device-type windows` 命令行参数和系统检查

### 4. 依赖管理

- **`requirements_windows.txt`** - Windows 特定依赖
  ```
  pyautogui>=0.9.54
  mss>=9.0.1
  PyGetWindow>=0.0.9
  pillow>=10.0.0
  ```

### 5. 文档和示例

- **`docs/windows_setup.md`** - 完整的 Windows 使用指南
- **`examples/windows_usage.py`** - Python API 使用示例
- **`scripts/test_windows.py`** - Windows 模块测试脚本

## 使用方法

### 安装依赖

```bash
# 安装基础依赖
pip install -r requirements.txt
pip install -e .

# 安装 Windows 依赖
pip install -r requirements_windows.txt
```

### 命令行使用

```bash
# 交互模式
python main.py --device-type windows --base-url http://localhost:8000/v1

# 单次任务
python main.py --device-type windows --base-url http://localhost:8000/v1 "打开记事本，输入Hello World"

# 查看支持的应用
python main.py --device-type windows --list-apps
```

### Python API 使用

```python
from phone_agent import PhoneAgent
from phone_agent.agent import AgentConfig
from phone_agent.device_factory import DeviceType, set_device_type
from phone_agent.model import ModelConfig

# 设置为 Windows 模式
set_device_type(DeviceType.WINDOWS)

# 配置并创建 Agent
model_config = ModelConfig(
    base_url="http://localhost:8000/v1",
    model_name="autoglm-phone-9b",
)

agent_config = AgentConfig(
    max_steps=50,
    lang="cn",
    verbose=True,
)

agent = PhoneAgent(
    model_config=model_config,
    agent_config=agent_config,
)

# 执行任务
result = agent.run("打开记事本，输入Hello Windows")
print(result)
```

## 测试

运行测试脚本验证 Windows 模块：

```bash
python scripts/test_windows.py
```

## 平台切换

所有平台共存，通过 `--device-type` 参数切换：

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

## 技术实现

| 功能 | Android/HarmonyOS | iOS | Windows |
|------|------------------|-----|---------|
| 截图 | ADB/HDC screencap | WDA screenshot | mss |
| 点击 | ADB/HDC input tap | WDA tap | pyautogui.click() |
| 输入 | ADB Keyboard | WDA keyboard | pyautogui.write() |
| 滑动 | ADB/HDC input swipe | WDA swipe | pyautogui.drag() |
| 启动应用 | am start / aa start | WDA launch | subprocess.Popen() |

## 文件清单

```
phone_agent/
├── windows/                      # 新增：Windows 模块
│   ├── __init__.py
│   ├── screenshot.py
│   ├── device.py
│   ├── input.py
│   └── connection.py
├── config/
│   └── apps_windows.py          # 新增：Windows 应用配置
├── device_factory.py            # 修改：添加 WINDOWS 支持
└── ...

docs/
└── windows_setup.md             # 新增：Windows 使用文档

examples/
└── windows_usage.py             # 新增：Windows 示例

scripts/
└── test_windows.py              # 新增：Windows 测试脚本

requirements_windows.txt         # 新增：Windows 依赖
main.py                          # 修改：添加 Windows 支持
```

## 注意事项

1. **权限**：某些应用可能需要管理员权限
2. **屏幕分辨率**：坐标基于当前分辨率，切换显示器需注意
3. **多显示器**：默认使用主显示器
4. **中文输入**：确保系统输入法支持中文
5. **反自动化**：某些应用（游戏、安全软件）可能阻止自动化操作

## 完成状态

✅ Windows 模块完全集成
✅ 与现有 Android/HarmonyOS/iOS 模块共存
✅ 命令行和 Python API 支持
✅ 文档和示例完整
✅ 测试脚本可用
