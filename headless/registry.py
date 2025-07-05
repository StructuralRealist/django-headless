from typing import Type, Dict, Optional, TypedDict

from django.db import models

class ModelConfig(TypedDict):
    model: Type[models.Model]
    singleton: bool


class HeadlessRegistry:
    """
    A registry to store registered Django models.
    """

    def __init__(self):
        self._models: Dict[str, ModelConfig] = {}

    def register(self,  model_class: Type[models.Model], singleton = False):
        """
        Register a model in the registry.

        Args:
            model_class: The Django model class to register
            singleton: Whether the model should be registered as a singleton
        """
        self._models[model_class.__name__.lower()] = {
            "model": model_class,
            "singleton": singleton
        }

    def get_model(self, name: str) -> Optional[ModelConfig]:
        """
        Get a model by name.

        Args:
            name: The name of the model to get.
        """
        return self._models.get(name.lower())

    def get_models(self) -> Dict[str, ModelConfig]:
        """
        Get all registered models.
        """
        return self._models.copy()

    def __len__(self):
        return len(self._models)


# Create a default registry
headless_registry = HeadlessRegistry()
