from unittest import TestCase
from mock import Mock, create_autospec

from interactors import GuildInteractor
from services import ApiService


class TestGuildInteractor(TestCase):
    def setUp(self):
        self.api_service = create_autospec(ApiService)
        self.api_service.get_guild_members = Mock(return_value=[{"character": {"level": 100}}, {"character": {"level": 110}}])
        self.guild_interactor = GuildInteractor(api_service=self.api_service)

    def test_get_max_level_guild_members(self):
        guild_members = self.guild_interactor.get_guild_members("Botany Bay", "Executus", True)
        self.assertEqual(1, len(guild_members))

    def test_get_all_guild_members(self):
        guild_members = self.guild_interactor.get_guild_members("Botany Bay", "Executus", False)
        self.assertEqual(2, len(guild_members))

