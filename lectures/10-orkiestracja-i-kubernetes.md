# Wykład 10: Orkiestracja kontenerów i wprowadzenie do Kubernetes (2 godz.)

## 10.1 Dlaczego potrzebujemy orkiestracji?

Gdy aplikacja składa się z wielu kontenerów rozproszonych na wielu hostach, potrzebujemy narzędzia do automatycznego zarządzania nimi.

```mermaid
graph TD
    PROB["Problemy w produkcji"] --> SC["Skalowanie<br/>Jak dodać więcej instancji?"]
    PROB --> HA["Wysoka dostępność<br/>Co gdy kontener padnie?"]
    PROB --> LB["Load balancing<br/>Jak rozdzielić ruch?"]
    PROB --> UP["Aktualizacje<br/>Jak wdrożyć bez downtime?"]
    PROB --> SD["Service discovery<br/>Jak kontenery się odnajdują?"]
    PROB --> MON["Monitoring<br/>Jak śledzić stan?"]
```

### Docker Compose vs orkiestracja

| Cecha | Docker Compose | Docker Swarm | Kubernetes |
|-------|---------------|-------------|------------|
| Hosty | Jeden | Wiele | Wiele |
| Skalowanie | Ręczne | Automatyczne | Automatyczne |
| Self-healing | ❌ | ✅ | ✅ |
| Load balancing | ❌ | ✅ | ✅ |
| Rolling updates | ❌ | ✅ | ✅ |
| Złożoność | Niska | Średnia | Wysoka |
| Użycie | Development | Mała produkcja | Duża produkcja |

## 10.2 Docker Swarm — powtórzenie i rozszerzenie

```mermaid
graph TD
    subgraph "Docker Swarm"
        M1["Manager 1<br/>(Leader)"]
        M2["Manager 2"]
        M3["Manager 3"]
        W1["Worker 1"]
        W2["Worker 2"]
        W3["Worker 3"]
        W4["Worker 4"]
    end
    
    M1 <-->|"Raft consensus"| M2
    M1 <-->|"Raft consensus"| M3
    M1 -->|"Zarządza"| W1
    M1 -->|"Zarządza"| W2
    M2 -->|"Zarządza"| W3
    M3 -->|"Zarządza"| W4
```

### Kluczowe pojęcia Swarm

| Pojęcie | Opis |
|---------|------|
| **Node** | Maszyna w klastrze (manager lub worker) |
| **Service** | Definicja zadania (obraz, repliki, porty) |
| **Task** | Pojedyncza instancja kontenera |
| **Stack** | Grupa powiązanych usług (z Compose file) |
| **Overlay network** | Sieć łącząca kontenery między hostami |

### Swarm w praktyce

```bash
# Inicjalizacja
docker swarm init

# Tworzenie usługi z replikami
docker service create --name api --replicas 5 --publish 8080:80 myapi:v1

# Rolling update
docker service update --image myapi:v2 --update-parallelism 2 --update-delay 10s api

# Rollback
docker service rollback api

# Globalny serwis (1 instancja na każdym node)
docker service create --mode global --name monitor prom/node-exporter

# Stack deploy
docker stack deploy -c docker-compose.yml myapp
docker stack ls
docker stack services myapp
docker stack rm myapp
```

## 10.3 Wprowadzenie do Kubernetes

Kubernetes (K8s) to **system orkiestracji kontenerów** stworzony przez Google, obecnie rozwijany przez CNCF. Jest standardem branżowym dla zarządzania kontenerami w produkcji.

```mermaid
graph TD
    subgraph "Control Plane"
        API["API Server"]
        ETCD["etcd<br/>(baza danych)"]
        SCHED["Scheduler"]
        CM["Controller Manager"]
    end
    
    subgraph "Worker Node 1"
        KL1["kubelet"]
        KP1["kube-proxy"]
        CR1["Container Runtime"]
        P1["Pod A"]
        P2["Pod B"]
    end
    
    subgraph "Worker Node 2"
        KL2["kubelet"]
        KP2["kube-proxy"]
        CR2["Container Runtime"]
        P3["Pod C"]
        P4["Pod D"]
    end
    
    API --> KL1
    API --> KL2
    API --> ETCD
    SCHED --> API
    CM --> API
```

### Architektura Kubernetes

| Komponent | Rola |
|-----------|------|
| **API Server** | Centralny punkt komunikacji (REST API) |
| **etcd** | Rozproszona baza klucz-wartość (stan klastra) |
| **Scheduler** | Przydziela Pody do Node'ów |
| **Controller Manager** | Utrzymuje pożądany stan (repliki, deployment) |
| **kubelet** | Agent na każdym Node (zarządza Podami) |
| **kube-proxy** | Zarządza siecią na Node |

## 10.4 Podstawowe obiekty Kubernetes

```mermaid
graph TD
    subgraph "Obiekty K8s"
        POD["Pod<br/>(najmniejsza jednostka)"]
        DEP["Deployment<br/>(zarządza ReplicaSet)"]
        RS["ReplicaSet<br/>(utrzymuje N replik)"]
        SVC["Service<br/>(load balancer)"]
        ING["Ingress<br/>(routing HTTP)"]
        CM2["ConfigMap<br/>(konfiguracja)"]
        SEC2["Secret<br/>(dane wrażliwe)"]
        PV["PersistentVolume<br/>(storage)"]
        NS["Namespace<br/>(izolacja)"]
    end
    
    DEP --> RS --> POD
    SVC --> POD
    ING --> SVC
```

### Pod
Najmniejsza jednostka w K8s — jeden lub więcej kontenerów współdzielących sieć i storage.

```yaml
# pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  containers:
    - name: app
      image: myapp:v1
      ports:
        - containerPort: 5000
      resources:
        limits:
          memory: "256Mi"
          cpu: "500m"
```

### Deployment
Zarządza cyklem życia Podów — skalowanie, aktualizacje, rollback.

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: app
          image: myapp:v1
          ports:
            - containerPort: 5000
          readinessProbe:
            httpGet:
              path: /health
              port: 5000
            initialDelaySeconds: 5
          livenessProbe:
            httpGet:
              path: /health
              port: 5000
            initialDelaySeconds: 15
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

### Service
Stabilny endpoint (IP + DNS) dla grupy Podów.

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 5000
  type: ClusterIP  # ClusterIP | NodePort | LoadBalancer
```

```mermaid
graph LR
    CLIENT["Klient"] --> SVC["Service<br/>myapp-service:80"]
    SVC --> P1["Pod 1<br/>:5000"]
    SVC --> P2["Pod 2<br/>:5000"]
    SVC --> P3["Pod 3<br/>:5000"]
```

## 10.5 kubectl — narzędzie CLI

```bash
# Informacje o klastrze
kubectl cluster-info
kubectl get nodes

# Zarządzanie Podami
kubectl get pods
kubectl describe pod myapp
kubectl logs myapp
kubectl exec -it myapp -- bash

# Deployment
kubectl apply -f deployment.yaml
kubectl get deployments
kubectl rollout status deployment/myapp
kubectl rollout undo deployment/myapp

# Skalowanie
kubectl scale deployment myapp --replicas=5

# Usługi
kubectl get services
kubectl expose deployment myapp --port=80 --target-port=5000

# Namespace
kubectl get namespaces
kubectl create namespace staging
```

## 10.6 Kubernetes vs Docker Swarm

```mermaid
graph LR
    subgraph "Docker Swarm"
        S1["✅ Prosty setup"]
        S2["✅ Wbudowany w Docker"]
        S3["✅ Docker Compose compatible"]
        S4["❌ Mniejszy ekosystem"]
        S5["❌ Mniej funkcji"]
    end
    
    subgraph "Kubernetes"
        K1["✅ Standard branżowy"]
        K2["✅ Ogromny ekosystem"]
        K3["✅ Zaawansowane funkcje"]
        K4["❌ Stroma krzywa uczenia"]
        K5["❌ Złożona konfiguracja"]
    end
```

| Cecha | Docker Swarm | Kubernetes |
|-------|-------------|------------|
| Krzywa uczenia | Łagodna | Stroma |
| Setup | Minuty | Godziny |
| Skalowanie | Dobre | Doskonałe |
| Ekosystem | Mały | Ogromny (Helm, Istio, ...) |
| Auto-scaling | Ręczne | HPA, VPA |
| Storage | Ograniczone | PV, PVC, StorageClass |
| Networking | Overlay | CNI (Calico, Flannel, ...) |
| Popularność | Malejąca | Dominująca |

## 10.7 Lokalne środowiska Kubernetes

```mermaid
graph TD
    LOCAL["Lokalne K8s"] --> MINI["Minikube"]
    LOCAL --> KIND["kind<br/>(K8s in Docker)"]
    LOCAL --> K3D["k3d<br/>(k3s in Docker)"]
    LOCAL --> DD["Docker Desktop<br/>(wbudowany K8s)"]
    LOCAL --> MICRO["MicroK8s"]
```

```bash
# Minikube
minikube start
minikube dashboard

# kind (Kubernetes in Docker)
kind create cluster
kind load docker-image myapp:v1

# k3d (k3s in Docker)
k3d cluster create mycluster
```

## 10.8 Helm — menedżer pakietów Kubernetes

```mermaid
graph LR
    HELM["Helm"] -->|"install"| CHART["Chart<br/>(pakiet)"]
    CHART --> REL["Release<br/>(instancja)"]
    
    subgraph "Chart"
        T["templates/"]
        V["values.yaml"]
        CH["Chart.yaml"]
    end
```

```bash
# Instalacja aplikacji z Helm
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install my-postgres bitnami/postgresql

# Własny chart
helm create myapp
helm install myapp ./myapp --values values-prod.yaml

# Aktualizacja
helm upgrade myapp ./myapp

# Rollback
helm rollback myapp 1
```

## 10.9 Przyszłość konteneryzacji

```mermaid
mindmap
  root((Przyszłość<br/>kontenerów))
    WebAssembly (WASM)
      Docker + WASM
      Lżejsze niż kontenery
      Bezpieczniejsze
    Serverless Containers
      AWS Fargate
      Google Cloud Run
      Azure Container Apps
    GitOps
      ArgoCD
      Flux
      Deklaratywne wdrożenia
    Service Mesh
      Istio
      Linkerd
      Observability
    AI/ML Workloads
      GPU containers
      Model serving
      Training pipelines
    eBPF
      Networking
      Security
      Observability
```

### Docker + WebAssembly

```bash
# Uruchomienie modułu WASM w Docker
docker run --runtime=io.containerd.wasmedge.v1 --platform=wasi/wasm myapp.wasm
```

### Trendy
- **WASM** — lżejsza alternatywa dla kontenerów (Docker już wspiera)
- **GitOps** — infrastruktura jako kod w Git (ArgoCD, Flux)
- **Service Mesh** — zaawansowane zarządzanie ruchem (Istio)
- **Serverless containers** — kontenery bez zarządzania infrastrukturą
- **eBPF** — nowa generacja networking i security w kontenerach

## 10.10 Podsumowanie kursu

```mermaid
graph TD
    subgraph "Co poznaliśmy"
        W1["Konteneryzacja<br/>i Docker"]
        W2["Obrazy<br/>i rejestry"]
        W3["Dockerfile<br/>i budowanie"]
        W4["Zarządzanie<br/>kontenerami"]
        W5["Wolumeny<br/>i dane"]
        W6["Sieci<br/>Docker"]
        W7["Docker<br/>Compose"]
        W8["Bezpieczeństwo<br/>i best practices"]
        W9["CI/CD<br/>i produkcja"]
        W10["Orkiestracja<br/>i Kubernetes"]
    end
    
    W1 --> W2 --> W3 --> W4 --> W5
    W5 --> W6 --> W7 --> W8 --> W9 --> W10
```

### Kluczowe umiejętności po kursie
1. Rozumienie konteneryzacji i jej zastosowań
2. Tworzenie i zarządzanie obrazami Docker
3. Pisanie efektywnych Dockerfile (multi-stage, cache, security)
4. Zarządzanie cyklem życia kontenerów
5. Trwałe przechowywanie danych (wolumeny)
6. Konfiguracja sieci Docker
7. Orkiestracja z Docker Compose
8. Stosowanie dobrych praktyk bezpieczeństwa
9. Integracja Docker z CI/CD
10. Podstawy orkiestracji (Swarm, Kubernetes)

### Pytania kontrolne
1. Kiedy Docker Compose nie wystarcza i potrzebna jest orkiestracja?
2. Jakie są główne komponenty architektury Kubernetes?
3. Czym jest Pod w Kubernetes?
4. Jak Kubernetes zapewnia wysoką dostępność?
5. Jakie są różnice między Docker Swarm a Kubernetes?
6. Co to jest Helm i do czego służy?

### Literatura
- Kubernetes Documentation: https://kubernetes.io/docs/
- Docker Swarm: https://docs.docker.com/engine/swarm/
- Helm: https://helm.sh/docs/
- CNCF Landscape: https://landscape.cncf.io/
- „Kubernetes in Action" — Marko Lukša
