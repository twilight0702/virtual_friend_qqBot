from ncatbot.core import BotClient
from ncatbot.core.message import GroupMessage, PrivateMessage
from ncatbot.utils.config import config
from ncatbot.utils.logger import get_log

_log = get_log()

config.set_bot_uin("3949941233")  # 设置 bot qq 号 (必填)
config.set_ws_uri("ws://localhost:3001")  # 设置 napcat websocket server 地址
config.set_token("") # 设置 token (napcat 服务器的 token)

bot = BotClient()


@bot.group_event()
async def on_group_message(msg: GroupMessage):
    _log.info(msg)
    if msg.raw_message == "测试":
        await msg.reply(text="NcatBot 测试成功喵~")


@bot.private_event()
async def on_private_message(msg: PrivateMessage):
    _log.info(msg)
    
    # 处理测试命令
    if msg.raw_message == "测试":
        await msg.reply("NcatBot 测试成功喵~")

if __name__ == "__main__":
    bot.run()