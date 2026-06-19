### Materiały z przedmiotu "Aplikacje w środowisku kontenerowym"

> **Wymiar godzinowy:** 20 godz. wykładu + 60 godz. laboratorium  
> **Główne narzędzie:** Docker

---

#### I. Wymagania
  - :zap: zainstalowany [Docker](https://docs.docker.com/get-started/get-docker/),
  - :zap: zainstalowany [Docker Compose](https://docs.docker.com/compose/) (wbudowany w Docker od wersji 20.10+),
  - :zap: konto na [DockerHub](https://hub.docker.com/),
  - :zap: terminal / wiersz poleceń (Linux, macOS lub Windows z WSL2).

#### II. Pożyteczne linki
  - [DevOps with Docker](https://devopswithdocker.com/) course (i także na [GitHub'ie](https://github.com/docker-hy/docker-hy.github.io)),
  - [DevOps with Kubernetes](https://devopswithkubernetes.com/) training.

> Dodatkowe, pomocne materiały do ćwiczeń znajdują się w folderze [`supporting-materials/basic-docker-training/`](supporting-materials/basic-docker-training/README.md) (wersje PL/EN).

---

#### III. Wykłady (20 godz. — 10 × 2 godz.)

Wszystkie wykłady znajdują się w folderze [`lectures/`](lectures/).

| # | Temat wykładu | Plik |
|---|--------------|------|
| 1 | Wprowadzenie do konteneryzacji | [01-wprowadzenie-do-konteneryzacji.md](lectures/01-wprowadzenie-do-konteneryzacji.md) |
| 2 | Obrazy Docker i rejestry | [02-obrazy-i-rejestry.md](lectures/02-obrazy-i-rejestry.md) |
| 3 | Dockerfile i budowanie obrazów | [03-dockerfile-budowanie-obrazow.md](lectures/03-dockerfile-budowanie-obrazow.md) |
| 4 | Kontenery — zarządzanie i cykl życia | [04-kontenery-zarzadzanie-cykl-zycia.md](lectures/04-kontenery-zarzadzanie-cykl-zycia.md) |
| 5 | Wolumeny i trwałość danych | [05-wolumeny-i-trwalosc-danych.md](lectures/05-wolumeny-i-trwalosc-danych.md) |
| 6 | Sieci Docker | [06-sieci-docker.md](lectures/06-sieci-docker.md) |
| 7 | Docker Compose — orkiestracja wielu kontenerów | [07-docker-compose.md](lectures/07-docker-compose.md) |
| 8 | Bezpieczeństwo i dobre praktyki Docker | [08-bezpieczenstwo-i-dobre-praktyki.md](lectures/08-bezpieczenstwo-i-dobre-praktyki.md) |
| 9 | CI/CD i Docker w produkcji | [09-ci-cd-i-docker-w-produkcji.md](lectures/09-ci-cd-i-docker-w-produkcji.md) |
| 10 | Orkiestracja kontenerów i Kubernetes | [10-orkiestracja-i-kubernetes.md](lectures/10-orkiestracja-i-kubernetes.md) |

---

#### IV. Laboratoria (60 godz. — 10 × 6 godz.)

Wszystkie laboratoria znajdują się w folderze [`labs/`](labs/).

| # | Temat laboratorium | Plik | Kluczowe zagadnienia |
|---|-------------------|------|---------------------|
| 1 | Pierwsze kroki z Dockerem | [01-pierwsze-kroki-z-dockerem.md](labs/01-pierwsze-kroki-z-dockerem.md) | Instalacja, `docker run`, obrazy, kontenery, porty |
| 2 | Budowanie obrazów z Dockerfile | [02-budowanie-obrazow-dockerfile.md](labs/02-budowanie-obrazow-dockerfile.md) | Dockerfile, FROM, RUN, COPY, CMD, ENTRYPOINT, multi-stage |
| 3 | Wolumeny i trwałość danych | [03-wolumeny-i-trwalosc-danych.md](labs/03-wolumeny-i-trwalosc-danych.md) | Volumes, bind mounts, tmpfs, bazy danych, backup |
| 4 | Sieci Docker | [04-sieci-docker.md](labs/04-sieci-docker.md) | Bridge, user-defined networks, DNS, izolacja, porty |
| 5 | Docker Compose — podstawy | [05-docker-compose-podstawy.md](labs/05-docker-compose-podstawy.md) | YAML, services, volumes, networks, depends_on, .env |
| 6 | Docker Compose — zaawansowany | [06-docker-compose-zaawansowany.md](labs/06-docker-compose-zaawansowany.md) | Profiles, secrets, override, reverse proxy, monitoring |
| 7 | Konteneryzacja aplikacji | [07-konteneryzacja-aplikacji.md](labs/07-konteneryzacja-aplikacji.md) | Python, Node.js, Django, PHP, Java, multi-stage |
| 8 | Bezpieczeństwo i optymalizacja | [08-bezpieczenstwo-i-optymalizacja.md](labs/08-bezpieczenstwo-i-optymalizacja.md) | Skanowanie, Hadolint, nie-root, capabilities, rozmiar |
| 9 | Własny projekt Docker Compose | [09-projekt-docker-compose.md](labs/09-projekt-docker-compose.md) | Pełna aplikacja: Nginx + API + DB + Cache |
| 10 | Powtórzenie i przygotowanie do egzaminu | [10-powtorzenie-i-egzamin.md](labs/10-powtorzenie-i-egzamin.md) | DevOps with Docker, zadania egzaminacyjne |

---

#### V. Zawartość repozytorium

| Folder | Opis |
|--------|------|
| [`lectures/`](lectures/) | 10 wykładów w plikach Markdown (z diagramami Mermaid) |
| [`labs/`](labs/) | 10 laboratoriów w plikach Markdown |
| [`reports/`](reports/) | Szablon sprawozdania |
| [`supporting-materials/`](supporting-materials/) | Materiały pomocnicze (ćwiczenia, kurs „DevOps with Docker", przykładowe projekty) |
| ↳ [`basic-docker-training/`](supporting-materials/basic-docker-training/README.md) | Standardowe ćwiczenia z Dockera (PL/EN) |
| ↳ [`devops-with-docker/`](supporting-materials/devops-with-docker/) | Kurs „DevOps with Docker" (PL/EN) |
| ↳ [`examples/`](supporting-materials/examples/) | Przykładowe projekty Docker (Node.js, PHP, Python, Django, Java, Go, sieci, dobre praktyki) |

##### Szczegółowy opis zawartości `supporting-materials/`

**[`basic-docker-training/`](supporting-materials/basic-docker-training/README.md)** — Szkolenie z podstaw Dockera (wersja 2024 r., oryginał: [David Elner](https://github.com/delner/docker-training)). Zawiera 6 ćwiczeń w wersjach PL i EN:
  1. Uruchamianie kontenerów
  2. Modyfikowanie obrazów
  3. Budowanie obrazów
  4. Udostępnianie obrazów
  5. Wolumeny
  6. Sieci

  Dodatkowo foldery `ex3/` i `ex5/` z plikami pomocniczymi do ćwiczeń.

**[`devops-with-docker/`](supporting-materials/devops-with-docker/)** — Kurs „DevOps with Docker" (oryginał: University of Helsinki). Materiały w wersjach PL i EN, podzielone na 3 części:
  - **Part 1** (7 sekcji) — Podstawy: uruchamianie kontenerów, obrazy, Dockerfile, interakcja z kontenerami
  - **Part 2** (5 sekcji) — Docker Compose, wolumeny, sieci, orkiestracja wielu kontenerów
  - **Part 3** (6 sekcji) — Tematy zaawansowane: CI/CD, bezpieczeństwo, optymalizacja, wdrażanie

  Folder `img/` zawiera ilustracje i diagramy wykorzystywane w materiałach.

**[`examples/`](supporting-materials/examples/)** — Przykładowe projekty Docker z plikami `Dockerfile` i/lub `docker-compose.yaml`:

| Folder | Opis |
|--------|------|
| `01-nodejs` | Prosta aplikacja Node.js |
| `02-php-mysql` | Aplikacja PHP z bazą MySQL (Docker Compose) |
| `03-python` | Prosta aplikacja Python |
| `04-django` | Aplikacja Django z bazą SQLite |
| `05-mongodb-v1` | Aplikacja Node.js z bazą MongoDB (Docker Compose) |
| `06-msb` | Aplikacja Go — porównanie single-stage vs multi-stage build |
| `07-docker-cp` | Przykład użycia `docker cp` |
| `08-best-practices-dockerfile` | Dobre i złe praktyki w Dockerfile (Python, Node.js) |
| `09-best-practices-docker-compose` | Dobre i złe praktyki w Docker Compose |
| `10-networks` | Konfiguracje sieci Docker (front-back, internal, macvlan) |
| `11-django-react` | Pełna aplikacja Django + React (Docker Compose) |
| `12-java-spring-boot` | Aplikacja Java Spring Boot z Docker Compose |

---

#### VI. Zadania do realizacji (we wszystkich laboratoriach)
  - należy przeanalizować wszystkie ćwiczenia, wykonując na swoim komputerze wszystkie wyszczególnione komendy,
  - tam, gdzie napisane jest „wymagany screenshot XY", należy dokonać zapisu bieżącego stanu terminala poprzez zrzut ekranu, a plik nazwać `XY.png`,
  - na zrzucie ekranu powinien znajdować się informacja o danym użytkowniku (idealnie numer indeksu),
  - można np. nazwać folder roboczy `kontenery-123456`, gdzie `123456` to numer indeksu :smiley:,
  - ww. plik umieszczamy w pliku `README.md`, dotyczącym danego ćwiczenia, wraz z krótkim opisem.

#### VII. Pytania egzaminacyjne
1. Utwórz `Dockerfile`, w którym z hosta do kontenera kopiowany będzie folder `code` i zbuduj go. Uruchom skrypt wewnątrz kontenera.
2. Skopiuj wybrany plik tekstowy z hosta do kontenera Dockerowego.
3. Skopiuj wybrany plik tekstowy z kontenera Dockerowego do hosta.
4. Pokaż działanie komend `ENTRYPOINT` i `CMD` w wybranym projekcie.
5. Pokaż działanie usługi bazodanowej z wykorzystaniem `docker-compose`.
6. Pokaż działanie komend `ADD`, `COPY` i `WORKDIR` w wybranym projekcie.
7. Pokaż działanie `docker compose` w swoim projekcie.
8. Omów na podstawie swojej aplikacji komendy `docker inspect` i `docker logs`.
9. Czym są sieci w Dockerze? Zaprezentuj przykład na bazie swojego projektu.
10. Jaka jest różnica między obrazem i kontenerem? Pokaż przykład budowania obrazu i uruchamiania kontenera.
11. Pokaż jak „wejść" do wybranego kontenera. Utwórz w nim plik tekstowy. Zademonstruj trwałość danych z wolumenem.
12. Zbuduj obraz, nadaj mu tag i opublikuj na DockerHubie. Następnie usuń lokalnie i pobierz z DockerHuba.
13. Pokaż co najmniej dwie dobre praktyki związane z `Dockerfile`.
14. Pokaż co najmniej dwie dobre praktyki związane z `docker-compose.yaml`.
