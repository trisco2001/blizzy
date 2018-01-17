from configurations import RequestParameters
from interactors import GuildInteractor, ItemInteractor
from presenters import ItemPresenter, GuildPresenter, IntentPresenter
from processors import GetItemLevel
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
    GetItemLevel(character_identity_service, item_presenter)
]


def lambda_handler(event, context):
    if event['request']['type'] == "IntentRequest":
        intent_model = intent_presenter.parse(intent_object=event['request']['intent'])

        for processor in registeredIntentProcessors:
            if processor.supported_intent_name() == intent_model.name:
                return processor.process(intent_model)