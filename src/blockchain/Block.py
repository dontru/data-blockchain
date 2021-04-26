import json
import time
from hashlib import sha256


class Block:
    HASH_START = "0" * 2

    def __init__(self, previous_hash: str, index: int, timestamp: float, data: str, proof: int = 0):
        self.previous_hash = previous_hash
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.proof = proof

    @classmethod
    def genesis(cls, data: str) -> 'Block':
        return cls("", 0, time.time(), data).work()

    @classmethod
    def create(cls, previous: 'Block', data: str) -> 'Block':
        return cls(previous.hexdigest(), previous.index + 1, time.time(), data).work()

    def work(self) -> 'Block':
        while not self.valid_proof():
            self.proof += 1
        return self

    def valid_proof(self) -> bool:
        return self.hexdigest().startswith(self.HASH_START)

    def hexdigest(self) -> str:
        return sha256(str(self).encode('utf-8')).hexdigest()

    def __str__(self):
        return json.dumps(self.__dict__)
