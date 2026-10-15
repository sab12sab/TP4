FROM python:3.11-slim

WORKDIR /app

# scikit-learn a besoin de libgomp au démarrage (OpenMP).
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# pip 24.0 de l'image refuse un wheel si le téléchargement a été coupé.
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --retries 5 --timeout 120 -r requirements.txt

COPY train_model.py app.py .
# Même fichier que la correction : /models/model.joblib, le modèle seul.
RUN python train_model.py

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
