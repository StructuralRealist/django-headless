from django.apps import AppConfig
from django.urls import path
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet

from ..utils import is_runserver


class DjangoHeadlessRestConfig(AppConfig):
    name = "headless.rest"
    label = "headless_rest"

    def ready(self):
        from ..registry import headless_registry
        from ..utils import log
        from .routers import rest_router
        from .viewsets import SingletonViewSet
        from .urls import urlpatterns

        if is_runserver():
            log(":building_construction:", "Setting up REST routes")
            models = headless_registry.get_models()

            for [label, model_config] in models.items():
                model_class = model_config["model"]
                singleton = model_config["singleton"]

                class Serializer(serializers.ModelSerializer):
                    class Meta:
                        model = model_class
                        fields = "__all__"

                if singleton:

                    class ViewSet(SingletonViewSet):
                        queryset = model_class.objects.first()
                        serializer_class = Serializer

                    log("   |---", f"/{label} (singleton)")
                    urlpatterns.append(
                        path(
                            label,
                            ViewSet.as_view(
                                {
                                    "get": "retrieve",
                                    "put": "update",
                                    "patch": "partial_update",
                                }
                            ),
                        )
                    )

                else:

                    class ViewSet(ModelViewSet):
                        queryset = model_class.objects.all()
                        serializer_class = Serializer

                    log("   |---", f"/{label}")
                    rest_router.register(label, ViewSet)
