from __future__ import annotations

import logging
import logging.config
import sys
from pathlib import Path
from typing import Any, Mapping, TextIO

from scrapy_simple.conf.default_settings import (
    DEFAULT_LOG_DATEFORMAT,
    DEFAULT_LOG_FORMAT,
    DEFAULT_LOGGING,
    DEFAULT_LOGGER_NAME,
    DEFAULT_LOG_LEVEL,
    DEFAULT_SETTINGS,
)

_scrapy_simple_root_handler: logging.Handler | None = None
_stdout: TextIO = sys.stdout
_stderr: TextIO = sys.stderr


class TopLevelFormatter(logging.Filter):
    """
    将子 logger 名称压缩为顶层名称
    例如：scrapy_simple.xxx.yyy 压缩成 scrapy_simple
    """

    def __init__(self, loggers: list[str] | tuple[str, ...] | None = None):
        super().__init__()
        self.loggers = tuple(loggers or (DEFAULT_LOGGER_NAME,))

    def filter(self, record: logging.LogRecord) -> bool:
        for logger_name in self.loggers:
            if record.name == logger_name or record.name.startswith(
                f"{logger_name}."
            ):
                record.name = logger_name
                break
        return True


class StreamLogger:
    """把 stdout/stderr 风格的写入转成 logging 调用。"""

    def __init__(self, logger: logging.Logger, log_level: int = logging.INFO):
        self.logger = logger
        self.log_level = log_level

    def write(self, buf: str) -> int:
        if not buf:
            return 0

        written = 0
        for line in buf.rstrip().splitlines():
            message = line.rstrip()
            if message:
                self.logger.log(self.log_level, message)
            written += len(line)
        return written

    def flush(self) -> None:
        for handler in self.logger.handlers:
            handler.flush()

    def isatty(self) -> bool:
        return False


def _merge_settings(
    settings: Mapping[str, Any] | None = None,
    **overrides: Any,
) -> dict[str, Any]:
    merged = dict(DEFAULT_SETTINGS)
    if settings:
        merged.update(dict(settings))

    cleaned_overrides = {
        key: value for key, value in overrides.items() if value is not None
    }
    merged.update(cleaned_overrides)
    return merged


def _normalize_level(level: str | int) -> int:
    if isinstance(level, int):
        return level

    if isinstance(level, str):
        normalized = level.strip().upper()
        if not normalized:
            raise ValueError("日志级别不能为空")

        level_value = logging.getLevelName(normalized)
        if isinstance(level_value, int):
            return level_value

    raise ValueError(f"无效的日志级别: {level!r}")


def _get_formatter(settings: Mapping[str, Any]) -> logging.Formatter:
    return logging.Formatter(
        settings.get("LOG_FORMAT", DEFAULT_LOG_FORMAT),
        datefmt=settings.get("LOG_DATEFORMAT", DEFAULT_LOG_DATEFORMAT),
    )


def _get_handler(settings: Mapping[str, Any]) -> logging.Handler:
    if not settings.get("LOG_ENABLED", True):
        return logging.NullHandler()

    log_file = settings.get("LOG_FILE")
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        mode = "a" if settings.get("LOG_FILE_APPEND", True) else "w"
        handler: logging.Handler = logging.FileHandler(
            log_path,
            mode=mode,
            encoding=settings.get("LOG_ENCODING", "utf-8"),
        )
    else:
        handler = logging.StreamHandler(_stderr)

    handler.setLevel(
        _normalize_level(settings.get("LOG_LEVEL", DEFAULT_LOG_LEVEL))
    )
    handler.setFormatter(_get_formatter(settings))
    if settings.get("LOG_SHORT_NAMES", True):
        handler.addFilter(
            TopLevelFormatter([settings.get("LOG_NAME", DEFAULT_LOGGER_NAME)])
        )
    return handler


def get_scrapy_simple_root_handler() -> logging.Handler | None:
    """返回当前安装的项目 root handler。"""
    return _scrapy_simple_root_handler


def _uninstall_scrapy_simple_root_handler() -> None:
    global _scrapy_simple_root_handler

    if _scrapy_simple_root_handler is None:
        return

    logging.root.removeHandler(_scrapy_simple_root_handler)
    _scrapy_simple_root_handler.close()
    _scrapy_simple_root_handler = None


def install_scrapy_simple_root_handler(
    settings: Mapping[str, Any] | None = None,
    **overrides: Any,
) -> logging.Handler:
    """按配置安装项目 root handler。"""
    global _scrapy_simple_root_handler

    merged_settings = _merge_settings(settings, **overrides)
    _uninstall_scrapy_simple_root_handler()

    handler = _get_handler(merged_settings)
    logging.root.setLevel(logging.NOTSET)
    logging.root.addHandler(handler)
    _scrapy_simple_root_handler = handler
    return handler


def configure_logging(
    settings: Mapping[str, Any] | None = None,
    install_root_handler: bool = True,
    **overrides: Any,
) -> dict[str, Any]:
    """初始化项目日志系统。"""
    merged_settings = _merge_settings(settings, **overrides)

    logging.config.dictConfig(DEFAULT_LOGGING)
    logging.captureWarnings(True)

    if install_root_handler:
        install_scrapy_simple_root_handler(merged_settings)

    if merged_settings.get("LOG_STDOUT"):
        sys.stdout = StreamLogger(
            logging.getLogger(
                merged_settings.get("LOG_NAME", DEFAULT_LOGGER_NAME)
            ),
            _normalize_level(merged_settings.get("LOG_LEVEL", DEFAULT_LOG_LEVEL)),
        )
    else:
        sys.stdout = _stdout

    return merged_settings


def get_logger(name: str | None = None) -> logging.Logger:
    if not name:
        return logging.getLogger(DEFAULT_LOGGER_NAME)

    if name == DEFAULT_LOGGER_NAME or name.startswith(f"{DEFAULT_LOGGER_NAME}."):
        return logging.getLogger(name)

    logger_name = f"{DEFAULT_LOGGER_NAME}.{name.lstrip('.')}"
    return logging.getLogger(logger_name)



def get_configured_logger(
    name: str | None = None,
    settings: Mapping[str, Any] | None = None,
    install_root_handler: bool = True,
    **overrides: Any,
) -> logging.Logger:
    """先配置日志，再返回指定 logger。"""
    configure_logging(
        settings=settings,
        install_root_handler=install_root_handler,
        **overrides,
    )
    return get_logger(name)


logger = get_configured_logger()

__all__ = [
    "DEFAULT_LOGGING",
    "DEFAULT_LOG_DATEFORMAT",
    "DEFAULT_LOG_FORMAT",
    "DEFAULT_LOG_LEVEL",
    "DEFAULT_LOGGER_NAME",
    "DEFAULT_SETTINGS",
    "StreamLogger",
    "TopLevelFormatter",
    "configure_logging",
    "get_configured_logger",
    "get_logger",
    "get_scrapy_simple_root_handler",
    "install_scrapy_simple_root_handler",
    "logger",
]
