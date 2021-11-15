import uvicorn
from fastapi import FastAPI
from app.core import settings
from app.api.v1 import api_router

app = FastAPI(title="Simple Finance Tracker")
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return "hello"


if __name__ == '__main__':
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
