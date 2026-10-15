"""API iris de l'exercice, comme dans la correction.

Elle ne réentraîne rien : elle charge le modèle déjà écrit par train.py.
Le conteneur infer lance encore predict.py. Ce fichier est le service HTTP.
"""

import os

import joblib
from fastapi import FastAPI
from pydantic import BaseModel

# L'exercice monte le volume sur /model. La correction utilise /models/model.joblib.
MODEL_PATH = os.getenv("MODEL_PATH", "/model/iris_model.joblib")
CLASSES = ["setosa", "versicolor", "virginica"]

app = FastAPI(title="Iris inference")


def charger_modele():
    objet = joblib.load(MODEL_PATH)
    # train.py enregistre un dictionnaire. La correction enregistre le modèle seul.
    if isinstance(objet, dict) and "model" in objet:
        noms = list(objet.get("target_names") or CLASSES)
        return objet["model"], noms
    return objet, CLASSES


model, classes = charger_modele()


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
    return {"class": classes[int(model.predict(x)[0])]}
