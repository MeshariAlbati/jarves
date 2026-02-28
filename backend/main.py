from dotenv import load_dotenv
load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from scheduler.jobs import start_scheduler, scheduler
from bot.telegram_bot import application


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Jarves is starting")
    start_scheduler()
    async with application:
        await application.start()
        await application.updater.start_polling()
        yield
        await application.updater.stop()
        await application.stop()
    print("Jarves is shutting down")
    scheduler.shutdown()


app = FastAPI(title="Jarves", version="0.1.0", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "Jarves is running"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
