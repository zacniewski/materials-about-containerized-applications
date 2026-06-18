---
title: "Interakcja z kontenerem przez wolumeny i porty"
---

Wróćmy do yt-dlp. Działa, ale dość pracochłonne jest przenoszenie pobranych filmów na maszynę hosta.

Możemy użyć [wolumenów](https://docs.docker.com/storage/volumes/) Dockera, aby łatwiej przechowywać pobrane pliki poza efemerycznym storage kontenera. Dzięki [bind mount](https://docs.docker.com/storage/bind-mounts/) możemy podmontować plik lub katalog z naszej maszyny (hosta) do kontenera.

Uruchommy kontener z opcją `-v`, która wymaga ścieżki absolutnej. Montujemy nasz bieżący katalog jako `/mydir` w kontenerze, nadpisując wszystko, co umieściliśmy w tym folderze w naszym Dockerfile.

```console
$ docker run -v "$(pwd):/mydir" yt-dlp https://www.youtube.com/watch?v=DptFY_MszQs
```

Wolumen to po prostu folder (lub plik) współdzielony między maszyną hosta a kontenerem. Jeśli plik w wolumenie zostanie zmodyfikowany przez program działający w kontenerze, zmiany nie znikną po wyłączeniu kontenera, ponieważ plik istnieje na hoście. To główny cel wolumenów — w przeciwnym razie po restarcie kontenera pliki nie byłyby dostępne. Wolumeny można też używać do współdzielenia plików między kontenerami oraz uruchamiania programów, które potrafią ładować zmienione pliki.

W naszym yt-dlp chcieliśmy podmontować cały katalog, ponieważ nazwy plików są dość przypadkowe. Gdybyśmy chcieli utworzyć wolumen tylko z jednym plikiem, też możemy, wskazując go bezpośrednio. Na przykład `-v "$(pwd)/material.md:/mydir/material.md"` — w ten sposób moglibyśmy edytować material.md lokalnie i mieć tę zmianę w kontenerze (i odwrotnie). Zauważ też, że `-v` utworzy katalog, jeśli plik nie istnieje.

## Ćwiczenie 1.9

::::info Exercise 1.9: Volumes

W tym ćwiczeniu nie tworzymy nowego Dockerfile.

Obraz `devopsdockeruh/simple-web-service` tworzy znacznik czasu co dwie sekundy do `/usr/src/app/text.log`, gdy nie podano mu polecenia. Uruchom kontener z bind mount tak, aby logi były tworzone w Twoim systemie plików.

Prześlij komendę, której użyłeś do wykonania ćwiczenia.

**Wskazówka:** przeczytaj notatkę tuż przed tym ćwiczeniem!

::::

## Umożliwianie zewnętrznych połączeń do kontenerów

Ten kurs nie wchodzi głęboko w mechanizmy komunikacji między programami. Jeśli chcesz to poznać dogłębnie, zajrzyj do zajęć z Systemów Operacyjnych lub Sieci. Tutaj wystarczy znać kilka prostych rzeczy:

- Wysyłanie komunikatów: Programy mogą wysyłać komunikaty na adresy [URL](https://en.wikipedia.org/wiki/URL), takie jak: http://127.0.0.1:3000, gdzie HTTP to [_protokół_](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol), 127.0.0.1 to adres IP, a 3000 to [_port_](https://en.wikipedia.org/wiki/Port_(computer_networking)). Zauważ, że część IP może być też [_nazwą hosta_](https://en.wikipedia.org/wiki/Hostname): 127.0.0.1 to także [_localhost_](https://en.wikipedia.org/wiki/Localhost), więc równie dobrze możesz użyć http://localhost:3000.

- Odbieranie komunikatów: Programy mogą nasłuchiwać na dowolnym dostępnym porcie. Jeśli program nasłuchuje na porcie 3000 i komunikat zostanie wysłany na ten port, program go odbierze i być może przetworzy.

Adres _127.0.0.1_ i nazwa hosta _localhost_ są szczególne — odnoszą się do samej maszyny lub kontenera, więc jeśli jesteś w kontenerze i wysyłasz komunikat na _localhost_, celem jest ten sam kontener. Podobnie, jeśli wysyłasz żądanie spoza kontenera na _localhost_, celem jest Twoja maszyna.

Można **zmapować port maszyny hosta na port kontenera**. Przykładowo, jeśli zmapujesz port 1000 na hoście na port 2000 w kontenerze, a następnie wyślesz żądanie na http://localhost:1000 na swoim komputerze, kontener otrzyma to żądanie, jeśli nasłuchuje na swoim porcie 2000.

Otwarcie połączenia z zewnątrz do kontenera Dockera odbywa się w dwóch krokach:

- Eksponowanie portu

- Publikowanie portu

Eksponowanie portu kontenera oznacza poinformowanie Dockera, że kontener nasłuchuje na określonym porcie. Niewiele to robi, poza pomocą ludziom w konfiguracji.

Publikowanie portu oznacza, że Docker zmapuje porty hosta na porty kontenera.

Aby eksponować port, dodaj linię `EXPOSE <port>` w Dockerfile

Aby opublikować port, uruchom kontener z `-p <host-port>:<container-port>`

Jeśli pominiesz port hosta i podasz tylko port kontenera, Docker automatycznie wybierze wolny port po stronie hosta:

```console
$ docker run -p 4567 app-in-port
```

Możemy też ograniczyć połączenia tylko do konkretnego protokołu, np. UDP, dodając protokół na końcu: `EXPOSE <port>/udp` oraz `-p <host-port>:<container-port>/udp`.

::::tip Security reminder: Opening a door to the internet

Skoro otwieramy port aplikacji, każdy z internetu może wejść i uzyskać dostęp do tego, co uruchamiasz.

Nie otwieraj pochopnie byle jakich portów — sposób dla atakującego to wykorzystanie portu otwartego do niebezpiecznego serwera. Prosty sposób, by tego uniknąć, to zdefiniowanie portu po stronie hosta tak: `-p 127.0.0.1:3456:3000`. Pozwoli to tylko na żądania z Twojego komputera przez port 3456 do aplikacji na porcie 3000, bez dostępu z zewnątrz.

Krótsza składnia, `-p 3456:3000`, odpowiada `-p 0.0.0.0:3456:3000`, co faktycznie otwiera port dla wszystkich.

Zwykle nie jest to ryzykowne. Ale w zależności od aplikacji, warto to rozważyć!

::::

## Ćwiczenie 1.10

::::info Exercise 1.10: Ports open

W tym ćwiczeniu nie tworzymy nowego Dockerfile.

Obraz `devopsdockeruh/simple-web-service` uruchomi usługę webową na porcie `8080`, gdy dostanie argument „server”. W [Ćwiczeniu 1.8](/part-1/section-3#exercises-17---18) stworzyłeś już obraz, który można użyć do uruchomienia usługi bez argumentów.

Użyj teraz flagi -p, aby uzyskać dostęp do treści w przeglądarce. Wyjście w przeglądarce powinno wyglądać mniej więcej tak:
`{ message: "You connected to the following path: ...`

Prześlij komendy, których użyłeś w tym ćwiczeniu.

::::
