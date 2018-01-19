from configurations import RequestParameters
from interactors import GuildInteractor, ItemInteractor
from presenters import ItemPresenter, GuildPresenter, IntentPresenter
from processors import GetItemLevel, Counter
from services import RequesterService, ApiService, CharacterIdentityService

request_parameters = RequestParameters()
requester = RequesterService(request_parameters, "https://us.api.battle.net")
api_service = ApiService(requester)
item_interactor = ItemInteractor(api_service)
guild_interactor = GuildInteractor(api_service)
item_presenter = ItemPresenter(item_interactor, guild_interactor)
guild_presenter = GuildPresenter(guild_interactor)
intent_presenter = IntentPresenter()
character_identity_service = CharacterIdentityService(guild_presenter)
registeredIntentProcessors = [
    GetItemLevel(character_identity_service, item_presenter),
    Counter()
]


def lambda_handler(event, context):
    print(event)
    if event['request']['type'] == "IntentRequest":
        intent_model = intent_presenter.parse(intent_object=event['request']['intent'], session_object=event['session'])

        for processor in registeredIntentProcessors:
            if processor.supported_intent_name() == intent_model.name:
                return processor.process(intent_model)

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