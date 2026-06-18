# Laboratorium 5: Docker Compose — podstawy (6 godz.)

## Cel laboratorium
Praktyczne poznanie Docker Compose: definiowanie usług, sieci, wolumenów w pliku YAML, zarządzanie stosem aplikacji wielokontenerowych.

## Wymagania wstępne
- Ukończone Laboratorium 1-4
- Zainstalowany Docker Compose (`docker compose version`)

---

## Część 1: Pierwszy docker-compose.yaml (60 min)

### Ćwiczenie 1.1: Prosty serwer Nginx

```bash
mkdir -p ~/docker-lab05/ex1 && cd ~/docker-lab05/ex1
```

Utwórz `docker-compose.yaml`:
```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
```

```bash
# Uruchomienie
docker compose up -d

# Status
docker compose ps

# Logi
docker compose logs

# Sprawdzenie
curl http://localhost:8080

# Zatrzymanie
docker compose down
```

> 📸 **Wymagany screenshot 1**: Wynik `docker compose ps`

### Ćwiczenie 1.2: Wiele usług

```bash
mkdir -p ~/docker-lab05/ex2 && cd ~/docker-lab05/ex2
```

```yaml
# docker-compose.yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: myapp

  cache:
    image: redis:7-alpine
```

```bash
docker compose up -d
docker compose ps
docker compose logs db
docker compose exec db psql -U postgres -c "SELECT version();"
docker compose down
```

> 📸 **Wymagany screenshot 2**: Trzy usługi działające jednocześnie

---

## Część 2: Aplikacja webowa z bazą danych (90 min)

### Ćwiczenie 2.1: Flask + PostgreSQL

```bash
mkdir -p ~/docker-lab05/flask-app && cd ~/docker-lab05/flask-app
```

Utwórz `app.py`:
```python
from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'db'),
        database=os.getenv('DB_NAME', 'myapp'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'secret')
    )

@app.route('/')
def hello():
    return '<h1>Flask + PostgreSQL w Docker Compose</h1>'

@app.route('/db')
def db_test():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT version();')
        version = cur.fetchone()[0]
        cur.close()
        conn.close()
        return jsonify({"status": "connected", "version": version})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Utwórz `requirements.txt`:
```
flask==3.0.0
psycopg2-binary==2.9.9
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

Utwórz `docker-compose.yaml`:
```yaml
services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DB_HOST=db
      - DB_NAME=myapp
      - DB_USER=postgres
      - DB_PASSWORD=secret
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: myapp
    volumes:
      - db-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  db-data:
```

```bash
docker compose up -d --build
docker compose ps
curl http://localhost:5000
curl http://localhost:5000/db
curl http://localhost:5000/health
```

> 📸 **Wymagany screenshot 3**: Aplikacja Flask połączona z PostgreSQL

### Ćwiczenie 2.2: Dodanie Adminer

Dodaj do `docker-compose.yaml`:
```yaml
  adminer:
    image: adminer
    ports:
      - "8080:8080"
    depends_on:
      - db
```

```bash
docker compose up -d
# Otwórz http://localhost:8080 — Server: db, User: postgres, Password: secret
```

> 📸 **Wymagany screenshot 4**: Adminer połączony z bazą danych

---

## Część 3: Zmienne środowiskowe i .env (45 min)

### Ćwiczenie 3.1: Plik .env

```bash
mkdir -p ~/docker-lab05/env-test && cd ~/docker-lab05/env-test
```

Utwórz `.env`:
```bash
POSTGRES_PASSWORD=super_secret_123
POSTGRES_DB=production_db
POSTGRES_USER=admin
APP_PORT=5000
```

Utwórz `docker-compose.yaml`:
```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
    ports:
      - "5432:5432"

  adminer:
    image: adminer
    ports:
      - "${APP_PORT:-8080}:8080"
```

```bash
# Sprawdź interpolację zmiennych
docker compose config

# Uruchom
docker compose up -d
docker compose exec db psql -U admin -d production_db -c "SELECT current_user, current_database();"
docker compose down
```

> 📸 **Wymagany screenshot 5**: Zmienne z .env użyte w konfiguracji

### Ćwiczenie 3.2: env_file

Utwórz `app.env`:
```bash
DEBUG=true
SECRET_KEY=my-secret-key-123
LOG_LEVEL=debug
```

```yaml
services:
  app:
    image: python:3.11-slim
    env_file:
      - app.env
    command: python -c "import os; [print(f'{k}={v}') for k,v in os.environ.items() if k in ('DEBUG','SECRET_KEY','LOG_LEVEL')]"
```

```bash
docker compose run --rm app
```

---

## Część 4: Sieci i wolumeny w Compose (60 min)

### Ćwiczenie 4.1: Izolacja sieciowa

```bash
mkdir -p ~/docker-lab05/networks && cd ~/docker-lab05/networks
```

```yaml
# docker-compose.yaml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    networks:
      - frontend

  app:
    image: alpine
    command: sleep 3600
    networks:
      - frontend
      - backend

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: secret
    networks:
      - backend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # brak dostępu do internetu
```

```bash
docker compose up -d

# App widzi nginx i db
docker compose exec app ping -c 2 nginx
docker compose exec app ping -c 2 db

# Nginx NIE widzi db
docker compose exec nginx ping -c 2 db  # FAIL

# Backend nie ma internetu
docker compose exec db ping -c 2 8.8.8.8  # FAIL

docker compose down
```

> 📸 **Wymagany screenshot 6**: Izolacja sieciowa w Docker Compose

### Ćwiczenie 4.2: Wolumeny nazwane

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql

volumes:
  pgdata:
    driver: local
```

Utwórz `init.sql`:
```sql
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    done BOOLEAN DEFAULT false
);
INSERT INTO tasks (title) VALUES ('Nauczyć się Docker Compose'), ('Zrobić projekt');
```

```bash
docker compose up -d
sleep 3
docker compose exec db psql -U postgres -c "SELECT * FROM tasks;"

# Dane przetrwają docker compose down (bez -v)
docker compose down
docker compose up -d
sleep 3
docker compose exec db psql -U postgres -c "SELECT * FROM tasks;"

# Usunięcie z wolumenami
docker compose down -v
```

> 📸 **Wymagany screenshot 7**: Dane z init.sql załadowane automatycznie

---

## Część 5: Komendy Docker Compose (45 min)

### Ćwiczenie 5.1: Przegląd komend

```bash
cd ~/docker-lab05/flask-app

# Build
docker compose build
docker compose build --no-cache app

# Up z budowaniem
docker compose up -d --build

# Logi konkretnej usługi
docker compose logs -f app
# Ctrl+C

# Exec
docker compose exec app python -c "print('Hello from app')"
docker compose exec db psql -U postgres -c "SELECT 1;"

# Run (jednorazowe uruchomienie)
docker compose run --rm app python -c "print('One-time command')"

# Skalowanie
docker compose up -d --scale app=3
docker compose ps

# Restart
docker compose restart app

# Stop vs Down
docker compose stop    # zatrzymuje, nie usuwa
docker compose start   # uruchamia ponownie
docker compose down    # zatrzymuje i usuwa
docker compose down -v # + usuwa wolumeny
```

> 📸 **Wymagany screenshot 8**: Skalowanie usługi (`--scale app=3`)

---

## Część 6: Depends_on i healthchecks (45 min)

### Ćwiczenie 6.1: Prawidłowa kolejność uruchamiania

```bash
mkdir -p ~/docker-lab05/depends && cd ~/docker-lab05/depends
```

```yaml
services:
  app:
    image: alpine
    command: sh -c "echo 'App started at:' && date && sleep 3600"
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: secret
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 3s
      timeout: 3s
      retries: 10
      start_period: 10s

  cache:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 3s
      timeout: 3s
      retries: 5
```

```bash
docker compose up -d
docker compose ps  # Obserwuj kolumnę STATUS (healthy)
docker compose logs app  # App uruchomiony po db i cache
docker compose down
```

> 📸 **Wymagany screenshot 9**: Usługi z healthcheck (healthy)

---

## Część 7: Przykład z repozytorium (45 min)

### Ćwiczenie 7.1: PHP + MySQL

Wykorzystaj przykład z repozytorium:
```bash
cd /ścieżka/do/repozytorium/supporting-materials/examples/02-php-mysql
cat docker-compose.yaml
cat src/index.php

docker compose up -d
# Otwórz http://localhost:8080
docker compose down
```

### Ćwiczenie 7.2: Node.js + MongoDB

```bash
cd /ścieżka/do/repozytorium/supporting-materials/examples/05-mongodb-v1
cat docker-compose.yaml
cat Dockerfile

docker compose up -d --build
docker compose ps
docker compose logs
docker compose down
```

> 📸 **Wymagany screenshot 10**: Przykład z repozytorium uruchomiony

---

## Zadania do samodzielnego wykonania

### Zadanie 1: WordPress + MySQL
Utwórz `docker-compose.yaml` uruchamiający WordPress z bazą MySQL. Skonfiguruj wolumeny dla danych.

### Zadanie 2: Stos MEAN/MERN
Utwórz konfigurację Compose dla stosu: MongoDB + Express + (Angular/React) + Node.js.

### Zadanie 3: Override files
Utwórz `docker-compose.yaml` (bazowy) i `docker-compose.override.yaml` (development z bind mounts i debug).

---

## Podsumowanie

Po ukończeniu tego laboratorium powinieneś umieć:
- ✅ Pisać pliki docker-compose.yaml
- ✅ Definiować usługi, sieci i wolumeny
- ✅ Używać zmiennych środowiskowych i plików .env
- ✅ Konfigurować depends_on z healthchecks
- ✅ Zarządzać stosem komendami docker compose
- ✅ Izolować usługi w osobnych sieciach
- ✅ Skalować usługi
