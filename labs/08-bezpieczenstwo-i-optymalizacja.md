# Laboratorium 8: Bezpieczeństwo i optymalizacja Docker (6 godz.)

## Cel laboratorium
Praktyczne stosowanie dobrych praktyk bezpieczeństwa i optymalizacji obrazów Docker: skanowanie podatności, użytkownik nie-root, minimalne obrazy, Hadolint.

## Wymagania wstępne
- Ukończone Laboratorium 1-7

---

## Część 1: Skanowanie podatności (60 min)

### Ćwiczenie 1.1: Docker Scout

```bash
# Skanowanie oficjalnego obrazu
docker scout cves python:3.11
docker scout quickview python:3.11

# Porównanie wariantów
docker scout quickview python:3.11-slim
docker scout quickview python:3.11-alpine
```

> 📸 **Wymagany screenshot 1**: Wynik skanowania Docker Scout

### Ćwiczenie 1.2: Trivy

```bash
# Skanowanie z Trivy (w kontenerze)
docker run --rm aquasec/trivy image python:3.11-slim
docker run --rm aquasec/trivy image --severity HIGH,CRITICAL python:3.11-slim
docker run --rm aquasec/trivy image python:3.11-alpine
```

> 📸 **Wymagany screenshot 2**: Porównanie podatności slim vs alpine

---

## Część 2: Optymalizacja rozmiaru obrazów (90 min)

### Ćwiczenie 2.1: Porównanie obrazów bazowych

```bash
docker pull python:3.11
docker pull python:3.11-slim
docker pull python:3.11-alpine

docker images python --format "table {{.Tag}}\t{{.Size}}"
```

> 📸 **Wymagany screenshot 3**: Porównanie rozmiarów obrazów Python

### Ćwiczenie 2.2: Optymalizacja Dockerfile krok po kroku

```bash
mkdir -p ~/docker-lab08/optimize && cd ~/docker-lab08/optimize
```

Utwórz `app.py`:
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Optimized Docker Image!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Utwórz `requirements.txt`: `flask==3.0.0`

**Wersja 1 — nieoptymalna:**
```dockerfile
# Dockerfile.v1
FROM python:3.11
WORKDIR /app
RUN apt-get update && apt-get install -y vim curl wget
COPY . .
RUN pip install -r requirements.txt
CMD python app.py
```

**Wersja 2 — slim + cache:**
```dockerfile
# Dockerfile.v2
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

**Wersja 3 — alpine + nie-root + healthcheck:**
```dockerfile
# Dockerfile.v3
FROM python:3.11-alpine
RUN addgroup -S app && adduser -S -G app app
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=app:app . .
USER app
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=5s CMD wget -qO- http://localhost:5000/ || exit 1
CMD ["python", "app.py"]
```

**Wersja 4 — multi-stage:**
```dockerfile
# Dockerfile.v4
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim
RUN groupadd -r app && useradd -r -g app -d /app app
WORKDIR /app
COPY --from=builder /root/.local /home/app/.local
COPY --chown=app:app . .
USER app
ENV PATH=/home/app/.local/bin:$PATH
EXPOSE 5000
CMD ["python", "app.py"]
```

```bash
docker build -t opt:v1 -f Dockerfile.v1 .
docker build -t opt:v2 -f Dockerfile.v2 .
docker build -t opt:v3 -f Dockerfile.v3 .
docker build -t opt:v4 -f Dockerfile.v4 .

docker images opt --format "table {{.Tag}}\t{{.Size}}"
```

> 📸 **Wymagany screenshot 4**: Porównanie rozmiarów 4 wersji obrazu

---

## Część 3: Hadolint — linting Dockerfile (45 min)

### Ćwiczenie 3.1: Analiza Dockerfile

Utwórz `Dockerfile.bad`:
```dockerfile
FROM python:latest
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y wget
COPY . .
RUN pip install -r requirements.txt
RUN cd /app && ls
CMD python app.py
```

```bash
# Skanowanie z Hadolint
docker run --rm -i hadolint/hadolint < Dockerfile.bad

# Skanowanie dobrego Dockerfile
docker run --rm -i hadolint/hadolint < Dockerfile.v3
```

> 📸 **Wymagany screenshot 5**: Ostrzeżenia Hadolint i ich naprawa

### Ćwiczenie 3.2: Naprawa ostrzeżeń

Napraw `Dockerfile.bad` zgodnie z zaleceniami Hadolint i zeskanuj ponownie.

---

## Część 4: Bezpieczeństwo runtime (60 min)

### Ćwiczenie 4.1: Użytkownik nie-root

```bash
# Domyślnie — root
docker run --rm python:3.11-slim python -c "import os; print(f'UID: {os.getuid()}, GID: {os.getgid()}')"

# Z USER w Dockerfile
docker run --rm opt:v3 python -c "import os; print(f'UID: {os.getuid()}, GID: {os.getgid()}')"
```

### Ćwiczenie 4.2: Read-only filesystem

```bash
docker run --rm --read-only --tmpfs /tmp nginx:alpine sh -c "echo test > /tmp/ok.txt && echo 'tmpfs OK' && echo test > /var/fail.txt" 2>&1 || true
```

### Ćwiczenie 4.3: Ograniczenia zasobów

```bash
# Limit pamięci
docker run --rm --memory=64m python:3.11-slim python -c "
import sys
print(f'Memory limit test')
try:
    data = bytearray(100 * 1024 * 1024)  # 100MB
except MemoryError:
    print('MemoryError — limit działa!')
"

# Limit CPU
docker run -d --name cpu-test --cpus=0.5 ubuntu bash -c "while true; do :; done"
docker stats --no-stream cpu-test
docker stop cpu-test && docker rm cpu-test
```

> 📸 **Wymagany screenshot 6**: Ograniczenia zasobów w działaniu

### Ćwiczenie 4.4: Capabilities

```bash
# Domyślne capabilities
docker run --rm alpine sh -c "cat /proc/1/status | grep -i cap"

# Usunięcie wszystkich + dodanie potrzebnych
docker run --rm --cap-drop=ALL --cap-add=NET_BIND_SERVICE nginx:alpine sh -c "cat /proc/1/status | grep -i cap"
```

---

## Część 5: Dobre praktyki Dockerfile z repozytorium (45 min)

### Ćwiczenie 5.1: Analiza przykładów

```bash
cd /ścieżka/do/repozytorium/supporting-materials/examples/08-best-practices-dockerfile
cat Dockerfile.python-bad
cat Dockerfile.python-good
cat Dockerfile.node-good
```

Porównaj i opisz różnice między złym a dobrym Dockerfile.

> 📸 **Wymagany screenshot 7**: Porównanie dobrych i złych praktyk

### Ćwiczenie 5.2: Dobre praktyki Docker Compose

```bash
cd /ścieżka/do/repozytorium/supporting-materials/examples/09-best-practices-docker-compose
cat docker-compose.bad.yaml
cat docker-compose.good.yaml
cat docker-compose.good2.yaml
```

> 📸 **Wymagany screenshot 8**: Porównanie dobrych i złych praktyk Compose

---

## Część 6: Docker Bench Security (30 min)

### Ćwiczenie 6.1: Audyt bezpieczeństwa

```bash
docker run --rm --net host --pid host \
  --userns host --cap-add audit_control \
  -v /var/lib:/var/lib:ro \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /etc:/etc:ro \
  docker/docker-bench-security
```

> 📸 **Wymagany screenshot 9**: Wynik Docker Bench Security

---

## Zadania do samodzielnego wykonania

### Zadanie 1: Optymalizacja własnego obrazu
Weź obraz z poprzednich laboratoriów i zoptymalizuj go maksymalnie. Udokumentuj każdy krok i redukcję rozmiaru.

### Zadanie 2: Bezpieczny Dockerfile
Napisz Dockerfile spełniający wszystkie dobre praktyki: konkretny tag, nie-root, healthcheck, .dockerignore, multi-stage, minimalne pakiety.

### Zadanie 3: Skanowanie projektu
Zeskanuj 3 różne obrazy (oficjalny, własny, społeczności) narzędziem Trivy. Porównaj wyniki i zaproponuj poprawki.

---

## Podsumowanie

Po ukończeniu tego laboratorium powinieneś umieć:
- ✅ Skanować obrazy pod kątem podatności (Scout, Trivy)
- ✅ Optymalizować rozmiar obrazów Docker
- ✅ Używać Hadolint do analizy Dockerfile
- ✅ Stosować ograniczenia zasobów i capabilities
- ✅ Konfigurować read-only filesystem
- ✅ Przeprowadzać audyt bezpieczeństwa Docker
