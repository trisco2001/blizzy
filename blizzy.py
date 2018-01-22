import json

from configurations import RequestParameters, GetItemLevel as GetItemLevelConfiguration
from interactors import GuildInteractor, ItemInteractor
from presenters import ItemPresenter, GuildPresenter, IntentPresenter, IntentModel
from processors import GetItemLevel as GetItemLevelProcessor, Counter as CounterProcessor, Yes as YesProcessor, No as NoProcessor
from services import RequesterService, ApiService, CharacterIdentityService, SerializationService

request_parameters = RequestParameters()
requester = RequesterService(request_parameters, "https://us.api.battle.net")
api_service = ApiService(requester)
item_interactor = ItemInteractor(api_service)
guild_interactor = GuildInteractor(api_service)
item_presenter = ItemPresenter(item_interactor, guild_interactor)
guild_presenter = GuildPresenter(guild_interactor)
intent_configurations = [
    GetItemLevelConfiguration()
]
intent_presenter = IntentPresenter(intent_configurations)
character_identity_service = CharacterIdentityService(guild_presenter)
serialization_service = SerializationService()
get_item_level_processor = GetItemLevelProcessor(character_identity_service, item_presenter)
counter_processor = CounterProcessor()
yes_processor = YesProcessor(destination_processors=[counter_processor, get_item_level_processor])
no_processor = NoProcessor(destination_processors=[counter_processor, get_item_level_processor])
registered_intent_processors = [
    get_item_level_processor,
    counter_processor,
    yes_processor,
    no_processor
]


def lambda_handler(event, context):
    if event['request']['type'] == "IntentRequest":
        intent_model = intent_presenter.parse(intent_object=event['request']['intent'], session_object=event['session'])

        for processor in registered_intent_processors:
            if processor.supported_intent_name() == intent_model.name:
                return serialization_service.response_entity_to_json(processor.process(intent_model))

        return {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "I can't figure out what you're asking me. The intent I got was {0}.".format(intent_model.name)
                },
                "shouldEndSession": True
            }
        }