# Przykład 03: Python + API Open-Meteo

Prosty skrypt w Pythonie pobierający dane pogodowe dla Gdyni z darmowego API Open-Meteo. Pokazuje jak przekazywać zmienne środowiskowe do kontenera.

## Instrukcje

1. **Budowanie obrazu:**
   ```bash
   docker build -t meteo-gdynia .
   ```

2. **Uruchomienie skryptu (domyślne parametry):**
   ```bash
   docker run --rm meteo-gdynia
   ```

3. **Uruchomienie z własnymi parametrami (zmienne środowiskowe):**
   ```bash
   docker run --rm -e HOURS_AHEAD=12 -e LAT=54.52 -e LON=18.53 meteo-gdynia
   ```

## Zmienne środowiskowe
| Zmienna | Opis | Domyślnie |
|---------|------|-----------|
| `LAT` | Szerokość geograficzna | `54.52` (Gdynia) |
| `LON` | Długość geograficzna | `18.53` (Gdynia) |
| `HOURS_AHEAD` | Liczba godzin prognozy | `24` |
| `TIMEZONE` | Strefa czasowa | `Europe/Warsaw` |

## Kluczowe aspekty
- **`--rm`:** Automatycznie usuwa kontener po zakończeniu działania skryptu (dobra praktyka dla kontenerów typu "one-shot").
- **`-e`:** Przekazuje zmienne środowiskowe, które skrypt Pythona odczytuje przez `os.getenv()`.
