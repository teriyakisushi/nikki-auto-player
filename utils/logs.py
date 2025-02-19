from rich import print as rprint
from loguru import logger


def log(
    message: str,
    style: str = "white",
    level: str = "INFO",
    *args,
    **kwargs
) -> None:

    # Rprint
    rprint(f"[{style}]{message}[/{style}]")

    # logger
    log_func = getattr(logger, level.lower(), logger.info)
    log_func(message)
