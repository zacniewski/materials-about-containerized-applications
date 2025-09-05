---
title: 'Migracja do Docker Compose'
---

Nawet przy prostym obrazie mieliśmy już do czynienia z wieloma opcjami wiersza poleceń podczas budowania, wypychania i uruchamiania obrazu.

Teraz przejdziemy do narzędzia [Docker Compose](https://docs.docker.com/compose/), aby tym zarządzać. Docker Compose był kiedyś osobnym narzędziem, ale teraz jest zintegrowany z Dockerem i można go używać jak pozostałych komend Dockera.

Docker Compose został zaprojektowany, aby uprościć uruchamianie aplikacji wielokontenerowych za pomocą pojedynczej komendy.

Załóżmy, że jesteśmy w katalogu z naszym Dockerfile o następującej treści:

```dockerfile
FROM ubuntu:22.04

WORKDIR /mydir

RUN apt-get update && apt-get install -y curl python3
RUN curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
RUN chmod a+x /usr/local/bin/yt-dlp

ENTRYPOINT ["/usr/local/bin/yt-dlp"]
```

Utwórzmy teraz plik `docker-compose.yml`:

```yaml
version: '3.8'

services:
  yt-dlp-ubuntu:
    image: <username>/<repositoryname>
    build: .
```

Ustawienie version nie jest bardzo restrykcyjne — po prostu musi być powyżej 2, bo inaczej składnia różni się znacząco. Zobacz <https://docs.docker.com/compose/compose-file/> po więcej informacji.

Wartość klucza `build` może być ścieżką w systemie plików (w przykładzie to bieżący katalog `.`) albo obiektem z kluczami `context` i `dockerfile`, patrz [dokumentacja](https://docs.docker.com/compose/compose-file/build/).

Teraz możemy budować i wypychać obraz tylko tymi komendami:

```console
$ docker compose build
$ docker compose push
```

## Wolumeny w Docker Compose

Aby uruchomić obraz tak jak wcześniej, musimy dodać bind mounts. Wolumeny w Docker Compose definiujemy składnią `lokalizacja-na-hoście:lokalizacja-w-kontenerze`. Compose może działać bez ścieżki absolutnej:

```yaml
version: '3.8'

services:

  yt-dlp-ubuntu:
    image: <username>/<repositoryname>
    build: .
    volumes:
      - .:/mydir
    container_name: yt-dlp
```

Możemy też nadać kontenerowi nazwę, której będzie używać podczas działania, przez container_name. Nazwę usługi można wykorzystać do uruchomienia:

```console
$ docker compose run yt-dlp-ubuntu https://imgur.com/JY5tHqr
```

## Ćwiczenie 2.1

::::info Exercise 2.1

  Wykorzystajmy teraz Docker Compose z prostą usługą webową, której użyliśmy w [Ćwiczeniu 1.3](/part-1/section-2#exercise-13)

  Bez polecenia `devopsdockeruh/simple-web-service` będzie tworzył logi w `/usr/src/app/text.log`.

  Utwórz plik docker-compose.yml, który uruchamia `devopsdockeruh/simple-web-service` i zapisuje logi w Twoim systemie plików.

  Prześlij docker-compose.yml i upewnij się, że działa po prostu po uruchomieniu `docker compose up`, jeśli plik logów istnieje.

::::

## Usługi webowe w Docker Compose

Compose jest naprawdę przeznaczony do uruchamiania usług webowych, więc przejdźmy od prostych wrapperów binarnych do uruchamiania usługi HTTP.

<https://github.com/jwilder/whoami> to prosta usługa, która wypisuje bieżący identyfikator kontenera (hostname).

```console
$ docker container run -d -p 8000:8000 jwilder/whoami
  736ab83847bb12dddd8b09969433f3a02d64d5b0be48f7a5c59a594e3a6a3541
```

Wejdź przeglądarką lub curl na localhost:8000 — oba odpowiedzą identyfikatorem.

Zatrzymaj kontener, aby nie blokował portu 8000.

```console
$ docker container stop 736ab83847bb
$ docker container rm 736ab83847bb
```

Utwórzmy nowy katalog i plik Docker Compose `whoami/docker-compose.yml` na podstawie opcji z wiersza poleceń.

```yaml
version: '3.8'

services:
  whoami:
    image: jwilder/whoami
    ports:
      - 8000:8000
```

Przetestuj:

```console
$ docker compose up -d
$ curl localhost:8000
```

Zmienne środowiskowe można też przekazywać kontenerom w Docker Compose w następujący sposób:

```yaml
version: '3.8'

services:
  backend:
    image: your-backend-image
    environment:
      - VARIABLE=VALUE
      - VARIABLE2=VALUE2
```

Zauważ, że istnieją też [inne](https://docs.docker.com/compose/environment-variables/set-environment-variables/), być może bardziej eleganckie sposoby definiowania zmiennych środowiskowych w Docker Compose.

## Ćwiczenia 2.2 - 2.3

::::info Exercise 2.2

  Przeczytaj, jak dodać command do docker-compose.yml w [dokumentacji](https://docs.docker.com/compose/compose-file/compose-file-v3/#command).

  Znany obraz `devopsdockeruh/simple-web-service` może posłużyć do uruchomienia usługi webowej — zobacz [ćwiczenie 1.10](/part-1/section-5#exercise-110).

  Utwórz docker-compose.yml i użyj go, aby uruchomić usługę tak, aby można było z niej korzystać w przeglądarce.

  Prześlij docker-compose.yml i upewnij się, że działa po prostu po uruchomieniu `docker compose up`

::::

::::caution Mandatory Exercise 2.3

  Jak już widzieliśmy, uruchomienie aplikacji z dwoma programami nie było trywialne i komendy robiły się długie.

  W [poprzedniej części](/part-1/section-6) stworzyliśmy Dockerfile zarówno dla [frontendu](https://github.com/docker-hy/material-applications/tree/main/example-frontend), jak i [backendu](https://github.com/docker-hy/material-applications/tree/main/example-backend) aplikacji przykładowej. Teraz uprość użycie do jednego pliku docker-compose.yml.

  Skonfiguruj backend i frontend z [części 1](/part-1/section-6#exercises-111-114), aby działały w Docker Compose.

  Prześlij docker-compose.yml

::::
