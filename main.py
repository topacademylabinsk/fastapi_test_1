import uvicorn

from app.web import app

if __name__ == "__main__":
    uvicorn.run(app=app)
