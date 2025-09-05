# Ćwiczenie 5: Wolumeny

W tym ćwiczeniu nauczymy się pracować z wolumenami Dockera, aby utrwalać dane między kontenerami.

Aby to osiągnąć, skonfigurujemy serwer Apache HTTPD i zapiszemy pliki HTML w wolumenie.

### Uruchamianie serwera

Aby uruchomić nasz serwer Apache HTTPD, wykonaj to polecenie:

```
$ docker run --rm -d --name apache -p 80:80 httpd:2.4
d87e0a193dde5652ac762d8849983c2cadb5116b80c8a61a4180e350d678b4d2
```

To polecenie uruchomi nowy kontener z HTTPD 2.4, nada mu nazwę `apache`, zmapuje port `80` na maszynę gospodarza (więcej o tym później) i ustawi flagę usunięcia kontenera po zatrzymaniu.

Po starcie możemy uruchomić `curl localhost`, aby pobrać stronę domyślną z serwera:

```
$ curl localhost
<html><body><h1>It works!</h1></body></html>
$
```

To domyślny plik `index.html` dołączony do nowej instalacji Apache 2.4. Zastąpmy go własną treścią HTML.

Aby to zrobić, użyjemy polecenia `docker cp`, podobnego do `scp`, które kopiuje pliki między hostem a kontenerami. Skopiujmy plik `index.html` z katalogu, w którym znajduje się ten README:

```
$ docker cp index.html apache:/usr/local/apache2/htdocs/
$
```

Pierwsza ścieżka to źródło (nasz nowy plik na hoście), a druga to miejsce docelowe. `apache` to nazwa kontenera, do którego kopiujemy, a `/usr/local/apache2/htdocs/` to katalog, z którego serwer WWW serwuje HTML.

Ponowne uruchomienie `curl` wygląda teraz nieco inaczej:

```
$ curl localhost
<html><body><h1>It works in Docker!</h1></body></html>
$
```

##### Potencjalny problem z danymi

Ten kontener, przez czas swojego życia, będzie serwował nasz nowy plik HTML.

Jednak w praktyce kontenery Dockera są efemeryczne. Mogą niespodziewanie się zatrzymać, a w niektórych wdrożeniach być usuwane bez ostrzeżenia. Jeśli polegasz na stanie kontenera, możesz utracić ważne dane, gdy kontener padnie. To szczególnie istotne w przypadku baz danych, które powinny stanowić trwałe magazyny.

W przypadku naszego serwera HTTPD samo zatrzymanie kontenera spowoduje jego automatyczne usunięcie. Możemy uruchomić kolejny kontener w jego miejsce, ale nie będzie on miał naszych zmian.

```
$ docker stop apache
apache
$ docker run --rm -d --name apache -p 80:80 httpd:2.4
9bd0620e3d8464456c368b1fe9b82733282d980a7c3f854b8cba7726f0a02958
$ curl localhost
<html><body><h1>It works!</h1></body></html>
$
```

Aby zachować dane między awariami i aktualizacjami, użyjemy wolumenów do utrwalania danych między kolejnymi generacjami kontenerów.

### Zarządzanie wolumenami

Wolumeny w Dockerze to magazyny plików, które istnieją niezależnie od kontenerów. Działają podobnie do wolumenów EBS w Amazon Web Services oraz innych nośników montowalnych, jak pendrive’y. Można je tworzyć, usuwać i montować w kontenerach w określonych lokalizacjach, podobnie jak poleceniem `mount` w Linuksie.

Aby wylistować wolumeny, uruchom `docker volume ls`:

```
$ docker volume ls
DRIVER              VOLUME NAME
$
```
Aby utworzyć nowy wolumen, uruchom `docker volume create` i podaj nazwę wolumenu.

```
$ docker volume create myvolume
myvolume
$ docker volume ls
DRIVER              VOLUME NAME
local               myvolume
$
```

Aby usunąć wolumen, uruchom `docker volume rm` z jego nazwą.

```
$ docker volume rm myvolume
myvolume
$ docker volume ls
DRIVER              VOLUME NAME
$
```

### Montowanie wolumenów w kontenerach

Najpierw utwórz nowy wolumen `httpd_htdocs`:

```
$ docker volume create httpd_htdocs
httpd_htdocs
$
```

Następnie ponownie uruchom `docker run`, przekazując flagę montowania `-v`.

```
$ docker run --rm -d --name apache -p 80:80 -v httpd_htdocs:/usr/local/apache2/htdocs/ httpd:2.4
c21dd93fea83d710b4d4c954911862760030723df6a5b42650e462e388fe6049
$
```

I ponownie skopiuj nasz zmodyfikowany plik HTML.

```
$ docker cp index.html apache:/usr/local/apache2/htdocs/
$
```

Uruchom `curl`, aby zweryfikować wynik.

```
$ curl localhost
<html><body><h1>It works in Docker!</h1></body></html>
$
```

Aby zobaczyć działanie wolumenu, zatrzymaj kontener. Dzięki `--rm` podczas `run`, kontener powinien zostać usunięty po zatrzymaniu.

```
$ docker stop apache
apache
$
```

Następnie ponownie uruchom httpd takim samym poleceniem jak wcześniej. Tym razem po `curl` zobaczysz, że nasze zmiany w pliku nadal są obecne.

```
$ docker run --rm -d --name apache -p 80:80 -v httpd_htdocs:/usr/local/apache2/htdocs/ httpd:2.4
c21dd93fea83d710b4d4c954911862760030723df6a5b42650e462e388fe6049
$ curl localhost
<html><body><h1>It works in Docker!</h1></body></html>
$
```

Ten wolumen możemy zamontować w dowolnym kontenerze HTTPD, co daje elastyczność w podmienianiu kontenerów na nowsze wersje bez utraty danych.

Uruchom `docker stop apache`, aby zatrzymać i usunąć kontener, a następnie `docker volume rm httpd_htdocs`, aby usunąć wolumen.

### Montowanie katalogów hosta w kontenerach

Alternatywnie, jeśli masz katalog na hoście, którego chcesz używać jak wolumenu, możesz również zamontować katalogi hosta. Technika ta jest przydatna w środowiskach developerskich, gdy chcesz zamontować lokalne repozytorium do obrazu Dockera i modyfikować jego zawartość bez przebudowy lub kopiowania plików.

Flaga `-v` do tego celu jest prawie identyczna jak wcześniej. Wystarczy podać bezwzględną ścieżkę do lokalnego katalogu. W naszym przypadku przekażemy `.` aby wskazać katalog `5-volumes` w tym repozytorium, który zawiera zmodyfikowaną wersję pliku HTML.

```
$ pwd
/home/david/src/docker-training/exercises/basic/5-volumes/
$ docker run --rm -d --name apache -p 80:80 -v /home/david/src/docker-training/exercises/basic/5-volumes/:/usr/local/apache2/htdocs/ httpd:2.4
0d91516b20ea6113b5dcca08ada6465095dc68663b3d2201dc0490165764f842
$ curl localhost
<html><body><h1>It works!</h1></body></html>
$
```

Z montażem katalogu hosta w miejscu, zmodyfikuj plik `index.html` w tym katalogu, zapisz, a następnie ponownie uruchom `curl`.

```
$ curl localhost
<html><body><h1>It works quite well in Docker!</h1></body></html>
$
```

Widzisz, że zmiany w pliku pojawiają się natychmiast w kontenerze, bez potrzeby `docker cp`.

Uruchom `docker stop apache`, aby zatrzymać i usunąć kontener.

# KONIEC ĆWICZENIA 5
