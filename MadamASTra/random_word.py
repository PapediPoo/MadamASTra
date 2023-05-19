'''
Generates random words
'''
import random
import json
import requests

class WordGenerator():
    '''
    Generates random words by either
    1. getting them online
    2. using a list of offline words
    '''
    RANDOMWORDURL = "https://random-word-api.herokuapp.com/word"
    OFFLINEWORDS = [
        "which", "apple", "chemical", "beautiful", "fell",
        "broken", "scientist", "party", "farm", "religious",
        "sit", "likely", "basic", "solid", "mud",
        "buried", "though", "diameter", "mad", "origin",
        "elephant", "brush", "stiff", "environment", "chosen",
        "tank", "stick", "amount", "development", "officer",
        "offer", "fully", "poet", "water", "swim",
        "aloud", "pond", "shape", "tales", "dirty",
        "battle", "lunch", "sitting", "eager", "twelve",
        "stone", "finger", "once", "bag", "short",
        "hearing", "desk", "composition", "asleep", "rear",
        "slowly", "hardly", "save", "quietly", "extra",
        "mostly", "everything", "top", "different", "plane",
        "vegetable", "helpful", "exactly", "trade", "diagram",
        "tool", "fence", "rest", "sweet", "blank",
        "everything", "live", "you", "age", "date",
        "offer", "wolf", "wrote", "try", "football",
        "box", "late", "war", "increase", "state",
        "gulf", "once", "system", "after", "half",
        "far", "worse", "his", "brass", "modern"
    ]

    def __init__(self) -> None:
        pass

    def generate(self, length=None, number=1) -> list[str]:
        '''
        Tries to fetch a random word online.
        If it fails, falls back to a static offline list
        '''
        request_url = self.RANDOMWORDURL
        if length is not None and number is not None:
            request_url += f"?length={length}&number={number}"
        elif length is not None:
            request_url += f"?length={length}"
        elif number is not None:
            request_url += f"?number={number}"
        response = requests.get(request_url, timeout=1)
        if response.ok:
            return json.loads(response.content.decode('utf-8'))
        return self.__generate_offline(number)

    def __generate_offline(self, number) -> str:
        result = []
        for _ in range(number):
            idx = random.randint(0, len(self.OFFLINEWORDS))
            result.append(self.OFFLINEWORDS[idx])
        return result
