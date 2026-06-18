# Przykład 01: Node.js

Prosty przykład konteneryzacji statycznej strony serwowanej przez serwer HTTP w Node.js.

## Instrukcje

1. **Budowanie obrazu:**
   ```bash
   docker build -t nodejs-image .
   ```

2. **Sprawdzanie dostępnych obrazów:**
   ```bash
   docker image ls
   ```

3. **Uruchamianie kontenera w tle:**
   ```bash
   docker run -d --name nodejs-container -p 3000:3000 nodejs-image
   ```

4. **Sprawdzanie działających kontenerów:**
   ```bash
   docker ps
   ```

5. **Dostęp do aplikacji:**
   Otwórz przeglądarkę i przejdź pod adres: [http://localhost:3000](http://localhost:3000)

## Kluczowe komendy
- `-d`: uruchomienie w trybie "detached" (w tle).
- `-p 3000:3000`: mapowanie portu hosta (3000) na port kontenera (3000).
- `--name`: nadanie własnej nazwy kontenerowi.
