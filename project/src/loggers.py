import os
from loguru import logger

logger.add(
    os.path.abspath('logs/logs.log'),
    format='{time} {level} {message}',
    rotation='1 day',
    compression='zip',
    colorize=True
)
