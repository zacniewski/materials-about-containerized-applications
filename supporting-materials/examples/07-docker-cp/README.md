# Kopiowanie plików między hostem a kontenerem (docker cp)

Ten folder zawiera krótką instrukcję i gotowe przykłady użycia polecenia `docker cp` do kopiowania plików:
- z hosta do kontenera,
- z kontenera na hosta,
- z użyciem nazw/ID kontenerów, również w projektach uruchamianych przez Docker Compose.

Polecenie `docker cp` działa podobnie do `cp`/`tar` i nie wymaga działających wolumenów. Dobrze sprawdza się do jednorazowego przeniesienia plików, np. logów czy artefaktów builda.

## Szybki skrót składni

- Host ➜ Kontener:
  ```bash
  docker cp <SRC_PATH> <CONTAINER>:<DEST_PATH>
  ```
- Kontener ➜ Host:
  ```bash
  docker cp <CONTAINER>:<SRC_PATH> <DEST_PATH>
  ```

Wskazówki:
- Jeśli `SRC_PATH` lub `DEST_PATH` to katalog i kończy się `/`, kopiowana jest zawartość katalogu; bez `/` kopiowany jest katalog jako całość.
- Możesz używać nazwy kontenera albo jego ID.

---

## Przygotowanie (szybki kontener do ćwiczeń)
Aby przetestować przykłady, uruchom lekki kontener (np. Alpine) „na długo”:
```bash
docker run -d --name cp-demo alpine:3.20 sleep 1d
```
Upewnij się, że działa:
```bash
docker ps --filter name=cp-demo
```

---

## Host ➜ Kontener (przykłady)

1) Skopiuj pojedynczy plik do katalogu domowego roota w kontenerze:
```bash
echo "Hello from host" > host-file.txt

docker cp host-file.txt cp-demo:/root/
```
Weryfikacja w kontenerze:
```bash
docker exec -it cp-demo sh -c 'ls -l /root && cat /root/host-file.txt'
```

2) Skopiuj katalog wraz z zawartością do `/opt/app` (katalog zostanie utworzony):
```bash
mkdir -p example-dir && echo "a" > example-dir/a.txt && echo "b" > example-dir/b.txt

docker cp example-dir cp-demo:/opt/app
# wynik: /opt/app/example-dir/...
```

3) Skopiuj zawartość katalogu (zwróć uwagę na końcowy slash):
```bash
docker cp example-dir/ cp-demo:/opt/app/only-contents/
# wynik: pliki a.txt, b.txt trafią bezpośrednio do /opt/app/only-contents/
```

4) Skopiuj i jednocześnie zmień nazwę pliku docelowego:
```bash
docker cp host-file.txt cp-demo:/root/renamed-in-container.txt
```

---

## Kontener ➜ Host (przykłady)

1) Skopiuj pojedynczy plik z kontenera na hosta:
```bash
docker cp cp-demo:/root/host-file.txt ./from-container.txt
ls -l ./from-container.txt && cat ./from-container.txt
```

2) Skopiuj katalog (zachowanie analogiczne do `cp`):
```bash
docker cp cp-demo:/opt/app ./backup-app
# wynik: ./backup-app/app/... (lub ./backup-app/example-dir/... jeśli kopiowałeś poprzednie przykłady)
```

3) Skopiuj wyłącznie zawartość katalogu (z końcowym `/`):
```bash
docker cp cp-demo:/opt/app/ ./backup-app-contents/
```

Uwaga o właścicielach/permach: tryby plików są zazwyczaj zachowane, natomiast UID/GID na hoście mogą zostać przypisane do użytkownika uruchamiającego `docker` (zależnie od platformy). Jeśli musisz ściśle zachować właścicieli/ACL, rozważ wariant z `tar` poniżej.

---

## Zaawansowane: zachowanie właścicieli i praw (tar przez `docker exec`)

Kiedy wymagasz jak najwierniejszego odwzorowania własności i praw, użyj `tar` po obu stronach:

- Kontener ➜ Host (zachowanie właścicieli i trybów):
```bash
# -p w tarze stara się zachować prawa/właścicieli (może wymagać sudo na hoście)
docker exec cp-demo tar -C / -cf - opt/app \
  | sudo tar -C ./backup-app-exact -xpf -
```

- Host ➜ Kontener (zachowanie praw wewnątrz kontenera):
```bash
# Tworzymy archiwum i wypakowujemy je w kontenerze pod /opt/app
sudo tar -C ./example-dir -cf - . \
  | docker exec -i cp-demo tar -C /opt/app -xpf -
```

---

## Użycie z Docker Compose

`docker compose` (v2) uruchamia kontenery o nazwach bazujących na nazwie projektu i serwisu, np. `myproj_web_1`. Aby skopiować plik, podaj faktyczną nazwę kontenera albo użyj `docker compose ps`:

1) Znajdź nazwę kontenera serwisu:
```bash
docker compose ps
```

2) Użyj `docker cp` z tą nazwą:
```bash
# przykład: kopiowanie .env do serwisu web
CONTAINER=$(docker compose ps -q web)
docker cp .env "$CONTAINER":/app/.env
```

Uwaga: Istnieje również podkomenda `docker compose cp` (w nowszych wersjach Compose). Jeśli jest dostępna w Twojej wersji, możesz pisać:
```bash
# równoważne, gdy komenda jest dostępna
docker compose cp .env web:/app/.env
```
Jeżeli otrzymasz błąd „unknown command: cp”, Twoja wersja Compose tej komendy nie posiada — wtedy użyj klasycznego `docker cp` z nazwą/ID kontenera.

---

## Kopiowanie między dwoma kontenerami (bezpośrednio)
Najprościej: skopiuj na hosta, potem do drugiego kontenera. Dla zachowania praw:
```bash
docker exec src-container tar -C / -cf - path/in/src \
  | docker exec -i dst-container tar -C /dest -xpf -
```

---

## Sprzątanie

Gdy skończysz próby z `cp-demo`:
```bash
docker rm -f cp-demo
rm -rf example-dir backup-app backup-app-contents backup-app-exact from-container.txt host-file.txt
```

---

## Najczęstsze problemy i wskazówki
- „No such container/path”: sprawdź nazwę kontenera (`docker ps`, `docker compose ps`) i ścieżkę.
- Uprawnienia: kopiując do ścieżek systemowych (np. `/usr/local/bin`), kontener może wymagać uprawnień roota. W razie potrzeby uruchom kontener z użytkownikiem root lub kopiuj do katalogu, gdzie masz prawa.
- Windows/PowerShell: pamiętaj o cytowaniu ścieżek i zmiennych (`"${PWD}"`).
- W Compose: jeśli masz wiele replik serwisu (scale), każdy replica-kontener ma inną nazwę — wskaż właściwy.
