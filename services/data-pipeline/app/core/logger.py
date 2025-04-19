import logging
import os


class ShortPathFormatter(logging.Formatter):
    def format(self, record):
        # Keep only the last 2 segments of the file path
        path_parts = os.path.normpath(record.pathname).split(os.sep)
        short_path = (
            os.path.join(*path_parts[-2:]) if len(path_parts) >= 2 else record.pathname
        )
        record.short_path = short_path
        return super().format(record)


# Create logger
logger = logging.getLogger("data-pipeline")
logger.setLevel(logging.INFO)

# Create console handler and set level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Custom formatter with short path
formatter = ShortPathFormatter(
    "%(asctime)s - %(levelname)s - %(short_path)s - %(message)s", "%Y-%m-%d %H:%M:%S"
)
console_handler.setFormatter(formatter)

# Add handler
if not logger.hasHandlers():
    logger.addHandler(console_handler)
