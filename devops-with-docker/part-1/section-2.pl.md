---
title: "Uruchamianie i zatrzymywanie kontenerów"
---

Następnie zaczniemy używać bardziej przydatnego obrazu niż hello-world. Możemy uruchomić Ubuntu po prostu poleceniem `docker run ubuntu`.

```console
$ docker run ubuntu
  Unable to find image 'ubuntu:latest' locally
  latest: Pulling from library/ubuntu
  83ee3a23efb7: Pull complete
  db98fc6f11f0: Pull complete
  f611acd52c6c: Pull complete
  Digest: sha256:703218c0465075f4425e58fac086e09e1de5c340b12976ab9eb8ad26615c3715
  Status: Downloaded newer image for ubuntu:latest
```

Antyklimatyczne, bo w zasadzie nic się nie stało. Obraz został pobrany, uruchomiony i to by było na tyle. Właściwie próbowaliśmy otworzyć powłokę, ale do interakcji musimy dodać kilka flag. `-t` utworzy [tty](https://itsfoss.com/what-is-tty-in-linux/).

```console
$ docker run -t ubuntu
  root@f83969ce2cd1:/#
```

Jesteśmy teraz w kontenerze, ale jeśli wpiszemy `ls` i wciśniemy enter... nic się nie stanie. Nasz terminal nie wysyła danych do kontenera. Flaga `-i` nakaże przekazywać STDIN do kontenera. Jeśli utkniesz w tamtym terminalu, możesz po prostu zatrzymać kontener.

```console
$ docker run -it ubuntu
  root@2eb70ecf5789:/# ls
  bin  boot  dev  etc  home  lib  lib32  lib64  libx32  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
```

Świetnie! Znamy już przynajmniej 3 użyteczne flagi. `-i` (interactive), `-t` (tty) i `-d` (detached).

Dorzućmy kilka kolejnych i uruchommy kontener w tle:

```console
$ docker run -d -it --name looper ubuntu sh -c 'while true; do date; sleep 1; done'
```

::::tip Quotes

Jeśli korzystasz z wiersza poleceń (Windows), musisz użyć podwójnych cudzysłowów wokół skryptu, tj. `docker run -d -it --name looper ubuntu sh -c "while true; do date; sleep 1; done"`. Cudzysłowy pojedyncze lub podwójne mogą prześladować Cię później w trakcie kursu.

::::

- Pierwsza część, `docker run -d`. Powinna być już znajoma — uruchomienie kontenera w trybie odłączonym.

- Następnie `-it` to skrót od `-i` i `-t`. Również znajome — `-it` pozwala wchodzić w interakcję z kontenerem poprzez wiersz poleceń.

- Ponieważ uruchomiliśmy kontener z `--name looper`, możemy się do niego łatwo odwoływać.

- Obraz to `ubuntu`, a to, co po nim następuje, to polecenie przekazane do kontenera.

Aby sprawdzić, czy działa, uruchom `docker container ls`

Śledźmy (`-f`) wyjście logów:

```console
$ docker logs -f looper
  Thu Mar  1 15:51:29 UTC 2023
  Thu Mar  1 15:51:30 UTC 2023
  Thu Mar  1 15:51:31 UTC 2023
  ...
```

Przetestujmy wstrzymanie looper bez wychodzenia lub zatrzymywania. W innym terminalu uruchom `docker pause looper`. Zwróć uwagę, że wypisywanie logów w pierwszym terminalu się zatrzymało. Aby wznowić, użyj `docker unpause looper`.

Pozostaw logi otwarte i dołącz do działającego kontenera z drugiego terminala używając 'attach':

```console
$ docker attach looper
  Thu Mar  1 15:54:38 UTC 2023
  Thu Mar  1 15:54:39 UTC 2023
  ...
```

Masz teraz logi procesu (STDOUT) w dwóch terminalach. Teraz naciśnij control+c w oknie, które jest dołączone. Kontener zostaje zatrzymany, ponieważ proces przestaje działać.

Jeśli chcemy dołączyć do kontenera, upewniając się, że nie zamkniemy go z drugiego terminala, możemy określić, aby nie podłączać STDIN za pomocą opcji `--no-stdin`. Uruchommy zatrzymany kontener poleceniem `docker start looper` i dołączmy do niego z `--no-stdin`.

Następnie spróbuj control+c.

```console
$ docker start looper

$ docker attach --no-stdin looper
  Thu Mar  1 15:56:11 UTC 2023
  Thu Mar  1 15:56:12 UTC 2023
  ^C
```

Kontener będzie dalej działał. Control+c spowoduje teraz tylko rozłączenie ze STDOUT.

### Uruchamianie procesów w kontenerze za pomocą docker exec ###

Często napotykamy sytuacje, w których musimy wykonać polecenia w działającym kontenerze. Można to zrobić za pomocą polecenia `docker exec`.

Możemy np. wylistować wszystkie pliki w domyślnym katalogu kontenera (czyli w root):

```console
$ docker exec looper ls -la
total 56
drwxr-xr-x   1 root root 4096 Mar  6 10:24 .
drwxr-xr-x   1 root root 4096 Mar  6 10:24 ..
-rwxr-xr-x   1 root root    0 Mar  6 10:24 .dockerenv
lrwxrwxrwx   1 root root    7 Feb 27 16:01 bin -> usr/bin
drwxr-xr-x   2 root root 4096 Apr 18  2022 boot
drwxr-xr-x   5 root root  360 Mar  6 10:24 dev
drwxr-xr-x   1 root root 4096 Mar  6 10:24 etc
drwxr-xr-x   2 root root 4096 Apr 18  2022 home
lrwxrwxrwx   1 root root    7 Feb 27 16:01 lib -> usr/lib
drwxr-xr-x   2 root root 4096 Feb 27 16:01 media
drwxr-xr-x   2 root root 4096 Feb 27 16:01 mnt
drwxr-xr-x   2 root root 4096 Feb 27 16:01 opt
dr-xr-xr-x 293 root root    0 Mar  6 10:24 proc
drwx------   2 root root 4096 Feb 27 16:08 root
drwxr-xr-x   5 root root 4096 Feb 27 16:08 run
lrwxrwxrwx   1 root root    8 Feb 27 16:01 sbin -> usr/sbin
drwxr-xr-x   2 root root 4096 Feb 27 16:01 srv
dr-xr-xr-x  13 root root    0 Mar  6 10:24 sys
drwxrwxrwt   2 root root 4096 Feb 27 16:08 tmp
drwxr-xr-x  11 root root 4096 Feb 27 16:01 usr
drwxr-xr-x  11 root root 4096 Feb 27 16:08 var
```

Możemy uruchomić powłokę Bash w kontenerze w trybie interaktywnym, a następnie wykonywać dowolne polecenia w tej sesji Bash:

```console
$ docker exec -it looper bash

  root@2a49df3ba735:/# ps aux

  USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
  root         1  0.2  0.0   2612  1512 pts/0    Ss+  12:36   0:00 sh -c while true; do date; sleep 1; done
  root        64  1.5  0.0   4112  3460 pts/1    Ss   12:36   0:00 bash
  root        79  0.0  0.0   2512   584 pts/0    S+   12:36   0:00 sleep 1
  root        80  0.0  0.0   5900  2844 pts/1    R+   12:36   0:00 ps aux
```

Z listy `ps aux` widać, że nasz proces `bash` otrzymał PID (process ID) 64.

Będąc już w kontenerze, zachowuje się on tak, jak można by oczekiwać po Ubuntu i możemy wyjść z kontenera poleceniem `exit`, a następnie ubić lub zatrzymać kontener.

Nasz looper nie zatrzyma się po sygnale SIGTERM wysłanym przez polecenie stop. Aby zakończyć proces, stop po okresie karencji wysyła SIGKILL. W tym przypadku po prostu szybciej jest użyć kill.

```console
$ docker kill looper
$ docker rm looper
```

Wykonanie powyższych dwóch poleceń jest zasadniczo równoważne z uruchomieniem `docker rm --force looper`

Uruchommy kolejny proces z `-it` i dodajmy `--rm`, aby został automatycznie usunięty po zakończeniu. `--rm` zapewnia, że nie zostają po nas śmieci w postaci kontenerów. Oznacza to także, że nie można użyć `docker start`, aby uruchomić kontener po jego zakończeniu.

```console
$ docker run -d --rm -it --name looper-it ubuntu sh -c 'while true; do date; sleep 1; done'
```

Teraz dołączmy do kontenera i naciśnijmy control+p, control+q, aby odłączyć się od STDOUT.

```console
$ docker attach looper-it

  Mon Jan 15 19:50:42 UTC 2018
  Mon Jan 15 19:50:43 UTC 2018
  ^P^Qread escape sequence
```

Gdybyśmy zamiast tego użyli ctrl+c, wysłałoby to sygnał kill, a następnie usunęło kontener, ponieważ określiliśmy `--rm` w poleceniu `docker run`.

### Ćwiczenie 1.3

::::info Exercise 1.3: Secret message

Skoro się rozgrzaliśmy, czas wejść do kontenera w trakcie jego działania!

Obraz `devopsdockeruh/simple-web-service:ubuntu` uruchomi kontener, który zapisuje logi do pliku. Wejdź do działającego kontenera i użyj `tail -f ./text.log`, aby śledzić logi. Co 10 sekund zegar wyśle Ci „sekretną wiadomość”.

Prześlij sekretne hasło i użyte polecenia w odpowiedzi.

::::

## Niedopasowana platforma hosta

Jeśli pracujesz na Macu M1/M2, bardzo prawdopodobne, że zobaczysz poniższe ostrzeżenie podczas uruchamiania obrazu _devopsdockeruh/simple-web-service:ubuntu_:

```console
WARNING: The requested image's platform (linux/amd64) does not match the detected 
host platform (linux/arm64/v8) and no specific platform was requested
```

Mimo tego ostrzeżenia możesz uruchomić kontener. Ostrzeżenie w zasadzie mówi, w czym problem — obraz używa innej architektury procesora niż Twoja maszyna.

Obraz może zostać użyty, ponieważ Docker Desktop for Mac domyślnie stosuje emulator, gdy architektura procesora obrazu nie odpowiada architekturze hosta. Warto jednak zauważyć, że wykonywanie z emulacją może być mniej wydajne niż uruchamianie obrazu na zgodnej, natywnej architekturze procesora.

Gdy uruchamiasz np. `docker run ubuntu`, nie dostajesz ostrzeżenia — dlaczego? Wiele popularnych obrazów to tzw. [obrazy wieloplatformowe](https://docs.docker.com/build/building/multi-platform/), co oznacza, że jeden obraz zawiera warianty dla różnych architektur. Kiedy zamierzasz pobrać lub uruchomić taki obraz, Docker wykrywa architekturę hosta i dostarcza właściwy typ obrazu.

## Ubuntu w kontenerze to po prostu... Ubuntu

Kontener uruchomiony z obrazem Ubuntu działa podobnie jak zwykłe Ubuntu:

```console
$ docker run -it ubuntu
root@881a1d4ecff2:/# ls
bin   dev  home  media  opt   root  sbin  sys  usr
boot  etc  lib   mnt    proc  run   srv   tmp  var
root@881a1d4ecff2:/# ps
  PID TTY          TIME CMD
    1 pts/0    00:00:00 bash
   13 pts/0    00:00:00 ps
root@881a1d4ecff2:/# date
Wed Mar  1 12:08:24 UTC 2023
root@881a1d4ecff2:/#
```

Taki obraz jak Ubuntu zawiera już przyzwoity zestaw narzędzi, ale czasem akurat tego jednego nam brakuje w standardowej dystrybucji. Załóżmy, że chcemy edytować pliki w kontenerze. Stary dobry edytor [Nano](https://www.nano-editor.org/) idealnie się nada. Możemy go zainstalować w kontenerze przy użyciu [apt-get](https://help.ubuntu.com/community/AptGet/Howto):

```console
$ docker run -it ubuntu
root@881a1d4ecff2:/# apt-get update
root@881a1d4ecff2:/# apt-get -y install nano
root@881a1d4ecff2:/# cd tmp/
root@881a1d4ecff2:/tmp# nano temp_file.txt
```

Jak widać, instalacja programu lub biblioteki w kontenerze przebiega tak samo, jak w „zwykłym” Ubuntu. Zasadnicza różnica jest taka, że instalacja Nano nie jest trwała — jeśli usuniemy nasz kontener, wszystko znika. Wkrótce zobaczymy, jak uzyskać trwalsze rozwiązanie, budując obrazy idealnie dopasowane do naszych celów.

## Ćwiczenie 1.4

::::info Exercise 1.4: Missing dependencies

Uruchom obraz Ubuntu z procesem `sh -c 'while true; do echo "Input website:"; read website; echo "Searching.."; sleep 1; curl http://$website; done'`

Jeśli jesteś na Windowsie, będziesz chciał zamienić `'` i `"` miejscami: `sh -c "while true; do echo 'Input website:'; read website; echo 'Searching..'; sleep 1; curl http://$website; done"`.

Zauważysz, że brakuje kilku elementów wymaganych do poprawnego działania. Przypomnij sobie, jakich flag użyć, aby kontener faktycznie czekał na dane wejściowe.

> Zwróć też uwagę, że curl NIE jest jeszcze zainstalowany w kontenerze. Będziesz musiał zainstalować go z wnętrza kontenera.

Przetestuj podanie `helsinki.fi` jako wejścia do aplikacji. Powinna odpowiedzieć mniej więcej tak:

```html
<html>
  <head>
    <title>301 Moved Permanently</title>
  </head>

  <body>
    <h1>Moved Permanently</h1>
    <p>The document has moved <a href="http://www.helsinki.fi/">here</a>.</p>
  </body>
</html>
```

Tym razem zwróć polecenie, którego użyłeś do uruchomienia procesu, oraz polecenia, których użyłeś do naprawy wynikłych problemów.

**Wskazówka**: aby zainstalować brakujące zależności, możesz uruchomić nowy proces z `docker exec`.

* To ćwiczenie ma wiele rozwiązań; jeśli curl dla helsinki.fi działa, to znaczy, że jest ukończone. Czy potrafisz wymyślić inne (sprytne) rozwiązania?

::::
