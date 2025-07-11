import datetime
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, status, HTTPException
from peewee import *
from pydantic import BaseModel

db = SqliteDatabase("reviews.db", check_same_thread=False)


class ReviewPydantic(BaseModel):
    text: str
    sentiment: Optional[str] = None
    created_at: Optional[datetime.datetime] = None


class Review(Model):
    text: str = TextField()
    sentiment: str = TextField()
    created_at: datetime.datetime = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        db_table = "reviews"


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.connect()
    db.create_tables([Review])
    yield
    db.close()


app = FastAPI(lifespan=lifespan)


def check_includes(keyworkds: list, text: str) -> bool:
    return any(map(lambda k: k in text, keyworkds))


@app.post("/reviews", status_code=status.HTTP_204_NO_CONTENT)
async def create_reviews(review: ReviewPydantic):
    if check_includes(["хорош", "люблю"], review.text):
        sentiment = "positive"
    elif check_includes(["плохо", "ненавиж"], review.text):
        sentiment = "negative"
    else:
        sentiment = "neutral"
    r = Review(
        text=review.text, sentiment=sentiment, created_at=datetime.datetime.utcnow().isoformat()
    )
    r.save()
    return True


@app.get("/reviews")
async def read_reviews(sentiment: str | None = None):
    query = Review.select()
    if sentiment is not None:
        if sentiment not in ["neutral", "positive", "negative"]:
            raise HTTPException(status_code=422, detail="invalid filter value")
        query = query.where(Review.sentiment == sentiment)
    return [
        {
            "id": r.id,
            "text": r.text,
            "sentiment": r.sentiment,
            "created_at": r.created_at,
        }
        for r in query
    ]
