# Laboratorium 2: Budowanie obrazów z Dockerfile (6 godz.)

## Cel laboratorium
Nauka tworzenia własnych obrazów Docker za pomocą Dockerfile — od prostych do zaawansowanych, z wykorzystaniem multi-stage builds.

## Wymagania wstępne
- Ukończone Laboratorium 1
- Podstawowa znajomość Pythona lub Node.js

---

## Część 1: Pierwszy Dockerfile (60 min)

### Ćwiczenie 1.1: Prosty obraz z Pythonem

Utwórz katalog roboczy:
```bash
mkdir -p ~/docker-lab02/hello-python && cd ~/docker-lab02/hello-python
```

Utwórz plik `app.py`:
```python
# app.py
import platform
import os

print("=" * 40)
print("Witaj z kontenera Docker!")
print(f"Python: {platform.python_version()}")
print(f"System: {platform.system()} {platform.release()}")
print(f"Hostname: {os.uname().nodename}")
print(f"Użytkownik: {os.getenv('USER', 'nieznany')}")
print("=" * 40)
```

Utwórz `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY app.py .
CMD ["python", "app.py"]
```

Zbuduj i uruchom:
```bash
docker build -t hello-python:v1 .
docker run --rm hello-python:v1
```

> 📸 **Wymagany screenshot 1**: Wynik budowania i uruchomienia obrazu

### Ćwiczenie 1.2: Analiza warstw

```bash
# Historia warstw
docker history hello-python:v1

# Rozmiar obrazu
docker images hello-python
```

### Ćwiczenie 1.3: Obraz z zależnościami

Utwórz `requirements.txt`:
```
flask==3.0.0
requests==2.31.0
```

Utwórz `app.py` (nowa wersja):
```python
from flask import Flask
import requests
import os

app = Flask(__name__)

@app.route('/')
def hello():
    hostname = os.uname().nodename
    return f"<h1>Witaj z kontenera {hostname}!</h1><p>Flask działa w Dockerze.</p>"

@app.route('/health')
def health():
    return {"status": "ok"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Utwórz `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

```bash
docker build -t flask-app:v1 .
docker run -d --name flask-test -p 5000:5000 flask-app:v1
curl http://localhost:5000
curl http://localhost:5000/health
```

> 📸 **Wymagany screenshot 2**: Aplikacja Flask działająca w kontenerze

---

## Część 2: Instrukcje Dockerfile w praktyce (90 min)

### Ćwiczenie 2.1: WORKDIR, COPY, ADD

```bash
mkdir -p ~/docker-lab02/workdir-test && cd ~/docker-lab02/workdir-test
```

Utwórz strukturę plików:
```bash
mkdir -p src config
echo "print('Hello from src')" > src/main.py
echo "DEBUG=true" > config/app.conf
echo "Dane testowe" > data.txt
tar czf archive.tar.gz data.txt
```

Utwórz `Dockerfile`:
```dockerfile
FROM python:3.11-slim

# WORKDIR tworzy katalog jeśli nie istnieje
WORKDIR /app

# COPY — kopiowanie plików
COPY src/ ./src/
COPY config/app.conf ./config/

# ADD — rozpakowuje archiwum automatycznie
ADD archive.tar.gz ./extracted/

# Sprawdzenie struktury
RUN ls -la /app/ && ls -la /app/extracted/

CMD ["python", "src/main.py"]
```

```bash
docker build -t workdir-test .
docker run --rm workdir-test
```

### Ćwiczenie 2.2: ENV i ARG

```bash
mkdir -p ~/docker-lab02/env-test && cd ~/docker-lab02/env-test
```

Utwórz `app.py`:
```python
import os
print(f"APP_NAME: {os.getenv('APP_NAME', 'brak')}")
print(f"APP_VERSION: {os.getenv('APP_VERSION', 'brak')}")
print(f"ENVIRONMENT: {os.getenv('ENVIRONMENT', 'brak')}")
print(f"DEBUG: {os.getenv('DEBUG', 'brak')}")
```

Utwórz `Dockerfile`:
```dockerfile
# ARG — dostępny tylko podczas budowania
ARG PYTHON_VERSION=3.11

FROM python:${PYTHON_VERSION}-slim

# ENV — dostępny w kontenerze
ENV APP_NAME="Moja Aplikacja" \
    APP_VERSION="1.0.0" \
    ENVIRONMENT="production"

WORKDIR /app
COPY app.py .

# ARG po FROM musi być ponownie zadeklarowany
ARG BUILD_DATE
LABEL build_date=${BUILD_DATE}

CMD ["python", "app.py"]
```

```bash
# Budowanie z argumentami
docker build --build-arg BUILD_DATE=$(date +%Y-%m-%d) -t env-test:v1 .

# Uruchomienie z domyślnymi ENV
docker run --rm env-test:v1

# Nadpisanie ENV z CLI
docker run --rm -e ENVIRONMENT=development -e DEBUG=true env-test:v1
```

> 📸 **Wymagany screenshot 3**: Różnica między domyślnymi a nadpisanymi zmiennymi

### Ćwiczenie 2.3: CMD vs ENTRYPOINT

```bash
mkdir -p ~/docker-lab02/cmd-test && cd ~/docker-lab02/cmd-test
```

Utwórz `greet.py`:
```python
import sys
name = sys.argv[1] if len(sys.argv) > 1 else "Świat"
print(f"Cześć, {name}!")
```

**Wariant A — tylko CMD:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY greet.py .
CMD ["python", "greet.py"]
```

```bash
docker build -t greet-cmd .
docker run --rm greet-cmd                    # Cześć, Świat!
docker run --rm greet-cmd echo "nadpisane"   # echo nadpisane (CMD nadpisany!)
```

**Wariant B — ENTRYPOINT + CMD:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY greet.py .
ENTRYPOINT ["python", "greet.py"]
CMD ["Świat"]
```

```bash
docker build -t greet-entry -f Dockerfile.entry .
docker run --rm greet-entry              # Cześć, Świat!
docker run --rm greet-entry "Docker"     # Cześć, Docker!
docker run --rm greet-entry "Student"    # Cześć, Student!
```

> 📸 **Wymagany screenshot 4**: Porównanie zachowania CMD vs ENTRYPOINT

### Ćwiczenie 2.4: USER — użytkownik nie-root

```bash
mkdir -p ~/docker-lab02/user-test && cd ~/docker-lab02/user-test
```

```dockerfile
FROM python:3.11-slim

# Tworzenie użytkownika
RUN groupadd -r appuser && useradd -r -g appuser -d /app appuser

WORKDIR /app
COPY --chown=appuser:appuser app.py .

# Przełączenie na nie-root
USER appuser

CMD ["python", "-c", "import os; print(f'UID: {os.getuid()}, User: {os.getenv(\"USER\", \"appuser\")}')"]
```

```bash
echo "" > app.py
docker build -t user-test .
docker run --rm user-test
# Porównaj z:
docker run --rm python:3.11-slim python -c "import os; print(f'UID: {os.getuid()}')"
```

---

## Część 3: .dockerignore i kontekst budowania (30 min)

### Ćwiczenie 3.1: Wpływ .dockerignore

```bash
mkdir -p ~/docker-lab02/ignore-test && cd ~/docker-lab02/ignore-test

# Utwórz pliki
echo "print('app')" > app.py
mkdir -p node_modules .git __pycache__
dd if=/dev/zero of=node_modules/big-file bs=1M count=50 2>/dev/null
echo "secret" > .env
```

Bez `.dockerignore`:
```bash
docker build -t ignore-test:without .
# Zwróć uwagę na "Sending build context to docker daemon"
```

Utwórz `.dockerignore`:
```
node_modules
.git
__pycache__
*.pyc
.env
.vscode
.idea
```

Z `.dockerignore`:
```bash
docker build -t ignore-test:with .
# Porównaj rozmiar kontekstu
```

> 📸 **Wymagany screenshot 5**: Porównanie rozmiaru kontekstu z i bez .dockerignore

---

## Część 4: Multi-stage builds (60 min)

### Ćwiczenie 4.1: Multi-stage dla aplikacji Go

```bash
mkdir -p ~/docker-lab02/go-multistage && cd ~/docker-lab02/go-multistage
```

Utwórz `main.go`:
```go
package main

import (
    "fmt"
    "net/http"
    "os"
)

func main() {
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        hostname, _ := os.Hostname()
        fmt.Fprintf(w, "Hello from Go container: %s\n", hostname)
    })
    fmt.Println("Server starting on :8080")
    http.ListenAndServe(":8080", nil)
}
```

Utwórz `go.mod`:
```
module hello-go
go 1.22
```

**Dockerfile bez multi-stage:**
```dockerfile
FROM golang:1.22
WORKDIR /app
COPY . .
RUN go build -o server .
EXPOSE 8080
CMD ["./server"]
```

**Dockerfile z multi-stage:**
```dockerfile
# Stage 1: Build
FROM golang:1.22 AS builder
WORKDIR /app
COPY go.mod .
COPY main.go .
RUN CGO_ENABLED=0 GOOS=linux go build -o server .

# Stage 2: Run
FROM scratch
COPY --from=builder /app/server /server
EXPOSE 8080
ENTRYPOINT ["/server"]
```

```bash
docker build -t go-app:single -f Dockerfile.single .
docker build -t go-app:multi -f Dockerfile.multi .

# Porównaj rozmiary!
docker images go-app
```

> 📸 **Wymagany screenshot 6**: Porównanie rozmiarów obrazów single vs multi-stage

### Ćwiczenie 4.2: Multi-stage dla Node.js

```bash
mkdir -p ~/docker-lab02/node-multistage && cd ~/docker-lab02/node-multistage
```

Utwórz `package.json`:
```json
{
  "name": "docker-node-app",
  "version": "1.0.0",
  "scripts": { "start": "node server.js" },
  "dependencies": { "express": "^4.18.0" }
}
```

Utwórz `server.js`:
```javascript
const express = require('express');
const app = express();
app.get('/', (req, res) => res.send(`Hello from Node.js ${process.version}!`));
app.listen(3000, () => console.log('Server on port 3000'));
```

```dockerfile
# Stage 1: Install dependencies
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Production
FROM node:20-alpine
RUN addgroup -S app && adduser -S -G app app
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY --chown=app:app . .
USER app
EXPOSE 3000
CMD ["node", "server.js"]
```

```bash
docker build -t node-app:v1 .
docker run -d --name node-test -p 3000:3000 node-app:v1
curl http://localhost:3000
```

---

## Część 5: Optymalizacja cache (45 min)

### Ćwiczenie 5.1: Kolejność instrukcji

```bash
mkdir -p ~/docker-lab02/cache-test && cd ~/docker-lab02/cache-test
```

Utwórz `requirements.txt`:
```
flask==3.0.0
```

Utwórz `app.py`:
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Wersja 1"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**Dockerfile ZŁY (cache nie działa):**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "app.py"]
```

**Dockerfile DOBRY (cache działa):**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

```bash
# Zbuduj oba warianty
docker build -t cache-bad -f Dockerfile.bad .
docker build -t cache-good -f Dockerfile.good .

# Zmień app.py (np. "Wersja 2")
sed -i 's/Wersja 1/Wersja 2/' app.py

# Przebuduj — obserwuj użycie cache
docker build -t cache-bad:v2 -f Dockerfile.bad .
docker build -t cache-good:v2 -f Dockerfile.good .
```

> 📸 **Wymagany screenshot 7**: Porównanie użycia cache (CACHED vs brak)

---

## Część 6: HEALTHCHECK i LABEL (30 min)

### Ćwiczenie 6.1: Healthcheck

```bash
mkdir -p ~/docker-lab02/health-test && cd ~/docker-lab02/health-test
```

Utwórz `app.py`:
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "OK"

@app.route('/health')
def health():
    return {"status": "healthy"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Utwórz `requirements.txt`:
```
flask==3.0.0
```

```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir flask==3.0.0
COPY app.py .

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

EXPOSE 5000
CMD ["python", "app.py"]
```

```bash
docker build -t health-test .
docker run -d --name health-app -p 5000:5000 health-test

# Obserwuj status zdrowia
docker ps  # kolumna STATUS pokaże (health: starting) → (healthy)

# Po chwili:
docker inspect --format='{{.State.Health.Status}}' health-app
```

> 📸 **Wymagany screenshot 8**: Kontener ze statusem `healthy`

---

## Część 7: Budowanie i publikacja na Docker Hub (45 min)

### Ćwiczenie 7.1: Tagowanie i push

```bash
# Zaloguj się do Docker Hub
docker login

# Zbuduj obraz z tagiem
docker build -t flask-app:v1 ~/docker-lab02/hello-python/

# Otaguj dla Docker Hub (zamień USERNAME na swoje)
docker tag flask-app:v1 USERNAME/flask-app:v1
docker tag flask-app:v1 USERNAME/flask-app:latest

# Wyślij na Docker Hub
docker push USERNAME/flask-app:v1
docker push USERNAME/flask-app:latest

# Usuń lokalne obrazy
docker rmi USERNAME/flask-app:v1 USERNAME/flask-app:latest

# Pobierz z Docker Hub
docker pull USERNAME/flask-app:v1
docker run --rm USERNAME/flask-app:v1
```

> 📸 **Wymagany screenshot 9**: Obraz na Docker Hub i pobranie go

---

## Zadania do samodzielnego wykonania

### Zadanie 1: Dockerfile dla Django
Napisz Dockerfile dla przykładowej aplikacji Django z folderu `supporting-materials/examples/04-django` w repozytorium.

### Zadanie 2: Multi-stage dla Pythona
Stwórz multi-stage Dockerfile, który w pierwszym etapie instaluje zależności, a w drugim kopiuje tylko potrzebne pliki.

### Zadanie 3: Optymalizacja rozmiaru
Weź dowolny obraz z ćwiczeń i zoptymalizuj go: zmień obraz bazowy na `alpine` lub `slim`, dodaj `.dockerignore`, użyj multi-stage build. Porównaj rozmiary.

---

## Podsumowanie

Po ukończeniu tego laboratorium powinieneś umieć:
- ✅ Pisać Dockerfile od podstaw
- ✅ Używać instrukcji: FROM, RUN, COPY, ADD, WORKDIR, ENV, ARG, CMD, ENTRYPOINT
- ✅ Rozumieć różnicę między CMD a ENTRYPOINT
- ✅ Tworzyć multi-stage builds
- ✅ Optymalizować cache warstw
- ✅ Konfigurować HEALTHCHECK
- ✅ Publikować obrazy na Docker Hub
