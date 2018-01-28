from unittest import TestCase
from mock import create_autospec, Mock

from services import RequesterService, ApiService


class TestApiService(TestCase):
    def setUp(self):
        self.requester_service = create_autospec(RequesterService)
        self.api_service = ApiService(requester_service=self.requester_service)

    def test_get_character_items(self):
        self.requester_service.request = Mock(return_value={"items": [1, 2, 3, 4]})
        character_items = self.api_service.get_character_items(character_name="Gamlin", server_name="Executus")
        self.assertEquals(len(character_items), 4)

    def test_get_guild_members(self):
        self.requester_service.request = Mock(return_value={"members": [1, 2, 3, 4]})
        character_items = self.api_service.get_guild_members(guild_name="Botany Bay", server_name="Executus")
        self.assertEquals(len(character_items), 4)
