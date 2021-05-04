from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import blockchain


app = FastAPI()
db = blockchain.DB('Blockchain.SQLite3')
templates = Jinja2Templates(directory='templates')


@app.get("/", response_class=HTMLResponse)
def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/get", response_class=HTMLResponse)
def get(request: Request, block_hash: str = Form(...)):
    print("get block_hash", block_hash)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "blockchain": db.get_blockchain(block_hash),
        "block_hash": block_hash,
    })


@app.post("/add", response_class=HTMLResponse)
def add(request: Request, previous_hash: str = Form(...), data: str = Form(...)):
    block = db.add_block(previous_hash, data) if previous_hash != "GENESIS" else db.add_genesis(data)
    block_hash = block.hexdigest()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "blockchain": db.get_blockchain(block_hash),
        "block_hash": block_hash,
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
