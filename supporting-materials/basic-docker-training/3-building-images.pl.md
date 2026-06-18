# Ćwiczenie 3: Budowanie obrazów

W tym ćwiczeniu nauczymy się tworzyć nowy obraz Dockera.

Podobnie jak w „Changing Images”, dodamy narzędzie `ping` do obrazu `ubuntu:16.04`. Wynik obu ćwiczeń powinien być równoważny.

### Przygotowanie

Najpierw pobierz obraz `ubuntu:16.04` komendą `docker pull`. (Możesz już go mieć po poprzednim ćwiczeniu.)

```
$ docker pull ubuntu:16.04
16.04: Pulling from library/ubuntu
c62795f78da9: Pull complete 
d4fceeeb758e: Pull complete 
5c9125a401ae: Pull complete 
0062f774e994: Pull complete 

6b33fd031fac: Pull complete 
Digest: sha256:c2bbf50d276508d73dd865cda7b4ee9b5243f2648647d21e3a471dd3cc4209a0
Status: Downloaded newer image for ubuntu:16.04
$
```

Jeśli wciąż masz obraz z poprzedniego ćwiczenia „Changing Images”, usuńmy go teraz. Upewnij się, że wcześniej wykonasz `docker rm` wszystkich kontenerów opartych o ten obraz — inaczej usunięcie się nie powiedzie.

```
$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
delner/ping         latest              78ba830008a6        45 minutes ago      159MB
ubuntu              16.04               6a2f32de169d        4 days ago          117MB
$ docker rmi 78b
Untagged: delner/ping:latest
Deleted: sha256:78ba830008a61a09f9eae8ca4ead0966ff501457c23df0f635e0651253b3d0e3
Deleted: sha256:94b1207f7fb25468a3e1c16e604f8e65d9ed4df783fa057c368b635d7b086e39
$
```

### Tworzenie Dockerfile

Tak jak w „Changing Images”, zainstalujemy `ping` na bazie `ubuntu`, aby utworzyć nowy obraz. W przeciwieństwie do tamtego ćwiczenia nie będziemy uruchamiać ani modyfikować kontenerów, aby to zrobić.

Zamiast tego użyjemy `Dockerfile`. `Dockerfile` to swego rodzaju „przepis”, zawierający listę instrukcji jak zbudować nowy obraz.

1. Utwórz nowy plik o nazwie `Dockerfile` w katalogu roboczym:

    ```
    $ touch Dockerfile
    $
    ```

2. Otwórz `Dockerfile` w ulubionym edytorze.

2. Wewnątrz pliku dodamy kilka istotnych nagłówków.

    Dyrektywa `FROM` wskazuje obraz bazowy, na którym budowany będzie nowy obraz (u nas: Ubuntu).

    Dyrektywa `LABEL` dodaje etykietę do obrazu — przydatne metadane.

    Dodaj dwie linie na górze pliku:

    ```
    FROM ubuntu:16.04
    LABEL author="David Elner"
    ```

3. Następnie dodamy kilka komend modyfikujących obraz.

    Dyrektywa `RUN` uruchamia komendę wewnątrz obrazu i zapisuje wszelkie zmiany w systemie plików jako nową warstwę (commit). Typowy Dockerfile zawiera kilka instrukcji `RUN` — każda dokłada zmiany na poprzednie.

    Aby zainstalować `ping`, musimy uruchomić `apt-get update` i `apt-get install`. Najpierw dodaj `apt-get update`:

    ```
    RUN apt-get update
    ```

    Następnie dodaj `apt-get install`:

    ```
    RUN apt-get install -y iputils-ping
    ```

    Zwróć uwagę na flagę `-y`. Podczas budowania obrazów Docker komendy działają w trybie nieinteraktywnym. Zwykle `apt-get` pyta „Y/n?”, czy kontynuować. Flaga `-y` omija to pytanie, zawsze odpowiadając „Y”.

    Nasz plik powinien wyglądać tak:

    ```
    FROM ubuntu:16.04
    LABEL author="David Elner"

    RUN apt-get update

    RUN apt-get install -y iputils-ping
    ```

    I tyle — możemy budować obraz.

### Budowanie Dockerfile

Do budowania obrazów z Dockerfile używamy `docker build`. To polecenie czyta Dockerfile i uruchamia jego instrukcje, tworząc nowy obraz.

1. Zbudujmy obraz.

    Uruchomienie poniższego polecenia buduje i taguje obraz:

    ```
    $ docker build -t 'delner/ping' .
    Sending build context to Docker daemon    190kB
    Step 1/4 : FROM ubuntu:16.04
     ---> 6a2f32de169d
    Step 2/4 : LABEL author "David Elner"
     ---> Running in 50f765b29144
     ---> 27bfa513216f
    Removing intermediate container 50f765b29144
    Step 3/4 : RUN apt-get update
     ---> Running in ae8647e54bd1
    Get:1 http://security.ubuntu.com/ubuntu xenial-security InRelease [102 kB]
    Get:2 http://security.ubuntu.com/ubuntu xenial-security/universe Sources [30.0 kB]
    ...
     ---> 1f4fe5596cb1
    Removing intermediate container ae8647e54bd1
    Step 4/4 : RUN apt-get install -y iputils-ping
     ---> Running in e6a838d41cef
    Reading package lists...
    Building dependency tree...
    ...
     ---> 918648f00b92
    Removing intermediate container e6a838d41cef
    Successfully built 918648f00b92
    $
    ```

    Użycie `.` w argumentach jest tu istotne. `docker build` domyślnie szuka pliku o nazwie `Dockerfile`. Podając `.`, mówimy Dockerowi, aby użył `Dockerfile` z bieżącego katalogu. Gdyby plik nazywał się inaczej, należałoby to zmienić w komendzie.

    Zwróć uwagę na „kroki” w wyjściu. Każda dyrektywa w Dockerfile odpowiada krokowi; po zakończeniu kroku powstaje commit. Dlaczego to ważne?

    Docker układa warstwy (commity) jedna na drugiej, jak cebulę. Dzięki temu obrazy są mniejsze, a przy ponownym budowaniu można ponownie używać niezmienionych warstw, co przyspiesza buildy.

    Zobaczymy cache w akcji, jeśli po prostu uruchomimy to samo polecenie ponownie:

    ```
    $ docker build -t 'delner/ping' .
    Sending build context to Docker daemon    191kB
    Step 1/4 : FROM ubuntu:16.04
     ---> 6a2f32de169d
    Step 2/4 : LABEL author "David Elner"
     ---> Using cache
     ---> 27bfa513216f
    Step 3/4 : RUN apt-get update
     ---> Using cache
     ---> 1f4fe5596cb1
    Step 4/4 : RUN apt-get install -y iputils-ping
     ---> Using cache
     ---> 918648f00b92
    Successfully built 918648f00b92
    $
    ```

    Po `docker images` zobaczymy nowo zbudowany obraz.

    ```
    $ docker images
    REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
    delner/ping         latest              918648f00b92        9 minutes ago       159MB
    ubuntu              16.04               6a2f32de169d        4 days ago          117MB
    ```

### Optymalizacja Dockerfile

Nowy obraz ma `159MB`, a bazowy `117MB`. To spora różnica jak na instalację kilku narzędzi — zajmuje więcej miejsca i wydłuża push/pull.

Dlaczego aż tyle? Sekret tkwi w `RUN`. Jak wspomniano, po `RUN` commitowane są wszystkie zmiany w systemie plików — także logi i dane tymczasowe, których w obrazie nie potrzebujemy.

W naszym przypadku `apt-get` generuje sporo „śmieci”. Musimy nieco zmodyfikować `RUN`.

Zacznijmy od czyszczenia po instalacji. Dodaj na dole Dockerfile:

```
RUN apt-get clean \
    && cd /var/lib/apt/lists && rm -fr *Release* *Sources* *Packages* \
    && truncate -s 0 /var/log/*log
```

Ponowne `build` daje...

```
$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
delner/ping         latest              912bc1c7c059        4 seconds ago       159MB
ubuntu              16.04               6a2f32de169d        4 days ago          117MB
$
```

...brak poprawy? O co chodzi?

Ponieważ warstwy są układane jedna na drugiej, jeśli „śmieci” powstały w poprzedniej warstwie, sprzątanie w kolejnej nie zmniejszy ich historii — rozmiar zostaje.

„Śmieci” pochodzą z `apt-get update`, które zostawia listy pakietów. Najprościej scalić powiązane `RUN` w jedno.

Przepisany Dockerfile powinien wyglądać tak:

```
FROM ubuntu:16.04
LABEL author="David Elner"

RUN apt-get update \
    && apt-get install -y iputils-ping \
    && apt-get clean \
    && cd /var/lib/apt/lists && rm -fr *Release* *Sources* *Packages* \
    && truncate -s 0 /var/log/*log
```

Po ponownym `build` obrazy wyglądają tak:

```
$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
delner/ping         latest              622e555950e0        12 seconds ago      121MB
ubuntu              16.04               6a2f32de169d        4 days ago          117MB
$
```

Teraz nowy obraz jest większy tylko o 4MB — duża poprawa.

### Inne dyrektywy Dockerfile

Istnieje [wiele innych przydatnych dyrektyw](https://docs.docker.com/engine/reference/builder/) dostępnych w Dockerfile.

Kilka ważnych:

 - `COPY`: Kopiuje pliki z hosta do obrazu Dockera.
 - `WORKDIR`: Ustala domyślny katalog pracy dla komend.
 - `CMD`: Ustala domyślne polecenie do uruchomienia.
 - `ENV`: Ustala domyślną zmienną środowiskową.
 - `EXPOSE`: Domyślne wystawienie portu.
 - `ARG`: Argument czasu budowy (dla bardziej konfigurowalnych buildów).

Ponieważ nasz Dockerfile służy do `ping`, dodajmy `ENV` i `CMD`.

```
FROM ubuntu:16.04
LABEL author="David Elner"

ENV PING_TARGET "google.com"

RUN apt-get update \
    && apt-get install -y iputils-ping \
    && apt-get clean \
    && cd /var/lib/apt/lists && rm -fr *Release* *Sources* *Packages* \
    && truncate -s 0 /var/log/*log

CMD ["sh", "-c", "ping $PING_TARGET"]
```

Te nowe dyrektywy oznaczają, że po uruchomieniu `docker run -it delner/ping` obraz automatycznie wykona `ping google.com`.

```
$ docker run -it delner/ping
PING google.com (172.217.10.46) 56(84) bytes of data.
64 bytes from lga34s13-in-f14.1e100.net (172.217.10.46): icmp_seq=1 ttl=37 time=0.300 ms
64 bytes from lga34s13-in-f14.1e100.net (172.217.10.46): icmp_seq=2 ttl=37 time=0.373 ms
64 bytes from lga34s13-in-f14.1e100.net (172.217.10.46): icmp_seq=3 ttl=37 time=0.378 ms
^C
--- google.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2078ms
rtt min/avg/max/mdev = 0.300/0.350/0.378/0.038 ms
$
```

### Więcej o Dockerfile

Większość obrazów w świecie Dockera budowana jest z Dockerfile, a przeglądanie Dockerfile z ulubionych repozytoriów to świetny sposób, aby zrozumieć jak działają i jak ulepszyć własne obrazy. Szukaj ich na DockerHub i GitHub!

# KONIEC ĆWICZENIA 3
