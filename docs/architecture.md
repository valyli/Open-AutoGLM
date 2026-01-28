# Open-AutoGLM 项目架构说明

## 核心概念

### Open-AutoGLM 是什么？

**Open-AutoGLM 不是一个模型，而是一个设备自动化控制框架。**

它的作用是：
1. 调用 AutoGLM 视觉模型（远程部署）
2. 将模型的决策转化为实际的设备操作
3. 支持多平台：Android、HarmonyOS、iOS、Windows

### AutoGLM 模型是什么？

**AutoGLM 是一个视觉语言模型（VLM）**，能够：
- 看懂屏幕截图
- 理解用户任务
- 决策下一步操作

**模型的输入输出：**

```
输入：
- 屏幕截图（图片）
- 用户任务（文字）："打开微信，给张三发消息"
- 当前应用状态

输出：
<think>
当前在桌面，需要先启动微信应用。
我应该执行 Launch 动作来打开微信。
</think>
<answer>
do(action="Launch", app="微信")
</answer>
```

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                         用户                                  │
│                "打开微信，给张三发消息"                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    PhoneAgent (agent.py)                     │
│                      核心控制器                               │
│  • 接收用户指令                                               │
│  • 管理执行循环                                               │
│  • 协调各个模块                                               │
└────────┬────────────────────────┬───────────────────────────┘
         │                        │
         ▼                        ▼
┌──────────────────┐    ┌──────────────────────────────────┐
│  ModelClient     │    │   DeviceFactory                  │
│  (model/)        │    │   (device_factory.py)            │
│                  │    │                                  │
│  调用 AutoGLM    │    │   选择设备类型：                  │
│  视觉模型        │    │   • ADB (Android)                │
└────────┬─────────┘    │   • HDC (HarmonyOS)              │
         │              │   • iOS (iPhone)                 │
         │              │   • Windows (PC)                 │
         │              └────────┬─────────────────────────┘
         │                       │
         ▼                       ▼
┌──────────────────┐    ┌──────────────────────────────────┐
│  AutoGLM 模型    │    │   设备控制模块                     │
│  (远程服务)      │    │                                  │
│                  │    │   adb/    hdc/    ios/   windows/│
│  输入：截图+指令  │    │   ├── screenshot.py (截图)       │
│  输出：思考+动作  │    │   ├── device.py (点击/滑动)      │
│                  │    │   ├── input.py (输入文本)        │
│                  │    │   └── connection.py (连接管理)   │
└──────────────────┘    └────────┬─────────────────────────┘
                                 │
                                 ▼
                        ┌──────────────────────────────────┐
                        │   实际设备/系统                    │
                        │   📱 Android 手机                 │
                        │   🔷 HarmonyOS 设备               │
                        │   🍎 iPhone                       │
                        │   💻 Windows 电脑                 │
                        └──────────────────────────────────┘
```

## 部署架构

### 方案 1：完全本地部署

```
┌─────────────────────────────────────────┐
│          你的电脑（需要 GPU）             │
│                                         │
│  ┌────────────────────────────────┐    │
│  │  AutoGLM 模型服务               │    │
│  │  localhost:8000                │    │
│  │  (需要 24GB+ 显存)              │    │
│  └──────────┬─────────────────────┘    │
│             │ HTTP API                 │
│             ▼                          │
│  ┌────────────────────────────────┐    │
│  │  Open-AutoGLM 项目              │    │
│  │  python main.py                │    │
│  └──────────┬─────────────────────┘    │
│             │ USB/WiFi/本地            │
│             ▼                          │
│  ┌────────────────────────────────┐    │
│  │  被控设备                       │    │
│  │  手机/本机                      │    │
│  └────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

### 方案 2：分离部署（推荐）

```
┌──────────────────────┐        ┌──────────────────────┐
│   远程服务器（GPU）   │        │    你的电脑（普通）   │
│                      │        │                      │
│  ┌────────────────┐  │        │  ┌────────────────┐  │
│  │ AutoGLM 模型   │  │        │  │ Open-AutoGLM   │  │
│  │ server:8000    │◄─┼────API─┼──│ 项目           │  │
│  └────────────────┘  │        │  └────────┬───────┘  │
│                      │        │           │          │
└──────────────────────┘        │           │ USB/WiFi │
                                │           ▼          │
                                │  ┌────────────────┐  │
                                │  │ 被控设备       │  │
                                │  └────────────────┘  │
                                └──────────────────────┘
```

### 方案 3：使用第三方 API（最简单）

```
┌──────────────────────┐        ┌──────────────────────┐
│  智谱 AI / ModelScope │        │    你的电脑          │
│                      │        │                      │
│  ┌────────────────┐  │        │  ┌────────────────┐  │
│  │ AutoGLM API    │  │        │  │ Open-AutoGLM   │  │
│  │ (已部署)       │◄─┼────API─┼──│ 项目           │  │
│  └────────────────┘  │        │  └────────┬───────┘  │
│                      │        │           │          │
└──────────────────────┘        │           │ USB/WiFi │
                                │           ▼          │
                                │  ┌────────────────┐  │
                                │  │ 被控设备       │  │
                                │  └────────────────┘  │
                                └──────────────────────┘
```

## 执行流程

### 完整执行循环

```
用户输入: "打开微信，给张三发消息"
    ↓
PhoneAgent.run()
    ↓
┌─────────────────────────────────────┐
│         执行循环（自动重复）          │
│                                     │
│  1. 截图当前屏幕                     │
│     DeviceFactory.get_screenshot()  │
│     📸 截图：显示桌面                │
│     ↓                               │
│  2. 发送给 AutoGLM 模型              │
│     ModelClient.request()           │
│     输入: 截图 + 任务描述            │
│     ↓                               │
│  3. 模型返回决策                     │
│     <think>需要启动微信</think>      │
│     <answer>                        │
│       do(action="Launch", app="微信")│
│     </answer>                       │
│     ↓                               │
│  4. 解析并执行动作                   │
│     ActionHandler.execute()         │
│     DeviceFactory.launch_app("微信") │
│     ↓                               │
│  5. 等待界面变化                     │
│     ↓                               │
│  6. 回到步骤 1（继续循环）           │
│                                     │
└─────────────────────────────────────┘
    ↓
任务完成或达到最大步数
```

### 单步执行示例

**第 1 步：启动应用**
```
截图: [桌面画面]
模型输出: do(action="Launch", app="微信")
执行: adb shell am start com.tencent.mm
```

**第 2 步：点击搜索**
```
截图: [微信首页]
模型输出: do(action="Tap", element=[500, 100])
执行: adb shell input tap 500 100
```

**第 3 步：输入文字**
```
截图: [搜索框已激活]
模型输出: do(action="Type", text="张三")
执行: adb shell input text "张三"
```

**第 4 步：点击联系人**
```
截图: [搜索结果]
模型输出: do(action="Tap", element=[300, 200])
执行: adb shell input tap 300 200
```

## 核心模块说明

### 1. PhoneAgent (agent.py)

**作用**：核心控制器，管理整个执行流程

**主要方法**：
```python
class PhoneAgent:
    def run(task: str) -> str:
        """执行任务，返回结果"""
        
    def step(task: str) -> StepResult:
        """执行单步，用于调试"""
        
    def reset():
        """重置状态，开始新任务"""
```

### 2. ModelClient (model/client.py)

**作用**：与 AutoGLM 模型通信

**主要方法**：
```python
class ModelClient:
    def request(messages: list) -> ModelResponse:
        """发送请求到模型，返回决策"""
```

### 3. DeviceFactory (device_factory.py)

**作用**：设备抽象层，统一不同平台的接口

**主要方法**：
```python
class DeviceFactory:
    def get_screenshot() -> Screenshot:
        """截图"""
        
    def tap(x: int, y: int):
        """点击"""
        
    def type_text(text: str):
        """输入文字"""
        
    def launch_app(app_name: str):
        """启动应用"""
```

### 4. 平台实现模块

**adb/** - Android 平台
```python
# 使用 ADB 命令控制 Android 设备
adb shell screencap      # 截图
adb shell input tap      # 点击
adb shell am start       # 启动应用
```

**hdc/** - HarmonyOS 平台
```python
# 使用 HDC 命令控制鸿蒙设备
hdc shell snapshot_display  # 截图
hdc shell uitest uiInput    # 点击
hdc shell aa start          # 启动应用
```

**ios/** - iOS 平台
```python
# 使用 WebDriverAgent 控制 iPhone
wda.screenshot()         # 截图
wda.tap()               # 点击
wda.launch()            # 启动应用
```

**windows/** - Windows 平台
```python
# 使用 PyAutoGUI 控制 Windows
mss.grab()              # 截图
pyautogui.click()       # 点击
subprocess.Popen()      # 启动应用
```

## 项目目录结构

```
Open-AutoGLM/
├── phone_agent/              # 核心代码
│   ├── agent.py             # PhoneAgent 主控制器
│   ├── device_factory.py    # 设备抽象层
│   │
│   ├── model/               # 模型通信
│   │   └── client.py        # ModelClient
│   │
│   ├── actions/             # 动作处理
│   │   └── handler.py       # ActionHandler
│   │
│   ├── config/              # 配置文件
│   │   ├── apps.py          # Android 应用列表
│   │   ├── apps_harmonyos.py # 鸿蒙应用列表
│   │   ├── apps_ios.py      # iOS 应用列表
│   │   ├── apps_windows.py  # Windows 应用列表
│   │   ├── prompts_zh.py    # 中文 Prompt
│   │   └── prompts_en.py    # 英文 Prompt
│   │
│   ├── adb/                 # Android 实现
│   │   ├── screenshot.py
│   │   ├── device.py
│   │   ├── input.py
│   │   └── connection.py
│   │
│   ├── hdc/                 # HarmonyOS 实现
│   ├── ios/                 # iOS 实现
│   └── windows/             # Windows 实现
│
├── main.py                  # 命令行入口
├── examples/                # 使用示例
├── docs/                    # 文档
└── requirements.txt         # 依赖列表
```

## 关键概念对比

| 概念 | 说明 | 部署位置 |
|------|------|---------|
| **AutoGLM 模型** | 视觉语言模型，AI 大脑 | 远程服务器/云端 |
| **Open-AutoGLM 项目** | 控制框架，执行器 | 你的电脑 |
| **被控设备** | 手机/电脑 | 连接到你的电脑 |

## 类比理解

```
┌──────────────────────────────────────────┐
│  遥控无人机系统                           │
│                                          │
│  遥控器 (Open-AutoGLM)                   │
│    • 发送指令                            │
│    • 接收反馈                            │
│    • 本地运行                            │
│                                          │
│  AI 大脑 (AutoGLM 模型)                  │
│    • 分析图像                            │
│    • 决策动作                            │
│    • 云端/服务器运行                     │
│                                          │
│  无人机 (手机/电脑)                      │
│    • 被控制的设备                        │
│    • 执行动作                            │
└──────────────────────────────────────────┘
```

## 使用示例

### 命令行使用

```bash
# 使用远程模型
python main.py \
  --device-type adb \
  --base-url http://your-server:8000/v1 \
  --model autoglm-phone-9b \
  "打开微信"

# 使用第三方 API
python main.py \
  --device-type adb \
  --base-url https://open.bigmodel.cn/api/paas/v4 \
  --model autoglm-phone \
  --apikey sk-xxxxx \
  "打开微信"

# Windows 平台
python main.py \
  --device-type windows \
  --base-url http://localhost:8000/v1 \
  "打开记事本"
```

### Python API 使用

```python
from phone_agent import PhoneAgent
from phone_agent.agent import AgentConfig
from phone_agent.model import ModelConfig

# 配置模型
model_config = ModelConfig(
    base_url="http://your-server:8000/v1",
    model_name="autoglm-phone-9b",
)

# 配置 Agent
agent_config = AgentConfig(
    max_steps=100,
    lang="cn",
    verbose=True,
)

# 创建 Agent
agent = PhoneAgent(
    model_config=model_config,
    agent_config=agent_config,
)

# 执行任务
result = agent.run("打开微信，给张三发消息")
print(result)
```

## 常见问题

### Q: Open-AutoGLM 包含模型吗？

**A: 不包含。** Open-AutoGLM 是控制框架，模型需要单独部署或使用第三方 API。

### Q: 模型必须自己部署吗？

**A: 不是。** 可以选择：
1. 自己部署（需要 GPU）
2. 使用第三方 API（智谱 AI、ModelScope）
3. 使用别人部署好的服务

### Q: Open-AutoGLM 运行在哪里？

**A: 你的电脑上。** 它通过 USB/WiFi 连接到被控设备，通过网络连接到模型服务。

### Q: 支持哪些平台？

**A: 四个平台：**
- Android（通过 ADB）
- HarmonyOS（通过 HDC）
- iOS（通过 WebDriverAgent）
- Windows（通过 PyAutoGUI）

### Q: 可以离线使用吗？

**A: 不能完全离线。** 需要网络连接到模型服务，但被控设备可以是本地的。

## 相关资源

- **模型下载**：[Hugging Face](https://huggingface.co/zai-org/AutoGLM-Phone-9B)
- **第三方 API**：
  - [智谱 BigModel](https://docs.bigmodel.cn/)
  - [ModelScope](https://modelscope.cn/models/ZhipuAI/AutoGLM-Phone-9B)
- **平台配置**：
  - [Android 配置](../README.md#android-环境准备)
  - [iOS 配置](ios_setup/ios_setup.md)
  - [Windows 配置](windows_setup.md)
