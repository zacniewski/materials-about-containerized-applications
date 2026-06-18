# Laboratorium 1: Pierwsze kroki z Dockerem (6 godz.)

## Cel laboratorium
Poznanie podstaw Dockera: instalacja, uruchamianie kontenerów, pobieranie obrazów, podstawowe komendy CLI.

## Wymagania wstępne
- Zainstalowany Docker Engine lub Docker Desktop
- Konto na [Docker Hub](https://hub.docker.com/)
- Terminal / wiersz poleceń

---

## Część 1: Weryfikacja instalacji (30 min)

### Ćwiczenie 1.1: Sprawdzenie wersji Docker

```bash
# Sprawdź wersję Docker
docker --version

# Szczegółowe informacje
docker version

# Informacje o systemie Docker
docker info
```

> 📸 **Wymagany screenshot 1**: Wynik komendy `docker version`

### Ćwiczenie 1.2: Hello World

```bash
# Uruchom pierwszy kontener
docker run hello-world
```

Przeanalizuj wynik:
1. Docker nie znalazł obrazu lokalnie
2. Pobrał obraz z Docker Hub
3. Utworzył kontener z tego obrazu
4. Uruchomił kontener, który wypisał komunikat
5. Kontener zakończył działanie

> 📸 **Wymagany screenshot 2**: Wynik komendy `docker run hello-world`

### Ćwiczenie 1.3: Sprawdzenie pobranych obrazów i kontenerów

```bash
# Lista pobranych obrazów
docker images

# Lista wszystkich kontenerów (w tym zatrzymanych)
docker ps -a
```

**Pytanie:** Dlaczego kontener `hello-world` ma status `Exited`?

---

## Część 2: Pobieranie i zarządzanie obrazami (45 min)

### Ćwiczenie 2.1: Pobieranie obrazów

```bash
# Pobierz obraz Ubuntu
docker pull ubuntu:22.04

# Pobierz obraz Alpine (bardzo mały)
docker pull alpine:3.19

# Pobierz obraz Nginx
docker pull nginx:alpine

# Sprawdź listę obrazów
docker images
```

> 📸 **Wymagany screenshot 3**: Lista pobranych obrazów (`docker images`)

### Ćwiczenie 2.2: Porównanie rozmiarów obrazów

```bash
# Porównaj rozmiary
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

**Pytanie:** Który obraz jest najmniejszy? Dlaczego?

### Ćwiczenie 2.3: Wyszukiwanie obrazów

```bash
# Wyszukaj obrazy Python na Docker Hub
docker search python --limit 5

# Wyszukaj obrazy z co najmniej 100 gwiazdkami
docker search --filter stars=100 python
```

### Ćwiczenie 2.4: Inspekcja obrazu

```bash
# Szczegóły obrazu
docker image inspect ubuntu:22.04

# Historia warstw
docker history ubuntu:22.04

# Tylko rozmiar
docker image inspect ubuntu:22.04 --format='{{.Size}}'
```

### Ćwiczenie 2.5: Usuwanie obrazów

```bash
# Usuń obraz hello-world (najpierw usuń kontener)
docker rm $(docker ps -aq --filter ancestor=hello-world)
docker rmi hello-world

# Sprawdź
docker images
```

---

## Część 3: Uruchamianie kontenerów (90 min)

### Ćwiczenie 3.1: Tryb interaktywny

```bash
# Uruchom Ubuntu interaktywnie
docker run -it ubuntu:22.04 bash

# Wewnątrz kontenera:
cat /etc/os-release
whoami
hostname
ls /
pwd

# Zainstaluj pakiet
apt-get update && apt-get install -y curl
curl --version

# Wyjdź z kontenera
exit
```

> 📸 **Wymagany screenshot 4**: Sesja interaktywna w kontenerze Ubuntu

**Pytanie:** Co się stanie z zainstalowanym `curl` po wyjściu z kontenera?

### Ćwiczenie 3.2: Tryb detached (w tle)

```bash
# Uruchom Nginx w tle
docker run -d --name moj-nginx nginx:alpine

# Sprawdź działające kontenery
docker ps

# Sprawdź logi
docker logs moj-nginx

# Sprawdź szczegóły
docker inspect moj-nginx
```

> 📸 **Wymagany screenshot 5**: Wynik `docker ps` z działającym kontenerem nginx

### Ćwiczenie 3.3: Mapowanie portów

```bash
# Zatrzymaj poprzedni kontener
docker stop moj-nginx
docker rm moj-nginx

# Uruchom z mapowaniem portów
docker run -d --name moj-nginx -p 8080:80 nginx:alpine

# Sprawdź
docker ps

# Otwórz w przeglądarce: http://localhost:8080
# Lub użyj curl:
curl http://localhost:8080
```

> 📸 **Wymagany screenshot 6**: Strona powitalna Nginx w przeglądarce (localhost:8080)

### Ćwiczenie 3.4: Zmienne środowiskowe

```bash
# Uruchom kontener ze zmiennymi środowiskowymi
docker run -d --name moj-mysql \
  -e MYSQL_ROOT_PASSWORD=mojehaslo \
  -e MYSQL_DATABASE=testdb \
  -p 3306:3306 \
  mysql:8

# Sprawdź logi (poczekaj na inicjalizację)
docker logs -f moj-mysql
# Ctrl+C aby przerwać śledzenie logów

# Połącz się z bazą
docker exec -it moj-mysql mysql -u root -pmojehaslo -e "SHOW DATABASES;"
```

> 📸 **Wymagany screenshot 7**: Lista baz danych MySQL w kontenerze

### Ćwiczenie 3.5: Automatyczne usuwanie kontenera

```bash
# Kontener usunie się po zakończeniu
docker run --rm ubuntu:22.04 echo "Ten kontener się sam usunie"

# Sprawdź — nie powinno go być
docker ps -a | grep "sam usunie"

# Interaktywny z auto-usuwaniem
docker run --rm -it alpine:3.19 sh -c "echo 'Alpine Linux'; cat /etc/os-release"
```

### Ćwiczenie 3.6: Nadawanie nazw kontenerom

```bash
# Bez nazwy — Docker generuje losową
docker run -d nginx:alpine
docker ps  # zobacz losową nazwę

# Z nazwą
docker run -d --name web-server nginx:alpine
docker ps  # zobacz nazwę "web-server"

# Sprzątanie
docker stop $(docker ps -q)
docker rm $(docker ps -aq)
```

---

## Część 4: Zarządzanie kontenerami (60 min)

### Ćwiczenie 4.1: Start, stop, restart

```bash
# Uruchom kontener
docker run -d --name test-nginx -p 8080:80 nginx:alpine

# Zatrzymaj
docker stop test-nginx

# Sprawdź status
docker ps -a

# Uruchom ponownie
docker start test-nginx

# Restart
docker restart test-nginx

# Sprawdź
curl http://localhost:8080
```

### Ćwiczenie 4.2: Wykonywanie komend w kontenerze (exec)

```bash
# Uruchom kontener
docker run -d --name moj-ubuntu ubuntu:22.04 sleep 3600

# Wykonaj komendę
docker exec moj-ubuntu cat /etc/os-release

# Interaktywna sesja
docker exec -it moj-ubuntu bash

# Wewnątrz:
apt-get update && apt-get install -y procps
ps aux
exit

# Sprawdź procesy z zewnątrz
docker top moj-ubuntu
```

> 📸 **Wymagany screenshot 8**: Wynik `docker exec` i `docker top`

### Ćwiczenie 4.3: Kopiowanie plików (docker cp)

```bash
# Utwórz plik na hoście
echo "Witaj z hosta!" > plik-z-hosta.txt

# Skopiuj do kontenera
docker cp plik-z-hosta.txt moj-ubuntu:/tmp/

# Sprawdź w kontenerze
docker exec moj-ubuntu cat /tmp/plik-z-hosta.txt

# Utwórz plik w kontenerze
docker exec moj-ubuntu bash -c "echo 'Witaj z kontenera!' > /tmp/plik-z-kontenera.txt"

# Skopiuj z kontenera na hosta
docker cp moj-ubuntu:/tmp/plik-z-kontenera.txt ./

# Sprawdź na hoście
cat plik-z-kontenera.txt
```

> 📸 **Wymagany screenshot 9**: Kopiowanie plików między hostem a kontenerem

### Ćwiczenie 4.4: Logi kontenerów

```bash
# Uruchom kontener generujący logi
docker run -d --name logger ubuntu:22.04 \
  bash -c "while true; do echo \"Log: \$(date)\"; sleep 2; done"

# Wszystkie logi
docker logs logger

# Ostatnie 5 linii
docker logs --tail 5 logger

# Śledzenie na żywo
docker logs -f logger
# Ctrl+C aby przerwać

# Z timestampami
docker logs -t --tail 3 logger
```

### Ćwiczenie 4.5: Statystyki zasobów

```bash
# Uruchom kilka kontenerów
docker run -d --name web1 nginx:alpine
docker run -d --name web2 nginx:alpine

# Statystyki na żywo
docker stats
# Ctrl+C aby przerwać

# Jednorazowy snapshot
docker stats --no-stream

# Formatowanie
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

> 📸 **Wymagany screenshot 10**: Wynik `docker stats`

---

## Część 5: Inspekcja i diagnostyka (45 min)

### Ćwiczenie 5.1: docker inspect

```bash
# Uruchom kontener
docker run -d --name inspect-test -p 9090:80 nginx:alpine

# Pełna inspekcja
docker inspect inspect-test

# Adres IP
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' inspect-test

# Stan kontenera
docker inspect -f '{{.State.Status}}' inspect-test

# Mapowanie portów
docker inspect -f '{{json .NetworkSettings.Ports}}' inspect-test

# Zmienne środowiskowe
docker inspect -f '{{json .Config.Env}}' inspect-test
```

> 📸 **Wymagany screenshot 11**: Adres IP kontenera z `docker inspect`

### Ćwiczenie 5.2: docker diff

```bash
# Uruchom kontener i zmodyfikuj go
docker run -it --name diff-test ubuntu:22.04 bash

# Wewnątrz kontenera:
touch /nowy-plik.txt
echo "test" > /tmp/dane.txt
rm /etc/hostname
exit

# Sprawdź zmiany
docker diff diff-test
```

**Pytanie:** Co oznaczają litery A, C, D w wyniku `docker diff`?

### Ćwiczenie 5.3: docker port

```bash
docker run -d --name port-test -p 8081:80 -p 8443:443 nginx:alpine

# Sprawdź mapowanie portów
docker port port-test
docker port port-test 80
```

---

## Część 6: Sprzątanie (30 min)

### Ćwiczenie 6.1: Usuwanie kontenerów i obrazów

```bash
# Zatrzymaj wszystkie kontenery
docker stop $(docker ps -q)

# Usuń wszystkie zatrzymane kontenery
docker container prune -f

# Sprawdź zajętość dysku
docker system df

# Usuń nieużywane obrazy
docker image prune -f

# Usuń WSZYSTKO nieużywane
docker system prune -f

# Sprawdź ponownie
docker system df
```

> 📸 **Wymagany screenshot 12**: Wynik `docker system df` przed i po czyszczeniu

---

## Zadania do samodzielnego wykonania

### Zadanie 1: Serwer HTTP
Uruchom kontener z serwerem HTTP Apache (`httpd:alpine`) na porcie 8888. Otwórz stronę w przeglądarce.

### Zadanie 2: Baza PostgreSQL
Uruchom kontener PostgreSQL z hasłem `student123` i bazą danych `uczelnia`. Połącz się z bazą i utwórz tabelę.

### Zadanie 3: Eksploracja kontenera
Uruchom kontener `python:3.11-slim` interaktywnie. Sprawdź wersję Pythona, zainstaluj bibliotekę `requests` i napisz prosty skrypt.

### Zadanie 4: Porównanie obrazów
Pobierz trzy warianty obrazu Python: `python:3.11`, `python:3.11-slim`, `python:3.11-alpine`. Porównaj ich rozmiary i zawartość.

---

## Podsumowanie

Po ukończeniu tego laboratorium powinieneś umieć:
- ✅ Sprawdzić instalację Docker i wersję
- ✅ Pobierać obrazy z Docker Hub
- ✅ Uruchamiać kontenery w trybie interaktywnym i detached
- ✅ Mapować porty między hostem a kontenerem
- ✅ Wykonywać komendy w działającym kontenerze
- ✅ Kopiować pliki między hostem a kontenerem
- ✅ Przeglądać logi i statystyki kontenerów
- ✅ Inspekcjonować kontenery (`docker inspect`)
- ✅ Czyścić nieużywane zasoby Docker
