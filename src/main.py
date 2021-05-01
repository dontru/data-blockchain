from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import blockchain


app = FastAPI()
db = blockchain.DB('Blockchain.SQLite3')
templates = Jinja2Templates(directory='templates')


@app.get("/get/{block_hash}", response_class=HTMLResponse)
def get(request: Request, block_hash: str):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "blockchain": db.get_blockchain(block_hash)
    })


@app.get("/api/block/{block_hash}")
def get_block(block_hash: str):
    return {"block": db.get(block_hash)}


@app.get("/api/blockchain/{block_hash}")
def get_blockchain(block_hash: str):
    return {"blockchain": db.get_blockchain(block_hash)}


@app.post("/api/add_genesis/{data}")
def add_genesis(data: str):
    block = db.add_genesis(data)
    return {"block_hash": block.hexdigest()}


@app.post("/api/add_block/{previous_hash}/{data}")
def add_block(previous_hash: str, data: str):
    block = db.add_block(previous_hash, data)
    return {"block_hash": block.hexdigest() if block is not None else None}
