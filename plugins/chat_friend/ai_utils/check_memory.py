# 该文件用于使用deepseek决定记忆存储相关判断

from openai import AsyncOpenAI, OpenAIError  # 处理 OpenAI 相关错误
from ..config.config_loader import get_character
import asyncio
from .ai_helper import use_ai

# 用于判断临时记忆存储
async def check_temp_memory(user_id, content) -> str:
    prompt = (
        "你是bot，请总结以下用户和你的对话，如果内容有意义（如新信息、有助于理解上下文、表明用户情绪或意图），"
        "请生成一段不超过30字的简要概括。否则，返回'无重要内容'。"
    )
    return await use_ai(prompt, content)

# 用于判断中期记忆存储
async def check_mid_memory(user_id, content) -> str:
    prompt = (
        "你是bot，正在和该人类用户对话，请总结以下对话，如果内容对未来对话可能有帮助（如用户提及个人信息、兴趣爱好、"
        "长期计划、偏好等），请生成一段50字以内的关于该用户特点的简要概括。"
        "如果没有长期价值但值得短期参考，请简要概括。否则，返回'无重要内容'。"
    )
    return await use_ai(prompt, content)

# 用于判断长期记忆存储
async def check_long_memory(user_id, content) -> str:
    prompt = (
        "请总结以下对话，并判断其是否具有长期价值（如用户的核心偏好、重要经历、重要承诺、"
        "未来计划、习惯等）。如果有，请生成一段关于该用户特点的精炼总结，不超过60字，否则返回'无重要内容'。"
    )
    return await use_ai(prompt, content)
