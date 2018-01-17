from urllib.parse import urljoin
import difflib
import requests
from presenters import GuildPresenter


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