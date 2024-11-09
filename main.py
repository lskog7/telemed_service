from fastapi import FastAPI
import logging
from contextlib import asynccontextmanager

# Define logging rules
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info(f"Loading 'Telemed project'")

    yield
    logging.info(f"Shutting down 'Telemed project'")

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8222, reload=True)