# Laboratorium 6: Docker Compose — zaawansowane scenariusze (6 godz.)

## Cel laboratorium
Zaawansowane użycie Docker Compose: profiles, secrets, override files, multi-environment, reverse proxy, monitoring.

## Wymagania wstępne
- Ukończone Laboratorium 5

---

## Część 1: Override files i multi-environment (90 min)

### Ćwiczenie 1.1: Development vs Production

```bash
mkdir -p ~/docker-lab06/multi-env && cd ~/docker-lab06/multi-env
```

Utwórz `app.py`:
```python
from flask import Flask
import os
app = Flask(__name__)

@app.route('/')
def hello():
    env = os.getenv('ENVIRONMENT', 'unknown')
    debug = os.getenv('DEBUG', 'false')
    return f"<h1>Environment: {env}</h1><p>Debug: {debug}</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.getenv('DEBUG', 'false').lower() == 'true')
```

Utwórz `requirements.txt`: `flask==3.0.0`

Utwórz `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

Utwórz `docker-compose.yaml` (bazowy):
```yaml
services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - ENVIRONMENT=production
      - DEBUG=false
    restart: unless-stopped
```

Utwórz `docker-compose.override.yaml` (dev — ładowany automatycznie):
```yaml
services:
  app:
    volumes:
      - ./app.py:/app/app.py
    environment:
      - ENVIRONMENT=development
      - DEBUG=true
    restart: "no"
```

Utwórz `docker-compose.prod.yaml`:
```yaml
services:
  app:
    environment:
      - ENVIRONMENT=production
      - DEBUG=false
    restart: always
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
```

```bash
# Development (automatycznie ładuje override)
docker compose up -d --build
curl http://localhost:5000
docker compose down

# Production (jawne wskazanie plików)
docker compose -f docker-compose.yaml -f docker-compose.prod.yaml up -d --build
curl http://localhost:5000
docker compose -f docker-compose.yaml -f docker-compose.prod.yaml down
```

> 📸 **Wymagany screenshot 1**: Różne środowiska (development vs production)

---

## Część 2: Profiles (60 min)

### Ćwiczenie 2.1: Warunkowe usługi

```bash
mkdir -p ~/docker-lab06/profiles && cd ~/docker-lab06/profiles
```

```yaml
# docker-compose.yaml
services:
  app:
    image: nginx:alpine
    ports:
      - "80:80"

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: secret

  # Tylko w trybie debug
  adminer:
    image: adminer
    ports:
      - "8080:8080"
    profiles:
      - debug

  # Tylko w trybie monitoring
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    profiles:
      - monitoring

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    profiles:
      - monitoring
```

```bash
# Bez profili — tylko app i db
docker compose up -d
docker compose ps

# Z profilem debug
docker compose --profile debug up -d
docker compose ps

# Z profilem monitoring
docker compose --profile monitoring up -d
docker compose ps

# Oba profile
docker compose --profile debug --profile monitoring up -d
docker compose ps

docker compose --profile debug --profile monitoring down
```

> 📸 **Wymagany screenshot 2**: Różne profile — różne zestawy usług

---

## Część 3: Nginx jako reverse proxy (90 min)

### Ćwiczenie 3.1: Reverse proxy dla aplikacji

```bash
mkdir -p ~/docker-lab06/reverse-proxy && cd ~/docker-lab06/reverse-proxy
mkdir -p app
```

Utwórz `app/app.py`:
```python
from flask import Flask
import os
app = Flask(__name__)

@app.route('/')
def hello():
    return f"<h1>Hello from {os.uname().nodename}</h1>"

@app.route('/api/data')
def data():
    return {"message": "API response", "host": os.uname().nodename}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Utwórz `app/requirements.txt`: `flask==3.0.0`

Utwórz `app/Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

Utwórz `nginx.conf`:
```nginx
upstream app_servers {
    server app:5000;
}

server {
    listen 80;

    location / {
        proxy_pass http://app_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/ {
        proxy_pass http://app_servers;
        proxy_set_header Host $host;
    }
}
```

Utwórz `docker-compose.yaml`:
```yaml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - app

  app:
    build: ./app
    expose:
      - "5000"

volumes: {}
```

```bash
docker compose up -d --build
curl http://localhost
curl http://localhost/api/data

# Skalowanie aplikacji
docker compose up -d --scale app=3
# Wielokrotne zapytania — różne hosty
for i in $(seq 1 6); do curl -s http://localhost/api/data | python3 -m json.tool; done

docker compose down
```

> 📸 **Wymagany screenshot 3**: Load balancing — różne hosty w odpowiedziach

---

## Część 4: Monitoring z Prometheus i Grafana (60 min)

### Ćwiczenie 4.1: Stos monitoringu

```bash
mkdir -p ~/docker-lab06/monitoring && cd ~/docker-lab06/monitoring
```

Utwórz `prometheus.yml`:
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']
```

Utwórz `docker-compose.yaml`:
```yaml
services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana
    depends_on:
      - prometheus

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    ports:
      - "8080:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    privileged: true

  # Aplikacja do monitorowania
  web:
    image: nginx:alpine
    ports:
      - "80:80"

volumes:
  prometheus-data:
  grafana-data:
```

```bash
docker compose up -d

# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000 (admin/admin)
# cAdvisor: http://localhost:8080

# W Grafana dodaj data source: Prometheus, URL: http://prometheus:9090
```

> 📸 **Wymagany screenshot 4**: Dashboard Grafana z metrykami kontenerów

```bash
docker compose down -v
```

---

## Część 5: Secrets w Compose (45 min)

### Ćwiczenie 5.1: Zarządzanie sekretami

```bash
mkdir -p ~/docker-lab06/secrets/secrets-dir && cd ~/docker-lab06/secrets
echo "super_secret_password_123" > secrets-dir/db_password.txt
echo "my_secret_api_key_456" > secrets-dir/api_key.txt
```

```yaml
# docker-compose.yaml
services:
  db:
    image: postgres:16-alpine
    secrets:
      - db_password
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    volumes:
      - db-data:/var/lib/postgresql/data

  app:
    image: alpine
    secrets:
      - db_password
      - api_key
    command: sh -c "echo 'DB Password:' && cat /run/secrets/db_password && echo 'API Key:' && cat /run/secrets/api_key && sleep 3600"

secrets:
  db_password:
    file: ./secrets-dir/db_password.txt
  api_key:
    file: ./secrets-dir/api_key.txt

volumes:
  db-data:
```

```bash
docker compose up -d
docker compose logs app
docker compose exec app ls -la /run/secrets/
docker compose down -v
```

> 📸 **Wymagany screenshot 5**: Sekrety dostępne w kontenerze

---

## Część 6: Logging w Compose (30 min)

### Ćwiczenie 6.1: Konfiguracja logowania

```yaml
services:
  app:
    image: nginx:alpine
    ports:
      - "80:80"
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
        tag: "{{.Name}}"

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: secret
    logging:
      driver: json-file
      options:
        max-size: "5m"
        max-file: "2"
```

```bash
docker compose up -d
# Generuj ruch
for i in $(seq 1 20); do curl -s http://localhost > /dev/null; done
docker compose logs --tail 10 app
docker compose down
```

---

## Część 7: Projekt — pełna aplikacja (45 min)

### Ćwiczenie 7.1: Django + React z repozytorium

```bash
cd /ścieżka/do/repozytorium/supporting-materials/examples/11-django-react
cat docker-compose.yaml
docker compose up -d --build
docker compose ps
# Sprawdź działanie aplikacji
docker compose down
```

Lub stwórz własny stos:

```yaml
# Pełny stos: Nginx + App + DB + Cache + Adminer
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - app
    networks:
      - frontend

  app:
    build: ./app
    environment:
      - DATABASE_URL=postgresql://postgres:${DB_PASS}@db:5432/myapp
      - REDIS_URL=redis://cache:6379
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_healthy
    networks:
      - frontend
      - backend

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: ${DB_PASS}
      POSTGRES_DB: myapp
    volumes:
      - db-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - backend

  cache:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 3
    networks:
      - backend

  adminer:
    image: adminer
    ports:
      - "8080:8080"
    profiles:
      - debug
    networks:
      - backend

volumes:
  db-data:

networks:
  frontend:
  backend:
    internal: true
```

> 📸 **Wymagany screenshot 6**: Pełny stos aplikacji uruchomiony

---

## Zadania do samodzielnego wykonania

### Zadanie 1: ELK Stack
Uruchom stos ELK (Elasticsearch + Logstash + Kibana) z Docker Compose.

### Zadanie 2: CI/CD lokalne
Utwórz konfigurację Compose z Gitea (self-hosted Git) + Drone CI.

### Zadanie 3: Własny projekt
Zaprojektuj i uruchom własną aplikację wielokontenerową z co najmniej 3 usługami, sieciami, wolumenami i healthchecks.

---

## Podsumowanie

Po ukończeniu tego laboratorium powinieneś umieć:
- ✅ Konfigurować różne środowiska (dev/prod) z override files
- ✅ Używać profiles do warunkowego uruchamiania usług
- ✅ Konfigurować Nginx jako reverse proxy z load balancingiem
- ✅ Uruchamiać stos monitoringu (Prometheus + Grafana)
- ✅ Zarządzać sekretami w Docker Compose
- ✅ Konfigurować logowanie kontenerów
