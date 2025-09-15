from django.test import SimpleTestCase

from .utils import camel_to_kebab, is_jsonable, flatten
from .settings import headless_settings
from .registry import HeadlessRegistry


class UtilsTests(SimpleTestCase):
    def test_camel_to_kebab_basic(self):
        self.assertEqual(camel_to_kebab("CamelCase"), "camel-case")
        self.assertEqual(camel_to_kebab("camelCase"), "camel-case")
        self.assertEqual(camel_to_kebab("URLValue"), "urlvalue")
        self.assertEqual(camel_to_kebab(""), "")
        self.assertIsNone(camel_to_kebab(None))

    def test_is_jsonable(self):
        self.assertTrue(is_jsonable({"a": 1}))
        self.assertTrue(is_jsonable([1, 2, 3]))
        self.assertFalse(is_jsonable(set([1, 2, 3])))

    def test_flatten(self):
        self.assertEqual(flatten([[1, 2], [3], [], [4, 5]]), [1, 2, 3, 4, 5])


class SettingsTests(SimpleTestCase):
    def test_defaults_available(self):
        # Ensure default settings are accessible and of expected types
        self.assertIsNone(headless_settings.AUTH_SECRET_KEY)
        self.assertIsInstance(headless_settings.AUTH_SECRET_KEY_HEADER, str)
        self.assertIsInstance(headless_settings.FILTER_EXCLUSION_SYMBOL, str)
        self.assertIsInstance(headless_settings.NON_FILTER_FIELDS, list)
        # DEFAULT_SERIALIZER_CLASS resolves to a class
        from rest_framework.serializers import ModelSerializer

        self.assertTrue(issubclass(headless_settings.DEFAULT_SERIALIZER_CLASS, ModelSerializer))


class RegistryTests(SimpleTestCase):
    def test_registry_register_and_get(self):
        # Create a fake model class with minimal _meta interface
        class _Meta:
            label_lower = "app.model"

        class FakeModel:
            _meta = _Meta()

        reg = HeadlessRegistry()
        reg.register(FakeModel, singleton=True)
        self.assertEqual(len(reg), 1)
        cfg = reg.get_model("APP.Model")
        self.assertIsNotNone(cfg)
        self.assertIs(cfg["model"], FakeModel)
        self.assertTrue(cfg["singleton"])