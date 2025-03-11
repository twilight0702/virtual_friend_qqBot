from .user_state import USER_CHARACTERS, USER_INPUTS, USER_TASKS
from ..ai_utils.ai_helper import ai_message
from .task_manager import schedule_task
from ..config.config_loader import get_character 

# 直接接收私聊消息部分
async def handle_private_message(msg, api):

    user_id = msg.user_id

    # 特殊情况处理
    if msg.raw_message == "测试":
        await api.post_private_msg(user_id, text="Ncatbot 插件测试成功喵")
        return

    if msg.raw_message.startswith("切换角色"):
        character = msg.raw_message.split(maxsplit=1)[1] if len(msg.raw_message.split()) > 1 else None
        if not character:
            await api.post_private_msg(user_id, "正确格式：切换角色 角色名")
            return

        if character not in get_character(""):
            await api.post_private_msg(user_id, "未知角色")
            return

        USER_CHARACTERS[user_id] = character
        await api.post_private_msg(user_id, f"已切换至 {character} 人格")
        return

    # 处理用户输入
    character = USER_CHARACTERS.get(user_id, "魈")
    if user_id in USER_INPUTS:
        USER_INPUTS[user_id] += " " + msg.raw_message
    else:
        USER_INPUTS[user_id] = msg.raw_message

    # 取消旧任务，启动新任务
    await schedule_task(user_id, api, character)
