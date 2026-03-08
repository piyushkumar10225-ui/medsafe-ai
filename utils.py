import logging

def setup_logger(name: str) -> logging.Logger:
    """Sets up a standardized logger for modules."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

def common_disclaimer():
    """Returns the standard medical disclaimer."""
    return "Disclaimer: MedSafe AI provides educational health information and does not replace professional medical advice."
