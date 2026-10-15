"""API iris du TP 4 : la même que infer/app.py, plus le compteur Redis."""

import os

import joblib
import redis
from fastapi import FastAPI
from pydantic import BaseModel

MODEL_PATH = os.getenv("MODEL_PATH", "/models/model.joblib")
CLASSES = ["setosa", "versicolor", "virginica"]

app = FastAPI(title="Iris inference")

# « base » est le nom du service Redis dans docker-compose.yml.
compteur = redis.Redis(
    host=os.environ.get("REDIS_HOST", "base"),
    port=int(os.environ.get("REDIS_PORT", "6379")),
    decode_responses=True,
)
CLE_COMPTEUR = "predictions"

model = joblib.load(MODEL_PATH)


class Flower(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(f: Flower):
    x = [[f.sepal_length, f.sepal_width, f.petal_length, f.petal_width]]
    espece = CLASSES[int(model.predict(x)[0])]
    total = compteur.incr(CLE_COMPTEUR)
    return {"class": espece, "predictions": total}


@app.get("/stats")
def stats():
    total = compteur.get(CLE_COMPTEUR)
    return {"predictions": int(total or 0)}
