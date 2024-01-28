from fastapi import FastAPI

from backend.api.creators import creator_router


app = FastAPI()
app.include_router(creator_router)


@app.get("/")
def root():
    return {"message": "Hello World"}
