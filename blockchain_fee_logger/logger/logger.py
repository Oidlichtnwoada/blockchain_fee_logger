import logging
import sys

DEFAULT_LOG_LEVEL = logging.INFO


class LoggerFactory:
    logger: logging.Logger | None = None

    @classmethod
    def get_logger(cls) -> logging.Logger:
        if cls.logger is None:
            logger = logging.getLogger(cls.__name__)
            logger.setLevel(DEFAULT_LOG_LEVEL)
            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setLevel(logging.NOTSET)
            stdout_handler.addFilter(lambda record: record.levelno <= logging.INFO)
            stderr_handler = logging.StreamHandler(sys.stderr)
            stderr_handler.setLevel(logging.WARNING)
            log_format = logging.Formatter("%(levelname)s: %(message)s")
            stdout_handler.setFormatter(log_format)
            stderr_handler.setFormatter(log_format)
            logger.addHandler(stdout_handler)
            logger.addHandler(stderr_handler)
            cls.logger = logger
        return cls.logger
