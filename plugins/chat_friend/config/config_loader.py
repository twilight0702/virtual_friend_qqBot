import json
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

_CONFIG_PATH = Path(__file__).parent / "characters.json"
_CHARACTERS = {}

def load_config():
    global _CHARACTERS
    try:
        with open(_CONFIG_PATH, 'r', encoding='utf-8') as f:
            _CHARACTERS = json.load(f)
        print(f"配置已重载，当前角色：{list(_CHARACTERS.keys())}")
    except Exception as e:
        print(f"配置加载失败：{str(e)}")

class ConfigHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == str(_CONFIG_PATH):
            load_config()

# 初始化加载
load_config()

# 启动文件监听
observer = Observer()
observer.schedule(ConfigHandler(), path=str(_CONFIG_PATH.parent))
observer.start()

# 修改get_character函数
def get_character(name=None):
    if name:
        return _CHARACTERS.get(name)
    return _CHARACTERS  # 返回全部角色用于存在性检查