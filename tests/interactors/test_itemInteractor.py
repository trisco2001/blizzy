from unittest import TestCase
from mock import Mock, create_autospec

from interactors import ItemInteractor
from services import ApiService


class TestItemInteractor(TestCase):
    def setUp(self):
        self.api_service = create_autospec(ApiService)
        self.item_interactor = ItemInteractor(api_service=self.api_service)
        self.character_items = {"tabard": {"level": 100},"neck": {"level": 100}, "head": {"level": 101}}
        self.character_items_cared_about = {"neck": {"level": 100}, "head": {"level": 101}}
        self.api_service.get_character_items = Mock(return_value=self.character_items)

    def test_get_item_by_name(self):
        neck = self.item_interactor.get_item_by_name("neck", character_items=self.character_items)
        self.assertDictEqual({"level": 100}, neck)

    def test_get_items_for_character(self):
        items = self.item_interactor.get_items_for_character("Gamlin", "Executus")
        self.assertEqual(2, len(items))
