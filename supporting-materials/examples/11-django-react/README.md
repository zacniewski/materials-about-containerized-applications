11-django-react — ToDo (Django + React) na docker-compose

Opis
Prosta aplikacja ToDo z backendem w Django (Django REST Framework) i frontendem w React (Vite). Front komunikuje się z API przy użyciu axios.

Jak uruchomić
1. Przejdź do katalogu examples/11-django-react
2. Uruchom: docker compose up --build
3. Otwórz w przeglądarce:
   - Frontend (Vite): http://localhost:5173
   - Backend (API): http://localhost:8000/api/todos/

Architektura
- Service backend (Django + DRF)
  - Port: 8000
  - Endpointy API: /api/todos/ (CRUD) oraz /api/todos/{id}/toggle/ (POST)
  - CORS: domyślnie http://localhost:5173 (można zmienić env CORS_ORIGINS)
- Service frontend (React + Vite)
  - Port: 5173
  - axios łączy się z VITE_API_BASE (w compose ustawione http://localhost:8000)

Kluczowe pliki
- docker-compose.yaml
- backend/Dockerfile, backend/requirements.txt, backend/manage.py
- backend/server/settings.py, backend/server/urls.py, backend/server/wsgi.py
- backend/todos/* (model, serializer, viewset, admin)
- frontend/Dockerfile, frontend/package.json, frontend/vite.config.js, frontend/index.html
- frontend/src/main.jsx, frontend/src/App.jsx, frontend/src/api.js

Zmienne środowiskowe (compose)
- Backend: DJANGO_DEBUG=1, DJANGO_SECRET_KEY=change-me-in-dev, DJANGO_ALLOWED_HOSTS=*, CORS_ORIGINS=http://localhost:5173
- Frontend: VITE_API_BASE=http://localhost:8000

Sprzątanie
- Zatrzymanie: docker compose down
- Budowa bez kesza: docker compose build --no-cache
