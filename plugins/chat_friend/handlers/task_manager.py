import asyncio
from ..ai_utils.ai_helper import ai_message
from .user_state import USER_INPUTS, USER_TASKS
from ..memory.memory_manager import insert_temp_memory, manage_temp_memory, manage_mid_memory

async def send_delayed_message(user_id, api, character):
    """ 等待用户输入结束后，再发送完整消息 """
    await asyncio.sleep(5)  # 5秒无新输入才执行

    if user_id in USER_INPUTS:
        final_message = USER_INPUTS.pop(user_id)  # 取出缓冲内容
        try:
            await insert_temp_memory(user_id, final_message, "user")
        except Exception as e:
            print(f"Error inserting temp memory: {e}")
        ai_response = await ai_message(final_message, character,user_id)

        # 分段回复
        for sentence in ai_response.split("。"):
            if sentence.strip():
                await api.post_private_msg(user_id, sentence.strip())
                try:
                    await insert_temp_memory(user_id, sentence.strip(), "bot")
                except Exception as e:
                    print(f"Error inserting temp memory: {e}")
                await asyncio.sleep(1.5)  # 模拟打字间隔
        await manage_temp_memory(user_id)
        await manage_mid_memory(user_id)
        USER_TASKS.pop(user_id, None)  # 任务完成后删除

async def schedule_task(user_id, api, character):
    """ 取消旧任务并启动新任务 """
    if user_id in USER_TASKS:
        USER_TASKS[user_id].cancel()  # 取消旧任务
    task = asyncio.create_task(send_delayed_message(user_id, api, character))
    USER_TASKS[user_id] = task
