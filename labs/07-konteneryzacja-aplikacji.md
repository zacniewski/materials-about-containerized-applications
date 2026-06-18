# Laboratorium 7: Konteneryzacja różnych typów aplikacji (6 godz.)

## Cel laboratorium
Praktyczna konteneryzacja aplikacji w różnych technologiach: Python/Django, Node.js, Java Spring Boot, PHP. Praca z przykładami z repozytorium.

## Wymagania wstępne
- Ukończone Laboratorium 1-6

---

## Część 1: Aplikacja Python/Flask (60 min)

### Ćwiczenie 1.1: Konteneryzacja od zera

```bash
mkdir -p ~/docker-lab07/flask-app && cd ~/docker-lab07/flask-app
```

Utwórz `app.py`:
```python
from flask import Flask, jsonify, request
import os, datetime

app = Flask(__name__)
tasks = []

@app.route('/')
def index():
    return '<h1>Task Manager API</h1><p>Endpoints: /api/tasks (GET, POST)</p>'

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    task = {"id": len(tasks)+1, "title": data.get("title"), "created": str(datetime.datetime.now())}
    tasks.append(task)
    return jsonify(task), 201

@app.route('/health')
def health():
    return jsonify({"status": "ok", "hostname": os.uname().nodename})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Utwórz `requirements.txt`: `flask==3.0.0`

Utwórz `.dockerignore`:
```
__pycache__
*.pyc
.env
.git
venv
```

Utwórz `Dockerfile`:
```dockerfile
FROM python:3.11-slim
RUN groupadd -r app && useradd -r -g app app
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=app:app . .
USER app
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=5s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1
CMD ["python", "app.py"]
```

```bash
docker build -t task-api:v1 .
docker run -d --name task-api -p 5000:5000 task-api:v1
curl http://localhost:5000
curl -X POST http://localhost:5000/api/tasks -H "Content-Type: application/json" -d '{"title":"Nauczyć się Dockera"}'
curl http://localhost:5000/api/tasks
docker stop task-api && docker rm task-api
```

> 📸 **Wymagany screenshot 1**: API Flask działające w kontenerze

---

## Część 2: Aplikacja Node.js/Express (60 min)

### Ćwiczenie 2.1: Konteneryzacja z repozytorium

```bash
cd /ścieżka/do/repozytorium/supporting-materials/examples/01-nodejs
cat Dockerfile
cat index.html
docker build -t node-app:v1 .
docker run -d --name node-app -p 3000:3000 node-app:v1
curl http://localhost:3000
docker stop node-app && docker rm node-app
```

> 📸 **Wymagany screenshot 2**: Aplikacja Node.js z repozytorium

### Ćwiczenie 2.2: Express API od zera

```bash
mkdir -p ~/docker-lab07/express-app && cd ~/docker-lab07/express-app
```

Utwórz `package.json`:
```json
{
  "name": "express-docker",
  "version": "1.0.0",
  "main": "server.js",
  "scripts": { "start": "node server.js" },
  "dependencies": { "express": "^4.18.0" }
}
```

Utwórz `server.js`:
```javascript
const express = require('express');
const os = require('os');
const app = express();

app.get('/', (req, res) => {
    res.json({
        message: 'Hello from Express in Docker!',
        hostname: os.hostname(),
        platform: os.platform(),
        uptime: process.uptime()
    });
});

app.get('/health', (req, res) => res.json({ status: 'ok' }));

app.listen(3000, () => console.log('Server running on port 3000'));
```

Utwórz `Dockerfile`:
```dockerfile
FROM node:20-alpine
RUN addgroup -S app && adduser -S -G app app
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY --chown=app:app . .
USER app
EXPOSE 3000
CMD ["node", "server.js"]
```

```bash
docker build -t express-app:v1 .
docker run -d --name express -p 3000:3000 express-app:v1
curl http://localhost:3000
docker stop express && docker rm express
```

---

## Część 3: Aplikacja Django (90 min)

### Ćwiczenie 3.1: Django z repozytorium

```bash
cd /ścieżka/do/repozytorium/supporting-materials/examples/04-django
cat Dockerfile
cat docker-compose.yaml
cat requirements.txt

docker compose up -d --build
docker compose ps
# Sprawdź aplikację
docker compose down
```

> 📸 **Wymagany screenshot 3**: Aplikacja Django uruchomiona

### Ćwiczenie 3.2: Django + PostgreSQL + Docker Compose

```bash
mkdir -p ~/docker-lab07/django-project && cd ~/docker-lab07/django-project
```

Utwórz `docker-compose.yaml`:
```yaml
services:
  web:
    build: .
    command: >
      sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:secret@db:5432/django_db
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - .:/app

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: django_db
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  pgdata:
```

---

## Część 4: Aplikacja PHP + MySQL (60 min)

### Ćwiczenie 4.1: PHP z repozytorium

```bash
cd /ścieżka/do/repozytorium/supporting-materials/examples/02-php-mysql
cat docker-compose.yaml
cat src/index.php

docker compose up -d
# Otwórz http://localhost:8080
docker compose ps
docker compose down
```

> 📸 **Wymagany screenshot 4**: Aplikacja PHP + MySQL

---

## Część 5: Aplikacja Java Spring Boot (60 min)

### Ćwiczenie 5.1: Spring Boot z repozytorium

```bash
cd /ścieżka/do/repozytorium/supporting-materials/examples/12-java-spring-boot
cat Dockerfile
cat docker-compose.yml

docker compose up -d --build
docker compose ps
docker compose logs
docker compose down
```

> 📸 **Wymagany screenshot 5**: Aplikacja Java Spring Boot

---

## Część 6: Multi-stage build w praktyce (30 min)

### Ćwiczenie 6.1: Go — multi-stage build z repozytorium

```bash
cd /ścieżka/do/repozytorium/supporting-materials/examples/06-msb
cat Dockerfile.single
cat Dockerfile.multi
cat main.go

docker build -t go-single -f Dockerfile.single .
docker build -t go-multi -f Dockerfile.multi .
docker images | grep go-
```

> 📸 **Wymagany screenshot 6**: Porównanie rozmiarów single vs multi-stage

---

## Zadania do samodzielnego wykonania

### Zadanie 1: Konteneryzacja własnego projektu
Wybierz dowolny projekt (własny lub open-source) i skonteneryzuj go. Napisz Dockerfile i docker-compose.yaml.

### Zadanie 2: Optymalizacja
Weź dowolny Dockerfile z ćwiczeń i zoptymalizuj go: multi-stage, mniejszy obraz bazowy, nie-root user, healthcheck.

### Zadanie 3: Dobre praktyki z repozytorium
Przeanalizuj przykłady z `supporting-materials/examples/08-best-practices-dockerfile` i `supporting-materials/examples/09-best-practices-docker-compose`. Zastosuj je w swoim projekcie.

---

## Podsumowanie

Po ukończeniu tego laboratorium powinieneś umieć:
- ✅ Konteneryzować aplikacje Python/Flask/Django
- ✅ Konteneryzować aplikacje Node.js/Express
- ✅ Konteneryzować aplikacje PHP i Java
- ✅ Stosować multi-stage builds w praktyce
- ✅ Konfigurować Docker Compose dla różnych stosów technologicznych
- ✅ Stosować dobre praktyki (nie-root, healthcheck, .dockerignore)
