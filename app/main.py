from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.get("/hi/")
async def root():
    return {"message": "Hi TA team!"}

handler = Mangum(app)
