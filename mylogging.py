import logging

log_config = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "timed_rotating_file_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "logfile.log",
            "when": "midnight",  # 每天午夜（0点）轮换
            "interval": 1,       # 轮换周期为1天
            "backupCount": 30,   # 保留最近30个备份
            "formatter": "default",
            "level": "INFO",
            "encoding": "utf-8",  # 添加编码设置
        },
    },
    "root": {
        "handlers": ["timed_rotating_file_handler"],
        "level": "INFO",
    },
}

# 正式环境
# logging.config.dictConfig(log_config)  

# 开发环境
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s  - %(levelname)s - %(message)s')
logging.getLogger("watchfiles.main").setLevel(logging.ERROR)  # 忽略watchfiles的日志
