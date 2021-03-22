import logging

import rich
import rich.logging

logger = None


def get_xinstall_logger():
    global logger
    if logger is None:
        logging.basicConfig(
            level="NOTSET",
            format="%(message)s",
            datefmt="[%X]",
            handlers=[rich.logging.RichHandler(rich_tracebacks=True)],
        )

        logger = logging.getLogger("xinstall")

    return logger
