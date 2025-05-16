"""
Custom logging configuration for the Luxottica Customer Churn project
Handles both file and console logging with rotation and detailed formatting
"""

import os
import sys
import logging
from datetime import datetime
from typing import Optional
from logging.handlers import RotatingFileHandler

def setup_logger(
    name: str = "luxottica_churn",
    log_level: int = logging.INFO,
    log_dir: str = "logs",
    console_output: bool = True,
    max_log_size: int = 10,  # in MB
    backup_count: int = 5
) -> logging.Logger:
    """
    Configures a production-ready logger with file rotation and console output.
    
    Args:
        name: Logger name (will appear in logs)
        log_level: DEBUG/INFO/WARNING/ERROR/CRITICAL
        log_dir: Directory to store log files
        console_output: Whether to print to stdout
        max_log_size: Max log file size in MB before rotation
        backup_count: Number of backup logs to keep
        
    Returns:
        Configured logger instance
    """
    # Create log directory if needed
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure log format
    log_format = (
        "[%(asctime)s] [%(levelname)s] "
        "[%(module)s.%(funcName)s:%(lineno)d] - %(message)s"
    )
    formatter = logging.Formatter(log_format)
    
    # Initialize logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Prevent duplicate handlers in Jupyter/IPython
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # Configure rotating file handler
    log_filename = f"{datetime.now().strftime('%Y-%m-%d')}.log"
    log_filepath = os.path.join(log_dir, log_filename)
    
    file_handler = RotatingFileHandler(
        log_filepath,
        maxBytes=max_log_size*1024*1024,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Configure console output if enabled
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger

# Default logger instance for the project
logger = setup_logger()

# Example usage (will only execute when run directly)
if __name__ == "__main__":
    logger.info("Logger configured successfully")
    logger.debug("Debugging message")
    logger.warning("Sample warning")
    logger.error("Test error", exc_info=True)