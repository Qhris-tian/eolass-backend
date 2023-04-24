from src.logging import log


def start_app_handler():  # pragma: no cover
    """
    Handles process initailization upon application start up.
    """
    log.info("Starting application...")


def shutdown_app_handler():  # pragma: no cover
    """
    Handles process initailization upon application shut down.
    """
    log.info("Shutting donw application...")
