import sys

from fastapi import FastAPI
import uvicorn

from src.routers import api_router

def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router.router)
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)