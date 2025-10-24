# Python-based client querying Open-Meteo for Gdynia
FROM python:3.12-slim

# Ensure no .pyc files and buffered output for timely logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set workdir
WORKDIR /app

# Install dependencies first (better layer caching)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py ./

# Default env (can be overridden at run time)
ENV LAT=54.5189 \
    LON=18.5319 \
    TIMEZONE=Europe/Warsaw \
    HOURS_AHEAD=24

# Run the app
CMD ["python", "app.py"]
