USER_CHARACTERS = {}  # {user_id: character} 记录用户的角色
USER_INPUTS = {}      # {user_id: message}  存储用户输入缓冲
USER_TASKS = {}       # {user_id: asyncio.Task}  存储用户的延迟任务
