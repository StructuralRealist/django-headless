__title__ = "Django Headless"
__version__ = "1.0.0-canary.1"
__author__ = "Leon van der Grient"
__license__ = "BSD 3-Clause"

from typing import Type

from django.db import models
from .registry import headless_registry

# Version synonym
VERSION = __version__


def headless(singleton = False):
    """
    Decorator to register a Django model to a registry.

    Usage:
        @headless()
        class MyModel(models.Model):
            pass
    """

    def decorator(model_class: Type[models.Model]):
        headless_registry.register(model_class, singleton=singleton)

        return model_class

    return decorator
