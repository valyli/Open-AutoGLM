#!/usr/bin/env python3
"""Example: Use AutoGLM with a custom image instead of screenshot."""

import base64
import sys
from pathlib import Path

from phone_agent import PhoneAgent
from phone_agent.agent import AgentConfig
from phone_agent.model import ModelConfig
from phone_agent.model.client import MessageBuilder


def load_image_as_base64(image_path: str) -> str:
    """Load an image file and convert to base64."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def run_with_image(image_path: str, task: str, base_url: str, model_name: str, analysis_only: bool = True):
    """Run AutoGLM with a custom image."""
    
    # Load image
    print(f"Loading image: {image_path}")
    image_base64 = load_image_as_base64(image_path)
    
    # Create model config
    model_config = ModelConfig(
        base_url=base_url,
        model_name=model_name,
        max_tokens=8000,  # Increase from default 3000 to avoid truncation
    )
    
    # Create agent config
    agent_config = AgentConfig(
        max_steps=1,  # Only one step for image analysis
        verbose=True,
    )
    
    # Create agent
    agent = PhoneAgent(
        model_config=model_config,
        agent_config=agent_config,
    )
    
    # Build custom message with image
    if analysis_only:
        # Use grounding-optimized prompt for bounding box detection
        system_prompt = """You are a helpful AI assistant specialized in image analysis and object localization.
When asked to locate objects, provide bounding boxes in the format [[x1,y1,x2,y2]] where coordinates are normalized by image dimensions and scaled by 1000.
Use <|begin_of_box|> and <|end_of_box|> tokens to mark bounding boxes in your response."""
    else:
        system_prompt = agent.agent_config.system_prompt
    
    agent._context = [
        MessageBuilder.create_system_message(system_prompt),
        MessageBuilder.create_user_message(
            text=task,
            image_base64=image_base64
        )
    ]
    
    # Get model response
    print(f"\nTask: {task}\n")
    print("=" * 50)
    print("💭 AI 分析:")
    print("-" * 50)
    
    response = agent.model_client.request(agent._context)
    
    print("\n" + "=" * 50)
    print("🎯 AI 回答:")
    print("-" * 50)
    print(response.action)
    print("=" * 50)


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print("Usage: python image_input.py <image_path> <task> [base_url] [model_name] [--action]")
        print("\nExamples:")
        print('  python image_input.py screenshot.png "这个界面上有什么按钮？"')
        print('  python image_input.py app.jpg "帮我点击登录按钮" http://localhost:8000/v1 autoglm-phone-9b --action')
        sys.exit(1)
    
    image_path = sys.argv[1]
    task = sys.argv[2]
    
    # Parse remaining arguments
    remaining_args = sys.argv[3:]
    base_url = "http://localhost:8000/v1"
    model_name = "autoglm-phone-9b"
    analysis_only = True  # Default to analysis mode
    
    for arg in remaining_args:
        if arg == "--action":
            analysis_only = False
        elif arg.startswith("http"):
            base_url = arg
        else:
            model_name = arg
    
    # Check if image exists
    if not Path(image_path).exists():
        print(f"Error: Image file not found: {image_path}")
        sys.exit(1)
    
    run_with_image(image_path, task, base_url, model_name, analysis_only)


if __name__ == "__main__":
    main()
