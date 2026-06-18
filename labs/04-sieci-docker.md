# Laboratorium 4: Sieci Docker (6 godz.)

## Cel laboratorium
Praktyczne poznanie sieci Docker: bridge, user-defined networks, DNS, mapowanie portów, komunikacja między kontenerami, izolacja sieciowa.

## Wymagania wstępne
- Ukończone Laboratorium 1-3

---

## Część 1: Domyślna sieć bridge (60 min)

### Ćwiczenie 1.1: Eksploracja domyślnej sieci

```bash
# Lista sieci
docker network ls

# Szczegóły domyślnej sieci bridge
docker network inspect bridge

# Uruchom dwa kontenery
docker run -d --name kontener-a alpine sleep 3600
docker run -d --name kontener-b alpine sleep 3600

# Sprawdź adresy IP
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' kontener-a
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' kontener-b

# Ping po IP — działa
docker exec kontener-a ping -c 3 $(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' kontener-b)

# Ping po nazwie — NIE działa w domyślnej bridge!
docker exec kontener-a ping -c 3 kontener-b
```

> 📸 **Wymagany screenshot 1**: Ping po IP działa, po nazwie nie

### Ćwiczenie 1.2: Interfejsy sieciowe w kontenerze

```bash
docker exec kontener-a ip addr
docker exec kontener-a ip route
docker exec kontener-a cat /etc/resolv.conf
```

```bash
docker stop kontener-a kontener-b && docker rm kontener-a kontener-b
```

---

## Część 2: User-defined bridge networks (90 min)

### Ćwiczenie 2.1: Tworzenie sieci i DNS

```bash
# Utwórz sieć
docker network create moja-siec

# Uruchom kontenery w sieci
docker run -d --name web --network moja-siec nginx:alpine
docker run -d --name app --network moja-siec alpine sleep 3600

# DNS działa!
docker exec app ping -c 3 web
docker exec app nslookup web
```

> 📸 **Wymagany screenshot 2**: DNS działa w user-defined network

### Ćwiczenie 2.2: Izolacja sieci

```bash
# Utwórz drugą sieć
docker network create inna-siec

# Kontener w innej sieci
docker run -d --name isolated --network inna-siec alpine sleep 3600

# Nie może pingować kontenerów z moja-siec
docker exec isolated ping -c 2 web  # FAIL — izolacja!
```

> 📸 **Wymagany screenshot 3**: Izolacja — kontener z innej sieci nie widzi web

### Ćwiczenie 2.3: Podłączanie do wielu sieci

```bash
# Podłącz kontener app do obu sieci
docker network connect inna-siec app

# Teraz app widzi oba kontenery
docker exec app ping -c 2 web       # OK — moja-siec
docker exec app ping -c 2 isolated  # OK — inna-siec

# Odłącz od sieci
docker network disconnect inna-siec app
```

### Ćwiczenie 2.4: Sieć z niestandardową konfiguracją

```bash
docker network create \
  --driver bridge \
  --subnet 172.30.0.0/16 \
  --gateway 172.30.0.1 \
  custom-net

docker run -d --name custom-c1 --network custom-net --ip 172.30.0.10 alpine sleep 3600
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' custom-c1
```

```bash
# Sprzątanie
docker stop $(docker ps -q) && docker rm $(docker ps -aq)
docker network rm moja-siec inna-siec custom-net
```

---

## Część 3: Mapowanie portów (60 min)

### Ćwiczenie 3.1: Różne tryby mapowania

```bash
# Konkretny port
docker run -d --name web1 -p 8080:80 nginx:alpine

# Losowy port
docker run -d --name web2 -p 80 nginx:alpine
docker port web2

# Tylko localhost
docker run -d --name web3 -p 127.0.0.1:8081:80 nginx:alpine

# Wiele portów
docker run -d --name web4 -p 8082:80 -p 8443:443 nginx:alpine

# Sprawdź
docker ps --format "table {{.Names}}\t{{.Ports}}"
curl http://localhost:8080
curl http://localhost:8081
```

> 📸 **Wymagany screenshot 4**: Kontenery z różnymi mapowaniami portów

```bash
docker stop web1 web2 web3 web4 && docker rm web1 web2 web3 web4
```

---

## Część 4: Komunikacja między usługami (90 min)

### Ćwiczenie 4.1: Aplikacja webowa + baza danych

```bash
# Utwórz sieć
docker network create app-net

# Uruchom PostgreSQL
docker run -d --name db \
  --network app-net \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=myapp \
  postgres:16-alpine

sleep 5

# Uruchom Adminer (GUI do bazy danych)
docker run -d --name adminer \
  --network app-net \
  -p 8080:8080 \
  adminer

# Otwórz http://localhost:8080
# Server: db, Username: postgres, Password: secret, Database: myapp
```

> 📸 **Wymagany screenshot 5**: Adminer połączony z bazą PostgreSQL

### Ćwiczenie 4.2: Frontend + Backend + Baza danych (izolacja)

```bash
# Utwórz sieci
docker network create frontend-net
docker network create backend-net

# Baza danych — tylko backend
docker run -d --name db2 \
  --network backend-net \
  -e POSTGRES_PASSWORD=secret \
  postgres:16-alpine

# Redis — tylko backend
docker run -d --name cache \
  --network backend-net \
  redis:7-alpine

sleep 3

# Aplikacja — obie sieci
docker run -d --name app \
  --network backend-net \
  alpine sleep 3600
docker network connect frontend-net app

# Nginx — tylko frontend
docker run -d --name nginx \
  --network frontend-net \
  -p 80:80 \
  nginx:alpine

# Testy komunikacji
docker exec app ping -c 2 db2    # OK — backend
docker exec app ping -c 2 cache  # OK — backend
docker exec app ping -c 2 nginx  # OK — frontend
docker exec nginx ping -c 2 db2  # FAIL — izolacja!
```

> 📸 **Wymagany screenshot 6**: Nginx nie może pingować bazy danych (izolacja)

### Ćwiczenie 4.3: Aliasy sieciowe

```bash
docker network create alias-net

# Kontener z aliasem
docker run -d --name postgres-main \
  --network alias-net \
  --network-alias database \
  --network-alias db \
  -e POSTGRES_PASSWORD=secret \
  postgres:16-alpine

docker run --rm --network alias-net alpine ping -c 2 database
docker run --rm --network alias-net alpine ping -c 2 db
docker run --rm --network alias-net alpine ping -c 2 postgres-main
```

---

## Część 5: Sieć host i none (30 min)

### Ćwiczenie 5.1: Sieć host

```bash
# Kontener używa sieci hosta (tylko Linux)
docker run -d --name host-nginx --network host nginx:alpine

# Nginx nasłuchuje na porcie 80 hosta (bez -p!)
curl http://localhost:80

docker stop host-nginx && docker rm host-nginx
```

### Ćwiczenie 5.2: Sieć none

```bash
docker run --rm --network none alpine ip addr
# Tylko interfejs loopback (lo)

docker run --rm --network none alpine ping -c 1 8.8.8.8
# Brak sieci — błąd!
```

> 📸 **Wymagany screenshot 7**: Kontener z siecią none — brak interfejsów sieciowych

---

## Część 6: Diagnostyka sieci (30 min)

### Ćwiczenie 6.1: Narzędzia diagnostyczne

```bash
docker network create diag-net
docker run -d --name diag --network diag-net nginx:alpine

# Inspekcja sieci
docker network inspect diag-net

# Sprawdzenie DNS
docker run --rm --network diag-net alpine nslookup diag

# Sprawdzenie portów
docker exec diag netstat -tlnp 2>/dev/null || docker exec diag ss -tlnp

# Sprawdzenie połączenia
docker run --rm --network diag-net alpine wget -qO- http://diag:80
```

---

## Część 7: Sprzątanie (15 min)

```bash
docker stop $(docker ps -q) 2>/dev/null
docker rm $(docker ps -aq) 2>/dev/null
docker network prune -f
docker system df
```

> 📸 **Wymagany screenshot 8**: Wynik czyszczenia sieci

---

## Zadania do samodzielnego wykonania

### Zadanie 1: Sieć wewnętrzna
Utwórz sieć z flagą `--internal` (bez dostępu do internetu). Uruchom w niej kontener i sprawdź, że nie ma dostępu do internetu, ale może komunikować się z innymi kontenerami w tej sieci.

### Zadanie 2: Architektura trójwarstwowa
Zaprojektuj i uruchom architekturę: Nginx (frontend) → Python/Node app (backend) → PostgreSQL (database), z odpowiednią izolacją sieciową.

### Zadanie 3: Round-robin DNS
Uruchom 3 kontenery z tym samym aliasem sieciowym. Sprawdź, jak Docker rozdziela zapytania DNS.

---

## Podsumowanie

Po ukończeniu tego laboratorium powinieneś umieć:
- ✅ Tworzyć i zarządzać sieciami Docker
- ✅ Konfigurować DNS w user-defined networks
- ✅ Izolować kontenery w osobnych sieciach
- ✅ Mapować porty w różnych trybach
- ✅ Łączyć kontenery w architekturę wielowarstwową
- ✅ Diagnostykować problemy sieciowe
