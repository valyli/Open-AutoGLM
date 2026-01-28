#!/usr/bin/env python3
"""Example: Using PhoneAgent with Windows."""

from phone_agent import PhoneAgent
from phone_agent.agent import AgentConfig
from phone_agent.device_factory import DeviceType, set_device_type
from phone_agent.model import ModelConfig

# Set device type to Windows
set_device_type(DeviceType.WINDOWS)

# Configure model
model_config = ModelConfig(
    base_url="http://localhost:8000/v1",
    model_name="autoglm-phone-9b",
)

# Configure agent
agent_config = AgentConfig(
    max_steps=50,
    lang="cn",  # or "en"
    verbose=True,
)

# Create agent
agent = PhoneAgent(
    model_config=model_config,
    agent_config=agent_config,
)

# Run tasks
print("Example 1: Open Notepad and type text")
result = agent.run("打开记事本，输入'Hello Windows'")
print(f"Result: {result}\n")

agent.reset()

print("Example 2: Open Calculator")
result = agent.run("打开计算器")
print(f"Result: {result}\n")

agent.reset()

print("Example 3: Open Chrome and search")
result = agent.run("打开Chrome浏览器，搜索Python教程")
print(f"Result: {result}\n")
