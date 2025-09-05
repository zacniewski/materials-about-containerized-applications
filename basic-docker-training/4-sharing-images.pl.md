# Ćwiczenie 4: Udostępnianie obrazów

W tym ćwiczeniu nauczymy się, jak udostępniać obrazy Dockera przy użyciu DockerHuba. DockerHub to GitHub dla Dockera: świetne miejsce, aby znaleźć obrazy społeczności i wysyłać własne.

Będziemy potrzebować naszego obrazu `ping` z ćwiczenia „Building Images”, więc najpierw je ukończ, aby mieć obraz do udostępnienia.

### Pierwsze kroki

Aby udostępniać obrazy na DockerHubie, potrzebujesz konta. Możesz się zarejestrować [tutaj](https://hub.docker.com/).

Większość funkcji DockerHuba jest podobna do GitHuba: wyszukiwarka obrazów, repozytoria oraz organizacje.

Narzędzie wiersza poleceń `docker` ma integrację z DockerHubem. Aby użyć niektórych funkcji, musisz się najpierw zalogować:

```
$ docker login
Login with your Docker ID to push and pull images from Docker Hub. If you don't have a Docker ID, head over to https://hub.docker.com to create one.
Username: delner
Password: 
Login Succeeded
$
```

### Wyszukiwanie obrazów

Użyj polecenia `docker search`, aby wyszukiwać obrazy:

```
$ docker search kafka
NAME                        DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
wurstmeister/kafka          Multi-Broker Apache Kafka Image                 319                  [OK]
spotify/kafka               A simple docker image with both Kafka and ...   200                  [OK]
ches/kafka                  Apache Kafka. Tagged versions. JMX. Cluste...   70                   [OK]
sheepkiller/kafka-manager   kafka-manager                                   61                   [OK]
$
```

Gdy znajdziesz interesujący obraz, możesz pobrać go lokalnie poleceniem `docker pull` (omówione w ćwiczeniu „Running Containers”).

### Tagowanie obrazów

W poprzednim ćwiczeniu „Building Images” zbudowaliśmy i otagowaliśmy obraz jako `<DockerHub username>/ping`. Jeśli przez pomyłkę użyłeś innego tagu niż nazwa użytkownika na DockerHubie, to nic — możemy go prze-tagować.

Użyj `docker tag`, by dodać nowy tag z Twoją nazwą użytkownika i nadaj mu wersję:

```
$ docker images
REPOSITORY                                                TAG                 IMAGE ID            CREATED             SIZE
ping                                                      latest              a980ae1c79ea        2 minutes ago       121MB
ubuntu                                                    16.04               6a2f32de169d        5 days ago          117MB
$ docker tag ping delner/ping:1.0
$ docker images
REPOSITORY                                                TAG                 IMAGE ID            CREATED             SIZE
delner/ping                                               1.0                 a980ae1c79ea        5 minutes ago       121MB
ping                                                      latest              a980ae1c79ea        5 minutes ago       121MB
ubuntu                                                    16.04               6a2f32de169d        5 days ago          117MB
$ 
```

Widzisz, że to samo ID obrazu jest teraz przypisane do starego i nowego tagu. Aby usunąć stary tag, uruchom `docker rmi` z nazwą starego tagu:

```
$ docker rmi ping
Untagged: ping:latest
$ docker images
REPOSITORY                                                TAG                 IMAGE ID            CREATED             SIZE
delner/ping                                               1.0                 a980ae1c79ea        6 minutes ago       121MB
ubuntu                                                    16.04               6a2f32de169d        5 days ago          117MB
$ 
```

### Wysyłanie obrazów (push)

Aby wysłać obraz, wystarczy wywołać `docker push` z odpowiednim tagiem.

```
$ docker push delner/ping:1.0
The push refers to a repository [docker.io/delner/ping]
3b372b8ab44b: Pushed 
ab4b9ad8d212: Mounted from library/ubuntu 
57e913ee49e5: Mounted from library/ubuntu 
2ea6deead2b0: Mounted from library/ubuntu 
7cbd4b94e525: Mounted from library/ubuntu 
e86a0c422723: Mounted from library/ubuntu 
1.0: digest: sha256:1881fd1efdde061d3aede939b8696c0e6d0b36e9f8b38abccb1074bc60592a60 size: 1568
$
```

Automatycznie utworzy to nowe publiczne repozytorium na DockerHubie pod organizacją z tagu. Podając swoją nazwę użytkownika, utworzysz repozytorium pod adresem `https://hub.docker.com/r/<USERNAME>/ping/`. Śmiało, zajrzyj na stronę nowego repo!

Można też wysyłać obrazy do rejestrów innych niż DockerHub, np. AWS Elastic Container Registry, zmieniając część repozytorium w tagu tak, aby odpowiadała właściwemu URL.

# KONIEC ĆWICZENIA 4
