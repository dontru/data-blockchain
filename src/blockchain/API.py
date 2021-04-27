from fastapi import FastAPI

from .Block import Block
from .BlockchainDB import BlockchainDB

# uvicorn blockchain.API:app --reload
app = FastAPI()
db = BlockchainDB('Blockchain.SQLite3')


@app.get("/block/{block_hash}")
def get_block(block_hash: str):
    return {"block": db.get(block_hash)}


@app.get("/blockchain/{block_hash}")
def get_blockchain(block_hash: str):
    blockchain = []
    while block := db.get(block_hash):
        blockchain.insert(0, block)
        block_hash = block.previous_hash
    return {"blockchain": blockchain}


@app.post("/add_genesis/{data}")
def add_genesis(data: str):
    db.add(block := Block.genesis(data))
    return {"block_hash": block.hexdigest()}


@app.post("/add_block/{previous_hash}/{data}")
def add_block(previous_hash: str, data: str):
    previous = db.get(previous_hash)
    if previous is not None:
        db.add(block := Block.create(previous, data))
        block_hash = block.hexdigest()
    else:
        block_hash = None
    return {"block_hash": block_hash}
