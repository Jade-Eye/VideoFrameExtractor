from core.config import ConfigManager

config = ConfigManager()

print(config.get("fps"))

config.set("fps", 8)

config.save()