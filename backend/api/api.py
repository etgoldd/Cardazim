from fastapi import FastAPI

app = FastAPI()

from backend.api.creators import creator_router

app.include_router(creator_router)
