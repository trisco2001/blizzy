from abc import abstractmethod


class IntentProcessor:

    @abstractmethod
    def supported_intent_name(self): raise NotImplementedError

    @abstractmethod
    def process(self, intent_model): raise NotImplementedError


class GetItemLevel(IntentProcessor):
    def __init__(self, character_identity_service, item_presenter):
        self.character_identity_service = character_identity_service
        self.item_presenter = item_presenter

    def supported_intent_name(self):
        return "GetItemLevel"

    def process(self, intent_model):
        guild_member = self.character_identity_service.identify_character(
            intent_model.slots.character, intent_model.slots.guild_name, intent_model.slots.server_name
        )
        if guild_member is None:
            return {
                "version": "1.0",
                "response": {
                    "outputSpeech": {
                        "type": "PlainText",
                        "text": "Sorry, but I couldn't figure out what character you were talking about. I thought I "
                                "heard you say {0}".format(intent_model.slots.character)
                    },
                    "shouldEndSession": True
                }
            }

        print("What we're going with: {0} from {1}".format(guild_member.name, guild_member.realm))
        character_item_level = self.item_presenter.get_average_item_level_for_character(server_name=guild_member.realm,
                                                                                   character_name=guild_member.name)
        return {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "{0}, from realm of {1}, has an average equipped item level of {2:.1f}".format(
                        guild_member.name, guild_member.realm, character_item_level.item_level
                    )
                },
                "shouldEndSession": True
            }
        }