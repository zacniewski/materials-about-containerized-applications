### Materiały z przedmiotu "Aplikacje w środowisku kontenerowym"

#### I. Wymagania
  - :zap: zainstalowany [Docker](https://docs.docker.com/get-started/get-docker/),
  - :zap: zainstalowany [Docker Compose](https://docs.docker.com/compose/),
  - :zap: konto na [DockerHub](https://hub.docker.com/),  
  - :zap: konto na [Coursera](https://www.coursera.org/).  

#### II. Laboratoria online
  - :zap: Kurs [Docker for Beginners with Hands-on labs](https://www.coursera.org/learn/docker-for-the-absolute-beginner) na platformie Coursera (wymagane konto),    
  - Play with Docker [labs](https://labs.play-with-docker.com/) (wymagane konto na `DockerHub`),    
  - :zap: Play with Docker [trainings](https://training.play-with-docker.com/) (wymagane konto na `DockerHub`),    
  > dla powyższego laboratorium (trainings) można wybrać między 'IT Pros and System Administrators' a 'Developers'.

#### III. Pożyteczne linki
  - [Docker](https://github.com/delner/docker-training/blob/master/README.md) training,  
  - [DevOps with Docker](https://devopswithdocker.com/) course (i także na [GitHub'ie](https://github.com/docker-hy/docker-hy.github.io)),  
  - [DevOps with Kubernetes](https://devopswithkubernetes.com/) training,  


#### IV. Zawartość repozytorium
  - :zap: folder [basic-docker-training](basic-docker-training/README.md) zawiera standardowe ćwiczenia z Dockera,  
  - :zap: folder [devops-with-docker](devops-with-docker) zawiera uaktualnioną wersję kursu 'DevOps with Docker',  
  - :zap: folder [final-repo-structure](final-repo-structure) zawiera sugerowaną strukturę repozytorium zaliczeniowego.  

#### V. Podział na bloki laboratoryjne
> Każdy blok składa się z trzech godzin zajęć,  
> planowanych jest 20 bloków (3 godz. x 20 = 60 godz.), w tym 1 blok "rezerwowy" (w razie potrzeby ukończenia pozostałych bloków).    


| Zagadnienie                                                         | Liczba bloków (godzin) |
|---------------------------------------------------------------------|------------------------|
| 1. Kurs "Docker for Beginners with Hands-on labs" (z Coursery)      | Bloki 1-3 (9 godzin)   |
| 2. Basic Docker training  (folder 'basic-docker-training' w repo)   | Bloki 4-6 (9 godzin)   |
| 3. Play with Docker trainings                                       | Bloki 7-8 (6 godzin)   |
| 4. DevOps with Docker (part 1) (folder 'devops-with-docker' w repo) | Bloki 9-11 (9 godzin)  |
| 5. DevOps with Docker (part 2)     (jak wyżej)                      | Bloki 12-14 (9 godzin) |
| 6. DevOps with Docker (part 3)     (jak wyżej)                      | Bloki 15-17 (9 godzin) |
| 7. Analiza projektu Docker'owego (np. własnego)                     | Bloki 18-19 (6 godzin) |
| 8. Blok rezerwowy                                                   | Blok 20 (3 godziny)    |
|                                                                     |                        |
| RAZEM:                                                              | Bloków: 20 (60 godzin) |


#### VI. Pytania, które mogą się pojawić na zaliczeniu (egzaminie)
1. Utwórz plik z obrazem `Dockerfile`, w którym z hosta do kontenera kopiowany będzie folder `code` (zawiera np. jeden skrypt w języku Python :snake:) i zbuduj go:  
    - uruchom ww. skrypt wewnątrz kontenera.
2. Skopiuj wybrany plik tekstowy z hosta (swojego komputera) do kontenera Dockerowego.
3. Skopiuj wybrany plik tekstowy z kontenera Dockerowego do hosta (swojego komputera).
4. Pokaż działanie komend `ENTRYPOINT` i `CMD` w wybranym projekcie.
5. Pokaż działanie usługi bazodanowej z wykorzystaniem `docker-compose`.
6. Pokaż działanie komend `ADD` i `COPY` i `WORKDIR` w wybranym projekcie.
7. Pokaż działanie `docker compose` w swoim projekcie.
8. Omów na podstawie swojej aplikacji komendy `docker inspect` i `docker logs`.
9. Czym są sieci w Dockerze? Zaprezentuj przykład na bazie swojego projektu.
10. Jaka jest różnica między obrazem i kontenerem? 
    Pokaż przykład budowania obrazu (`Dockerfile`) i uruchamiania na jego podstawie kontenera.
11. Pokaż jak "wejść" do wybranego kontenera.  
    Utwórz w nim plik tekstowy z dowolnymi danymi. 
    Co zrobić, żeby po zamknięciu kontenera dane z pliku były dostępne po ponownym uruchomieniu kontenera?  
    Zademonstruj dowolny sposób.
12. Zbuduj wybrany przez siebie obraz, nadaj mu 'tag' i opublikuj na DockerHubie. 
    Następnie usuń lokalnie ww. obraz i pobierz go z DockerHuba.  