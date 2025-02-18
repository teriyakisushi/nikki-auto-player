import sys
from pathlib import Path
from core.config import Config
from core.score import Score
from core.melody import Melody
from loguru import logger

# remove default logger
logger.remove(0)

# logs dir
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# custom logger
logger.add(
    # sys.stderr,
    log_dir / "{time:YYYY-MM-DD}.log",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> - <level>{level}</level> - <level>{message}</level>",
    enqueue=True,
    # colorize=True,
    backtrace=True,
    diagnose=True
)

__all__ = ['Config', 'Score', 'Melody']

config = Config()
score = Score(config)

if config.debug:
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> - <level>{level}</level> - <level>{message}</level>",
        colorize=True,
        level="DEBUG"
    )
