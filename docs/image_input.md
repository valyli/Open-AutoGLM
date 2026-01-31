# 图片输入功能

AutoGLM 支持输入自定义图片让 AI 分析，而不仅仅是实时截图。

## 使用方法

### 方式 1: 使用示例脚本（推荐）

```bash
# 基本用法
python examples/image_input.py screenshot.png "这个界面上有什么内容？"

# 指定模型服务
python examples/image_input.py app.jpg "帮我分析这个应用的界面" http://localhost:8000/v1 autoglm-phone-9b

# 分析按钮位置
python examples/image_input.py login.png "登录按钮在哪里？坐标是多少？"
```

### 方式 2: Python API

```python
import base64
from phone_agent import PhoneAgent
from phone_agent.model import ModelConfig
from phone_agent.model.client import MessageBuilder
from phone_agent.agent import AgentConfig

# 加载图片
def load_image_as_base64(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# 配置模型
model_config = ModelConfig(
    base_url="http://localhost:8000/v1",
    model_name="autoglm-phone-9b",
)

# 配置 Agent
agent_config = AgentConfig(
    max_steps=1,  # 只分析图片，不执行操作
    verbose=True,
)

# 创建 Agent
agent = PhoneAgent(
    model_config=model_config,
    agent_config=agent_config,
)

# 加载图片
image_base64 = load_image_as_base64("screenshot.png")

# 构建消息
agent._context = [
    MessageBuilder.create_system_message(agent.agent_config.system_prompt),
    MessageBuilder.create_user_message(
        text="这个界面上有什么按钮？",
        image_base64=image_base64
    )
]

# 获取 AI 分析
response = agent.model_client.request(agent._context)
print(f"AI 分析: {response.action}")
```

## 应用场景

### 1. 界面分析

```bash
python examples/image_input.py app_screenshot.png "分析这个应用的界面布局"
```

### 2. 按钮识别

```bash
python examples/image_input.py login_page.png "找出所有可点击的按钮及其坐标"
```

### 3. 文字提取

```bash
python examples/image_input.py document.png "提取图片中的所有文字"
```

### 4. UI 测试

```bash
python examples/image_input.py error_screen.png "这个错误页面显示了什么问题？"
```

### 5. 设计审查

```bash
python examples/image_input.py design.png "评价这个界面设计的可用性"
```

## 支持的图片格式

- PNG
- JPEG/JPG
- WebP
- BMP
- GIF（静态）

## 注意事项

1. **图片大小**：建议图片不超过 5MB，过大的图片会影响推理速度
2. **分辨率**：建议使用原始分辨率，模型会自动处理
3. **单次分析**：默认 `max_steps=1`，只分析图片不执行操作
4. **多图片**：目前每次只支持一张图片

## 与实时截图的区别

| 特性 | 实时截图 | 图片输入 |
|------|---------|---------|
| 数据来源 | 当前屏幕 | 本地文件 |
| 实时性 | 实时 | 静态 |
| 操作执行 | 支持 | 仅分析 |
| 使用场景 | 自动化操作 | 离线分析 |

## 示例输出

```bash
$ python examples/image_input.py /tmp/test_screenshot.png "这个界面上有什么？"

Loading image: /tmp/test_screenshot.png

Task: 这个界面上有什么？

==================================================
💭 AI 分析:
--------------------------------------------------
这是一个代码编辑器界面，显示了 Python 代码文件...
--------------------------------------------------
🎯 AI 回答:
finish(message="界面显示了一个代码编辑器，包含文件树、代码编辑区域和终端窗口...")
==================================================
```

## 故障排除

### 图片加载失败

```bash
Error: Image file not found: screenshot.png
```

**解决方案**：检查图片路径是否正确，使用绝对路径或相对路径

### 模型无法识别图片

**解决方案**：
1. 确保图片格式正确
2. 检查图片是否损坏
3. 尝试转换为 PNG 格式

### 分析结果不准确

**解决方案**：
1. 使用更清晰的图片
2. 调整提示词，提供更多上下文
3. 使用更高分辨率的图片
