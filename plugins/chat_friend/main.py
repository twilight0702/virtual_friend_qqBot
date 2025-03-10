import os
import asyncio

from ncatbot.plugin import BasePlugin, CompatibleEnrollment
from ncatbot.core.message import GroupMessage, PrivateMessage

bot = CompatibleEnrollment  # 兼容回调函数注册器

from .deepseek import ai_message
from .config.config_loader import get_character

class MyPlugin(BasePlugin):
    name = "chat_friend"  # 插件名称
    version = "0.0.1"  # 插件版本

    USER_CHARACTERS = {}  # 记录用户选择的角色 {user_id: character}
    USER_INPUTS = {}  # 存储用户输入缓冲
    USER_TASKS = {}  # 存储用户的延迟任务

    @bot.group_event()
    async def on_group_event(self, msg: GroupMessage):
        # 定义的回调函数
        if msg.raw_message == "测试":
            await self.api.post_group_msg(msg.group_id, text="Ncatbot 插件测试成功喵")

    @bot.private_event()
    async def on_private_message(self, msg: PrivateMessage):        
        user_id = msg.user_id  # **缺少的 user_id 赋值**

        # 处理测试命令
        if msg.raw_message == "测试":
            await self.api.post_private_msg(user_id, text="Ncatbot 插件测试成功喵")
            return
        
        # 处理角色切换 (格式：切换角色 魈)
        if msg.raw_message.startswith("切换角色"):
            try:
                character = msg.raw_message.split(maxsplit=1)[1]  # **提取角色名称**
                if character not in get_character(""):  # **检查角色是否存在**
                    await self.api.post_private_msg(user_id, "未知角色")
                    return
                self.USER_CHARACTERS[user_id] = character  # **记录用户选择**
                await self.api.post_private_msg(user_id, "已切换至" + character + "人格")
            except IndexError:
                await self.api.post_private_msg(user_id, "正确格式：切换角色 角色名")
            return
        
        # **输入缓冲**
        character = self.USER_CHARACTERS.get(user_id, "魈")  # **获取用户的角色**
        if user_id in self.USER_INPUTS:
            self.USER_INPUTS[user_id] += " " + msg.raw_message  # **累积输入**
        else:
            self.USER_INPUTS[user_id] = msg.raw_message  # **首次输入**
        
        # **取消之前的任务**
        if user_id in self.USER_TASKS:
            self.USER_TASKS[user_id].cancel()  # **取消原来的等待任务**
        
        # **启动新的等待任务**
        task = asyncio.create_task(self.send_delayed_message(user_id, character))
        self.USER_TASKS[user_id] = task  # **记录任务**

    async def send_delayed_message(self, user_id, character):
        """等待用户输入结束后，再发送完整消息"""
        await asyncio.sleep(5)  # **2秒无新输入，才执行**
        
        # **检查用户是否仍在输入**
        if user_id in self.USER_INPUTS:
            final_message = self.USER_INPUTS.pop(user_id)  # **取出并删除缓冲内容**
            ai_response = await ai_message(final_message, character)  # **修正 ai_message 调用**

            # **AI 分段回复**
            for sentence in ai_response.split("。"):  # **以句号拆分**
                if sentence.strip():
                    await self.api.post_private_msg(user_id, sentence.strip() + "")
                    await asyncio.sleep(1.5)  # **模拟打字间隔**
            
            # **任务完成后删除**
            self.USER_TASKS.pop(user_id, None)

    async def on_load(self):
        """插件加载时执行的操作"""
        print(f"{self.name} 插件已加载")
        print(f"插件版本: {self.version}")
