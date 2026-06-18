---
title: 'Kontenery w środowisku deweloperskim'
---

Kontenery świetnie sprawdzają się nie tylko w produkcji. Można ich używać także w środowiskach deweloperskich i dają kilka korzyści. Ten sam problem _u-mnie-działa_ pojawia się często, gdy do zespołu dołącza nowy programista. Nie wspominając o bólu głowy przy przełączaniu wersji runtime’u czy lokalnej bazy danych!

Na przykład [zespół wytwórczy oprogramowania](https://toska.dev/) na Uniwersytecie Helsińskim ma w pełni [skonteneryzowane środowisko deweloperskie](https://helda.helsinki.fi/items/9f681533-f488-406d-b2d8-a2f8b225f283). Zasadą we wszystkich projektach jest taki setup, by nowy deweloper musiał zainstalować jedynie Dockera i sklonować kod projektu z GitHuba, by zacząć. Żadna zależność nigdy nie jest instalowana na maszynie gospodarza; Git, Docker i wybrany edytor tekstu to jedyne potrzebne rzeczy.

Nawet jeśli Twoja aplikacja nie jest w pełni skonteneryzowana w trakcie developmentu, kontenery mogą być bardzo pomocne. Przykładowo, potrzebujesz zainstalować MongoDB w wersji 4.0.22 na porcie 5656. To teraz oneliner: "docker run -p 5656:27017 mongo:4.0.22" (MongoDB używa domyślnie portu 27017).

Skonteneryzujmy środowisko deweloperskie NodeJS. Jak być może wiesz, [NodeJS](https://nodejs.org/en/) to wieloplatformowy runtime JavaScriptu, który umożliwia uruchamianie JavaScriptu na Twojej maszynie, serwerach i urządzeniach wbudowanych, oraz wielu innych platformach.

Konfiguracja wymaga trochę znajomości działania NodeJS. Oto uproszczone wyjaśnienie, jeśli nie kojarzysz: biblioteki są zdefiniowane w `package.json` i `package-lock.json` i instalowane poleceniem `npm install`. [npm](https://www.npmjs.com/) to menedżer pakietów Node.

Aby uruchomić aplikację z pakietami mamy skrypt zdefiniowany w package.json, który instruuje Node, by wykonać index.js — plik główny/entry; tutaj skrypt wykonuje się `npm start`. Aplikacja ma już kod wykrywający zmiany w systemie plików i restartujący aplikację, jeśli wykryje zmiany.

Projekt „node-dev-env” znajdziesz tutaj: [https://github.com/docker-hy/material-applications/tree/main/node-dev-env](https://github.com/docker-hy/material-applications/tree/main/node-dev-env). Dodaliśmy już deweloperski Dockerfile i pomocny docker-compose.yml.

**Dockerfile**
```Dockerfile
FROM node:16

WORKDIR /usr/src/app

COPY package* ./

RUN npm install
```

**docker-compose.yml**
```yaml
version: '3.8'

services:
  node-dev-env:
    build: . # Build with the Dockerfile here
    command: npm start # Run npm start as the command
    ports:
      - 3000:3000 # The app uses port 3000 by default, publish it as 3000
    volumes:
      - ./:/usr/src/app # Let us modify the contents of the container locally
      - node_modules:/usr/src/app/node_modules # A bit of node magic, this ensures the dependencies built for the image are not available locally.
    container_name: node-dev-env # Container name for convenience

volumes: # This is required for the node_modules named volume
  node_modules:
```

I to wszystko. Użyjemy wolumenu, aby skopiować cały kod źródłowy do wolumenu, więc CMD uruchomi aplikację, nad którą pracujemy. Spróbujmy!

```console
$ docker compose up

...

Attaching to node-dev-env
node-dev-env  |
node-dev-env  | > dev-env@1.0.0 start
node-dev-env  | > nodemon index.js
node-dev-env  |
node-dev-env  | [nodemon] 2.0.7
node-dev-env  | [nodemon] to restart at any time, enter `rs`
node-dev-env  | [nodemon] watching path(s): *.*
node-dev-env  | [nodemon] watching extensions: js,mjs,json
node-dev-env  | [nodemon] starting `node index.js`
node-dev-env  | App listening in port 3000
```

Świetnie! Początkowy start jest nieco wolny. Teraz, gdy obraz już jest zbudowany, jest dużo szybciej. Całe środowisko możemy odbudować kiedy chcemy, używając `docker compose up --build`.

Sprawdźmy, czy aplikacja działa. Wejdź przeglądarką na [http://localhost:3000](http://localhost:3000) — powinna wykonać proste dodawanie na podstawie parametrów zapytania.

Jednak wynik nie ma sensu! Naprawmy błąd. Założę się, że chodzi o tę linię: [https://github.com/docker-hy/material-applications/blob/main/node-dev-env/index.js#L5](https://github.com/docker-hy/material-applications/blob/main/node-dev-env/index.js#L5)

Gdy zmienię linię na swojej maszynie, aplikacja natychmiast wykrywa zmianę plików:

```console
$ docker compose up

...

Attaching to node-dev-env
node-dev-env  |
node-dev-env  | > dev-env@1.0.0 start
node-dev-env  | > nodemon index.js
node-dev-env  |
node-dev-env  | [nodemon] 2.0.7
node-dev-env  | [nodemon] to restart at any time, enter `rs`
node-dev-env  | [nodemon] watching path(s): *.*
node-dev-env  | [nodemon] watching extensions: js,mjs,json
node-dev-env  | [nodemon] starting `node index.js`
node-dev-env  | App listening in port 3000
node-dev-env  | [nodemon] restarting due to changes...
node-dev-env  | [nodemon] starting `node index.js`
node-dev-env  | App listening in port 3000
```

A teraz po odświeżeniu strony widać, że poprawka zadziałała. Środowisko deweloperskie działa.

Kolejne ćwiczenie może być ekstremalnie proste albo ekstremalnie trudne. Śmiało — baw się dobrze.

## Ćwiczenie 2.11

::::info Exercise 2.11

  Wybierz jakiś swój projekt deweloperski i zacznij wykorzystywać kontenery w środowisku developmentowym.

  Wyjaśnij, co zrobiłeś. Może to być cokolwiek, np. wsparcie dla docker-compose.yml, aby usługi (jak bazy danych) były skonteneryzowane, albo nawet pełne skonteneryzowane środowisko deweloperskie.

::::

Jeśli interesuje Cię, jak zbudować skonteneryzowane środowisko deweloperskie dla aplikacji typu Single Page (React/Node), zajrzyj do kursu [Full stack open](https://fullstackopen.com), który ma [rozdział](https://fullstackopen.com/en/part12/basics_of_orchestration#development-in-containers) poświęcony temu tematowi.
