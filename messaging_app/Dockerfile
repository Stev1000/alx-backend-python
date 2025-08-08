# --- Base image ---
FROM python:3.10

# --- Environment ---
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=120

# (Optional: if you use Postgres, keep these. If not, you can remove them.)
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libpq-dev \
#   && rm -rf /var/lib/apt/lists/*

# --- Workdir ---
WORKDIR /app

# --- Copy requirements first (better caching) ---
COPY messaging_app/requirements.txt /app/requirements.txt

# --- Robust install: upgrade tooling, then install deps with retries & timeout ---
RUN python -m pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --retries 10 --timeout 120 -r requirements.txt

# --- Copy the rest of your app ---
COPY messaging_app/ /app/

# --- Expose & run ---
# messaging_app/Dockerfile
FROM python:3.10
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PIP_NO_CACHE_DIR=1
WORKDIR /app

COPY messaging_app/requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

COPY messaging_app/ /app/

# For local run the port mapping is: docker run "-p" 8000:8000 messaging_app
EXPOSE 8000

CMD ["gunicorn", "messaging_app.wsgi:application", "-b", "0.0.0.0:8000"]

