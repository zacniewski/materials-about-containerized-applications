# Ćwiczenie 6: Sieci

W tym ćwiczeniu nauczymy się pracować z sieciami Dockera i łączyć kontenery.

Aby to osiągnąć, skonfigurujemy dwie bazy Postgres i wykonamy zapytania między nimi.

### Listowanie sieci

Docker definiuje sieci, które grupują kontenery na potrzeby interoperacyjności i funkcji DNS.

Aby wylistować sieci, uruchom `docker network ls`:

```
$ docker network ls
NETWORK ID          NAME                         DRIVER              SCOPE
99cbf6b3d074        bridge                       bridge              local
4a2071abf006        host                         host                local
3789e459bd9c        none                         null                local
$
```

Istnieją 3 domyślne sieci: `bridge`, `host` i `none`. Każde inne, własne sieci również będą tu widoczne. Sieci `host` i `none` nie są istotne dla tego ćwiczenia, ale `bridge` nas interesuje.

### Domyślna sieć `bridge`

Wszystkie nowe kontenery, jeśli nie podano inaczej, są automatycznie dołączane do sieci `bridge`. Ta sieć działa jako „przejście” do sieci hosta, dzięki czemu kontenery Dockera mają dostęp do internetu.

Możemy sprawdzić szczegóły sieci `bridge`, uruchamiając `docker network inspect bridge`:

```
$ docker network inspect bridge
[
    {
        "Name": "bridge",
        "Id": "99cbf6b3d07476bca2aaca71413b1a7609338d7d8deae9d4af77b062a98672de",
        "Created": "2017-04-17T20:27:36.319424753-04:00",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "172.17.0.0/16",
                    "Gateway": "172.17.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Containers": {},
        "Options": {
            "com.docker.network.bridge.default_bridge": "true",
            "com.docker.network.bridge.enable_icc": "true",
            "com.docker.network.bridge.enable_ip_masquerade": "true",
            "com.docker.network.bridge.host_binding_ipv4": "0.0.0.0",
            "com.docker.network.bridge.name": "docker0",
            "com.docker.network.driver.mtu": "1500"
        },
        "Labels": {}
    }
]
$
```

Widać tu różne informacje o sieci, ale zwróć uwagę na wpis "Containers": {}. Zobaczysz tam kontenery aktualnie podłączone do sieci.

Uruchommy kontener `ping` i sprawdźmy ponownie:

```
$ docker run --rm -d --name dummy delner/ping:1.0
104633917dbfe00843722336838f163b800dde46e632e47470b204c21fc44f21
$ docker network inspect bridge
...
        "Containers": {
            "104633917dbfe00843722336838f163b800dde46e632e47470b204c21fc44f21": {
                "Name": "dummy",
                "EndpointID": "38f01d182b8d55de5f8ed3221f12086dd2eac3426b159cc8e6bda0075dbd0f47",
                "MacAddress": "02:42:ac:11:00:02",
                "IPv4Address": "172.17.0.2/16",
                "IPv6Address": ""
            }
        },
...
$
```

Widać, że kontener został dodany do sieci domyślnej. Dodajmy teraz kolejny kontener `ping` i ustawmy go, by pingował pierwszy.

```
$ docker run --rm -d -e PING_TARGET=172.17.0.2 --name pinger delner/ping:1.0
3a79f28b8ac36c0e7aae523c4831c9405c110d593c15a30639606250595b245b
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED              STATUS              PORTS               NAMES
3a79f28b8ac3        delner/ping:1.0     "sh -c 'ping $PING..."   4 seconds ago        Up 3 seconds                            pinger
104633917dbf        delner/ping:1.0     "sh -c 'ping $PING..."   About a minute ago   Up About a minute                       dummy
$ docker logs pinger
PING 172.17.0.2 (172.17.0.2) 56(84) bytes of data.
64 bytes from 172.17.0.2: icmp_seq=1 ttl=64 time=0.171 ms
64 bytes from 172.17.0.2: icmp_seq=2 ttl=64 time=0.100 ms
64 bytes from 172.17.0.2: icmp_seq=3 ttl=64 time=0.098 ms
64 bytes from 172.17.0.2: icmp_seq=4 ttl=64 time=0.098 ms
$
```

W logach `pinger` widać, że udało się spingować drugi kontener w sieci. Używanie IP działa, ale jest uciążliwe i podatne na błędy przy zmianie adresów. Lepiej używać nazwy hosta, konkretnie nazwy kontenera `dummy`, aby zawsze rozwiązywać właściwy host.

Uruchomienie `ping` z celem `dummy`:

```
$ docker run --rm -d -e PING_TARGET=dummy --name pinger delner/ping:1.0
3a79f28b8ac36c0e7aae523c4831c9405c110d593c15a30639606250595b245b
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED              STATUS              PORTS               NAMES
104633917dbf        delner/ping:1.0     "sh -c 'ping $PING..."   About a minute ago   Up About a minute                       dummy
$
```

...kończy się niepowodzeniem. Nazwa hosta nie została rozwiązana, więc polecenie kończy się błędem, a kontener wychodzi i zostaje automatycznie usunięty.

Domyślna sieć `bridge` nie pozwala automatycznie na sieciowanie po nazwach kontenerów. Możemy to jednak łatwo osiągnąć, tworząc sieć własną.

Zatrzymaj i usuń kontener `dummy` poleceniem `docker stop dummy`.

### Zarządzanie sieciami własnymi

Aby utworzyć nową sieć, użyj `docker network create` i podaj nazwę sieci.

```
$ docker network create skynet
c234438e88ab579be943859dbc0a89788563226c3a9a13b4f1a2c78d1d8000c9
$ docker network ls
NETWORK ID          NAME                         DRIVER              SCOPE
99cbf6b3d074        bridge                       bridge              local
4a2071abf006        host                         host                local
3789e459bd9c        none                         null                local
c234438e88ab        skynet                       bridge              local
$ docker network inspect skynet
[
    {
        "Name": "skynet",
        "Id": "c234438e88ab579be943859dbc0a89788563226c3a9a13b4f1a2c78d1d8000c9",
        "Created": "2017-04-18T01:28:56.982335289-04:00",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": {},
            "Config": [
                {
                    "Subnet": "172.26.0.0/16",
                    "Gateway": "172.26.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Containers": {},
        "Options": {},
        "Labels": {}
    }
]
$
```

Aby usuwać sieci, użyj `docker network rm` i podaj nazwę sieci.

### Dodawanie kontenerów do sieci

Uruchommy ponownie kontener `ping`, tym razem przypisując mu sieć:

```
$ docker run --rm -d --network skynet --name dummy delner/ping:1.0
```

Następnie `pinger`, celując w kontener `dummy`:

```
$ docker run --rm -d --network skynet -e PING_TARGET=dummy --name pinger delner/ping:1.0
28e68fed9fe28a4346951fa8b6f4147a16f2afec8671357f1ed5f27425914b0a
$ docker logs pinger
PING dummy (172.26.0.2) 56(84) bytes of data.
64 bytes from dummy.skynet (172.26.0.2): icmp_seq=1 ttl=64 time=0.101 ms
64 bytes from dummy.skynet (172.26.0.2): icmp_seq=2 ttl=64 time=0.102 ms
64 bytes from dummy.skynet (172.26.0.2): icmp_seq=3 ttl=64 time=0.116 ms
$
```

Tym razem nazwa hosta rozwiązuje się poprawnie — to działanie wbudowanego DNS Dockera. Jest to szczególnie przydatne przy orkiestracji wielu kontenerów w jednej aplikacji (np. serwer WWW, baza danych, cache). Zamiast IP można używać nazw kontenerów w łańcuchach połączeń.

Zatrzymaj i usuń kontenery poleceniami `docker stop pinger` oraz `docker stop dummy`.

### Połączenia między kontenerami w sieci

Potrafimy rozwiązywać nazwy hostów i pingować, ale to nie to samo co połączenia TCP/UDP między kontenerami.

Skonfigurujmy dwie bazy `postgres`: `widget` oraz `gadget`.

Uruchom każdą bazę i dodaj je do sieci:

```
$ docker run --rm -d --name widgetdb --network skynet -p 5432 postgres
7f0248e3c0f4f03159ef966fd9767a4c7e3412801f8b0445cebb933d1e84e020
$ docker run --rm -d --name gadgetdb --network skynet -p 5432 postgres
8dc66701837c695728abb9046db71924112a9b8f2f1e096094ab5b5d631e2f73
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                     NAMES
8dc66701837c        postgres            "docker-entrypoint..."   11 seconds ago      Up 10 seconds       0.0.0.0:32769->5432/tcp   gadgetdb
7f0248e3c0f4        postgres            "docker-entrypoint..."   40 seconds ago      Up 39 seconds       0.0.0.0:32768->5432/tcp   widgetdb
$
```

Domyślnie port 5432 jest zablokowany i niedostępny. Dodając jednak `-p 5432`, zezwalamy innym kontenerom na dostęp przez port 5432, domyślny port Postgresa.

Teraz, gdy bazy działają, uruchom sesję powłoki w `widgetdb` poleceniem `docker exec`:

```
$ docker exec -it widgetdb /bin/bash
root@7f0248e3c0f4:/#
```

Możesz połączyć się z lokalną bazą komendą `psql`. (Zakończ sesję `psql`, wpisując `\q`.)

```
root@7f0248e3c0f4:/# psql -U postgres
psql (9.6.2)
Type "help" for help.

postgres=# \q
root@7f0248e3c0f4:/#
```

Albo z bazą `gadget`, odwołując się do niej po nazwie:

```
root@7f0248e3c0f4:/# psql -U postgres -h gadgetdb
psql (9.6.2)
Type "help" for help.

postgres=# \q
root@7f0248e3c0f4:/#
```

Wpisz `exit`, aby zakończyć sesję, następnie `docker stop widgetdb gadgetdb`, aby zatrzymać i usunąć kontenery.

### Mapowanie portów na hosta

Czasami przydatny jest bezpośredni dostęp do aplikacji działającej w kontenerze Dockera, jakby działała na hoście.

W tym celu możesz zmapować porty z kontenera na port hosta. Zmienione polecenie z poprzedniego przykładu Postgresa wyglądałoby tak:

```
$ docker run --rm -d --name widgetdb --network skynet -p 5432:5432 postgres
```

Flaga `-p` o postaci `<host port>:<container port>` wykonuje mapowanie, udostępniając serwer pod `localhost:5432`:

Możesz następnie uruchomić `psql` (jeśli narzędzie jest zainstalowane) na hoście, aby połączyć się z bazą Postgresa:

```
$ psql -U postgres -h localhost
psql (9.6.2)
Type "help" for help.

postgres=# \q
$
```

Pamiętaj, że do jednego portu hosta można przypisać tylko jedną aplikację na raz. Jeśli spróbujesz uruchomić aplikację na hoście lub inny kontener, który chce zmapować już używany port, operacja się nie powiedzie.

Wpisz `docker stop widgetdb`, aby zatrzymać i usunąć kontener.

# KONIEC ĆWICZENIA 6
