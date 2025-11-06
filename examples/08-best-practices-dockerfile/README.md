# Najlepsze praktyki tworzenia Dockerfile

Ten folder zawiera krótką instrukcję wraz z gotowymi przykładami pokazującymi dobre praktyki pisania plików Dockerfile. Przykłady są proste, ale ilustrują realne problemy: wydajność buildów, bezpieczeństwo, powtarzalność i rozmiar obrazów.

Spis treści:
- Dlaczego te praktyki są ważne
- Złote zasady (TL;DR)
- Optymalizacja cache i warstw
- Multi-stage builds
- Minimalne obrazy bazowe i wersjonowanie
- Użytkownik nie-root i uprawnienia
- .dockerignore
- ARG/ENV, sekrety build-time
- Reproducible builds (powtarzalność)
- Metadane (LABEL), HEALTHCHECK, sygnały
- Typowe pułapki
- Przykłady do uruchomienia
- Checklista do code review Dockerfile

---

## Dlaczego to ważne?
Dobrze napisany Dockerfile:
- buduje się szybciej (lepsze wykorzystanie cache),
- tworzy mniejsze obrazy (tańsze transfery i szybsze wdrożenia),
- jest bezpieczniejszy (mniej pakietów, użytkownik nie-root),
- zwiększa powtarzalność (pinning wersji, brak "latest"),
- ułatwia utrzymanie (czytelna struktura, [metadane](https://docs.docker.com/reference/dockerfile/#label), testowalność).

---

## Złote zasady (TL;DR)
- Nie używaj `:latest`. Przypinaj [tagi](https://hackernoon.com/docker-images-name-vs-tag-vs-digest) i (jeśli to możliwe) również [digesty](https://docs.docker.com/dhi/core-concepts/digests/).  
- Używaj multi-stage buildów: kompiluj w jednym etapie, uruchamiaj w lżejszym.
- Dbaj o cache: najpierw kopiuj pliki zależności (`requirements.txt`, `package*.json`), potem instaluj deps, na końcu kopiuj resztę.
- Używaj `.dockerignore` aby nie kopiować śmieci.
- Uruchamiaj proces jako użytkownik nie-root.
- Minimalizuj obraz: Alpine, slim, distroless (jeśli to pasuje) – ale świadomie.
- Dodaj `LABEL` z metadanymi oraz (gdy ma sens) `HEALTHCHECK`.
- Używaj `CMD` dla domyślnej komendy, `ENTRYPOINT` tylko gdy naprawdę potrzebny.
- Czyszcząc cache menedżera pakietów łącz komendy RUN w jedną warstwę.
- Nie przechowuj sekretów w obrazie. Do buildów używaj `--secret`/`RUN --mount=type=secret`.

---

## Optymalizacja cache i warstw
Cache działa per-linia Dockerfile. Zmieniaj jak najrzadziej wczesne warstwy.
- Dla Pythona: najpierw kopiuj `requirements.txt`, instaluj zależności, dopiero potem `COPY . .`.
- Dla Node.js: kopiuj `package.json`/`package-lock.json` (lub `pnpm-lock.yaml`), `npm ci`, na końcu `COPY . .`.
- Łącz instalację pakietów systemowych i sprzątanie cache w jednym `RUN`:
  ```Dockerfile
  RUN apk add --no-cache curl
  # lub w Debian/Ubuntu:
  RUN apt-get update && apt-get install -y --no-install-recommends \
      curl \
    && rm -rf /var/lib/apt/lists/*
  ```

---

## Multi-stage builds
Oddziel etap budowania (kompilacja, pobieranie dev-deps) od etapu runtime. Do finalnego obrazu kopiuj tylko to, co potrzebne w czasie uruchomienia.

Zalety:
- mniejszy i bezpieczniejszy obraz końcowy,
- brak dev-dependencies w runtime,
- lepsza kontrola nad artefaktami (np. gotowe binarki, zbudowane assety).

Zobacz plik `Dockerfile.python-good` i `Dockerfile.node-good` w tym folderze.

---

## Minimalne obrazy bazowe i wersjonowanie
- Wybieraj obrazy slim/minimal – ale pamiętaj o kompatybilności (np. glibc vs musl).
- Zawsze pinniuj wersje: `python:3.12-slim`, `node:20.11-alpine`. Dla maksymalnej powtarzalności użyj digestów:
  ```Dockerfile
  FROM python:3.12-slim@sha256:DIGEST_GOES_HERE
  ```

---

## Użytkownik nie-root
Uruchamianie procesu jako root zwiększa ryzyko eskalacji uprawnień. W tworzonym obrazie:
- dodaj użytkownika i grupę,
- nadaj odpowiednie właścicielstwa katalogom z danymi,
- używaj `USER app` w końcówce Dockerfile.

---

## .dockerignore
`.dockerignore` działa jak `.gitignore` dla buildu. Zignoruj:
- katalogi VCS (`.git`, `.hg`),
- katalogi IDE (`.idea`, `.vscode`),
- build artefakty (`node_modules`, `dist`, `build`),
- sekrety i pliki lokalne (`.env`, `*.pem`, `*.key`, `*.crt`),
- pliki tymczasowe (`__pycache__`, `*.pyc`, `*.log`).

Patrz: `.dockerignore-example` w tym folderze.

---

## ARG/ENV, sekrety build-time
- `ARG` służy do parametrów dostępnych tylko podczas buildu.
- `ENV` ustawia zmienne na runtime.
- Sekrety przekazuj tylko przez mechanizmy typu BuildKit:
  ```bash
  DOCKER_BUILDKIT=1 docker build \
    --secret id=pypi_token,src=./.secrets/pypi_token \
    -t myimg .
  ```
  a w Dockerfile:
  ```Dockerfile
  # syntax=docker/dockerfile:1.7
  RUN --mount=type=secret,id=pypi_token echo "(używam sekretu w tym kroku)"
  ```

---

## Reproducible builds (powtarzalność)
- Pinniuj wersje pakietów systemowych i językowych.
- Ustal strefę czasową/locale (lub neutralne LC_ALL=C.UTF-8).
- Utrzymuj kolejność kroków i deterministyczne źródła (lockfile!).

---

## Metadane i zdrowie kontenera
- Dodaj `LABEL` z informacjami o projekcie, maintainerze, licencji.
- Rozważ `HEALTHCHECK` (jeśli aplikacja ma endpoint zdrowia). Przykład:
  ```Dockerfile
  HEALTHCHECK --interval=30s --timeout=3s \
    CMD wget -qO- http://localhost:8000/health || exit 1
  ```
- Prawidłowo używaj `CMD` (domyślna komenda aplikacji). `ENTRYPOINT` używaj, gdy chcesz zawsze wywoływać określony binarny wrapper.

---

## Typowe pułapki
- `COPY . .` bez `.dockerignore` → gigantyczne obrazy, brak cache.
- `apt-get upgrade` w obrazie → trudna do śledzenia baza, lepiej pinning pakietów.
- Brak `--no-install-recommends` (Debian/Ubuntu) lub `--no-cache` (Alpine).
- Uruchamianie jako root.
- `latest` zamiast konkretnej wersji.
- Trzymanie sekretów (kluczy) w obrazie.

---

## Przykłady do uruchomienia
W tym folderze znajdziesz:
- `Dockerfile.python-bad` – antywzorzec z komentarzami, czego unikać,
- `Dockerfile.python-good` – dobry wzorzec (multi-stage, non-root, cache, LABEL, HEALTHCHECK),
- `Dockerfile.node-good` – dobry wzorzec dla Node.js (multi-stage, npm ci/pnpm, non-root),
- `.dockerignore-example` – przykładowa lista ignorowanych plików.

Przykładowy build (Python good):
```bash
cd examples/08-best-practices-dockerfile
docker build -f Dockerfile.python-good -t demo/python-good .
```

Przykładowy build (Node good):
```bash
docker build -f Dockerfile.node-good -t demo/node-good .
```

Uruchomienie (jeśli obraz wystawia serwer na :8000):
```bash
docker run --rm -p 8000:8000 demo/python-good
```

---

## Checklista do code review Dockerfile
- [ ] Brak `latest`, wersje są przypięte.
- [ ] Jest `.dockerignore` i nie kopiujemy śmieci.
- [ ] Warstwy uporządkowane pod cache (lockfile → install → reszta kodu).
- [ ] Multi-stage: finalny obraz bez dev-deps.
- [ ] Użytkownik nie-root, poprawne prawa do katalogów.
- [ ] LABEL z metadanymi.
- [ ] HEALTHCHECK (jeśli ma sens).
- [ ] Brak sekretów w obrazie; użyto mechanizmów build-time secrets jeśli potrzebne.
- [ ] Rozmiar obrazu sensowny; brak zbędnych pakietów systemowych.
- [ ] CMD poprawnie uruchamia aplikację; sygnały są obsłużone (PID 1 nie jest problemem).
