import json
from collections import namedtuple
from enum import Enum

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

        item_levels = list(map(lambda cil: cil.item_level, character_item_levels))
        return sum(item_levels) / len(item_levels)


class GuildPresenter:
    def __init__(self, guild_interactor):
        self.guild_interactor = guild_interactor

    def get_guild_members(self, guild_name, server_name, max_level_only=False):
        characters = self.guild_interactor.get_guild_members(guild_name, server_name, max_level_only)
        return list(map(lambda c: Character(name=c["name"], level=c["level"], realm=c["realm"]), characters))


IntentModel = namedtuple("IntentModel", "name slots session_attributes")
CharacterSlotsModel = namedtuple("CharacterSlotsModel", "character guild_name server_name")


class IntentPresenter:
    def __init__(self, intent_configurations):
        self.intent_configurations = intent_configurations
        
    def parse(self, intent_object, session_object):
        if "slots" in intent_object:
            keys = map(lambda s: s, intent_object['slots'])
            values = map(lambda s: intent_object['slots'][s]['value'], intent_object['slots'])
            slots = dict(zip(keys, values))
        else:
            slots = {}

        if "attributes" in session_object:
            keys = map(lambda s: s, session_object['attributes'])
            values = map(lambda s: session_object['attributes'][s], session_object['attributes'])
            session_attributes = dict(zip(keys, values))
        else:
            session_attributes = {}

        for configuration in self.intent_configurations:
            if intent_object['name'] == configuration.supportedIntentName():
                configurations = configuration.slotConfigurations()
                slots.update(dict(configurations))

        return IntentModel(name=intent_object['name'], slots=slots, session_attributes=session_attributes)


class ImageModel:
    def __init__(self, small_image_url: str, large_image_url: str):
        self.small_image_url = small_image_url
        self.large_image_url = large_image_url


class CardModelType(Enum):
    SIMPLE = 0
    STANDARD = 1
    LINK_ACCOUNT = 2


class CardModel:
    def __init__(self, type: CardModelType, title: str = None, content: str = None, text: str = None, image: ImageModel = None):
        self.type = type
        self.title = title
        self.content = content
        self.text = text
        self.image = image


class SpeechModelType(Enum):
    PLAIN_TEXT = 0
    SSML = 1


class SpeechModel:
    def __init__(self, type: SpeechModelType, text: str):
        self.type = type
        self.text = text


class RepromptModel:
    def __init__(self, output_speech: SpeechModel):
        self.output_speech = output_speech


class ResponseModel:
    def __init__(self, output_speech: SpeechModel = None, card: CardModel = None, reprompt: RepromptModel = None, should_end_session: bool = True):
        self.output_speech = output_speech
        self.card = card
        self.reprompt = reprompt
        self.should_end_session = should_end_session


class ResponseEntity:
    def __init__(self, version: str, session_attributes: dict = None, response: ResponseModel = None):
        self.version = version
        self.session_attributes = session_attributes
        self.response = response


class SimpleError(ResponseEntity):
    def __init__(self, error_message):
        error_speech = SpeechModel(
            type=SpeechModelType.PLAIN_TEXT,
            text=error_message
        )
        response_model = ResponseModel(output_speech=error_speech)
        ResponseEntity.__init__(self, version="1.0", session_attributes=None, response=response_model)