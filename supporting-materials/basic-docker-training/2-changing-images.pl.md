# Ćwiczenie 2: Zmiana obrazów

W tym ćwiczeniu nauczymy się modyfikować istniejący obraz Dockera i zapisywać go jako nowy.

Aby to zrobić, zmodyfikujemy obraz `ubuntu:16.04`, aby zawierał narzędzie `ping`.

### Przygotowanie środowiska

Najpierw pobierz obraz `ubuntu:16.04` poleceniem `docker pull`. (Możesz już go mieć, jeśli ukończyłeś poprzednie ćwiczenie.)

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

### Modyfikowanie obrazu

Uruchomimy obraz w nowym kontenerze i zainstalujemy narzędzie `ping`.

1. Najpierw uruchom kontener z `/bin/bash`:

    ```
    $ docker run -it ubuntu:16.04 /bin/bash
    root@786b94c53c6d:/#
    ```

2. Spróbuj uruchomić `ping` w terminalu.

    ```
    root@786b94c53c6d:/# ping google.com
    bash: ping: command not found
    root@786b94c53c6d:/#
    ```

    Komenda nie istnieje. Obraz Ubuntu dla Dockera zawiera jedynie niezbędne minimum oprogramowania do działania kontenera. To nic — możemy zainstalować `ping`.

2. Najpierw zaktualizujemy listę oprogramowania.

    W środowiskach linuksowych opartych na Debianie (takich jak Ubuntu) nowe oprogramowanie instalujemy menedżerem pakietów `apt`. Dla osób z doświadczeniem na Macach jest to odpowiednik `homebrew`.

    Domyślnie, aby zmniejszyć rozmiar obrazu, obraz Ubuntu nie ma listy dostępnych pakietów. Musimy ją zaktualizować:

    ```
    root@786b94c53c6d:/# apt-get update
    Get:1 http://security.ubuntu.com/ubuntu xenial-security InRelease [102 kB]
    Get:2 http://security.ubuntu.com/ubuntu xenial-security/universe Sources [29.6 kB]   
    Get:3 http://archive.ubuntu.com/ubuntu xenial InRelease [247 kB]    
    Get:4 http://security.ubuntu.com/ubuntu xenial-security/main amd64 Packages [308 kB]
    Get:5 http://security.ubuntu.com/ubuntu xenial-security/restricted amd64 Packages [12.8 kB]
    Get:6 http://security.ubuntu.com/ubuntu xenial-security/universe amd64 Packages [132 kB]   
    Get:7 http://security.ubuntu.com/ubuntu xenial-security/multiverse amd64 Packages [2936 B]
    Get:8 http://archive.ubuntu.com/ubuntu xenial-updates InRelease [102 kB]                 
    Get:9 http://archive.ubuntu.com/ubuntu xenial-backports InRelease [102 kB]
    Get:10 http://archive.ubuntu.com/ubuntu xenial/universe Sources [9802 kB]
    Get:11 http://archive.ubuntu.com/ubuntu xenial/main amd64 Packages [1558 kB]
    Get:12 http://archive.ubuntu.com/ubuntu xenial/restricted amd64 Packages [14.1 kB]
    Get:13 http://archive.ubuntu.com/ubuntu xenial/universe amd64 Packages [9827 kB]
    Get:14 http://archive.ubuntu.com/ubuntu xenial/multiverse amd64 Packages [176 kB]
    Get:15 http://archive.ubuntu.com/ubuntu xenial-updates/universe Sources [186 kB]
    Get:16 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 Packages [652 kB]
    Get:17 http://archive.ubuntu.com/ubuntu xenial-updates/restricted amd64 Packages [13.2 kB]
    Get:18 http://archive.ubuntu.com/ubuntu xenial-updates/universe amd64 Packages [577 kB]
    Get:19 http://archive.ubuntu.com/ubuntu xenial-updates/multiverse amd64 Packages [9809 B]
    Get:20 http://archive.ubuntu.com/ubuntu xenial-backports/main amd64 Packages [4929 B]
    Get:21 http://archive.ubuntu.com/ubuntu xenial-backports/universe amd64 Packages [2567 B]
    Fetched 23.9 MB in 5s (4409 kB/s)                
    Reading package lists... Done
    root@786b94c53c6d:/#
    ```

3. Teraz możemy zainstalować `ping`.

    Wywołaj `apt-get install iputils-ping`, aby zainstalować pakiet zawierający `ping`:

    ```
    root@786b94c53c6d:/# apt-get install iputils-ping
    Reading package lists... Done
    Building dependency tree       
    Reading state information... Done
    The following additional packages will be installed:
      libffi6 libgmp10 libgnutls-openssl27 libgnutls30 libhogweed4 libidn11 libnettle6 libp11-kit0 libtasn1-6
    Suggested packages:
      gnutls-bin
    The following NEW packages will be installed:
      iputils-ping libffi6 libgmp10 libgnutls-openssl27 libgnutls30 libhogweed4 libidn11 libnettle6 libp11-kit0 libtasn1-6
    0 upgraded, 10 newly installed, 0 to remove and 0 not upgraded.
    Need to get 1303 kB of archives.
    After this operation, 3778 kB of additional disk space will be used.
    Do you want to continue? [Y/n] Y
    Get:1 http://archive.ubuntu.com/ubuntu xenial/main amd64 libgmp10 amd64 2:6.1.0+dfsg-2 [240 kB]
    Get:2 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 libnettle6 amd64 3.2-1ubuntu0.16.04.1 [93.5 kB]
    Get:3 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 libhogweed4 amd64 3.2-1ubuntu0.16.04.1 [136 kB]
    Get:4 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 libidn11 amd64 1.32-3ubuntu1.1 [45.6 kB]
    Get:5 http://archive.ubuntu.com/ubuntu xenial/main amd64 libffi6 amd64 3.2.1-4 [17.8 kB]
    Get:6 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 libp11-kit0 amd64 0.23.2-5~ubuntu16.04.1 [105 kB]
    Get:7 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 libtasn1-6 amd64 4.7-3ubuntu0.16.04.1 [43.2 kB]
    Get:8 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 libgnutls30 amd64 3.4.10-4ubuntu1.2 [547 kB]
    Get:9 http://archive.ubuntu.com/ubuntu xenial-updates/main amd64 libgnutls-openssl27 amd64 3.4.10-4ubuntu1.2 [21.9 kB]
    Get:10 http://archive.ubuntu.com/ubuntu xenial/main amd64 iputils-ping amd64 3:20121221-5ubuntu2 [52.7 kB]
    Fetched 1303 kB in 0s (1767 kB/s)   
    debconf: delaying package configuration, since apt-utils is not installed
    Selecting previously unselected package libgmp10:amd64.
    (Reading database ... 4764 files and directories currently installed.)
    ```

4. Zatwierdzenie zmian do nowego obrazu.

    Otwórz nową sesję na hoście i znajdź ID działającego kontenera (`docker ps`), następnie zatwierdź obraz:

    ```
    $ docker commit <CONTAINER_ID> youruser/ping:latest
    $ docker images
    ```

5. Przetestuj nowy obraz uruchamiając kontener i sprawdzając `ping`.

    ```
    $ docker run -it youruser/ping /bin/bash
    root@...:/# ping google.com
    ```

> Wskazówka: Upewnij się, że nie zmieniasz treści poleceń i kodu — pozostaw je dokładnie tak, jak w oryginale.
