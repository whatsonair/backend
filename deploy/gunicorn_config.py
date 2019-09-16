logconfig_dict = {
  "version": 1,
  "disable_existing_loggers": False,

  "root": {"level": "INFO", "handlers": ["console"]},
  "loggers": {
    "gunicorn.error": {
      "level": "DEBUG",
      "handlers": ["error_console"],
      "propagate": False,
    },

    "gunicorn.access": {
      "level": "INFO",
      "handlers": ["console"],
      "propagate": False,
    }
  },
  "handlers": {
    "console": {
      "class": "logging.StreamHandler",
      "formatter": "generic",
      "stream": "ext://sys.stdout"
    },
    "error_console": {
      "class": "logging.StreamHandler",
      "formatter": "generic",
      "stream": "ext://sys.stderr"
    },
  },
  "formatters": {
    "generic": {
      "format": "%(asctime)s [%(process)d] {%(name)s} %(levelname)s %(message)s",
      "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
      "class": "logging.Formatter"
    }
  }
}
