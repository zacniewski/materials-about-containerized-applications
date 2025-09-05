---
title: "Definiowanie warunków startowych kontenera"
---

Następnie zaczniemy zmierzać w stronę bardziej znaczącego obrazu. [yt-dlp](https://github.com/yt-dlp/yt-dlp) to program pobierający filmy z YouTube i [Imgur](https://imgur.com/). Dodajmy go do obrazu — ale tym razem zmienimy proces. Zamiast dotychczasowego podejścia, w którym dopisujemy rzeczy do Dockerfile i liczymy, że zadziałają, wypróbujmy inną metodę. Otwórzmy interaktywną sesję i przetestujmy wszystko, zanim „zapiszemy” to w Dockerfile.

Postępując zgodnie z [instrukcją instalacji yt-dlp](https://github.com/yt-dlp/yt-dlp/wiki/Installation), zaczniemy tak:

```console
$ docker run -it ubuntu:22.04

  root@8c587232a608:/# curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
  bash: curl: command not found
```

...i, jak już wiemy, curl nie jest zainstalowany — doinstalujmy `curl` poprzez `apt-get`.

```console
$ apt-get update && apt-get install -y curl
$ curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
```

W pewnym momencie mogłeś zauważyć, że _sudo_ też nie jest zainstalowane, ale nie jest nam potrzebne, bo jesteśmy _root_.

Teraz nadamy uprawnienia i uruchomimy pobrany plik wykonywalny:

```console
$ chmod a+rx /usr/local/bin/yt-dlp
$ yt-dlp
/usr/bin/env: 'python3': No such file or directory
```

OK, [dokumentacja](https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#dependencies) wspomina, że do uruchomienia yt-dlp potrzebny jest Python 3.8 lub nowszy. Zainstalujmy więc:

```console
$ apt-get install -y python3
```

Możemy spróbować uruchomić aplikację ponownie:

```console
$ yt-dlp

  Usage: yt-dlp [OPTIONS] URL [URL...]

  yt-dlp: error: You must provide at least one URL.
  Type yt-dlp --help to see a list of all options.
```

Działa, musimy tylko podać URL.

Skoro wiemy już dokładnie, czego potrzebujemy. Startując FROM ubuntu:22.04, dodamy powyższe kroki do naszego `Dockerfile`. Zawsze warto trzymać wiersze najbardziej podatne na zmiany na dole — dodając instrukcje na końcu, możemy zachować zcache’owane warstwy. To wygodna praktyka, by przyspieszyć build, gdy w Dockerfile występują czasochłonne operacje, jak pobieranie. Dodaliśmy też WORKDIR, który zapewni, że filmy będą pobierane do tego katalogu.

```dockerfile
FROM ubuntu:22.04

WORKDIR /mydir

RUN apt-get update && apt-get install -y curl python3
RUN curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
RUN chmod a+x /usr/local/bin/yt-dlp

CMD ["/usr/local/bin/yt-dlp"]
```

Nadpisaliśmy też polecenie obrazu (ustawione w obrazie bazowym) na _yt-dlp_. To jeszcze nie zadziała idealnie — zobaczmy dlaczego.

Zbudujmy teraz Dockerfile jako obraz `yt-dlp` i uruchommy go:

```console
$ docker build -t yt-dlp .
  ...

$ docker run yt-dlp

  Usage: yt-dlp [OPTIONS] URL [URL...]

  yt-dlp: error: You must provide at least one URL.
  Type yt-dlp --help to see a list of all options.
```

Jak dotąd dobrze. Naturalnym sposobem użycia byłoby podanie URL-a jako argumentu, ale niestety to nie działa:

```console
$ docker run yt-dlp https://www.youtube.com/watch?v=uTZSILGTskA

  docker: Error response from daemon: failed to create task for container: failed to create shim task: OCI runtime create failed: runc create failed: unable to start container process: exec: "https://www.youtube.com/watch?v=uTZSILGTskA": stat https://www.youtube.com/watch?v=uTZSILGTskA: no such file or directory: unknown.
  ERRO[0000] error waiting for container: context canceled
```

Jak już wiemy, _argument, który podaliśmy, zastępuje polecenie_ czyli `CMD`:

```console
$ docker run -it yt-dlp ps
  PID TTY          TIME CMD
    1 pts/0    00:00:00 ps
$ docker run -it yt-dlp ls -l
total 0
$ docker run -it yt-dlp pwd
/mydir
```

Potrzebujemy sposobu, by mieć coś _przed_ poleceniem. Na szczęście mamy: możemy użyć [ENTRYPOINT](https://docs.docker.com/engine/reference/builder/#entrypoint), aby zdefiniować główny wykonywalny program, a Docker połączy nasze argumenty uruchomienia z nim.

```dockerfile
FROM ubuntu:22.04

WORKDIR /mydir

RUN apt-get update && apt-get install -y curl python3
RUN curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
RUN chmod a+x /usr/local/bin/yt-dlp

# Replacing CMD with ENTRYPOINT
ENTRYPOINT ["/usr/local/bin/yt-dlp"]
```

I teraz działa tak, jak powinno:

```console
$ docker build -t yt-dlp .
$ docker run yt-dlp https://www.youtube.com/watch?v=XsqlHHTGQrw
[youtube] Extracting URL:https://www.youtube.com/watch?v=XsqlHHTGQrw
[youtube] uTZSILGTskA: Downloading webpage
[youtube] uTZSILGTskA: Downloading ios player API JSON
[youtube] uTZSILGTskA: Downloading android player API JSON
[youtube] uTZSILGTskA: Downloading m3u8 information
[info] uTZSILGTskA: Downloading 1 format(s): 22
[download] Destination: Master’s Programme in Computer Science ｜ University of Helsinki [XsqlHHTGQrw].mp4
[download] 100% of    6.29MiB in 00:00:00 at 9.95MiB/s
```

Z _ENTRYPOINT_ `docker run` wykonał teraz połączone `/usr/local/bin/yt-dlp https://www.youtube.com/watch?v=uTZSILGTskA` wewnątrz kontenera!

`ENTRYPOINT` vs `CMD` potrafi mylić — w poprawnie skonfigurowanym obrazie, jak nasz yt-dlp, polecenie reprezentuje listę argumentów dla entrypointu. Domyślnie entrypoint w Dockerze to `/bin/sh -c` i to jest użyte, jeśli nie ustawiono własnego. Dlatego podanie ścieżki do skryptu jako CMD działa: podajesz plik jako parametr do `/bin/sh -c`.

Jeśli obraz definiuje oba, wówczas CMD służy do podania [domyślnych argumentów](https://docs.docker.com/engine/reference/builder/#cmd) dla entrypointu. Dodajmy teraz CMD do Dockerfile:

```dockerfile
FROM ubuntu:22.04

WORKDIR /mydir

RUN apt-get update && apt-get install -y curl python3
RUN curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
RUN chmod a+x /usr/local/bin/yt-dlp

ENTRYPOINT ["/usr/local/bin/yt-dlp"]

# define a default argument
CMD ["https://www.youtube.com/watch?v=Aa55RKWZxxI"]
```

Teraz (po ponownym zbudowaniu) obraz można uruchomić bez argumentów, aby pobrać film zdefiniowany w CMD:

```console
$ docker run yt-dlp

  youtube] Extracting URL: https://www.youtube.com/watch?v=Aa55RKWZxxI
  [youtube] Aa55RKWZxxI: Downloading webpage
  [youtube] Aa55RKWZxxI: Downloading ios player API JSON
  [youtube] Aa55RKWZxxI: Downloading android player API JSON
  ...
  [download] 100% of    5.60MiB in 00:00:00 at 7.91MiB/s
```

Argument zdefiniowany przez CMD można _nadpisać_, podając go w wierszu poleceń:

```console
$ docker run yt-dlp https://www.youtube.com/watch?v=DptFY_MszQs
[youtube] Extracting URL: https://www.youtube.com/watch?v=DptFY_MszQs
[youtube] DptFY_MszQs: Downloading webpage
[youtube] DptFY_MszQs: Downloading ios player API JSON
[youtube] DptFY_MszQs: Downloading android player API JSON
[youtube] DptFY_MszQs: Downloading player 9bb09009
[youtube] DptFY_MszQs: Downloading m3u8 information
[info] DptFY_MszQs: Downloading 1 format(s): 22
[download] Destination: Welcome to Kumpula campus! ｜ University of Helsinki [DptFY_MszQs].mp4
[download] 100% of   29.92MiB in 00:00:04 at 7.10MiB/s
```

Oprócz tego istnieją dwa sposoby ustawiania ENTRYPOINT i CMD: forma **exec** i forma **shell**. Używaliśmy formy exec, gdzie uruchamiane jest samo polecenie. W formie shell polecenie jest owijane przez `/bin/sh -c` — przydatne, gdy trzeba ewaluować zmienne środowiskowe w poleceniu, jak `$MYSQL_PASSWORD` itp.

W formie shell polecenie podaje się jako string bez nawiasów. W formie exec polecenie i jego argumenty są listą (w nawiasach) — porównanie poniżej:

| Dockerfile                                                 | Resulting command                                |
| ---------------------------------------------------------- | ------------------------------------------------ |
| ENTRYPOINT /bin/ping -c 3 <br /> CMD localhost             | /bin/sh -c '/bin/ping -c 3' /bin/sh -c localhost |
| ENTRYPOINT ["/bin/ping","-c","3"] <br /> CMD localhost     | /bin/ping -c 3 /bin/sh -c localhost              |
| ENTRYPOINT /bin/ping -c 3 <br /> CMD ["localhost"]         | /bin/sh -c '/bin/ping -c 3' localhost            |
| ENTRYPOINT ["/bin/ping","-c","3"] <br /> CMD ["localhost"] | /bin/ping -c 3 localhost                         |

Ponieważ polecenie na końcu `docker run` będzie CMD, chcemy użyć ENTRYPOINT do określenia, co uruchomić, a CMD — który „command/argument” (w naszym przypadku URL) przekazać.

**W większości przypadków** możemy ignorować ENTRYPOINT przy budowaniu obrazów i używać tylko CMD. Na przykład obraz Ubuntu domyślnie ustawia ENTRYPOINT na bash, więc nie musimy się tym martwić. Daje nam to wygodę łatwego nadpisywania CMD, np. poprzez bash, aby wejść do kontenera.

Możemy sprawdzić, jak robią to inne projekty. Spróbujmy Pythona:

```console
$ docker pull python:3.11
...
$ docker run -it python:3.11
Python 3.11.8 (main, Feb 13 2024, 09:03:56) [GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> print("Hello, World!")
Hello, World!
>>> exit()

$ docker run -it python:3.11 --version
  docker: Error response from daemon: OCI runtime create failed: container_linux.go:370: starting container process caused: exec: "--version": executable file not found in $PATH: unknown.

$ docker run -it python:3.11 bash
  root@1b7b99ae2f40:/#

```

Z tego eksperymentu dowiedzieliśmy się, że ENTRYPOINT jest ustawiony na coś innego niż Python, ale CMD to Python i możemy go nadpisać, tutaj bashem. Gdyby ENTRYPOINT był Pythonem, moglibyśmy uruchomić `--version`. Możemy stworzyć własny obraz do użytku osobistego, jak w poprzednim ćwiczeniu, z nowym Dockerfile:

```dockerfile
FROM python:3.11
ENTRYPOINT ["python3"]
CMD ["--help"]
```

Wynikiem jest obraz, który ma Pythona jako ENTRYPOINT i możesz dodawać komendy na końcu, np. --version, aby zobaczyć wersję. Bez nadpisywania komendy wypisze pomoc.

Mamy teraz dwa problemy z projektem yt-dlp:

- Poważny: Pobrane pliki zostają w kontenerze

- Mniej istotny: Proces budowania kontenera tworzy wiele warstw, co zwiększa rozmiar obrazu

Najpierw naprawimy problem poważny. Problem mniejszy omówimy w części 3.

Sprawdzając `docker container ls -a`, możemy zobaczyć wszystkie dotychczasowe uruchomienia. Filtrowując listę tak:

```console
$ docker container ls -a --last 3

  CONTAINER ID        IMAGE               COMMAND                   CREATED                  STATUS                          PORTS               NAMES
  be9fdbcafb23        yt-dlp          "/usr/local/bin/yout…"    Less than a second ago   Exited (0) About a minute ago                       determined_elion
  b61e4029f997        f2210c2591a1        "/bin/sh -c \"/usr/lo…"   Less than a second ago   Exited (2) About a minute ago                       vigorous_bardeen
  326bb4f5af1e        f2210c2591a1        "/bin/sh -c \"/usr/lo…"   About a minute ago       Exited (2) 3 minutes ago                            hardcore_carson
```

Widzimy, że ostatni kontener to `be9fdbcafb23`, czyli dla nas ludzi `determined_elion`.

```console
$ docker diff determined_elion
  C /root
  A /root/.cache
  A /root/.cache/yt-dlp
  A /root/.cache/yt-dlp/youtube-nsig
  A /root/.cache/yt-dlp/youtube-nsig/9bb09009.json
  C /mydir
  A /mydir/Welcome to Kumpula campus! ｜ University of Helsinki [DptFY_MszQs].mp4
```

Spróbujmy komendy `docker cp`, aby skopiować plik z kontenera na maszynę hosta. Ponieważ nazwa pliku zawiera spacje, użyjmy cudzysłowów.

```console
$ docker cp "determined_elion://mydir/Welcome to Kumpula campus! ｜ University of Helsinki [DptFY_MszQs].mp4" .
```

Plik mamy już lokalnie i możemy go odtworzyć, jeśli mamy odpowiedni odtwarzacz. Niestety użycie `docker cp` nie jest właściwym sposobem naprawy naszego problemu. W następnej sekcji to ulepszymy.

## Ulepszony curler

Dzięki `ENTRYPOINT` możemy sprawić, by curler z [Ćwiczenia 1.7.](/part-1/section-3#exercises-17---18) był bardziej elastyczny.

Zmień skrypt tak, by pierwszy argument traktował jako wejście:

```bash
#!/bin/bash

echo "Searching..";
sleep 1;
curl http://$1;
```

I zmień CMD na ENTRYPOINT w formacie `["./script.sh"]`. Teraz możemy uruchomić

```bash
$ docker build . -t curler-v2
$ docker run curler-v2 helsinki.fi

  Searching..
    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                   Dload  Upload   Total   Spent    Left  Speed
  100   232  100   232    0     0  13647      0 --:--:-- --:--:-- --:--:-- 13647
  <!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
  <html><head>
  <title>301 Moved Permanently</title>
  </head><body>
  <h1>Moved Permanently</h1>
  <p>The document has moved <a href="https://www.helsinki.fi/">here</a>.</p>
  </body></html>
```
