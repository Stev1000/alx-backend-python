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
EXPOSE 8000
# Dev (simple): 
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Prod (recommended if you have wsgi set up):
# Replace "messaging_app" with your Django project name (the one with settings.py)
CMD ["gunicorn", "messaging_app.wsgi:application", "--bind", "0.0.0.0:8000"]
