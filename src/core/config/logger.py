import logging

import structlog
from structlog.types import EventDict, Processor, WrappedLogger

from src.core.config.settings import get_settings


def add_omni_cloud_severity(
    logger: WrappedLogger, method_name: str, event_dict: EventDict
) -> EventDict:
    """
    Ensures compatibility with both GCP (severity) and AWS/Datadog (level)
    by duplicating the log level key.

    Args:
        logger (WrappedLogger): The structlog logger instance.
        method_name (str): The name of the log method (info, error, etc).
        event_dict (EventDict): The current log event dictionary.

    Returns:
        EventDict: The mutated event dictionary.

    Raises:
        None.
    """
    level = event_dict.get("level")
    if level and isinstance(level, str):
        event_dict["severity"] = level.upper()
    return event_dict


def setup_logging() -> None:
    """
    Initializes the fast structured logging using PrintLoggerFactory.
    Bypasses standard logging to keep third-party libraries quiet.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.
    """
    settings = get_settings()

    # Tipado estricto nativo de Structlog en lugar de list[Any]
    processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
    ]

    # Pre-declaración estricta para que Mypy acepte tanto JSON como Console
    renderer: Processor

    if settings.LOG_JSON_FORMAT:
        # Production (Cloud) configuration
        processors.extend(
            [
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.format_exc_info,
                add_omni_cloud_severity,
            ]
        )
        renderer = structlog.processors.JSONRenderer()
    else:
        # Local development configuration
        processors.append(structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"))
        renderer = structlog.dev.ConsoleRenderer(colors=True, pad_event_to=0)

    structlog.configure(
        processors=processors + [renderer],
        logger_factory=structlog.PrintLoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.getLevelName(settings.LOG_LEVEL)
        ),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.BoundLogger:
    """
    Returns a named logger. Ensures setup is only called once.

    Args:
        name (str): The name of the logger namespace.

    Returns:
        structlog.BoundLogger: The configured structured logger.

    Raises:
        None.
    """
    if not structlog.is_configured():
        setup_logging()
    return structlog.get_logger(name)
