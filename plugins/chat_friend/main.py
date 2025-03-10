# main.py
import os

from ncatbot.plugin import BasePlugin, CompatibleEnrollment
from ncatbot.core.message import GroupMessage, PrivateMessage

bot = CompatibleEnrollment  # 兼容回调函数注册器

from .deepseek import ai_message
from .config.config_loader import get_character

class MyPlugin(BasePlugin):
    name = "chat_friend" # 插件名称
    version = "0.0.1" # 插件版本

    USER_CHARACTERS = {}  # 记录用户选择的角色 {user_id: character}

    @bot.group_event()
    async def on_group_event(self, msg: GroupMessage):
        # 定义的回调函数
        if msg.raw_message == "测试":
            await self.api.post_group_msg(msg.group_id, text="Ncatbot 插件测试成功喵")

    @bot.private_event()
    async def on_private_message(self, msg: PrivateMessage):        
        # 处理测试命令
        if msg.raw_message == "测试":
            await self.api.post_private_msg(msg.user_id, text="Ncatbot 插件测试成功喵")
            return
        
        # 处理角色切换 (格式：切换角色 魈)
        if msg.raw_message.startswith("切换角色"):
            try:
                # 提取角色名称
                character = msg.raw_message.split(maxsplit=1)[1]
                # 验证角色存在性
                if character not in get_character(""):  # 检查所有角色
                    await self.api.post_private_msg(msg.user_id,"未知角色")
                    return
                # 记录用户选择
                self.USER_CHARACTERS[msg.user_id] = character
                await self.api.post_private_msg(msg.user_id,"已切换至" + character + "人格")
            except IndexError:
                await self.api.post_private_msg(msg.user_id,"正确格式：切换角色 角色名")
            return
        
        # 处理AI消息
        current_character = self.USER_CHARACTERS.get(msg.user_id, "魈")  # 默认为魈
        return_msg=await ai_message(msg.raw_message, character=current_character)
        await self.api.post_private_msg(msg.user_id, return_msg)  
    async def on_load(self):
        # 插件加载时执行的操作, 可缺省
        print(f"{self.name} 插件已加载")
        print(f"插件版本: {self.version}")