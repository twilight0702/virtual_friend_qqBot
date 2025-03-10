from openai import AsyncOpenAI, OpenAIError  # 处理 OpenAI 相关错误
from .config.config_loader import get_character
import asyncio

client = AsyncOpenAI(api_key="sk-38b1d8c0152545758b2265cd85ffc3bf", base_url="https://api.deepseek.com")

# 处理API限流
async def handle_rate_limit():
    await asyncio.sleep(1)
    return "别、别一直发消息啦，喵~"

# 格式化文本
def format_response(text):
    return text.strip()

# 处理 AI 消息（接收文本，返回文本）
async def ai_message(user_input: str, character="魈") -> str:
    """ 
    处理 AI 对话请求
    :param user_input: 用户输入的消息文本
    :param character: 角色名称，默认为 "魈"
    :return: AI 回复的文本
    """
    try:
        char_config = get_character(character)
        
        response = await client.chat.completions.create(
            model="deepseek-reasoner",
            messages=[
                {"role": "system", "content": char_config["system_prompt"]},
                {"role": "user", "content": user_input},
            ],
            stream=False
        )

        return format_response(response.choices[0].message.content)
        
    except OpenAIError as e:  # 捕获所有 OpenAI 相关错误
        print(f"API 调用失败: {str(e)}")
        return char_config.get("error_msg", char_config["error_msg"])
