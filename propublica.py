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
        """
        Propublica takes authentication info in the header as X-API-Key
        """
        key = None
        with open("./api.json", "r") as file:
            key = json.load(file)
        h = {"X-API-Key": key[PROPUBLICA_INDEX]["key"]}
        return h

    @staticmethod
    def query(*args) -> str:
        """
        Propublica takes queries not like "? &"
        but with "/".

        Join the queries with "/" in right order. 
        """
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

    def process(self, d: dict) -> Dict:
        """
        Rewrites recieved json file into 
        {congress_identifying_key: [congressman_info1, congressman_info2, ...]}
        """
        hash_key = "_".join([d["results"][0]["chamber"], d["results"][0]["congress"]])        
        return {hash_key: d["results"][0]["members"]}


def update_house(congress_info: Congress, congress_num: int) -> None:
    m = congress_info.get_members(105, "house")
    h = congress_info.process(m)
    with open(f"congress_house_{congress_num}.json", "w") as file:
        json.dump(h, file)


def update_senate(congress_info: Congress, congress_num: int) -> None:
    m = congress_info.get_members(105, "senate")
    s = congress_info.process(m)
    with open(f"congress_senate_{congress_num}.json", "w") as file:
        json.dump(s, file)


if __name__ == "__main__":
    c = Congress()

    update_house(c, 105)
