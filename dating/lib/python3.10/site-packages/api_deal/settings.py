LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'  # 时区

USE_I18N = False  # 国际化

USE_L10N = False  # 本地化

USE_TZ = False  # 是否使用时区

log_path = './log/'

LOGGING = {
    'version': 1,  # 保留字
    'disable_existing_loggers': False,  # 禁用已经存在的logger实例
    'filters': {  # 过滤器
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },  # 针对 DEBUG = True 的情况
    },

    'formatters': {  # 日志文件的格式
        'standard': {
            'format': '%(levelname)s %(asctime)s %(module)s %(funcName)s %(lineno)d: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',  # 保存到文件，自动切
            'filename': log_path + "default.log",  # 日志文件
            'when': 'D',
            'backupCount': 30,  # 最多备份几个
            'formatter': 'standard',
            'encoding': 'utf-8',
        }
    },
    'loggers': {
        # 默认的logger应用如下配置
        'default': {
            'handlers': ['default'],
            'level': 'INFO',
        },
    }
}

LOGGING_LOCAL = {
    'version': 1,  # 保留字
    'disable_existing_loggers': False,  # 禁用已经存在的logger实例
    'filters': {  # 过滤器
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },  # 针对 DEBUG = True 的情况
    },

    'formatters': {  # 日志文件的格式
        'standard': {
            'format': '%(levelname)s %(asctime)s %(module)s %(funcName)s %(lineno)d: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        # 默认的logger应用如下配置
        'django.db.backends': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG'
        },
    }
}
