# Wykład 1: Wprowadzenie do konteneryzacji (2 godz.)

## 1.1 Czym jest konteneryzacja?

Konteneryzacja to metoda wirtualizacji na poziomie systemu operacyjnego, która pozwala uruchamiać aplikacje w izolowanych środowiskach zwanych **kontenerami**. W odróżnieniu od tradycyjnej wirtualizacji (maszyny wirtualne), kontenery współdzielą jądro systemu operacyjnego hosta, co czyni je znacznie lżejszymi i szybszymi.

### Kluczowe cechy konteneryzacji
- **Izolacja** — każdy kontener działa niezależnie od innych
- **Przenośność** — kontener działa tak samo na każdej maszynie
- **Lekkość** — brak potrzeby emulacji całego systemu operacyjnego
- **Szybkość** — uruchomienie kontenera trwa sekundy, nie minuty
- **Skalowalność** — łatwe tworzenie wielu instancji tej samej aplikacji

## 1.2 Historia konteneryzacji

```mermaid
timeline
    title Historia konteneryzacji
    1979 : chroot (Unix V7)
    2000 : FreeBSD Jails
    2004 : Solaris Zones
    2006 : cgroups (Google)
    2008 : LXC (Linux Containers)
    2013 : Docker (dotCloud)
    2014 : Kubernetes (Google)
    2015 : Open Container Initiative (OCI)
    2017 : containerd jako projekt CNCF
    2020 : Docker Desktop dla Linux
    2024 : Docker z WASM i AI
```

### Kamienie milowe
| Rok  | Wydarzenie | Znaczenie |
|------|-----------|-----------|
| 1979 | `chroot`  | Pierwsza forma izolacji systemu plików w Unix |
| 2006 | cgroups   | Google wprowadza kontrolę zasobów w jądrze Linux |
| 2008 | LXC       | Pierwsze pełne kontenery Linux |
| 2013 | Docker    | Rewolucja — kontenery stają się dostępne dla każdego |
| 2014 | Kubernetes| Orkiestracja kontenerów na dużą skalę |

## 1.3 Maszyny wirtualne vs kontenery

```mermaid
graph TB
    subgraph VM["Maszyna wirtualna"]
        A1[Aplikacja A] --> GOS1[Guest OS]
        A2[Aplikacja B] --> GOS2[Guest OS]
        GOS1 --> HV[Hypervisor]
        GOS2 --> HV
        HV --> HW1[Sprzęt / Host OS]
    end

    subgraph Container["Kontenery"]
        B1[Aplikacja A] --> CR1[Container Runtime]
        B2[Aplikacja B] --> CR1
        CR1 --> HOS[Host OS + Kernel]
        HOS --> HW2[Sprzęt]
    end
```

### Porównanie

| Cecha | Maszyna wirtualna | Kontener |
|-------|-------------------|----------|
| Izolacja | Pełna (osobne jądro) | Na poziomie procesu |
| Rozmiar | GB (pełny OS) | MB (tylko aplikacja + zależności) |
| Czas startu | Minuty | Sekundy |
| Wydajność | Narzut hypervisora | Bliska natywnej |
| Przenośność | Ograniczona | Bardzo wysoka |
| Gęstość | Dziesiątki na host | Setki/tysiące na host |
| Bezpieczeństwo | Silna izolacja | Słabsza izolacja (współdzielone jądro) |

## 1.4 Technologie stojące za kontenerami Linux

Kontenery w Linuxie opierają się na trzech kluczowych mechanizmach jądra:

### Namespaces (przestrzenie nazw)
Zapewniają **izolację** — każdy kontener widzi własny „świat":

```mermaid
graph LR
    subgraph "Namespace'y Linuxa"
        PID["PID — procesy"]
        NET["NET — sieć"]
        MNT["MNT — system plików"]
        UTS["UTS — hostname"]
        IPC["IPC — komunikacja międzyprocesowa"]
        USER["USER — użytkownicy"]
        CGROUP["CGROUP — widoczność cgroups"]
    end
```

- **PID namespace** — kontener widzi tylko swoje procesy (PID 1 = główny proces kontenera)
- **NET namespace** — własny stos sieciowy, interfejsy, tablice routingu
- **MNT namespace** — własny system plików (overlay filesystem)
- **UTS namespace** — własna nazwa hosta
- **IPC namespace** — izolacja komunikacji międzyprocesowej
- **USER namespace** — mapowanie użytkowników (root w kontenerze ≠ root na hoście)

### cgroups (Control Groups)
Zapewniają **kontrolę zasobów** — limitowanie CPU, pamięci, I/O:

```mermaid
graph TD
    CG[cgroups] --> CPU["CPU — limit rdzeni/czasu"]
    CG --> MEM["Memory — limit RAM"]
    CG --> IO["Block I/O — limit dysku"]
    CG --> NET2["Network — limit przepustowości"]
    CG --> PIDS["PIDs — limit liczby procesów"]
```

### Union Filesystem (OverlayFS)
Zapewnia **warstwowy system plików** — obrazy składają się z warstw tylko do odczytu, a kontener dodaje warstwę zapisu:

```mermaid
graph BT
    RW["Warstwa zapisu (R/W) — kontener"] --> OV[OverlayFS]
    R3["Warstwa 3 (R/O) — apt install"] --> OV
    R2["Warstwa 2 (R/O) — COPY pliki"] --> OV
    R1["Warstwa 1 (R/O) — obraz bazowy Ubuntu"] --> OV
```

## 1.5 Ekosystem konteneryzacji

```mermaid
graph TB
    subgraph "Ekosystem kontenerowy"
        D[Docker] --> CR[Container Runtime]
        P[Podman] --> CR
        CR --> CON[containerd]
        CR --> CRIO[CRI-O]
        CON --> RUNC[runc]
        CRIO --> RUNC
        
        K[Kubernetes] --> CON
        K --> CRIO
        
        REG[Rejestry obrazów]
        REG --> DH[Docker Hub]
        REG --> GCR[GitHub Container Registry]
        REG --> ECR[AWS ECR]
        REG --> ACR[Azure ACR]
    end
```

### Główne narzędzia
- **Docker** — najpopularniejsza platforma kontenerowa (nasze główne narzędzie)
- **Podman** — alternatywa bez demona (daemonless)
- **containerd** — runtime kontenerów (używany przez Docker i Kubernetes)
- **Kubernetes (K8s)** — orkiestracja kontenerów na dużą skalę
- **Docker Compose** — orkiestracja wielu kontenerów na jednym hoście

## 1.6 Zastosowania kontenerów w praktyce

### Typowe scenariusze użycia

```mermaid
mindmap
  root((Kontenery))
    Rozwój oprogramowania
      Jednolite środowisko dev
      Szybkie prototypowanie
      CI/CD pipelines
    Mikroserwisy
      Niezależne wdrażanie
      Skalowanie per serwis
      Izolacja awarii
    DevOps
      Infrastructure as Code
      Immutable infrastructure
      GitOps
    Chmura
      AWS ECS/EKS
      Azure AKS
      Google GKE
    Edge Computing
      IoT
      Lekkie środowiska
```

### Kto używa kontenerów?
- **Netflix** — tysiące mikroserwisów
- **Spotify** — ponad 1800 serwisów w kontenerach
- **Google** — uruchamia miliardy kontenerów tygodniowo
- **Allegro** — mikroserwisy na Kubernetes

## 1.7 Architektura Docker

```mermaid
graph LR
    CLI["Docker CLI<br/>(docker build, run, ...)"] -->|REST API| DAEMON["Docker Daemon<br/>(dockerd)"]
    DAEMON --> CONTAINERD["containerd"]
    CONTAINERD --> RUNC["runc"]
    RUNC --> C1["Kontener 1"]
    RUNC --> C2["Kontener 2"]
    DAEMON --> IMG["Zarządzanie obrazami"]
    DAEMON --> VOL["Zarządzanie wolumenami"]
    DAEMON --> NET["Zarządzanie sieciami"]
    
    REG["Docker Registry<br/>(Docker Hub)"] <-->|push/pull| DAEMON
```

### Komponenty Docker
1. **Docker CLI** — interfejs wiersza poleceń
2. **Docker Daemon (dockerd)** — serwer zarządzający kontenerami
3. **containerd** — runtime kontenerów
4. **runc** — niskopoziomowy runtime (tworzy kontenery)
5. **Docker Registry** — repozytorium obrazów (Docker Hub)

## 1.8 Instalacja Dockera

### Linux (Ubuntu/Debian)
```bash
# Aktualizacja pakietów
sudo apt-get update

# Instalacja zależności
sudo apt-get install -y ca-certificates curl gnupg

# Dodanie klucza GPG Dockera
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Dodanie repozytorium
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalacja Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Dodanie użytkownika do grupy docker
sudo usermod -aG docker $USER
```

### Weryfikacja instalacji
```bash
docker --version
docker compose version
docker run hello-world
```

## 1.9 Podstawowe pojęcia

```mermaid
graph TD
    DF[Dockerfile] -->|docker build| IMG[Obraz / Image]
    IMG -->|docker run| CONT[Kontener / Container]
    IMG -->|docker push| REG[Rejestr / Registry]
    REG -->|docker pull| IMG
    CONT -->|docker commit| IMG2[Nowy obraz]
    
    style DF fill:#f9f,stroke:#333
    style IMG fill:#bbf,stroke:#333
    style CONT fill:#bfb,stroke:#333
    style REG fill:#fbb,stroke:#333
```

| Pojęcie | Opis |
|---------|------|
| **Obraz (Image)** | Szablon tylko do odczytu, zawierający aplikację i jej zależności |
| **Kontener (Container)** | Uruchomiona instancja obrazu — izolowany proces |
| **Dockerfile** | Plik tekstowy z instrukcjami budowania obrazu |
| **Rejestr (Registry)** | Magazyn obrazów (np. Docker Hub) |
| **Warstwa (Layer)** | Pojedyncza zmiana w obrazie (każda instrukcja Dockerfile = warstwa) |
| **Tag** | Etykieta wersji obrazu (np. `ubuntu:22.04`) |
| **Wolumen (Volume)** | Trwałe przechowywanie danych poza kontenerem |

## 1.10 Podsumowanie

- Konteneryzacja to lekka forma wirtualizacji na poziomie OS
- Docker to najpopularniejsze narzędzie do pracy z kontenerami
- Kontenery opierają się na namespaces, cgroups i union filesystem
- Obraz to szablon, kontener to uruchomiona instancja obrazu
- Kontenery rewolucjonizują sposób tworzenia, dostarczania i uruchamiania aplikacji

### Pytania kontrolne
1. Czym różni się kontener od maszyny wirtualnej?
2. Jakie mechanizmy jądra Linux umożliwiają działanie kontenerów?
3. Jaka jest różnica między obrazem a kontenerem?
4. Wymień trzy zalety konteneryzacji.
5. Jakie komponenty wchodzą w skład architektury Docker?

### Literatura
- Docker Documentation: https://docs.docker.com/
- „Docker Deep Dive" — Nigel Poulton
- „Konteneryzacja z Dockerem" — materiały kursu
