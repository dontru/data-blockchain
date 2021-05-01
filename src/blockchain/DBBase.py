import sqlite3
from typing import Optional

from .Block import Block


class DBBase:
    CREATE_BLOCKS = 'CREATE TABLE Blocks (hash CHARACTER(64), ' \
                    'previous_hash CHARACTER(64), idx INT, timestamp DOUBLE, data TEXT, proof INT)'

    def __init__(self, database: str):
        self.database = database

    def add(self, block: Block) -> None:
        parameters = (block.hexdigest(), block.previous_hash, block.index, block.timestamp, block.data, block.proof)
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO Blocks VALUES (?, ?, ?, ?, ?, ?)', parameters)
            connection.commit()

    def get(self, block_hash: str) -> Optional[Block]:
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM Blocks WHERE hash=?', (block_hash,))
            rows = cursor.fetchall()
            return Block(*rows[0][1:]) if rows else None
