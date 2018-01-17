import json
from collections import namedtuple

CharacterItem = namedtuple("CharacterItem", "name level")
Character = namedtuple("Character", "name level realm")
CharacterItemLevel = namedtuple("Character", "name item_level realm")


class ItemPresenter:
    def __init__(self, item_interactor, guild_interactor):
        self.item_interactor = item_interactor
        self.guild_interactor = guild_interactor

    def get_items_for_character(self, character_name, server_name):
        raw_items = self.item_interactor.get_items_for_character(character_name, server_name)
        character_items = list(
            map(lambda raw_item: CharacterItem(name=raw_item["name"], level=raw_item["itemLevel"]), raw_items))
        return character_items

    def get_average_item_level_for_character(self, character_name, server_name):
        items = self.get_items_for_character(character_name, server_name)
        item_levels = list(map(lambda item: item.level, items))
        average_item_level = sum(item_levels) / len(item_levels)
        print("Character: {0} = {1:0.1f}".format(character_name, average_item_level))
        return CharacterItemLevel(name=character_name, realm=server_name, item_level=average_item_level)

    def get_average_item_level_for_guild(self, guild_name, server_name, include_top=0):
        guild_members = self.guild_interactor.get_guild_members(guild_name, server_name, max_level_only=True)
        character_item_levels = list(map(
            lambda m: self.get_average_item_level_for_character(m["name"], m["realm"]),
            guild_members)
        )
        character_item_levels = sorted(character_item_levels, key=lambda cil: cil.item_level, reverse=True)
        if include_top > 0:
            character_item_levels = character_item_levels[0:include_top]
            print("Only counting the top {0} members:".format(include_top))
            print(json.dumps(character_item_levels, indent=2))

        item_levels = list(map(lambda cil: cil.item_level, character_item_levels))
        return sum(item_levels) / len(item_levels)


class GuildPresenter:
    def __init__(self, guild_interactor):
        self.guild_interactor = guild_interactor

    def get_guild_members(self, guild_name, server_name, max_level_only=False):
        characters = self.guild_interactor.get_guild_members(guild_name, server_name, max_level_only)
        return list(map(lambda c: Character(name=c["name"], level=c["level"], realm=c["realm"]), characters))


IntentModel = namedtuple("IntentModel", "name slots")
SlotsModel = namedtuple("SlotsModel", "character guild_name server_name")


class IntentPresenter:
    def parse(self, intent_object):
        slots_model = SlotsModel(character=intent_object['slots']['character']['value'], guild_name="Botany Bay", server_name="Executus")
        return IntentModel(name=intent_object['name'], slots=slots_model)
