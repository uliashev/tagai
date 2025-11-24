import logging
from logging import StreamHandler, Formatter
from typing import Optional, Any

class AppLogger:
    def __init__(self, name: str, level: int = logging.INFO, extra: Optional[dict[str, Any]] = None) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        handler = StreamHandler()
        formatter = Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s] [%(request_id)s] %(message)s'
        )
        handler.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(handler)
        self.extra = extra or {}

    def _log(self, level: int, msg: str, **kwargs: Any) -> None:
        extra: dict[str, Any] = self.extra.copy()
        extra.update(kwargs.get('extra', {}))
        self.logger.log(level, msg, extra=extra)

    def info(self, msg: str, **kwargs: Any) -> None:
        self._log(logging.INFO, msg, **kwargs)

    def error(self, msg: str, **kwargs: Any) -> None:
        self._log(logging.ERROR, msg, **kwargs)

    def debug(self, msg: str, **kwargs: Any) -> None:
        self._log(logging.DEBUG, msg, **kwargs)

    def warning(self, msg: str, **kwargs: Any) -> None:
        self._log(logging.WARNING, msg, **kwargs)

    def critical(self, msg: str, **kwargs: Any) -> None:
        self._log(logging.CRITICAL, msg, **kwargs)