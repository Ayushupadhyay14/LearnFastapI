import logging
import os
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

def setup_logger():
  log_dir = "logs"
  os.makedirs(log_dir, exist_ok=True)
  log_file = os.path.join(log_dir, "rapp.log")

  # Create Handlers
  # file_handler = logging.FileHandler(log_file)
  stream_handler = logging.StreamHandler()
  rotate_file_handler = RotatingFileHandler(
    log_file,
    maxBytes=1024*1024*5,
    backupCount=3
  )

  # Set formatter with {}-style
  formatter = logging.Formatter(
    fmt = "{asctime} - {name} - {levelname} - {filename}:{funcName}:{lineno} - {message}",
    style="{"
  )

  # file_handler.setFormatter(formatter)
  stream_handler.setFormatter(formatter)
  rotate_file_handler.setFormatter(formatter)

  logger = logging.getLogger("ch131")
  logger.setLevel(logging.DEBUG)
  logger.handlers = []
  # logger.addHandler(file_handler)
  logger.addHandler(stream_handler)
  logger.addHandler(rotate_file_handler)

  return logger

# Create and export the logger
logger = setup_logger()