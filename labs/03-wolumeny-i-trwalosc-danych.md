# Laboratorium 3: Wolumeny i trwałość danych (6 godz.)

## Cel laboratorium
Praktyczne poznanie mechanizmów trwałego przechowywania danych w Docker: volumes, bind mounts, tmpfs. Praca z bazami danych i backup wolumenów.

## Wymagania wstępne
- Ukończone Laboratorium 1 i 2

---

## Część 1: Docker Volumes — podstawy (60 min)

### Ćwiczenie 1.1: Tworzenie i zarządzanie wolumenami

```bash
# Utwórz wolumen
docker volume create moje-dane

# Lista wolumenów
docker volume ls

# Szczegóły wolumenu
docker volume inspect moje-dane
```

> 📸 **Wymagany screenshot 1**: Wynik `docker volume inspect`

### Ćwiczenie 1.2: Użycie wolumenu z kontenerem

```bash
# Zapisz dane w wolumenie
docker run --rm -v moje-dane:/data ubuntu bash -c "echo 'Dane trwałe!' > /data/plik.txt && date >> /data/plik.txt"

# Odczytaj dane z innego kontenera
docker run --rm -v moje-dane:/data ubuntu cat /data/plik.txt

# Dane przetrwały! Kontener został usunięty (--rm), ale dane zostały.
```

### Ćwiczenie 1.3: Efemeryczność bez wolumenu

```bash
# Bez wolumenu — dane giną
docker run --name temp ubuntu bash -c "echo 'Dane tymczasowe' > /tmp/dane.txt"
docker start temp
docker exec temp cat /tmp/dane.txt  # OK — kontener istnieje

docker rm temp
# Dane zniknęły bezpowrotnie!
```

> 📸 **Wymagany screenshot 2**: Demonstracja trwałości danych z wolumenem vs bez

### Ćwiczenie 1.4: Wolumen tylko do odczytu

```bash
# Zapisz dane
docker run --rm -v moje-dane:/data ubuntu bash -c "echo 'Ważne dane' > /data/important.txt"

# Zamontuj jako read-only
docker run --rm -v moje-dane:/data:ro ubuntu bash -c "cat /data/important.txt"

# Próba zapisu — błąd!
docker run --rm -v moje-dane:/data:ro ubuntu bash -c "echo 'test' > /data/nowy.txt"
```

---

## Część 2: Bind mounts (60 min)

### Ćwiczenie 2.1: Montowanie katalogu z hosta

```bash
mkdir -p ~/docker-lab03/web-content
echo "<h1>Strona z hosta!</h1>" > ~/docker-lab03/web-content/index.html

# Zamontuj katalog z hosta do kontenera Nginx
docker run -d --name web \
  -p 8080:80 \
  -v ~/docker-lab03/web-content:/usr/share/nginx/html:ro \
  nginx:alpine

curl http://localhost:8080
```

> 📸 **Wymagany screenshot 3**: Strona serwowana z zamontowanego katalogu

### Ćwiczenie 2.2: Hot-reload z bind mount

```bash
# Zmień plik na hoście
echo "<h1>Zaktualizowana strona!</h1><p>Zmiana widoczna natychmiast.</p>" > ~/docker-lab03/web-content/index.html

# Sprawdź — zmiana widoczna bez restartu kontenera!
curl http://localhost:8080

docker stop web && docker rm web
```

### Ćwiczenie 2.3: Bind mount dla development

```bash
mkdir -p ~/docker-lab03/python-dev && cd ~/docker-lab03/python-dev

cat > app.py << 'EOF'
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1>Wersja 1 — development</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
EOF

cat > requirements.txt << 'EOF'
flask==3.0.0
EOF

cat > Dockerfile << 'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
EOF

docker build -t dev-app .
docker run -d --name dev \
  -p 5000:5000 \
  -v $(pwd)/app.py:/app/app.py \
  dev-app

curl http://localhost:5000

# Zmień app.py na hoście (np. "Wersja 2")
sed -i 's/Wersja 1/Wersja 2/' app.py

# Flask z debug=True automatycznie przeładuje!
sleep 2 && curl http://localhost:5000

docker stop dev && docker rm dev
```

> 📸 **Wymagany screenshot 4**: Hot-reload — zmiana kodu widoczna bez restartu

---

## Część 3: Bazy danych z wolumenami (90 min)

### Ćwiczenie 3.1: PostgreSQL z trwałymi danymi

```bash
# Utwórz wolumen
docker volume create pgdata

# Uruchom PostgreSQL
docker run -d --name postgres \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=studenci \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:16-alpine

# Poczekaj na inicjalizację
sleep 5

# Utwórz tabelę i dodaj dane
docker exec -it postgres psql -U postgres -d studenci -c "
CREATE TABLE studenci (
    id SERIAL PRIMARY KEY,
    imie VARCHAR(50),
    nazwisko VARCHAR(50),
    nr_indeksu VARCHAR(10)
);
INSERT INTO studenci (imie, nazwisko, nr_indeksu) VALUES
    ('Jan', 'Kowalski', '123456'),
    ('Anna', 'Nowak', '654321');
SELECT * FROM studenci;
"
```

> 📸 **Wymagany screenshot 5**: Tabela studenci w PostgreSQL

```bash
# Zatrzymaj i usuń kontener
docker stop postgres && docker rm postgres

# Uruchom nowy kontener z tym samym wolumenem
docker run -d --name postgres-new \
  -e POSTGRES_PASSWORD=secret \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:16-alpine

sleep 3

# Dane przetrwały!
docker exec -it postgres-new psql -U postgres -d studenci -c "SELECT * FROM studenci;"
```

> 📸 **Wymagany screenshot 6**: Dane zachowane po usunięciu i ponownym uruchomieniu kontenera

### Ćwiczenie 3.2: MySQL z wolumenem

```bash
docker volume create mysqldata

docker run -d --name mysql \
  -e MYSQL_ROOT_PASSWORD=secret \
  -e MYSQL_DATABASE=sklep \
  -v mysqldata:/var/lib/mysql \
  -p 3306:3306 \
  mysql:8

sleep 15  # MySQL potrzebuje więcej czasu na inicjalizację

docker exec -it mysql mysql -u root -psecret -e "
USE sklep;
CREATE TABLE produkty (id INT AUTO_INCREMENT PRIMARY KEY, nazwa VARCHAR(100), cena DECIMAL(10,2));
INSERT INTO produkty (nazwa, cena) VALUES ('Laptop', 3999.99), ('Mysz', 49.99);
SELECT * FROM produkty;
"
```

### Ćwiczenie 3.3: MongoDB z wolumenem

```bash
docker volume create mongodata

docker run -d --name mongo \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=secret \
  -v mongodata:/data/db \
  -p 27017:27017 \
  mongo:7

sleep 5

docker exec -it mongo mongosh -u admin -p secret --eval "
use testdb;
db.users.insertMany([
    {name: 'Jan', age: 25},
    {name: 'Anna', age: 30}
]);
db.users.find().pretty();
"
```

---

## Część 4: Współdzielenie wolumenów (45 min)

### Ćwiczenie 4.1: Writer-Reader pattern

```bash
docker volume create shared-logs

# Writer — generuje logi
docker run -d --name writer \
  -v shared-logs:/logs \
  ubuntu bash -c "while true; do echo \"\$(date): Log entry\" >> /logs/app.log; sleep 3; done"

# Reader — odczytuje logi
docker run --rm -v shared-logs:/logs:ro ubuntu tail -5 /logs/app.log

# Śledzenie na żywo
docker run --rm -v shared-logs:/logs:ro ubuntu tail -f /logs/app.log
# Ctrl+C po kilku wpisach

docker stop writer && docker rm writer
```

> 📸 **Wymagany screenshot 7**: Współdzielenie danych między kontenerami

---

## Część 5: Backup i restore wolumenów (60 min)

### Ćwiczenie 5.1: Backup wolumenu

```bash
# Upewnij się, że wolumen pgdata ma dane
docker exec -it postgres-new psql -U postgres -d studenci -c "SELECT * FROM studenci;"

# Backup do pliku tar
docker run --rm \
  -v pgdata:/source:ro \
  -v $(pwd):/backup \
  ubuntu tar czf /backup/pgdata-backup.tar.gz -C /source .

ls -lh pgdata-backup.tar.gz
```

### Ćwiczenie 5.2: Restore wolumenu

```bash
# Utwórz nowy wolumen
docker volume create pgdata-restored

# Restore z backupu
docker run --rm \
  -v pgdata-restored:/target \
  -v $(pwd):/backup:ro \
  ubuntu tar xzf /backup/pgdata-backup.tar.gz -C /target

# Uruchom PostgreSQL z przywróconym wolumenem
docker stop postgres-new && docker rm postgres-new

docker run -d --name postgres-restored \
  -e POSTGRES_PASSWORD=secret \
  -v pgdata-restored:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:16-alpine

sleep 3
docker exec -it postgres-restored psql -U postgres -d studenci -c "SELECT * FROM studenci;"
```

> 📸 **Wymagany screenshot 8**: Dane przywrócone z backupu

### Ćwiczenie 5.3: Backup bazy danych (pg_dump)

```bash
# Backup logiczny (pg_dump)
docker exec postgres-restored pg_dump -U postgres studenci > studenci_backup.sql

cat studenci_backup.sql

# Restore do nowej bazy
docker exec -i postgres-restored psql -U postgres -c "CREATE DATABASE studenci_copy;"
docker exec -i postgres-restored psql -U postgres studenci_copy < studenci_backup.sql
docker exec postgres-restored psql -U postgres -d studenci_copy -c "SELECT * FROM studenci;"
```

---

## Część 6: tmpfs mounts (30 min)

### Ćwiczenie 6.1: Dane w pamięci RAM

```bash
# tmpfs — dane w RAM
docker run --rm \
  --tmpfs /tmp:size=100m \
  ubuntu bash -c "
    echo 'Dane wrażliwe: hasło123' > /tmp/secret.txt
    cat /tmp/secret.txt
    df -h /tmp
  "

# Po zakończeniu kontenera dane znikają z RAM
```

### Ćwiczenie 6.2: Porównanie wydajności

```bash
# Zapis na tmpfs (RAM)
docker run --rm --tmpfs /data:size=100m ubuntu bash -c "
  time dd if=/dev/zero of=/data/testfile bs=1M count=50 2>&1
"

# Zapis na volume (dysk)
docker run --rm -v test-perf:/data ubuntu bash -c "
  time dd if=/dev/zero of=/data/testfile bs=1M count=50 2>&1
"

docker volume rm test-perf
```

---

## Część 7: Sprzątanie wolumenów (15 min)

### Ćwiczenie 7.1: Czyszczenie

```bash
# Lista wolumenów
docker volume ls

# Zatrzymaj i usuń kontenery
docker stop $(docker ps -q) 2>/dev/null
docker rm $(docker ps -aq) 2>/dev/null

# Usuń nieużywane wolumeny
docker volume prune -f

# Sprawdź
docker volume ls
docker system df
```

> 📸 **Wymagany screenshot 9**: Wynik czyszczenia wolumenów

---

## Zadania do samodzielnego wykonania

### Zadanie 1: Redis z trwałymi danymi
Uruchom Redis z wolumenem. Dodaj kilka kluczy, zatrzymaj kontener, uruchom ponownie i sprawdź, czy dane przetrwały.

### Zadanie 2: Serwer plików
Utwórz kontener Nginx serwujący pliki z katalogu na hoście. Dodawaj pliki na hoście i sprawdzaj ich dostępność przez przeglądarkę.

### Zadanie 3: Automatyczny backup
Napisz skrypt bash, który automatycznie tworzy backup wolumenu bazy danych z timestampem w nazwie pliku.

---

## Podsumowanie

Po ukończeniu tego laboratorium powinieneś umieć:
- ✅ Tworzyć i zarządzać wolumenami Docker
- ✅ Używać bind mounts do development (hot-reload)
- ✅ Konfigurować bazy danych z trwałymi wolumenami
- ✅ Współdzielić dane między kontenerami
- ✅ Wykonywać backup i restore wolumenów
- ✅ Używać tmpfs dla danych tymczasowych
- ✅ Czyścić nieużywane wolumeny
