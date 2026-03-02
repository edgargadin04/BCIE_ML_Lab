"""
Módulo de Logging Centralizado.

Provee un logger unificado con formato consistente para todo el pipeline.
"""

import logging
import sys
from pathlib import Path


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Crea o retorna un logger con formato estándar del proyecto.

    Args:
        name: Nombre del módulo (usar __name__).
        level: Nivel de logging (default: INFO).

    Returns:
        Logger configurado.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(level)
        formatter = logging.Formatter(
            fmt="%(asctime)s │ %(levelname)-8s │ %(name)-25s │ %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
