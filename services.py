from urllib.parse import urljoin
import difflib
import requests
from configurations import RequestParameters
from presenters import ResponseEntity, ResponseModel, SpeechModel, CardModel, RepromptModel, ImageModel, CardModelType, \
    SpeechModelType, GuildPresenter


class RequesterService:
    def __init__(self, request_parameters: RequestParameters, base_url: str):
        self.request_parameters = request_parameters
        self.base_url = base_url

    def request(self, resource: str, params: dict = None):
        if params is None:
            params = {}
        url = urljoin(base=self.base_url, url=resource)
        params["locale"] = self.request_parameters.locale
        params["apikey"] = self.request_parameters.key
        response = requests.get(url=url, params=params)
        return response


class ApiService:
    def __init__(self, requester_service: RequesterService):
        self.requester_service = requester_service

    def get_character_items(self, character_name: str, server_name: str):
        response = self.requester_service.request(
            resource="/wow/character/{0}/{1}".format(server_name, character_name),
            params={"fields": "items"}
        )
        return response.json()["items"]

    def get_guild_members(self, guild_name: str, server_name: str):
        response = self.requester_service.request(
            resource="/wow/guild/{0}/{1}".format(server_name, guild_name),
            params={"fields": "members"}
        )
        return response.json()["members"]


class CharacterIdentityService:

    def __init__(self, guild_presenter: GuildPresenter):
        self.guild_presenter = guild_presenter

    def identify_potential_characters(self, raw_name: str, guild_name: str, server_name: str):
        guild_members = self.guild_presenter.get_guild_members(guild_name, server_name, max_level_only=True)
        guild_member_names = map(lambda m: m.name, guild_members)
        print("What we heard: {0}".format(raw_name))
        close_matches = difflib.get_close_matches(raw_name, guild_member_names, cutoff=0.5)

        return list(map(lambda character_name: list(filter(lambda m: m.name == character_name, guild_members))[0], close_matches))


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
