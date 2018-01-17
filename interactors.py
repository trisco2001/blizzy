class GuildInteractor:
    def __init__(self, api_service):
        self.api_service = api_service

    def get_guild_members(self, guild_name, server_name, max_level_only=False):
        members = self.api_service.get_guild_members(guild_name, server_name)
        characters = map(lambda m: m["character"], members)
        if max_level_only:
            return list(filter(lambda c: c["level"] == 110, characters))

        return list(characters)


class ItemInteractor:
    itemsCaredAbout = ["head", "neck", "shoulder", "back", "chest",
                       "wrist", "hands", "waist", "legs", "feet",
                       "finger1", "finger2", "trinket1", "trinket2",
                       "mainHand"]

    def __init__(self, api_service):
        self.api_service = api_service

    @staticmethod
    def get_item_by_name(name, character_items):
        return character_items[name]

    def get_items_for_character(self, character_name, server_name):
        character_items = self.api_service.get_character_items(character_name, server_name)
        filtered_items = list(filter(lambda x: x in ItemInteractor.itemsCaredAbout, character_items))
        items = list(map(lambda name: ItemInteractor.get_item_by_name(name, character_items), filtered_items))
        return items
