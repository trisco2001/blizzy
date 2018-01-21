import random
from abc import abstractmethod

from presenters import ResponseEntity, ResponseModel, SpeechModel, SpeechModelType, CardModel, CardModelType, \
    RepromptModel, SimpleError


class IntentProcessor:

    @abstractmethod
    def supported_intent_name(self): raise NotImplementedError

    @abstractmethod
    def process(self, intent_model): raise NotImplementedError


class Counter(IntentProcessor):
    keep_going_varients = [
        "Should I keep going?",
        "Want to add another one?",
        "Let it ride?",
        "Again?",
        "Let me do another?"
    ]

    def supported_intent_name(self):
        return "CounterIntent"

    def process(self, intent_model):
        if "number" not in intent_model.session_attributes:
            intent_model.session_attributes["number"] = 0

        intent_model.session_attributes["number"] = intent_model.session_attributes["number"] + 1
        intent_model.session_attributes["destinationIntent"] = "CounterIntent"

        keep_going_statement = Counter.keep_going_varients[int(random.random() * len(Counter.keep_going_varients))]
        version = "1.0"
        response_text = "You are up to {0}. {1}".format(intent_model.session_attributes["number"], keep_going_statement)
        session_attributes = intent_model.session_attributes
        output_speech = SpeechModel(
            SpeechModelType.PLAIN_TEXT,
            text=response_text
        )
        card = CardModel(type=CardModelType.SIMPLE, title="Counter Intent", content=response_text)
        repromptSpeech = SpeechModel(SpeechModelType.PLAIN_TEXT, text="Want to increment again?")
        reprompt = RepromptModel(output_speech=repromptSpeech)

        response = ResponseModel(output_speech=output_speech, card=card, reprompt=reprompt, should_end_session=False)

        response_entity = ResponseEntity(version=version,
                                         session_attributes=session_attributes,
                                         response=response)

        return response_entity


class Yes(IntentProcessor):
    def __init__(self, destination_processors: list):
        self.destination_processors = destination_processors

    def supported_intent_name(self):
        return "YesIntent"

    def process(self, intent_model):
        if "destinationIntent" not in intent_model.session_attributes:
            return SimpleError(error_message="The destination intent was not found in the session attributes.")

        destination_intent = intent_model.session_attributes["destinationIntent"]
        for processor in self.destination_processors:
            if processor.supported_intent_name() == destination_intent:
                return processor.process(intent_model)

        return SimpleError(
            "The destination intent {0} was not supported in the Yes Intent Processor.".format(destination_intent)
        )


class No(IntentProcessor):

    def supported_intent_name(self):
        return "NoIntent"

    def process(self, intent_model):
        if "number" not in intent_model.session_attributes:
            intent_model.session_attributes["number"] = 1

        version = "1.0"
        response_text = "You finished at {0}.".format(intent_model.session_attributes["number"])
        output_speech = SpeechModel(
            SpeechModelType.PLAIN_TEXT,
            text=response_text
        )
        card = CardModel(type=CardModelType.SIMPLE, title="Counter Intent", content=response_text)

        response = ResponseModel(output_speech=output_speech, card=card, reprompt=None, should_end_session=True)

        response_entity = ResponseEntity(version=version,
                                         session_attributes=None,
                                         response=response)

        return response_entity


class GetItemLevel(IntentProcessor):
    def __init__(self, character_identity_service, item_presenter):
        self.character_identity_service = character_identity_service
        self.item_presenter = item_presenter

    def supported_intent_name(self):
        return "GetItemLevel"

    def process(self, intent_model):
        guild_member = self.character_identity_service.identify_character(
            intent_model.slots['character'], intent_model.slots['guild_name'], intent_model.slots['server_name']
        )
        if guild_member is None:
            return SimpleError(
                error_message="Sorry, but I couldn't figure out what character you were talking about. I thought "
                              "I heard you say {0}".format(intent_model.slots['character'])
            )

        character_item_level = self.item_presenter.get_average_item_level_for_character(server_name=guild_member.realm,
                                                                                        character_name=guild_member.name)

        speech = SpeechModel(
                type=SpeechModelType.PLAIN_TEXT,
                text="{0}, from realm of {1}, has an average equipped item level of {2:.1f}".format(
                        guild_member.name, guild_member.realm, character_item_level.item_level)
            )
        response_model = ResponseModel(output_speech=speech)
        response_entity = ResponseEntity(version="1.0", response=response_model)
        return response_entity
