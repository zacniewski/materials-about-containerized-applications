# Laboratorium 10: Powtórzenie materiału i przygotowanie do egzaminu (6 godz.)

## Cel laboratorium
Powtórzenie i utrwalenie wszystkich zagadnień z kursu. Rozwiązywanie zadań egzaminacyjnych. Praca z materiałami DevOps with Docker z repozytorium.

## Wymagania wstępne
- Ukończone Laboratorium 1-9

---

## Część 1: DevOps with Docker — wybrane ćwiczenia (120 min)

### Ćwiczenie 1.1: Materiały z repozytorium

Przejdź przez wybrane sekcje kursu DevOps with Docker:

```bash
# Część 1 — podstawy
cd /ścieżka/do/repozytorium/supporting-materials/devops-with-docker/part-1

# Przeczytaj i wykonaj ćwiczenia z:
# - section-1 (Definicje i podstawowe pojęcia)
# - section-2 (Uruchamianie i zatrzymywanie kontenerów)
# - section-3 (Dogłębne spojrzenie na obrazy)
# - section-4 (Definiowanie warunków startowych kontenera)
# - section-5 (Interakcja z kontenerem przez wolumeny i porty)
```

> 📸 **Wymagany screenshot 1**: Wykonane ćwiczenie z DevOps with Docker (Part 1)

### Ćwiczenie 1.2: Docker Compose z DevOps with Docker

```bash
# Część 2 — Docker Compose
cd /ścieżka/do/repozytorium/supporting-materials/devops-with-docker/part-2

# Przeczytaj i wykonaj ćwiczenia z:
# - section-1 (Migracja do Docker Compose)
# - section-2 (Sieci Dockera)
# - section-3 (Wolumeny w praktyce)
```

> 📸 **Wymagany screenshot 2**: Wykonane ćwiczenie z DevOps with Docker (Part 2)

### Ćwiczenie 1.3: Zaawansowane tematy

```bash
# Część 3 — bezpieczeństwo i optymalizacja
cd /ścieżka/do/repozytorium/supporting-materials/devops-with-docker/part-3

# Przeczytaj:
# - section-1 (Official Images and trust)
# - section-3 (Using a non-root user)
# - section-4 (Optimizing the image size)
```

> 📸 **Wymagany screenshot 3**: Wykonane ćwiczenie z DevOps with Docker (Part 3)

---

## Część 2: Zadania egzaminacyjne — praktyka (180 min)

Poniższe zadania odpowiadają pytaniom, które mogą pojawić się na egzaminie. Wykonaj każde z nich samodzielnie.

### Zadanie 1: Dockerfile z kopiowaniem kodu (20 min)

> Utwórz plik `Dockerfile`, w którym z hosta do kontenera kopiowany będzie folder `code` (zawiera skrypt Python) i zbuduj go. Uruchom skrypt wewnątrz kontenera.

```bash
mkdir -p ~/docker-exam/zad1/code && cd ~/docker-exam/zad1
echo 'print("Hello from Docker container!")' > code/app.py
echo 'import sys; print(f"Python {sys.version}")' >> code/app.py
```

Napisz Dockerfile, zbuduj obraz i uruchom skrypt.

> 📸 **Wymagany screenshot 4**: Skrypt Python uruchomiony w kontenerze

### Zadanie 2: Kopiowanie plików host ↔ kontener (15 min)

> Skopiuj plik tekstowy z hosta do kontenera i z kontenera do hosta.

```bash
# Utwórz kontener
docker run -d --name copy-test ubuntu sleep 3600

# Host → Kontener
echo "Dane z hosta $(date)" > host-file.txt
docker cp host-file.txt copy-test:/tmp/

# Kontener → Host
docker exec copy-test bash -c "echo 'Dane z kontenera' > /tmp/container-file.txt"
docker cp copy-test:/tmp/container-file.txt ./

cat host-file.txt
docker exec copy-test cat /tmp/host-file.txt
cat container-file.txt

docker stop copy-test && docker rm copy-test
```

> 📸 **Wymagany screenshot 5**: Kopiowanie plików w obu kierunkach

### Zadanie 3: ENTRYPOINT i CMD (20 min)

> Pokaż działanie komend `ENTRYPOINT` i `CMD` w wybranym projekcie.

```bash
mkdir -p ~/docker-exam/zad3 && cd ~/docker-exam/zad3
```

Utwórz `greet.sh`:
```bash
#!/bin/bash
echo "Witaj, ${1:-Świecie}! Czas: $(date)"
```

Utwórz `Dockerfile`:
```dockerfile
FROM ubuntu:22.04
COPY greet.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/greet.sh
ENTRYPOINT ["greet.sh"]
CMD ["Docker"]
```

```bash
docker build -t greet .
docker run --rm greet              # Witaj, Docker!
docker run --rm greet "Student"    # Witaj, Student!
docker run --rm greet "Egzamin"   # Witaj, Egzamin!
```

> 📸 **Wymagany screenshot 6**: Działanie ENTRYPOINT i CMD

### Zadanie 4: Baza danych z docker-compose (20 min)

> Pokaż działanie usługi bazodanowej z wykorzystaniem `docker-compose`.

```bash
mkdir -p ~/docker-exam/zad4 && cd ~/docker-exam/zad4
```

```yaml
# docker-compose.yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: exam123
      POSTGRES_DB: examdb
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      retries: 5

  adminer:
    image: adminer
    ports:
      - "8080:8080"
    depends_on:
      db:
        condition: service_healthy

volumes:
  pgdata:
```

```bash
docker compose up -d
docker compose exec db psql -U postgres -d examdb -c "CREATE TABLE students (id SERIAL, name TEXT); INSERT INTO students (name) VALUES ('Jan'), ('Anna'); SELECT * FROM students;"
```

> 📸 **Wymagany screenshot 7**: Baza danych z Docker Compose

### Zadanie 5: ADD, COPY, WORKDIR (15 min)

> Pokaż działanie komend `ADD`, `COPY` i `WORKDIR`.

```bash
mkdir -p ~/docker-exam/zad5/src && cd ~/docker-exam/zad5
echo "print('from src')" > src/app.py
echo "config data" > config.txt
tar czf data.tar.gz config.txt
```

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY src/app.py ./
ADD data.tar.gz ./extracted/
RUN ls -la /app/ && ls -la /app/extracted/
CMD ["python", "app.py"]
```

> 📸 **Wymagany screenshot 8**: Działanie ADD, COPY, WORKDIR

### Zadanie 6: docker inspect i docker logs (15 min)

> Omów komendy `docker inspect` i `docker logs`.

```bash
docker run -d --name inspect-demo -p 9090:80 nginx:alpine

# Logi
docker logs inspect-demo
docker logs --tail 5 -t inspect-demo

# Inspekcja
docker inspect -f '{{.State.Status}}' inspect-demo
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' inspect-demo
docker inspect -f '{{json .Config.Env}}' inspect-demo

docker stop inspect-demo && docker rm inspect-demo
```

> 📸 **Wymagany screenshot 9**: Wynik docker inspect i docker logs

### Zadanie 7: Sieci Docker (20 min)

> Czym są sieci w Dockerze? Zaprezentuj przykład.

```bash
docker network create exam-net
docker run -d --name web --network exam-net nginx:alpine
docker run -d --name client --network exam-net alpine sleep 3600

# DNS działa
docker exec client ping -c 3 web
docker exec client wget -qO- http://web:80

# Izolacja
docker run --rm alpine ping -c 1 web  # FAIL — inna sieć

docker stop web client && docker rm web client
docker network rm exam-net
```

> 📸 **Wymagany screenshot 10**: Sieci Docker — DNS i izolacja

### Zadanie 8: Obraz vs kontener + budowanie (20 min)

> Jaka jest różnica między obrazem i kontenerem? Pokaż budowanie obrazu i uruchamianie kontenera.

```bash
mkdir -p ~/docker-exam/zad8 && cd ~/docker-exam/zad8
echo 'from flask import Flask; app = Flask(__name__)
@app.route("/")
def hello(): return "Exam app!"
app.run(host="0.0.0.0", port=5000)' > app.py
echo "flask==3.0.0" > requirements.txt
```

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

```bash
# Budowanie OBRAZU
docker build -t exam-app:v1 .
docker images exam-app

# Uruchamianie KONTENERA z obrazu
docker run -d --name exam-c1 -p 5001:5000 exam-app:v1
docker run -d --name exam-c2 -p 5002:5000 exam-app:v1

# 1 obraz → 2 kontenery
docker ps --filter name=exam
curl http://localhost:5001
curl http://localhost:5002

docker stop exam-c1 exam-c2 && docker rm exam-c1 exam-c2
```

> 📸 **Wymagany screenshot 11**: Obraz i dwa kontenery z niego

### Zadanie 9: Wejście do kontenera + trwałość danych (20 min)

> Pokaż jak „wejść" do kontenera, utworzyć plik i zachować dane po restarcie.

```bash
docker volume create exam-data
docker run -d --name exam-vol -v exam-data:/data ubuntu sleep 3600

# Wejście do kontenera
docker exec -it exam-vol bash
# Wewnątrz:
echo "Ważne dane - $(date)" > /data/important.txt
cat /data/important.txt
exit

# Usunięcie kontenera
docker stop exam-vol && docker rm exam-vol

# Nowy kontener z tym samym wolumenem
docker run --rm -v exam-data:/data ubuntu cat /data/important.txt
# Dane przetrwały!

docker volume rm exam-data
```

> 📸 **Wymagany screenshot 12**: Trwałość danych z wolumenem

### Zadanie 10: Tag i Docker Hub (20 min)

> Zbuduj obraz, nadaj tag i opublikuj na DockerHub. Usuń lokalnie i pobierz.

```bash
docker build -t exam-app:v1 ~/docker-exam/zad8/
docker tag exam-app:v1 USERNAME/exam-app:v1

docker login
docker push USERNAME/exam-app:v1

docker rmi USERNAME/exam-app:v1 exam-app:v1
docker pull USERNAME/exam-app:v1
docker run --rm USERNAME/exam-app:v1 python -c "print('Pobrano z DockerHub!')"
```

> 📸 **Wymagany screenshot 13**: Obraz na Docker Hub

### Zadanie 11: Dobre praktyki Dockerfile (15 min)

> Pokaż co najmniej dwie dobre praktyki Dockerfile.

Przeanalizuj i porównaj:
```bash
cd /ścieżka/do/repozytorium/supporting-materials/examples/08-best-practices-dockerfile
cat Dockerfile.python-bad
cat Dockerfile.python-good
```

> 📸 **Wymagany screenshot 14**: Dobre praktyki Dockerfile

### Zadanie 12: Dobre praktyki docker-compose (15 min)

> Pokaż co najmniej dwie dobre praktyki docker-compose.yaml.

```bash
cd /ścieżka/do/repozytorium/supporting-materials/examples/09-best-practices-docker-compose
cat docker-compose.bad.yaml
cat docker-compose.good.yaml
```

> 📸 **Wymagany screenshot 15**: Dobre praktyki Docker Compose

---

## Część 3: Sprzątanie końcowe (15 min)

```bash
# Zatrzymaj wszystkie kontenery
docker stop $(docker ps -q) 2>/dev/null

# Usuń wszystkie kontenery
docker rm $(docker ps -aq) 2>/dev/null

# Usuń nieużywane zasoby
docker system prune -a --volumes -f

# Sprawdź
docker system df
```

---

## Checklist — co powinieneś umieć

| # | Zagadnienie | Sprawdzone? |
|---|------------|-------------|
| 1 | Uruchamianie kontenerów (`docker run`, `-d`, `-it`, `-p`, `-v`, `-e`) | ☐ |
| 2 | Zarządzanie kontenerami (`ps`, `stop`, `rm`, `exec`, `logs`, `inspect`) | ☐ |
| 3 | Budowanie obrazów (`Dockerfile`, `docker build`, `docker push`) | ☐ |
| 4 | Instrukcje Dockerfile (`FROM`, `RUN`, `COPY`, `ADD`, `CMD`, `ENTRYPOINT`, `WORKDIR`, `ENV`) | ☐ |
| 5 | Wolumeny (`docker volume`, `-v`, bind mounts, trwałość danych) | ☐ |
| 6 | Sieci (`docker network`, DNS, izolacja, mapowanie portów) | ☐ |
| 7 | Docker Compose (`docker-compose.yaml`, `up`, `down`, `exec`, `logs`) | ☐ |
| 8 | Kopiowanie plików (`docker cp`) | ☐ |
| 9 | Dobre praktyki (Dockerfile, docker-compose, bezpieczeństwo) | ☐ |
| 10 | Multi-stage builds | ☐ |
| 11 | Healthchecks | ☐ |
| 12 | Docker Hub (push, pull, tag) | ☐ |

---

## Podsumowanie kursu

Po ukończeniu wszystkich 10 laboratoriów powinieneś umieć:
- ✅ Swobodnie pracować z Docker CLI
- ✅ Pisać efektywne Dockerfile
- ✅ Projektować aplikacje wielokontenerowe z Docker Compose
- ✅ Zarządzać danymi (wolumeny, backup)
- ✅ Konfigurować sieci i izolację
- ✅ Stosować dobre praktyki bezpieczeństwa
- ✅ Publikować obrazy na Docker Hub
- ✅ Konteneryzować aplikacje w różnych technologiach

**Powodzenia na egzaminie! 🐳**
