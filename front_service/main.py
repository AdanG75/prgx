from fastapi import FastAPI, HTTPException

import requests


app = FastAPI()


@app.get("/")
async def hello():
    return {"Greetings": "Hello world"}


@app.get("/inner-server")
async def communicate_inner_server():
    response = requests.get("http://127.0.0.1:9856")

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPEception("Something went wrong")

