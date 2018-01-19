from abc import abstractmethod

class RequestParameters:
    def __init__(self):
        self.key = "kg6rep4h8xkeyn97wd92hv3nfcagf4pt"
        self.application = "TristanExperiments"
        self.secret = "Swkh4HG8pTQawVTd3zyk5dZmbBFPjQgV"
        self.locale = "en_US"
        
class IntentConfiguration:
    @abstractmethod
    def supportedIntentName():
        raise NotImplementedError
        
    @abstractmethod
    def slotConfigurations():
        return {}
        
class GetItemLevel(IntentConfiguration):
    def supportedIntentName():
        return "GetItemLevel"
        
    def slotConfigurations():
        return {
            "guild_name": "Botany Bay"
            "server_name": "Executus"
        }
