import uvicorn
from fastapi import FastAPI
from app.core import settings

app = FastAPI(title="Simple Finance Tracker")

if __name__ == '__main__':
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
