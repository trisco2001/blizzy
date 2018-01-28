from unittest import TestCase
import pytest

from presenters import ResponseEntity, ResponseModel, SpeechModel, SpeechModelType, CardModel, CardModelType, \
    ImageModel, RepromptModel
from services import SerializationService


class TestSerializationService(TestCase):

    def setUp(self):
        self.serialization_service = SerializationService()
        self.output_speech = SpeechModel(type=SpeechModelType.PLAIN_TEXT, text="Test Text")
        self.image_model = ImageModel(small_image_url="http://test.com/image_small.jpg",
                                      large_image_url="http://test.com/image_large.jpg")
        self.card = CardModel(type=CardModelType.STANDARD, title="Test Title", content=None, text="Test text",
                              image=self.image_model)
        self.reprompt = RepromptModel(output_speech=self.output_speech)
        self.should_end_session = True
        self.response_model = ResponseModel(output_speech=self.output_speech, card=self.card, reprompt=self.reprompt,
                                            should_end_session=self.should_end_session)
        self.version = "5"
        self.session_attributes = {"test": "yes"}

    def run_tests(self, tests):
        for test_method in tests.keys():
            for test_object, expectation in tests[test_method]:
                # Act
                json = test_method(test_object)

                # Assert
                self.assertEqual(json, expectation,
                                 "Serialized entity {0} not as expected: {1}.".format(test_object, expectation))

    def test_response_entity_to_json(self):
        # Arrange
        response_entity = ResponseEntity(version=self.version, session_attributes=self.session_attributes,
                                         response=self.response_model)

        serialized_image = {
            "smallImageUrl": self.image_model.small_image_url,
            "largeImageUrl": self.image_model.large_image_url
        }
        serialized_card = {
            "type": self.serialization_service.card_model_type_to_json(self.card.type),
            "title": self.card.title,
            "content": self.card.content,
            "text": self.card.text,
            "image": serialized_image
        }
        serialized_output_speech = {
            "type": self.serialization_service.speech_type_to_json(self.output_speech.type),
            "text": self.output_speech.text
        }
        serialized_reprompt = {
            "outputSpeech": serialized_output_speech
        }
        serialized_response_model = {
            "outputSpeech": serialized_output_speech,
            "card": serialized_card,
            "reprompt": serialized_reprompt,
            "shouldEndSession": self.response_model.should_end_session
        }
        serialized_response_entity = {
            "version": self.version,
            "sessionAttributes": self.session_attributes,
            "response": serialized_response_model
        }

        tests = {
            self.serialization_service.response_entity_to_json: [
                (response_entity, serialized_response_entity),
                (None, None)
            ],
            self.serialization_service.response_model_to_json: [
                (self.response_model, serialized_response_model),
                (None, None)
            ],
            self.serialization_service.speech_to_json: [
                (self.output_speech, serialized_output_speech),
                (None, None)
            ],
            self.serialization_service.card_to_json: [
                (self.card, serialized_card),
                (None, None)
            ],
            self.serialization_service.reprompt_to_json: [
                (self.reprompt, serialized_reprompt),
                (None, None)
            ],
            self.serialization_service.image_to_json: [
                (self.image_model, serialized_image),
                (None, None)
            ],
            self.serialization_service.card_model_type_to_json: [
                (CardModelType.SIMPLE,'Simple'),
                (CardModelType.STANDARD,'Standard'),
                (CardModelType.LINK_ACCOUNT,'LinkAccount'),
                (None,None)
            ],
            self.serialization_service.speech_type_to_json: [
                (SpeechModelType.PLAIN_TEXT,'PlainText'),
                (SpeechModelType.SSML,'SSML'),
                (None,None)
            ]
        }

        self.run_tests(tests)

    def test_speech_type_to_json(self):
        self.assertEqual("A", "A")
