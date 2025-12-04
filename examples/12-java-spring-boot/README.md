# Spring Boot To‑Do — uruchamianie z Docker Compose

Prosty przykład aplikacji To‑Do w Spring Boot 3 (Java 21) z bazą H2 (plikowa). Projekt znajduje się w tym katalogu i zawiera gotowy `Dockerfile` oraz `docker-compose.yml`.

## Wymagania
- Docker i Docker Compose (Docker Desktop lub docker compose v2)

## Szybki start (Docker Compose)
1. Przejdź do katalogu projektu:
   ```bash
   cd examples/12-java-spring-boot
   ```
2. Zbuduj obraz i uruchom kontener w tle:
   ```bash
   docker compose up --build -d
   ```
3. Podgląd logów aplikacji (opcjonalnie):
   ```bash
   docker compose logs -f
   ```

Po uruchomieniu aplikacja jest dostępna pod adresem:
- API: `http://localhost:8080/api/todos`
- Konsola H2: `http://localhost:8080/h2-console`
  - JDBC URL: `jdbc:h2:file:/data/todo-db`
  - Użytkownik: `sa`
  - Hasło: (puste)

Trwałość danych zapewnia wolumen `todo-data`, zamapowany na `/data` w kontenerze.

## Przykładowe wywołania API
- Lista zadań:
  ```bash
  curl http://localhost:8080/api/todos
  ```
- Utworzenie zadania:
  ```bash
  curl -X POST http://localhost:8080/api/todos \
    -H 'Content-Type: application/json' \
    -d '{"title":"Kup mleko","completed":false}'
  ```
- Aktualizacja (PUT):
  ```bash
  curl -X PUT http://localhost:8080/api/todos/1 \
    -H 'Content-Type: application/json' \
    -d '{"title":"Kup chleb","completed":true}'
  ```
- Częściowa zmiana (PATCH):
  ```bash
  curl -X PATCH http://localhost:8080/api/todos/1 \
    -H 'Content-Type: application/json' \
    -d '{"completed":true}'
  ```
- Usunięcie:
  ```bash
  curl -X DELETE http://localhost:8080/api/todos/1 -i
  ```

## Zatrzymanie i usunięcie zasobów
- Zatrzymanie kontenerów:
  ```bash
  docker compose down
  ```
- Zatrzymanie i usunięcie wolumenów (skasuje dane H2):
  ```bash
  docker compose down -v
  ```

## Uruchomienie lokalnie (bez Dockera) — opcjonalnie
Wymagane: Java 21, Maven.

```bash
cd examples/12-java-spring-boot
mvn spring-boot:run
```

Aplikacja wystartuje na `http://localhost:8080`. Domyślna konfiguracja H2 w `application.properties` wskazuje na ścieżkę `/data/todo-db` (używaną w kontenerze). Przy uruchamianiu lokalnym możesz zmienić ją np. na katalog tymczasowy lub w pamięci, np.:

```properties
spring.datasource.url=jdbc:h2:mem:testdb;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=FALSE
```

## Pliki w katalogu
- `Dockerfile` — wieloetapowy build JAR i obraz uruchomieniowy (Temurin 21 JRE)
- `docker-compose.yml` — definicja usługi `app`, publikacja portu 8080 i wolumen `todo-data`
- `src/main/java` — kod aplikacji (encja `Todo`, repozytorium JPA, REST `TodoController`)
- `src/main/resources/application.properties` — konfiguracja aplikacji i H2
- `pom.xml` — konfiguracja Maven (Spring Boot Web, Data JPA, H2, Validation)

## Dodatkowe uwagi
- Konsola H2 jest włączona dla wygody demo: `/h2-console`.
- Profil aktywny: `SPRING_PROFILES_ACTIVE=default` (możesz nadpisać w `docker-compose.yml`).
