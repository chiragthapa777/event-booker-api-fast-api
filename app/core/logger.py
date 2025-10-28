import logging
import json
import sys
from datetime import datetime, timezone

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "level": record.levelname,
            "location": f"{record.filename}/{record.funcName}:{record.lineno}",
            "message": record.getMessage()
        }
        # Include any extra fields passed with the record
        if hasattr(record, "__dict__"):
            for key, value in record.__dict__.items():
                # Skip default logging attributes
                if key not in (
                    "args", "asctime", "created", "exc_info", "exc_text", "filename",
                    "funcName", "levelname", "levelno", "lineno", "message", "module",
                    "msecs", "msg", "name", "pathname", "process", "processName",
                    "relativeCreated", "stack_info", "thread", "threadName","taskName"
                ):
                    log_record[key] = value

        return json.dumps(log_record, ensure_ascii=False)

_logger = None  # Internal logger instance

def setup_logger(level=logging.INFO):
    """Setup the global application logger."""
    global _logger
    _logger = logging.getLogger("app_logger")
    _logger.setLevel(level)

    # Prevent adding multiple handlers
    if not _logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        _logger.addHandler(handler)

def get_logger():
    """Return the configured logger instance."""
    global _logger
    if _logger is None:
        # Default setup if setup_logger() was not called
        setup_logger()
    return _logger
