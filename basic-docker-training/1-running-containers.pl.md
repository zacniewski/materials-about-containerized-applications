# Ćwiczenie 1: Uruchamianie kontenerów

W tym ćwiczeniu nauczysz się podstaw pobierania obrazów, uruchamiania, zatrzymywania oraz usuwania kontenerów.

### Pobieranie obrazu

Aby uruchamiać kontenery, najpierw musimy pobrać kilka obrazów.

1. Sprawdźmy, jakie obrazy mamy obecnie na naszej maszynie, uruchamiając `docker images`:

    ```
    artur@Artur-PC:~/Desktop/PROJECTS/materials-about-containerized-applications$ docker images
    REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
    ```
    >:exclamation: **Wymagany screenshot 01!**

2. W świeżej instalacji Dockera nie powinniśmy mieć żadnych obrazów. Pobierzmy więc jeden z DockerHuba.

    Zwykle pobieramy obrazy z DockerHuba po tagu. Wyglądają one tak:

    ```
    # Official Docker images
    <repo>:<tag>
    # ubuntu:22.04
    # elasticsearch:8.15.1
    # nginx:latest

    # User or organization made images
    <user or org>/<repo>:<tag>
    # delner/ubuntu:16.04
    # bitnami/rails:latest
    ```

    Obrazów możemy też szukać poleceniem `docker search <keyword>`

    ```
    $ docker search ubuntu
    NAME                             DESCRIPTION                                     STARS     OFFICIAL
    ubuntu                           Ubuntu is a Debian-based Linux operating sys…   17252     [OK]
    ubuntu/chiselled-jre             [MOVED TO ubuntu/jre] Chiselled JRE: distrol…   3         
    ubuntu/python                    A chiselled Ubuntu rock with the Python runt…   12        
    ubuntu/mimir                     Ubuntu ROCK for Mimir, a horizontally scalab…   0         
    ubuntu/dotnet-deps               Chiselled Ubuntu for self-contained .NET & A…   16        
    ubuntu/dotnet-aspnet             Chiselled Ubuntu runtime image for ASP.NET a…   22        
    ```
    >:exclamation: **Wymagany screenshot 02!**

    Obrazy znajdziesz też w sieci na [DockerHub](https://hub.docker.com/).

    Uruchom `docker pull ubuntu:22.04`, aby pobrać obraz Ubuntu 22.04 z DockerHuba.

    ```
    $ docker pull ubuntu:22:04
    22.04: Pulling from library/ubuntu
    857cc8cb19c0: Pull complete 
    Digest: sha256:adbb90115a21969d2fe6fa7f9af4253e16d45f8d4c1e930182610c4731962658
    Status: Downloaded newer image for ubuntu:22.04
    docker.io/library/ubuntu:22.04
    ```  
    >:exclamation: **Wymagany screenshot 03!**

3. Możemy też pobrać inne wersje tego samego obrazu.

    Uruchom `docker pull ubuntu:22.10`, aby pobrać obraz Ubuntu 22.10.

    ```
    22.10: Pulling from library/ubuntu
    3ad6ea492c35: Pull complete 
    Digest: sha256:e322f4808315c387868a9135beeb11435b5b83130a8599fd7d0014452c34f489
    Status: Downloaded newer image for ubuntu:22.10
    docker.io/library/ubuntu:22.10
    ```
    >:exclamation: **Wymagany screenshot 04!**
    
    Następnie, gdy uruchomimy `docker images`, powinniśmy zobaczyć:

    ```
    REPOSITORY   TAG       IMAGE ID       CREATED         SIZE
    ubuntu       22.04     53a843653cbc   4 weeks ago     77.9MB
    ubuntu       22.10     692eb4a905c0   14 months ago   70.3MB
    ```
    >:exclamation: **Wymagany screenshot 05!**

4.  Z czasem na Twojej maszynie może zebrać się wiele obrazów, więc dobrze jest usuwać te niepotrzebne.
    Uruchom `docker rmi <IMAGE ID>`, aby usunąć obraz Ubuntu 22.10, którego nie będziemy używać.

    ```
    $ docker rmi 692eb4a905c0
    Untagged: ubuntu:22.10
    Untagged: ubuntu@sha256:e322f4808315c387868a9135beeb11435b5b83130a8599fd7d0014452c34f489
    Deleted: sha256:692eb4a905c074054e0a35d647671f0e32ed150d15b23fd7bc745cfb2fdeddbd
    Deleted: sha256:1e8bb0620308641104e68d66f65c1e51de68d7df7240b8a99a251338631c6911
    ```
    >:exclamation: **Wymagany screenshot 06!**

    Alternatywnie, obrazy można usuwać po tagu lub po częściowym ID. W poprzednim przykładzie równoważne byłyby:
     - `docker rmi 69`
     - `docker rmi ubuntu:22.10`

    Uruchomienie `docker images` powinno odzwierciedlać usunięty obraz.

    ```
    $ docker images
    REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
    ubuntu       22.04     53a843653cbc   4 weeks ago   77.9MB
    ```
    >:exclamation: **Wymagany screenshot 07!**

    Skrót do usuwania wszystkich obrazów z systemu to `docker rmi $(docker images -a -q)`
    ```
    $ docker rmi $(docker images -a -q)
    ```

### Uruchamianie kontenerów

1. Uruchommy prosty kontener z Ubuntu i wejdźmy do jego powłoki:

    ```
    $ docker run -it --name ubuntu-shell ubuntu:22.04 /bin/bash
    root@<CONTAINER_ID>:/#
    ```
    >:exclamation: **Wymagany screenshot 08!**

2. W nowej powłoce spróbuj uruchomić kilka komend, np. `ls`, `pwd`, a następnie wyjdź z kontenera komendą `exit`.

    Po wyjściu sprawdź listę kontenerów:

    ```
    $ docker ps -a
    ```
    >:exclamation: **Wymagany screenshot 09!**

3. Uruchom ponownie ten sam kontener:

    ```
    $ docker start -i ubuntu-shell
    ```
    >:exclamation: **Wymagany screenshot 10!**

4. Zatrzymaj kontener i go usuń:

    ```
    $ docker stop ubuntu-shell
    $ docker rm ubuntu-shell
    $ docker ps -a
    ```
    >:exclamation: **Wymagany screenshot 11!**

### Dodatkowe przydatne komendy

- Wyświetlenie wszystkich kontenerów (również zatrzymanych): `docker ps -a`
- Usunięcie wszystkich zatrzymanych kontenerów: `docker container prune`
- Usunięcie nieużywanych obrazów: `docker image prune`
- Usunięcie WSZYSTKIEGO, co nieużywane (z ostrożnością): `docker system prune -a`

> Uwaga: Nie zmieniaj treści poleceń i kodu. Wystarczy je skopiować i wykonać na swojej maszynie.
