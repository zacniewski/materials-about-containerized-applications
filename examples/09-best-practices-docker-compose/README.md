# Najlepsze praktyki tworzenia pliku docker-compose (Python/Django)

Ten folder zawiera krótką instrukcję wraz z gotowymi przykładami dobrych praktyk dla Compose (docker-compose) w kontekście aplikacji Python/Django z bazą Postgres i Redis. Przykłady są proste, skupione i nie używają mechanizmu override ani profili.

Spis treści:
- Podstawy składni i struktura pliku docker-compose
- Najważniejsze komendy CLI (docker compose …)
- Dlaczego warto
- Złote zasady (TL;DR)
- Kluczowe sekcje i wzorce
- Przykładowe pliki Compose (good/bad)
- Uruchomienie przykładów
- Checklista do code review docker-compose

---

## Podstawy składni i struktura pliku docker-compose

Plik `docker-compose.yml` (lub `docker-compose.yaml`) opisuje wielokontenerową aplikację. Składnia opiera się na [Compose Spec](https://compose-spec.io/). Najważniejsze elementy:

- Top‑level klucze:
  - `name:` — logiczna nazwa projektu (prefiks dla nazw sieci i wolumenów). Jeśli brak, Compose użyje nazwy katalogu.
  - `services:` — lista usług/kontenerów, które mają być uruchomione razem.
  - `networks:` — zdefiniowane sieci, do których podłączane są usługi.
  - `volumes:` — named volumes, trwałe miejsca na dane.
  - (opcjonalnie) `configs:`/`secrets:` — szczególnie w Swarm/K8s; klasyczny `docker compose` traktuje je ograniczenie.
  - Pola rozszerzeń: `x-...` — prywatne sekcje pomocnicze (np. szablony, które potem wstrzykujesz aliasem YAML). Compose je ignoruje, ale możesz z nich korzystać przez aliasy.

Uwaga: współczesne Compose nie wymagają pola `version:` — jest przestarzałe w specyfikacji. Stosuj układ jak w przykładach poniżej.

Najczęstsze klucze w obrębie `services.<nazwa-usługi>`:
- Identyfikacja obrazu i budowanie:
  - `image:` — gotowy obraz z rejestru (np. `python:3.12-slim`).
  - `build:` — jak zbudować obraz z lokalnego Dockerfile (np. `build: .` albo struktura z `context`, `dockerfile`, `args`).
- Uruchamianie procesu:
  - `command:` — domyślna komenda (może nadpisać `CMD` z obrazu).
  - `entrypoint:` — rzadziej używane; zastępuje `ENTRYPOINT` obrazu.
- Konfiguracja środowiska:
  - `env_file:` — ścieżka(i) do plików `.env` wczytywanych do kontenera.
  - `environment:` — dodatkowe pary `KEY: VALUE` lub referencje `${VAR}` z interpolacją.
- I/O i sieć:
  - `ports:` — mapowanie portów host:kontener, np. `"8000:8000"`.
  - `volumes:` — montowanie named volumes lub bind‑mountów.
  - `networks:` — do jakich sieci należy usługa.
- Zależności i stan:
  - `depends_on:` — kolejność startu; z `condition: service_healthy` możesz czekać na healthcheck.
  - `healthcheck:` — jak sprawdzić gotowość usługi (test, interval, timeout, retries, start_period).
  - `restart:` — polityka restartu, np. `unless-stopped`.
- Obserwowalność i limity:
  - `logging:` — sterownik i rotacja logów.
  - `deploy:` — limity zasobów (głównie dla Swarm; lokalny `docker compose` ich nie egzekwuje).

Minimalny przykład (Python + Postgres), bez kotwic YAML:
```yaml
name: demo

services:
  web:
    image: python:3.12-slim
    working_dir: /app
    command: ["python", "-m", "http.server", "8000"]
    env_file: [.env]
    environment:
      APP_ENV: ${APP_ENV:-production}
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_started
    networks: [backend, frontend]

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: ${POSTGRES_USER:?set in .env}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?set in .env}
      POSTGRES_DB: ${POSTGRES_DB:-appdb}
    volumes:
      - pgdata:/var/lib/postgresql/data
    networks: [backend]

networks:
  frontend: {name: demo-frontend}
  backend: {name: demo-backend}

volumes:
  pgdata: {name: demo-pgdata}
```

W tym repo znajdziesz również wariant z kotwicami/aliasami YAML (`docker-compose.good.yaml`) i bez kotwic (`docker-compose.good2.yaml`).

---

## Najważniejsze komendy CLI (docker compose …)

Poniżej najczęściej używane polecenia CLI (nowa składnia: `docker compose`, bez myślnika):
- Uruchomienie w tle: `docker compose up -d`
- Podgląd logów: `docker compose logs -f` lub dla jednej usługi: `docker compose logs -f web`
- Lista kontenerów w projekcie: `docker compose ps`
- Wejście do shell’a w kontenerze: `docker compose exec web sh` (lub `bash` jeśli jest)
- Zatrzymanie: `docker compose stop`
- Restart usług: `docker compose restart [web db]`
- Usunięcie zasobów (kontenery, sieci; z `-v` także named volumes): `docker compose down -v`
- Budowanie obrazów (gdy używasz `build:`): `docker compose build`
- Pobranie obrazów z rejestru: `docker compose pull`
- Sprawdzenie/zwalidowanie pliku: `docker compose config` (połączy pliki, pokaże efekt interpolacji)

Dla wielu plików (`-f` wskazuje plik):
```bash
docker compose -f docker-compose.good.yaml up -d
```

Wskazówka: zawsze pracuj z aktualną wersją Docker Desktop/CLI v2+, aby mieć dostęp do najnowszych możliwości Compose.

---

## Dlaczego warto
Dobrze przygotowany plik `docker-compose`:
- ułatwia pracę zespołową (powtarzalne środowisko developerskie),
- poprawia bezpieczeństwo (izolacja sieci, brak secretów w repo),
- zmniejsza ilość awarii (healthcheck, kolejność startu, restart policy),
- upraszcza utrzymanie (czytelne nazwy, sekcje, kotwice/ankory do współdzielenia ustawień),
- upraszcza start bez dodatkowych plików (brak override i profili w tym przykładzie).

---

## Złote zasady (TL;DR)
- Nie używaj `latest`. Podawaj konkretne tagi obrazów (`python:3.12-slim`, `postgres:16`, `redis:7-alpine`).
- Trzymaj w `.env` wyłącznie niesekretne lub devowe zmienne; sekretów nie commituj — ładuj z plików poza repo lub z menedżera sekretów (Swarm/K8s/SealedSecrets/1Password/Vault).
- Używaj `env_file:` i/lub `.env` zamiast zasypywania `environment:` w YAML-u.
- Dodaj `healthcheck:` i używaj `depends_on.condition: service_healthy` dla właściwej kolejności startu.
- Rozdzielaj sieci (`frontend`, `backend`) i przypisuj usługi tylko do potrzebnych sieci.
- Używaj named volumes dla danych (np. `pgdata`), a bind-mountów unikaj w tym przykładzie – używamy named volumes także dla statycznych/mediów.
- Ustal `restart:` (np. `unless-stopped`) do usług długowiecznych.
- Używaj kotwic (anchor) i aliasów YAML do DRY (np. wspólne logowanie/zmienne).
- Dokumentuj wszystko w README i komentuj YAML.

Uwaga: sekcja `deploy:` (limity zasobów) jest honorowana przez Docker Swarm i nie przez klasyczne `docker compose` (local). Dla limitów lokalnych rozważ cgroups/parametry uruchomienia lub środowiska orkiestracji.

---

## Kluczowe sekcje i wzorce
- `env_file:` i `.env`: prosty sposób na konfigurację bez twardego wpisywania wartości w YAML.
- `healthcheck:`: wykrywanie gotowości usług, współpraca z `depends_on.condition: service_healthy`.
- `networks:`: separacja płaszczyzn (frontend/backend), mniejsze ryzyko wycieków.
- `volumes:`: trwały stan baz danych i innych usług (tu także `staticfiles` i `media` dla Django).
- `logging:`: ujednolicone sterowniki i limity rotacji logów.
- Kotwice/aliasy YAML: `x-logging: &default-logging` i użycie aliasu `*default-logging`.

---

## Przykładowe pliki
- `docker-compose.good.yaml` – dobry, skomentowany wzorzec pod Python/Django (bez override i profili). Używa kotwic YAML do współdzielenia ustawień (`&common-env`, `&default-logging`).
- `docker-compose.good2.yaml` – funkcjonalnie taki sam przykład jak wyżej, ale bez użycia kotwic/aliasów YAML (wszystko „rozpisane wprost”).
- `docker-compose.bad.yaml` – antywzorzec z komentarzami.
- `.env.example` – przykładowe zmienne środowiskowe (skopiuj do `.env`).

---

## Uruchomienie przykładów
1) Skopiuj `.env.example` do `.env` i ewentualnie zmodyfikuj wartości:
```bash
autocp .env.example .env 2>/dev/null || cp .env.example .env
```
2) Uruchom dobry przykład:
```bash
docker compose -f docker-compose.good.yaml up -d
```
Alternatywnie (ta sama funkcjonalność, bez kotwic YAML):
```bash
docker compose -f docker-compose.good2.yaml up -d
```
3) Zatrzymanie i usunięcie (łącznie z named volumes):
```bash
docker compose -f docker-compose.good.yaml down -v
```

Jeśli uruchamiałeś `good2`, analogicznie:
```bash
docker compose -f docker-compose.good2.yaml down -v
```

---

## Checklista do code review docker-compose
- [ ] Obrazy mają przypięte tagi (brak `latest`).
- [ ] Brak sekretów w repo; `.env` nie zawiera haseł produkcyjnych.
- [ ] Użyto `env_file:`/`.env`, a nie wstrzykniętych literalnych sekretów w YAML.
- [ ] Krytyczne zmienne są walidowane poprzez `${VAR:?msg}` albo mają bezpieczne domyślne `${VAR:-value}`.
- [ ] Poprawne cytowanie wartości (np. `DEBUG="0"`/`"false"` dla Django), brak pułapek z booleanami/liczbami.
- [ ] Brak wielowierszowych/niebezpiecznych sekretów w `.env`; użyto bezpieczniejszych mechanizmów (pliki poza repo / manager sekretów).
- [ ] Dodano `healthcheck` dla usług stanowych i zależności `depends_on.condition: service_healthy`.
- [ ] Zdefiniowano logiczne `networks` i usługi są przypisane tylko do potrzebnych sieci.
- [ ] Dane (DB, uploady) są w named volumes (nie giną po `down`).
- [ ] Zastosowano `restart:` dla usług długowiecznych.
- [ ] Użyto DRY przez kotwice YAML (logowanie, wspólne env).
- [ ] Plik jest krótko skomentowany, a README tłumaczy sposób użycia.

---

## Kotwice i aliasy YAML: co oznacza `&common-env`

W pliku `docker-compose.good.yaml` wykorzystujemy mechanizm kotwic (anchors) i aliasów YAML, aby unikać duplikacji (DRY):

```yaml
x-common-env: &common-env
  TZ: ${TZ:-UTC}
  APP_ENV: ${APP_ENV:-production}
```

- `&common-env` „kotwiczy” (nazwie) wspólny słownik zmiennych środowiskowych.
- W usługach wstrzykujemy go przez alias `*common-env` wraz z kluczem scalającym `<<:`:

```yaml
x-common-env: &common-env
  TZ: ${TZ:-UTC}
  APP_ENV: ${APP_ENV:-production}

services:
  web:
    environment:
      <<: *common-env
      # ...opcjonalnie własne klucze
```

Efekt: `TZ` i `APP_ENV` zostaną dodane do `environment` usługi bez powtarzania ich definicji w wielu miejscach.

Analogicznie działa `x-logging: &default-logging` + użycie `logging: *default-logging` dla spójnej konfiguracji logowania.

Uwaga: jeśli ten sam klucz pojawi się i w kotwicy, i lokalnie, zwykle „ostatni wygrywa” (wartość z późniejszej definicji nadpisze wcześniejszą).

Jeśli wolisz unikać kotwic, użyj alternatywnego pliku `docker-compose.good2.yaml`, w którym te same wartości są wpisane jawnie przy każdej usłudze.

---

## Zmienne środowiskowe: dobre i złe praktyki (Python/Django)

Poniżej kilka praktycznych porad oraz krótkie „good/bad” przykłady związane z konfiguracją przez zmienne środowiskowe w Docker Compose.

### 1) `.env` i `env_file:` – kiedy i jak używać
- `.env` w katalogu z `docker-compose` służy do interpolacji w samym pliku YAML (np. `${APP_PORT}`) oraz do przekazania do usług, jeśli używasz `env_file:`.
- `env_file:` pozwala wstrzyknąć wartości do `environment:` usług bez nadmiernego rozwlekania YAML.
- Precedencja (uproszczenie): wartości z `environment:` w YAML nadpiszą wartości z `env_file:`/`.env` dla danej usługi.

Good:
```yaml
services:
  web:
    env_file: [.env]
    environment:
      # jawne, bezpieczne domyślne
      APP_ENV: ${APP_ENV:-production}
```

Bad:
```yaml
services:
  web:
    # twarde wartości w YAML, trudne do zmiany między środowiskami
    environment:
      APP_ENV: production
      SECRET_KEY: s3cr3t # sekret w repo!
```

### 2) Wymagane i domyślne wartości (`${VAR:?}` i `${VAR:-}`)
- `${VAR:?komunikat}` – przerwie uruchamianie, jeśli `VAR` nie jest ustawione. Idealne dla krytycznych parametrów (np. hasła w dev/test, które wczytujesz spoza repo).
- `${VAR:-default}` – ustawia sensowną wartość domyślną, gdy zmienna nie jest podana.

Good:
```yaml
services:
  db:
    environment:
      POSTGRES_USER: ${POSTGRES_USER:?set in .env}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?set in .env}
      POSTGRES_DB: ${POSTGRES_DB:-appdb}
```

Bad:
```yaml
services:
  db:
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin # brak walidacji; zła praktyka
```

### 3) Cytowanie, booleany i liczby – unikaj cichych konwersji
- Compose traktuje wartości jako łańcuchy, ale YAML potrafi zinterpretować `true/false`, `on/off`, `yes/no`, `1/0`. W Django `DEBUG` powinien być stringiem i logika powinna go jawnie rzutować.
- Bezpiecznie cytuj: `DEBUG="0"` lub `DEBUG="false"` w `.env` i zrób rzutowanie w kodzie (np. `env_bool = os.getenv("DEBUG") == "1"`).

Good (`.env`):
```
DEBUG="0"
ALLOWED_HOSTS="localhost,127.0.0.1"
```

Bad (`.env`):
```
DEBUG=false   # może być zinterpretowane inaczej niż oczekujesz
```

### 4) Sekrety – nie trzymaj w repo
- `.env.example` to tylko szablon. Prawdziwy `.env` trzymaj poza repo i dystrybuuj bezpiecznym kanałem.
- Dla środowisk produkcyjnych używaj managerów sekretów (Swarm/K8s/1Password/Vault) albo montuj pliki z sekretami spoza repo (np. `env_file: ../secrets/prod.env`).
- Nie wkładaj długich sekretów/wielowierszowych kluczy do `.env` – użyj plików i wczytaj ścieżki.

Good:
```yaml
services:
  web:
    env_file: ../secrets/dev.env # poza repo
```

Bad:
```yaml
services:
  web:
    environment:
      SECRET_KEY: "very-long-production-secret-key" # w repo!
```

### 5) Per‑service override i kolejność scalania (kotwice)
- Jeśli używasz kotwic (`<<: *common-env`), pamiętaj: „ostatni wygrywa”. Umieszczenie merge nad lub pod lokalnymi kluczami wpływa na wynik.
- Jeżeli nie chcesz kotwic, użyj wariantu `good2` i wpisz jawne wartości – mniejsza magia, więcej powtarzalności.

Good (kotwica na początku, potem lokalne nadpisania):
```yaml
x-common-env: &common-env
  APP_ENV: production

environment:
  <<: *common-env
  APP_ENV: development
```

Bad (nieintencjonalne nadpisanie przez kotwicę wstawioną na końcu):
```yaml
x-common-env: &common-env
  APP_ENV: production

environment:
  APP_ENV: development
  <<: *common-env  # APP_ENV może wrócić do production
```

### 6) Escaping `$`, CRLF i inne pułapki
- Aby w `command:`/`healthcheck:` użyć dosłownego znaku `$`, wpisz `$$` (Compose inaczej spróbuje interpolować zmienne):
```yaml
healthcheck:
  test: ["CMD-SHELL", "echo $$HOME >/dev/null"]
```
- Uważaj na końce linii w `.env` – używaj UTF‑8 LF, nie CRLF (Windows). CRLF może powodować niewidoczne błędy.

### 7) Przykłady dla Django
- `.env.example` powinien zawierać tylko wartości przykładowe, bez prawdziwych sekretów:
```
APP_ENV=production
DEBUG="0"
ALLOWED_HOSTS="localhost,127.0.0.1"
SECRET_KEY=changeme # tylko w example!
```
- Kod aplikacji niech jednoznacznie rzutuje typy, np. w `settings.py`:
```python
import os

def env_bool(name, default="0"):
    return os.getenv(name, default) in {"1", "true", "True", "YES", "yes"}

DEBUG = env_bool("DEBUG", "0")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",") if os.getenv("ALLOWED_HOSTS") else []
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
```

---

### Mini „good/bad” ściąga

Good (krótki, bezpieczny fragment):
```yaml
services:
  web:
    env_file: [.env]
    environment:
      APP_ENV: ${APP_ENV:-production}
      TZ: ${TZ:-UTC}
      DEBUG: ${DEBUG:-"0"}
  db:
    environment:
      POSTGRES_USER: ${POSTGRES_USER:?set in .env}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?set in .env}
      POSTGRES_DB: ${POSTGRES_DB:-appdb}
```

Bad (czego unikać):
```yaml
services:
  web:
    environment:
      DEBUG: true   # niejednoznaczne
      SECRET_KEY: prod-secret-w-repo # sekret w YAML
  db:
    environment:
      POSTGRES_PASSWORD: admin # brak walidacji, słabe hasło
```

---

## Healthcheck: dobre i złe praktyki (Python/Django)

Healthcheck pozwala Compose/orkiestratorowi wykryć, kiedy usługa jest gotowa do pracy. W połączeniu z `depends_on.condition: service_healthy` możesz ustalić poprawną kolejność startu (np. `web` czeka na gotową bazę).

Najważniejsze zasady:
- Sprawdzaj „realną gotowość”, nie tylko to, że proces żyje. Dla HTTP sprawdź endpoint, dla DB – komendę klienta (`pg_isready`, `redis-cli ping`).
- Ustal rozsądne czasy: `interval` 10–30s, `timeout` 2–5s, `retries` 3–5, `start_period` dłuższy przy zimnym starcie/migracjach (10–60s).
- Na minimalnych obrazach (slim/alpine) unikaj `curl/wget`, jeśli ich nie ma. W Pythonie możesz użyć wbudowanych modułów (`urllib.request`, `socket`).
- Test musi zwracać kod wyjścia 0 dla „healthy” i !=0 dla „unhealthy”. Unikaj poleceń, które zawsze kończą się 0.
- Pamiętaj o escapingu `$` w `CMD-SHELL` (pisz `$$`), gdy używasz zmiennych powłoki.

### Dobre przykłady (Good)

Web (Python slim; HTTP 200 na porcie 8000, bez curl/wget):
```yaml
services:
  web:
    healthcheck:
      test: ["CMD-SHELL", "python - <<'PY'\nimport sys, urllib.request\ntry:\n    with urllib.request.urlopen('http://localhost:8000/health', timeout=2) as r:\n        sys.exit(0 if r.status == 200 else 1)\nexcept Exception:\n    sys.exit(1)\nPY"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 15s
```

Postgres (sprawdzenie gotowości serwera):
```yaml
services:
  db:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB:-appdb}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 15s
```

Redis (pomyślny `PING` daje `PONG`; na obrazie alpine dodaj `redis-cli` jeśli brak):
```yaml
services:
  redis:
    command: ["redis-server", "--appendonly", "yes"]
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5
```

Nginx (jeśli obraz ma `wget`/`busybox`):
```yaml
services:
  nginx:
    healthcheck:
      test: ["CMD-SHELL", "wget -qO- http://localhost:80/ >/dev/null"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 10s
```
Jeśli w obrazie nie ma żadnych narzędzi HTTP, rozważ prosty test gniazda TCP (busybox `nc`):
```yaml
healthcheck:
  test: ["CMD-SHELL", "nc -z localhost 80"]
  interval: 30s
  timeout: 3s
  retries: 3
```

### Złe przykłady (Bad)

- Brak healthcheck + `depends_on: [db]` (kolejność startu bywa losowa, aplikacja może ruszyć zanim DB będzie gotowa):
```yaml
services:
  web:
    depends_on: [db]  # brak condition: service_healthy
    # brak healthcheck
```

- Użycie narzędzi, których nie ma w obrazie (na `python:3.12-slim` brak `curl`/`wget`):
```yaml
services:
  web:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]  # curl nie istnieje → zawsze unhealthy
```

- Test, który zawsze zwraca 0 (fałszywa „zdrowość”):
```yaml
healthcheck:
  test: ["CMD-SHELL", "echo ok"]  # zawsze 0 – bez sensu
  interval: 1s   # zbyt agresywne: obciąża proces
  timeout: 1s
  retries: 1
```

### Wskazówki praktyczne
- Dopasuj `start_period` do czasu migracji/startu DB. Jeśli `web` wykonuje migracje przy starcie, wydłuż `start_period` dla `web` lub usuń healthcheck na czas długich migracji CI.
- Healthcheck ≠ liveness probe. Gdy healthcheck jest „unhealthy”, Compose nie restartuje automatycznie kontenera (to robią niektóre orkiestratory). Użyj `restart:` i monitoringu.
- Nie sprawdzaj zewnętrznych usług przez Internet – unikaj flaky. Weryfikuj tylko to, co lokalnie w kontenerze.
- Dla Django rozważ dedykowany endpoint `/health` zwracający 200 i minimalny payload (bez kosztownych zapytań).
