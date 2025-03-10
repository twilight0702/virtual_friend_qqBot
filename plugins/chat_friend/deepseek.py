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
        
        prompt=char_config["system_prompt"]+"请回复人类聊天的多条消息，保持自然节奏，以括号形式保留语气和动作。每条最好不超过25字, 每一条用'。'隔开，中间不要有额外的换行"
        response = await client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input},
            ],
            stream=False
        )

        # **正确的 await 调用**
        # formatted_text = await split_response_with_llm(response.choices[0].message.content)
        # return format_response(formatted_text)
        return format_response(response.choices[0].message.content)
        
    except OpenAIError as e:  # 捕获所有 OpenAI 相关错误
        if "rate limit" in str(e).lower():
            return await handle_rate_limit()  # 处理 API 限流
        print(f"API 调用失败: {str(e)}")
        return char_config.get("error_msg", "出错了，稍后再试喵~")

async def split_response_with_llm(text):
    """借助 LLM 将长文本拆成多条自然的短消息"""
    prompt = f"请将以下文本拆分成适合人类聊天的多条消息，保持自然节奏，每条最好不超过25字, 每一条用'。'隔开，中间不要有额外的换行：\n\n{text}"

    try:
        response = await client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个智能分段助手"},
                {"role": "user", "content": prompt},
            ],
            stream=False
        )

        return format_response(response.choices[0].message.content)
        
    except OpenAIError as e:  # 捕获所有 OpenAI 相关错误
        print(f"API 调用失败: {str(e)}")
        return text  # 如果拆分失败，返回原文本
