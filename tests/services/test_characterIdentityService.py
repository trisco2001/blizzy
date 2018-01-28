from unittest import TestCase
from mock import Mock, create_autospec

from presenters import Character, GuildPresenter
from services import CharacterIdentityService


class TestCharacterIdentityService(TestCase):
    def setUp(self):
        self.guild_presenter = create_autospec(GuildPresenter)
        self.guild_presenter.get_guild_members = Mock(return_value=[Character("Gamlin", 110, "Executus"),
                                                                    Character("Villianilla", 110, "Executus")])
        self.character_identity_service = CharacterIdentityService(guild_presenter=self.guild_presenter)

    def test_identify_potential_characters(self):
        # Arrange
        guild_name = "Botany Bay"
        server_name = "Executus"
        tests = [
            ("Derp", 0),
            ("Proxeidolon", 0),
            ("Gormlorn", 1),
            ("Camlin", 1),
            ("Villain", 1),
            ("Nilla", 1)
        ]

        for raw_name, expected_number in tests:
            # Act
            potential_characters = self.character_identity_service.identify_potential_characters(raw_name, guild_name,
                                                                                                 server_name)

            # Assert
            message = "The search for {0} yielded an incorrect number of results {1}, expected {2} instead.".format(
                    raw_name, len(potential_characters), expected_number
                )
            self.assertEqual(len(potential_characters), expected_number, message)
