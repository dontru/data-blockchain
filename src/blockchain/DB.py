from typing import Optional, List

from .Block import Block
from .DBBase import DBBase


class DB(DBBase):
    def get_blockchain(self, block_hash: str) -> List[Block]:
        blockchain = []
        while block := self.get(block_hash):
            blockchain.insert(0, block)
            block_hash = block.previous_hash
        return blockchain

    def add_genesis(self, data: str) -> Block:
        self.add(block := Block.genesis(data))
        return block

    def add_block(self, previous_hash: str, data: str) -> Optional[Block]:
        previous = self.get(previous_hash)
        if previous is not None:
            self.add(block := Block.create(previous, data))
            return block
