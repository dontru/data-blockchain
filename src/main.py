from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from blockchain import Block
from blockchain import BlockchainDB

# uvicorn main:app --reload
app = FastAPI()
db = BlockchainDB('Blockchain.SQLite3')
templates = Jinja2Templates(directory='client')


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


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
