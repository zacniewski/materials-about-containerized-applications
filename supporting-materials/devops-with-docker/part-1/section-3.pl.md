---
title: "Dogłębne spojrzenie na obrazy"
---

Obrazy (images) są podstawowymi klockami budulcowymi dla kontenerów i innych obrazów. „Konteneryzując” aplikację, dążysz do utworzenia obrazu.

Poznając, czym są obrazy i jak je tworzyć, będziesz gotów, aby zacząć wykorzystywać kontenery we własnych projektach.

## Skąd biorą się obrazy?

Gdy uruchamiasz polecenie takie jak `docker run hello-world`, Docker automatycznie przeszuka [Docker Hub](https://hub.docker.com/), jeśli obraz nie znajduje się lokalnie.

Oznacza to, że możemy pobrać i uruchomić dowolny publiczny obraz z serwerów Dockera. Na przykład, jeśli chcielibyśmy uruchomić instancję bazy danych PostgreSQL, moglibyśmy po prostu wykonać `docker run postgres`, co pobierze i uruchomi [https://hub.docker.com/_/postgres/](https://hub.docker.com/_/postgres/).

Możemy wyszukiwać obrazy w Docker Hub komendą `docker search`. Spróbuj wykonać `docker search hello-world`.

Wynik wyszukiwania zwraca wiele pozycji i wypisuje nazwę obrazu, krótki opis, liczbę gwiazdek oraz statusy „official” i „automated”.

```console
$ docker search hello-world

  NAME                         DESCRIPTION    STARS   OFFICIAL   AUTOMATED
  hello-world                  Hello World!…  1988     [OK]
  kitematic/hello-world-nginx  A light-weig…  153
  tutum/hello-world            Image to tes…  90                 [OK]
  ...
```

Przyjrzyjmy się liście.

Pierwszy wynik, `hello-world`, to obraz oficjalny. [Obrazy oficjalne](https://docs.docker.com/docker-hub/official_images/) są kuratorowane i przeglądane przez Docker, Inc. i zwykle aktywnie utrzymywane przez autorów. Budowane są z repozytoriów w organizacji [docker-library](https://github.com/docker-library).

W wynikach wyszukiwania CLI rozpoznasz obraz oficjalny po „[OK]” w kolumnie „OFFICIAL” oraz po tym, że nazwa obrazu nie ma prefiksu (czyli organizacji/użytkownika). W interfejsie Docker Hub strona takiego obrazu zamiast użytkownika lub organizacji pokaże „Docker Official Images” jako repozytorium. Zobacz np. [stronę `hello-world`](https://hub.docker.com/_/hello-world/).

Trzeci wynik, `tutum/hello-world`, jest oznaczony jako „automated”. Oznacza to, że obraz jest [budowany automatycznie](https://docs.docker.com/docker-hub/builds/) z repozytorium źródłowego. Na jego [stronie Docker Hub](https://hub.docker.com/r/tutum/hello-world/) zobaczysz historię „Builds” oraz link do „Source Repository” (w tym przypadku do GitHuba), z którego Docker Hub buduje obraz.

Drugi wynik, `kitematic/hello-world-nginx`, nie jest ani oficjalny, ani automatyczny. Nie wiemy, z czego ten obraz został zbudowany, ponieważ jego [strona w Docker Hub](https://hub.docker.com/r/kitematic/hello-world-nginx/) nie zawiera żadnych linków do repozytoriów. Jedyną informacją jest to, że obraz ma 9 lat. Nawet jeśli sekcja „Overview” zawierałaby linki do repozytorium, nie mielibyśmy gwarancji, że opublikowany obraz został zbudowany z tego źródła.

Istnieją też inne rejestry Docker konkurujące z Docker Hub, takie jak [Quay](https://quay.io/). Domyślnie `docker search` przeszukuje tylko Docker Hub, ale aby przeszukać inny rejestr, możesz dodać adres rejestru przed frazą, np. `docker search quay.io/hello`. Alternatywnie możesz używać stron www rejestru. Zobacz stronę [obrazu `nordstrom/hello-world` na Quay](https://quay.io/repository/nordstrom/hello-world). Strona pokazuje komendę do pobrania obrazu, co ujawnia, że możemy pobierać obrazy także z innych hostów niż Docker Hub:

`docker pull quay.io/nordstrom/hello-world`

Zatem jeśli nazwa hosta (tutaj: `quay.io`) jest pominięta, domyślnie pobierze z Docker Hub.

UWAGA: Próba wykonania powyższej komendy może zakończyć się błędem manifestu, ponieważ domyślny tag latest nie jest dostępny dla obrazu quay.io/nordstrom/hello-world. Podanie właściwego tagu spowoduje poprawne pobranie, np.
`docker pull quay.io/nordstrom/hello-world:2.0`

## Szczegółowe spojrzenie na obraz

Wróćmy do obrazu bardziej istotnego niż „hello-world” — obrazu Ubuntu, jednego z najczęściej używanych jako baza dla własnych obrazów.

Pobierzmy Ubuntu i spójrzmy na pierwsze linie:

```console
$ docker pull ubuntu
  Using default tag: latest
  latest: Pulling from library/ubuntu
```

Ponieważ nie podaliśmy tagu, Docker domyślnie użył `latest`, który zwykle oznacza najnowszy obraz zarejestrowany w rejestrze. **Jednakże** w tym przypadku [README repozytorium](https://hub.docker.com/_/ubuntu) mówi, że tag `ubuntu:latest` wskazuje na „najnowsze LTS”, ponieważ to wersja rekomendowana do ogólnego użytku.

Obrazy mogą mieć tagi, aby zapisywać różne wersje tego samego obrazu. Tag definiujesz, dodając `:<tag>` po nazwie obrazu.

[Strona Ubuntu w Docker Hub](https://hub.docker.com/r/library/ubuntu/tags/) ujawnia, że istnieje tag 22.04, który obiecuje obraz bazujący na Ubuntu 22.04. Pobierzmy i ten:

```console
$ docker pull ubuntu:22.04

  22.04: Pulling from library/ubuntu
  c2ca09a1934b: Downloading [============================================>      ]  34.25MB/38.64MB
  d6c3619d2153: Download complete
  0efe07335a04: Download complete
  6b1bb01b3a3b: Download complete
  43a98c187399: Download complete
```

Obrazy składają się z różnych warstw pobieranych równolegle, aby przyspieszyć pobieranie. Warstwy mają także inne znaczenia — porozmawiamy o nich w części 3.

Możemy również lokalnie tagować obrazy dla wygody, np. `docker tag ubuntu:22.04 ubuntu:jammy_jellyfish` tworzy tag `ubuntu:jammy_jellyfish`, który wskazuje na `ubuntu:22.04`.

Tagowanie jest też sposobem na „zmianę nazwy” obrazów. Uruchom `docker tag ubuntu:22.04 fav_distro:jammy_jellyfish` i sprawdź `docker image ls`, aby zobaczyć efekt.

Podsumowując, nazwa obrazu może składać się z 3 części plus tag. Zwykle: `registry/organisation/image:tag`. Może być jednak tak krótka jak `ubuntu` — wtedy rejestr domyślnie to Docker Hub, organizacja to _library_, a tag to _latest_. Organizacją może być także użytkownik, ale mówienie „organizacja” bywa czytelniejsze.

## Ćwiczenia 1.5 - 1.6

::::info Exercise 1.5: Sizes of images

W [Ćwiczeniu 1.3](/part-1/section-2#exercise-13) użyliśmy `devopsdockeruh/simple-web-service:ubuntu`.

Oto ta sama aplikacja, ale zamiast Ubuntu używa [Alpine Linux](https://www.alpinelinux.org/): `devopsdockeruh/simple-web-service:alpine`.

Pobierz oba obrazy i porównaj ich rozmiary.
Wejdź do kontenera Alpine i upewnij się, że funkcjonalność „sekretnej wiadomości” jest taka sama. Wersja Alpine nie ma `bash`, ale ma `sh`, bardziej podstawową powłokę.

::::

::::info Exercise 1.6: Hello Docker Hub

Uruchom `docker run -it devopsdockeruh/pull_exercise`.

Polecenie będzie czekało na dane wejściowe.

Przejrzyj [Docker Hub](https://hub.docker.com/), aby znaleźć dokumentację i Dockerfile użyty do stworzenia obrazu.

Przeczytaj Dockerfile i/lub dokumentację, aby dowiedzieć się, jakie wejście spowoduje, że aplikacja odpowie „sekretną wiadomością”.

Prześlij sekretną wiadomość i użyte polecenia w odpowiedzi.

::::

## Budowanie obrazów

Wreszcie zbudujemy własne obrazy i porozmawiamy o [`Dockerfile`](https://docs.docker.com/engine/reference/builder/) i o tym, dlaczego to świetne rozwiązanie.

Dockerfile to po prostu plik zawierający instrukcje budowania obrazu. Określasz, co powinno znaleźć się w obrazie, używając różnych dyrektyw. Poznamy dobre praktyki, tworząc taki plik.

Weźmy najprostszy program i najpierw go skonteneryzujmy. Oto skrypt „hello.sh”

**hello.sh**

```sh
#!/bin/sh

echo "Hello, docker!"
```

Najpierw sprawdźmy, czy w ogóle działa. Utwórz plik, nadaj uprawnienia do uruchamiania i uruchom:

```console
$ chmod +x hello.sh

$ ./hello.sh
  Hello, docker!
```

* Jeśli używasz Windows, możesz pominąć te dwa kroki i dodać chmod +x hello.sh do Dockerfile.

A teraz stwórzmy z niego obraz. Musimy utworzyć `Dockerfile`, który zadeklaruje wszystkie wymagane zależności. Przynajmniej potrzebuje czegoś, co uruchomi skrypty shell. Wybierzemy [Alpine](https://www.alpinelinux.org/), małą dystrybucję Linuksa często używaną do tworzenia niewielkich obrazów.

Mimo że używamy tutaj Alpine, w ćwiczeniach możesz używać Ubuntu. Obrazy Ubuntu domyślnie zawierają więcej narzędzi do debugowania problemów. W części 3 porozmawiamy więcej o tym, dlaczego małe obrazy są ważne.

Wybierzemy dokładnie, której wersji obrazu chcemy użyć. Gwarantuje to, że przypadkiem nie zaktualizujemy się do wersji z niekompatybilnymi zmianami i że wiemy, które obrazy wymagają aktualizacji, gdy pojawią się znane luki bezpieczeństwa w starych obrazach.

Utwórz teraz plik o nazwie „Dockerfile” i umieść w nim następujące instrukcje:

**Dockerfile**

```Dockerfile
# Start from the alpine image that is smaller but no fancy tools
FROM alpine:3.19

# Use /usr/src/app as our workdir. The following instructions will be executed in this location.
WORKDIR /usr/src/app

# Copy the hello.sh file from this directory to /usr/src/app/ creating /usr/src/app/hello.sh
COPY hello.sh .

# Alternatively, if we skipped chmod earlier, we can add execution permissions during the build.
# RUN chmod +x hello.sh

# When running docker run the command will be ./hello.sh
CMD ./hello.sh
```

Świetnie! Możemy użyć polecenia [docker build](https://docs.docker.com/engine/reference/commandline/build/), aby zamienić Dockerfile w obraz.

Domyślnie `docker build` szuka pliku o nazwie Dockerfile. Teraz możemy uruchomić `docker build` z instrukcją, skąd budować (`.`) i nadać nazwę (`-t <name>`):

```console
$ docker build . -t hello-docker
 => [internal] load build definition from Dockerfile                                                                                                                                              0.0s
 => => transferring dockerfile: 478B                                                                                                                                                              0.0s
 => [internal] load metadata for docker.io/library/alpine:3.19                                                                                                                                    2.1s
 => [auth] library/alpine:pull token for registry-1.docker.io                                                                                                                                     0.0s
 => [internal] load .dockerignore                                                                                                                                                                 0.0s
 => => transferring context: 2B                                                                                                                                                                   0.0s
 => [1/3] FROM docker.io/library/alpine:3.19@sha256:c5b1261d6d3e43071626931fc004f70149baeba2c8ec672bd4f27761f8e1ad6b                                                                              0.0s
 => [internal] load build context                                                                                                                                                                 0.0s
 => => transferring context: 68B                                                                                                                                                                  0.0s
 => [2/3] WORKDIR /usr/src/app                                                                                                                                                                    0.0s
 => [3/3] COPY hello.sh .                                                                                                                                                                         0.0s
 => exporting to image                                                                                                                                                                            0.0s
 => => exporting layers                                                                                                                                                                           0.0s
 => => writing image sha256:5f8f5d7445f34b0bcfaaa4d685a068cdccc1ed79e65068337a3a228c79ea69c8                                                                                                      0.0s
 => => naming to docker.io/library/hello-docker
```

Upewnijmy się, że obraz istnieje:

```console
$ docker image ls
  REPOSITORY            TAG          IMAGE ID       CREATED         SIZE
  hello-docker          latest       5f8f5d7445f3   4 minutes ago   7.73MB
```

::::tip Permission denied

Jeśli teraz otrzymujesz "/bin/sh: ./hello.sh: Permission denied", to dlatego, że wcześniej pominięto `chmod +x hello.sh`. Możesz po prostu odkomentować instrukcję RUN między COPY a CMD.

::::

::::tip not found

Jeśli teraz otrzymujesz "/bin/sh: ./hello.sh: not found" i używasz Windows, to może być tak, że Windows domyślnie używa końców linii [CRLF](https://www.cs.toronto.edu/~krueger/csc209h/tut/line-endings.html). Unix, w naszym przypadku Alpine, używa tylko LF, co sprawia, że kopiowany `hello.sh` staje się niepoprawnym skryptem w fazie build. Aby obejść problem, zmień końce linii na LF przed uruchomieniem `docker build`.

::::

Teraz uruchomienie aplikacji jest tak proste jak `docker run hello-docker`. Spróbuj!

Podczas buildu widzimy w output, że są trzy kroki: [1/3], [2/3] i [3/3]. Kroki te reprezentują [warstwy](https://docs.docker.com/build/guide/layers/) obrazu — każdy krok to nowa warstwa na bazowym obrazie (w naszym przypadku alpine:3.19).

Warstwy pełnią wiele funkcji. Często staramy się ograniczać ich liczbę, aby oszczędzać miejsce, ale warstwy mogą też działać jako cache podczas build. Jeśli edytujemy tylko ostatnie linie Dockerfile, polecenie build może wystartować od poprzedniej warstwy i przejść bezpośrednio do części, która się zmieniła. COPY automatycznie wykrywa zmiany w plikach, więc jeśli zmienimy hello.sh, uruchomi się od kroku 3/3, pomijając 1 i 2. To pozwala tworzyć szybsze potoki build. O optymalizacji porozmawiamy szerzej w części 3.

Możliwe jest też ręczne utworzenie nowych warstw ponad obrazem. Utwórzmy teraz plik `additional.txt` i skopiujmy go do kontenera.

Potrzebujemy dwóch terminali, które nazwijmy 1 i 2 w poniższych listingach. Zacznijmy od uruchomienia obrazu:

```console
# do this in terminal 1
$ docker run -it hello-docker sh
/usr/src/app #
```

Jesteśmy teraz wewnątrz kontenera. Zastąpiliśmy wcześniej zdefiniowane CMD poleceniem `sh` i użyliśmy -i oraz -t, by móc z nim wchodzić w interakcję.

W drugim terminalu skopiujemy plik do kontenera:

```console
# do this in terminal 2
$ docker ps
  CONTAINER ID   IMAGE          COMMAND   CREATED         STATUS         PORTS     NAMES
  9c06b95e3e85   hello-docker   "sh"      4 minutes ago   Up 4 minutes             zen_rosalind

$ touch additional.txt
$ docker cp ./additional.txt zen_rosalind:/usr/src/app/
```

Plik jest tworzony poleceniem `touch` tuż przed skopiowaniem.

Upewnijmy się, że plik został skopiowany do kontenera:

```console
# do this in terminal 1
/usr/src/app # ls
additional.txt  hello.sh
```

Świetnie! Wprowadziliśmy zmianę w kontenerze. Możemy użyć polecenia [docker diff](https://docs.docker.com/reference/cli/docker/container/diff/), aby sprawdzić, co się zmieniło

```console
# do this in terminal 2
$ docker diff zen_rosalind
  C /usr
  C /usr/src
  C /usr/src/app
  A /usr/src/app/additional.txt
  C /root
  A /root/.ash_history
```

Znak przed nazwą pliku wskazuje typ zmiany w systemie plików kontenera: A = dodano, D = usunięto, C = zmieniono. Plik additional.txt został utworzony, a nasze `ls` utworzyło .ash_history.

Następnie zapiszemy zmiany jako _nowy obraz_ poleceniem [docker commit](https://docs.docker.com/engine/reference/commandline/container_commit/):

```console
# do this in terminal 2
$ docker commit zen_rosalind hello-docker-additional
  sha256:2f63baa355ce5976bf89fe6000b92717f25dd91172aed716208e784315bfc4fd
$ docker image ls
  REPOSITORY                   TAG          IMAGE ID       CREATED          SIZE
  hello-docker-additional      latest       2f63baa355ce   3 seconds ago    7.73MB
  hello-docker                 latest       444f21cf7bd5   31 minutes ago   7.73MB
```

Technicznie `docker commit` dodał nową warstwę ponad obrazem `hello-docker`, a wynikowy obraz otrzymał nazwę `hello-docker-additional`.

W trakcie tego kursu właściwie więcej nie użyjemy `docker commit`. Dzieje się tak, ponieważ definiowanie zmian w Dockerfile jest znacznie bardziej zrównoważoną metodą zarządzania modyfikacjami. Żadnej magii ani skryptów — tylko Dockerfile, który można wersjonować.

Zróbmy więc to — stwórzmy hello-docker z tagiem v2, który zawiera plik additional.txt. Nowy plik można dodać instrukcją [RUN](https://docs.docker.com/engine/reference/builder/#run):

**Dockerfile**

```Dockerfile
# Start from the alpine image
FROM alpine:3.19

# Use /usr/src/app as our workdir. The following instructions will be executed in this location.
WORKDIR /usr/src/app

# Copy the hello.sh file from this location to /usr/src/app/ creating /usr/src/app/hello.sh.
COPY hello.sh .

# Execute a command with `/bin/sh -c` prefix.
RUN touch additional.txt

# When running Docker run the command will be ./hello.sh
CMD ./hello.sh
```

Tym razem użyliśmy RUN do wykonania polecenia `touch additional.txt`, które tworzy plik wewnątrz wynikowego obrazu. W zasadzie wszystko, co można wykonać w kontenerze opartym na tworzonym obrazie, można polecić uruchomić podczas budowy Dockerfile przez RUN.

Zbuduj teraz Dockerfile poleceniem `docker build . -t hello-docker:v2` i gotowe! Porównajmy wynik ls:

```
$ docker run hello-docker-additional ls
  additional.txt
  hello.sh

$ docker run hello-docker:v2 ls
  additional.txt
  hello.sh
```

Teraz wiemy, że wszystkie instrukcje w Dockerfile **poza** CMD (i jedną inną, o której zaraz się nauczymy) wykonywane są w czasie budowania. **CMD** wykonuje się przy `docker run`, chyba że ją nadpiszemy.

## Ćwiczenia 1.7 - 1.8

::::info Exercise 1.7: Image for script

Możemy ulepszyć nasze poprzednie rozwiązania, skoro już wiemy, jak stworzyć i zbudować Dockerfile.

Wróćmy teraz do [Ćwiczenia 1.4](/part-1/section-2#exercise-14).

Utwórz nowy plik `script.sh` na swojej maszynie lokalnej o następującej treści:

```bash
while true
do
  echo "Input website:"
  read website; echo "Searching.."
  sleep 1; curl http://$website
done
```

Utwórz Dockerfile dla nowego obrazu, który startuje z _ubuntu:22.04_ i dodaj instrukcje instalujące `curl` w tym obrazie. Następnie dodaj instrukcje kopiujące plik skryptu do obrazu i na końcu ustaw go do uruchamiania przy starcie kontenera za pomocą CMD.

Po wypełnieniu Dockerfile zbuduj obraz o nazwie „curler”.

* Jeśli dostajesz permission denied, użyj `chmod`, aby nadać uprawnienia do uruchomienia skryptu.

Poniższe powinno teraz działać:

```bash
$ docker run -it curler

  Input website:
  helsinki.fi
  Searching..
  <!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
  <html><head>
  <title>301 Moved Permanently</title>
  </head><body>
  <h1>Moved Permanently</h1>
  <p>The document has moved <a href="https://www.helsinki.fi/">here</a>.</p>
  </body></html>
```

Pamiętaj, że [RUN](https://docs.docker.com/engine/reference/builder/#run) można użyć do wykonywania poleceń podczas budowania obrazu!

Prześlij Dockerfile.

::::

::::info Exercise 1.8: Two line Dockerfile

Domyślnie nasz `devopsdockeruh/simple-web-service:alpine` nie ma CMD. Zamiast tego używa _ENTRYPOINT_, aby zadeklarować, która aplikacja jest uruchamiana.

O _ENTRYPOINT_ powiemy więcej w następnej sekcji, ale już teraz wiesz, że ostatni argument `docker run` może posłużyć do przekazania polecenia lub argumentu.

Jak mogłeś zauważyć, nie startuje on usługi webowej mimo nazwy „simple-web-service”. Potrzebny jest odpowiedni argument, aby uruchomić serwer!

Spróbuj `docker run devopsdockeruh/simple-web-service:alpine hello`. Aplikacja odczyta argument „hello”, ale poinformuje, że hello nie jest akceptowane.

W tym ćwiczeniu utwórz Dockerfile i użyj FROM oraz CMD, aby stworzyć zupełnie nowy obraz, który automatycznie uruchamia `server`.

Dokumentacja Dockera dla [CMD](https://docs.docker.com/engine/reference/builder/#cmd) mówi nieco pośrednio, że jeśli obraz ma zdefiniowany ENTRYPOINT, CMD służy do określania domyślnych argumentów.

Otaguj nowy obraz jako „web-server”.

Zwróć Dockerfile i komendę, której użyłeś do uruchomienia kontenera.

Uruchomienie zbudowanego obrazu „web-server” powinno wyglądać tak:

```console
$ docker run web-server
[GIN-debug] [WARNING] Creating an Engine instance with the Logger and Recovery middleware already attached.

[GIN-debug] [WARNING] Running in "debug" mode. Switch to "release" mode in production.
- using env:   export GIN_MODE=release
- using code:  gin.SetMode(gin.ReleaseMode)

[GIN-debug] GET    /*path                    --> server.Start.func1 (3 handlers)
[GIN-debug] Listening and serving HTTP on :8080
```

* Nie mamy jeszcze sposobu na dostęp do usługi webowej. W związku z tym wystarczy potwierdzić, że wypis w konsoli jest zgodny.

* Tytuł ćwiczenia może być przydatną wskazówką.

::::
