from logging import Logger, INFO, getLogger, StreamHandler, NOTSET, WARNING, Formatter
from sys import stdout, stderr

DEFAULT_LOG_LEVEL = INFO


class LoggerFactory:
    logger: Logger | None = None

    @classmethod
    def get_logger(cls) -> Logger:
        if cls.logger is None:
            logger = getLogger(cls.__name__)
            logger.setLevel(DEFAULT_LOG_LEVEL)
            stdout_handler = StreamHandler(stdout)
            stdout_handler.setLevel(NOTSET)
            stdout_handler.addFilter(lambda record: record.levelno <= INFO)
            stderr_handler = StreamHandler(stderr)
            stderr_handler.setLevel(WARNING)
            log_format = Formatter("%(levelname)s: %(message)s")
            stdout_handler.setFormatter(log_format)
            stderr_handler.setFormatter(log_format)
            logger.addHandler(stdout_handler)
            logger.addHandler(stderr_handler)
            cls.logger = logger
        return cls.logger
