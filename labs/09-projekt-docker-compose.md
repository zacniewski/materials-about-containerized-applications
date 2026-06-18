# Laboratorium 9: Własny projekt Docker Compose (6 godz.)

## Cel laboratorium
Samodzielne zaprojektowanie i uruchomienie aplikacji wielokontenerowej z wykorzystaniem Docker Compose. Zastosowanie wszystkich poznanych technik: Dockerfile, sieci, wolumeny, healthchecks, dobre praktyki.

## Wymagania wstępne
- Ukończone Laboratorium 1-8

---

## Część 1: Planowanie projektu (45 min)

### Ćwiczenie 1.1: Wybór projektu

Wybierz jeden z poniższych wariantów lub zaproponuj własny:

**Wariant A: Blog / CMS**
- Frontend: Nginx (pliki statyczne)
- Backend: Python/Flask lub Node.js/Express (API)
- Baza danych: PostgreSQL
- Cache: Redis
- Panel admina: Adminer

**Wariant B: E-commerce**
- Frontend: Nginx (reverse proxy)
- Backend: Python/Django lub Node.js
- Baza danych: PostgreSQL
- Cache: Redis
- Kolejka: RabbitMQ

**Wariant C: Monitoring Dashboard**
- Aplikacja: Python/Flask (generuje metryki)
- Prometheus (zbiera metryki)
- Grafana (wizualizacja)
- Baza danych: PostgreSQL (dane aplikacji)

**Wariant D: Własny pomysł**
- Minimum 3 usługi
- Co najmniej 1 usługa budowana z Dockerfile
- Baza danych z wolumenem
- Sieci z izolacją

### Ćwiczenie 1.2: Architektura

Narysuj diagram architektury swojego projektu (na papierze lub w narzędziu). Określ:
- Jakie usługi będą potrzebne?
- Jakie sieci (frontend/backend)?
- Jakie wolumeny (dane, konfiguracja)?
- Jakie porty będą opublikowane?
- Jakie zmienne środowiskowe?

> 📸 **Wymagany screenshot 1**: Diagram architektury projektu

---

## Część 2: Implementacja — przykład Wariant A (180 min)

### Ćwiczenie 2.1: Struktura projektu

```bash
mkdir -p ~/docker-lab09/blog-app/{backend,frontend,nginx,db-init} && cd ~/docker-lab09/blog-app
```

### Ćwiczenie 2.2: Backend (Flask API)

Utwórz `backend/app.py`:
```python
from flask import Flask, jsonify, request
import psycopg2
import redis
import os
import json

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'db'),
        database=os.getenv('DB_NAME', 'blog'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'secret')
    )

def get_cache():
    return redis.Redis(host=os.getenv('REDIS_HOST', 'cache'), port=6379, decode_responses=True)

@app.route('/api/posts', methods=['GET'])
def get_posts():
    r = get_cache()
    cached = r.get('posts')
    if cached:
        return jsonify({"source": "cache", "posts": json.loads(cached)})
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT id, title, content, created_at::text FROM posts ORDER BY created_at DESC')
    posts = [{"id": r[0], "title": r[1], "content": r[2], "created_at": r[3]} for r in cur.fetchall()]
    cur.close()
    conn.close()
    
    r.setex('posts', 60, json.dumps(posts))
    return jsonify({"source": "database", "posts": posts})

@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING id', 
                (data['title'], data['content']))
    post_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    
    get_cache().delete('posts')
    return jsonify({"id": post_id, "message": "Post created"}), 201

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Utwórz `backend/requirements.txt`:
```
flask==3.0.0
psycopg2-binary==2.9.9
redis==5.0.0
```

Utwórz `backend/Dockerfile`:
```dockerfile
FROM python:3.11-slim
RUN groupadd -r app && useradd -r -g app app
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=app:app . .
USER app
EXPOSE 5000
HEALTHCHECK --interval=15s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1
CMD ["python", "app.py"]
```

### Ćwiczenie 2.3: Frontend

Utwórz `frontend/index.html`:
```html
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <title>Blog Docker</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .post { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
        form { background: #f5f5f5; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
        input, textarea { width: 100%; padding: 8px; margin: 5px 0; box-sizing: border-box; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; cursor: pointer; border-radius: 3px; }
        .source { color: #888; font-size: 0.8em; }
    </style>
</head>
<body>
    <h1>🐳 Blog Docker</h1>
    <form id="postForm">
        <h3>Nowy post</h3>
        <input type="text" id="title" placeholder="Tytuł" required>
        <textarea id="content" placeholder="Treść" rows="4" required></textarea>
        <button type="submit">Dodaj post</button>
    </form>
    <div id="posts"></div>
    <script>
        async function loadPosts() {
            const res = await fetch('/api/posts');
            const data = await res.json();
            document.getElementById('posts').innerHTML = 
                `<p class="source">Źródło: ${data.source}</p>` +
                data.posts.map(p => `<div class="post"><h3>${p.title}</h3><p>${p.content}</p><small>${p.created_at}</small></div>`).join('');
        }
        document.getElementById('postForm').onsubmit = async (e) => {
            e.preventDefault();
            await fetch('/api/posts', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({title: document.getElementById('title').value, content: document.getElementById('content').value})
            });
            document.getElementById('title').value = '';
            document.getElementById('content').value = '';
            loadPosts();
        };
        loadPosts();
    </script>
</body>
</html>
```

### Ćwiczenie 2.4: Nginx (reverse proxy)

Utwórz `nginx/default.conf`:
```nginx
upstream backend {
    server backend:5000;
}

server {
    listen 80;

    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /health {
        proxy_pass http://backend;
    }
}
```

### Ćwiczenie 2.5: Inicjalizacja bazy danych

Utwórz `db-init/init.sql`:
```sql
CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO posts (title, content) VALUES 
    ('Witaj w Blog Docker!', 'To jest pierwszy post stworzony automatycznie przy inicjalizacji bazy danych.'),
    ('Docker Compose', 'Docker Compose pozwala uruchamiać aplikacje wielokontenerowe jedną komendą.');
```

### Ćwiczenie 2.6: Plik .env

Utwórz `.env`:
```bash
DB_PASSWORD=super_secret_123
DB_NAME=blog
DB_USER=postgres
```

### Ćwiczenie 2.7: Docker Compose

Utwórz `docker-compose.yaml`:
```yaml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
      - ./frontend:/usr/share/nginx/html:ro
    depends_on:
      backend:
        condition: service_healthy
    networks:
      - frontend
    restart: unless-stopped

  backend:
    build: ./backend
    environment:
      - DB_HOST=db
      - DB_NAME=${DB_NAME}
      - DB_USER=${DB_USER}
      - DB_PASSWORD=${DB_PASSWORD}
      - REDIS_HOST=cache
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_healthy
    networks:
      - frontend
      - backend
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    volumes:
      - db-data:/var/lib/postgresql/data
      - ./db-init:/docker-entrypoint-initdb.d:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - backend
    restart: unless-stopped

  cache:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 3
    networks:
      - backend
    restart: unless-stopped

  adminer:
    image: adminer
    ports:
      - "8080:8080"
    networks:
      - backend
    profiles:
      - debug

volumes:
  db-data:

networks:
  frontend:
  backend:
    internal: true
```

### Ćwiczenie 2.8: Uruchomienie i testowanie

```bash
# Uruchomienie
docker compose up -d --build

# Status
docker compose ps

# Sprawdzenie
curl http://localhost
curl http://localhost/api/posts
curl -X POST http://localhost/api/posts \
  -H "Content-Type: application/json" \
  -d '{"title":"Nowy post","content":"Treść nowego posta"}'
curl http://localhost/api/posts  # Drugie zapytanie — z cache!

# Logi
docker compose logs backend
docker compose logs db
```

> 📸 **Wymagany screenshot 2**: Aplikacja działająca w przeglądarce
> 📸 **Wymagany screenshot 3**: Wynik `docker compose ps` — wszystkie usługi healthy
> 📸 **Wymagany screenshot 4**: API zwracające dane z cache

---

## Część 3: Testowanie odporności (45 min)

### Ćwiczenie 3.1: Restart usługi

```bash
# Zatrzymaj backend
docker compose stop backend

# Sprawdź — nginx zwraca 502
curl http://localhost/api/posts

# Uruchom ponownie
docker compose start backend
sleep 5
curl http://localhost/api/posts  # Działa!
```

### Ćwiczenie 3.2: Trwałość danych

```bash
# Dodaj post
curl -X POST http://localhost/api/posts \
  -H "Content-Type: application/json" \
  -d '{"title":"Test trwałości","content":"Ten post powinien przetrwać restart"}'

# Zatrzymaj i usuń kontenery (bez wolumenów!)
docker compose down

# Uruchom ponownie
docker compose up -d --build
sleep 5

# Dane przetrwały!
curl http://localhost/api/posts
```

> 📸 **Wymagany screenshot 5**: Dane zachowane po restarcie

### Ćwiczenie 3.3: Tryb debug z Adminer

```bash
docker compose --profile debug up -d
# Otwórz http://localhost:8080
# Server: db, User: postgres, Password: (z .env)
```

> 📸 **Wymagany screenshot 6**: Adminer z danymi z bazy

---

## Część 4: Dokumentacja projektu (45 min)

### Ćwiczenie 4.1: README projektu

Utwórz `README.md` dla swojego projektu zawierający:
1. Opis projektu
2. Diagram architektury (Mermaid)
3. Wymagania
4. Instrukcja uruchomienia
5. Dostępne endpointy
6. Zmienne środowiskowe

> 📸 **Wymagany screenshot 7**: README projektu

---

## Zadania do samodzielnego wykonania

### Zadanie 1: Rozbudowa projektu
Dodaj do projektu nową funkcjonalność (np. rejestracja użytkowników, upload plików, wyszukiwanie).

### Zadanie 2: Monitoring
Dodaj Prometheus i Grafana do projektu (jako profil `monitoring`).

### Zadanie 3: CI/CD
Napisz plik GitHub Actions, który buduje i testuje Twój projekt.

---

## Podsumowanie

Po ukończeniu tego laboratorium powinieneś umieć:
- ✅ Zaprojektować architekturę aplikacji wielokontenerowej
- ✅ Zaimplementować pełny stos z Docker Compose
- ✅ Konfigurować reverse proxy (Nginx)
- ✅ Stosować cache (Redis) w aplikacji
- ✅ Testować odporność i trwałość danych
- ✅ Dokumentować projekt Docker
