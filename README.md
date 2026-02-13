# Projekt: Wirtualizacja i Konteneryzacja (WiK)
Aplikacja webowa z bazą danych i Reverse Proxy.

## Opis architektury
Projekt składa się z trzech kontenerów zarządzanych przez Docker Compose:
1. **Frontend/Proxy (Nginx):** Działa jako Reverse Proxy, udostępniając aplikację na porcie 80.
2. **Backend (Python/Flask):** Logika aplikacji. Kontener jest odizolowany w sieci wewnętrznej (brak bezpośredniego dostępu z zewnątrz).
3. **Baza danych (PostgreSQL):** Przechowuje notatki. Posiada trwały wolumin (persistence) oraz healthcheck.

## Jak uruchomić projekt?
Wymagane: Docker oraz Docker Compose.

1. Otwórz terminal w folderze projektu.
2. Uruchom polecenie:
   docker compose up -d --build

3. Aplikacja będzie dostępna pod adresem:
   http://localhost

## Funkcjonalności
- **Izolacja sieciowa:** Backend jest ukryty w prywatnej sieci `projekt-net`. Bezpośrednie wejście na port aplikacji (5000) jest zablokowane.
- **Healthcheck:** Backend oczekuje na pełne uruchomienie bazy danych przed startem (`depends_on: service_healthy`).
- **Trwałość danych:** Dane notatek są zapisywane w woluminie Dockera – nie znikają po restarcie kontenerów.
- **Interakcja :** Możliwość dodawania, wyświetlania i usuwania notatek (operacje INSERT, SELECT, DELETE).

## Zatrzymywanie
Aby zatrzymać projekt i posprzątać kontenery:
docker compose down