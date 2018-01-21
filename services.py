import json
from urllib.parse import urljoin
import difflib
import requests
from presenters import ResponseEntity, ResponseModel, SpeechModel, CardModel, RepromptModel, ImageModel, CardModelType, \
    SpeechModelType


class RequesterService:
    def __init__(self, apiKey, baseUrl):
        self.apiKey = apiKey
        self.baseUrl = baseUrl

    def request(self, resource, params=None):
        if params is None:
            params = {}
        url = urljoin(base=self.baseUrl, url=resource)
        params["locale"] = self.apiKey.locale
        params["apikey"] = self.apiKey.key
        response = requests.get(url=url, params=params)
        return response


class ApiService:
    def __init__(self, requester):
        self.requester = requester

    def get_character_items(self, character_name, server_name):
        response = self.requester.request("/wow/character/{0}/{1}".format(server_name, character_name),
                                          params={"fields": "items"})
        return response.json()["items"]

    def get_guild_members(self, guild_name, server_name):
        response = self.requester.request("/wow/guild/{0}/{1}".format(server_name, guild_name),
                                          params={"fields": "members"})
        return response.json()["members"]


class CharacterIdentityService:
    overrides = {
        "villain": "Villianilla",
        "nilla": "Villianilla",
        "villanova": "Villianilla",
        "a nilla": "Villianilla"
    }

    def __init__(self, guild_presenter):
        self.guild_presenter = guild_presenter

    def identify_character(self, raw_name, guild_name, server_name):
        guild_members = self.guild_presenter.get_guild_members(guild_name, server_name, max_level_only=True)
        guild_member_names = map(lambda m: m.name, guild_members)
        print("What we heard: {0}".format(raw_name))
        if raw_name.lower() in CharacterIdentityService.overrides.keys():
            character_name = CharacterIdentityService.overrides[raw_name.lower()]
            print("Resolved to {0} with an override".format(character_name))
        else:
            close_matches = difflib.get_close_matches(raw_name, guild_member_names, n=1, cutoff=0.4)
            if len(close_matches) == 0:
                character_name = None
            else:
                character_name = close_matches[0]

        if character_name is None:
            return None

        return list(filter(lambda m: m.name == character_name, guild_members))[0]


class SerializationService:
    def response_entity_to_json(self, response_entity: ResponseEntity):
        if response_entity is None:
            return None

        result = {
            "version": response_entity.version,
            "sessionAttributes": response_entity.session_attributes,
            "response": self.response_model_to_json(response_model=response_entity.response)
        }

        return result

    def response_model_to_json(self, response_model: ResponseModel):
        if response_model is None:
            return None

        return {
            "outputSpeech": self.speech_to_json(response_model.output_speech),
            "card": self.card_to_json(response_model.card),
            "reprompt": self.reprompt_to_json(response_model.reprompt),
            "shouldEndSession": response_model.should_end_session
        }

    def speech_to_json(self, output_speech: SpeechModel):
        if output_speech is None:
            return None

        return {
            "type": self.speech_type_to_json(output_speech.type),
            "text": output_speech.text
        }

    def card_to_json(self, card: CardModel):
        if card is None:
            return None

        return {
            "type": self.card_model_type_to_json(card.type),
            "title": card.title,
            "content": card.content,
            "text": card.text,
            "image": self.image_to_json(card.image)
        }

    def reprompt_to_json(self, reprompt: RepromptModel):
        if reprompt is None:
            return None

        return {
            "outputSpeech": self.speech_to_json(reprompt.output_speech)
        }

    def image_to_json(self, image: ImageModel = None):
        if image is None:
            return None

        return {
            "smallImageUrl": image.small_image_url,
            "largeImageUrl": image.large_image_url
        }

    def card_model_type_to_json(self, type: CardModelType = None):
        if type is None:
            return None

        cases = {
            CardModelType.SIMPLE: 'Simple',
            CardModelType.LINK_ACCOUNT: 'LinkAccount',
            CardModelType.STANDARD: 'Standard'
        }

        return cases.get(type, None)

    def speech_type_to_json(self, type: SpeechModelType = None):
        if type is None:
            return None

        cases = {
            SpeechModelType.PLAIN_TEXT: 'PlainText',
            SpeechModelType.SSML: 'SSML'
        }

        return cases.get(type, None)
