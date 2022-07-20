from multiprocessing import AuthenticationError
from typing import Dict
import requests
import json

from constant import *


class Congress:
    def __init__(self):
        self.api_head = self.header()

    @staticmethod
    def header() -> Dict:
        key = None
        with open("./api.json", "r") as file:
            key = json.load(file)
        h = {"X-API-Key": key[PROPUBLICA_INDEX]["key"]}
        return h

    @staticmethod
    def query(*args) -> str:
        return '/'.join(args)
    
    def get_members(self, congress:int, chamber:str) -> Dict:
        assert chamber in {"senate", "house"}
        assert congress in range(*CONGRESS_MEMBER[chamber])

        q = self.query(str(congress), chamber, "members.json")
        r = requests.get(
            url=''.join([PROPUBLICA_BASE, PROPUBLICA_VER, q]),
            headers=self.api_head
        )
        if r.status_code != 200:
            return None
        
        result = r.json()
        r.close()
        return result

    def get_committees(self, congress:int, chamber:str) -> Dict:
        assert chamber in {"senate", "house", "joint"}
        assert congress in range(*CONGRESS_COMMITTEE)

        q = self.query(str(congress), chamber, "committees.json")
        r = requests.get(
            url=''.join([PROPUBLICA_BASE, PROPUBLICA_VER, q]),
            headers=self.api_head
        )
        if r.status_code != 200:
            return None
        
        result = r.json()
        r.close()
        return result

    def process(self, d: dict):
        print(d["results"][-1]["congress"])
        print(d["results"][-1]["members"][0])


if __name__ == "__main__":
    c = Congress()
    r = c.get_members(102, "house")
    c.process(r)
