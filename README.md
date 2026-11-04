# doniczka-ai-server

Serwer backendowy dla inteligentnej doniczki (Doniczka AI) oparty o **FastAPI**, **TimescaleDB** (PostgreSQL) oraz **AWS S3**.

Interaktywna dokumentacja Swagger UI jest dostępna domyślnie pod adresem:
- **Swagger UI:** `http://localhost/docs` (lub `http://localhost:8000/docs` przy uruchomieniu lokalnym)
- **ReDoc:** `http://localhost/redoc`

---

## Spis treści

- [Format odpowiedzi](#format-odpowiedzi)
- [Słowniki i typy wyliczeniowe](#słowniki-i-typy-wyliczeniowe)
- [Dokumentacja Endpointów](#dokumentacja-endpointów)
  - [Urządzenia (`/devices`)](#urządzenia-devices)
    - [GET /devices/{id}](#get-devicesid)
    - [POST /devices](#post-devices)
    - [PATCH /devices/{id}](#patch-devicesid)
    - [DELETE /devices/{id}](#delete-devicesid)
  - [Telemetria (`/devices/{id}/telemetry`)](#telemetria-devicesidtelemetry)
    - [GET /devices/{id}/telemetry](#get-devicesidtelemetry)
  - [Zdjęcia roślin (`/devices/{id}/photos`)](#zdjęcia-roślin-devicesidphotos)
    - [GET /devices/{id}/photos](#get-devicesidphotos)
    - [POST /devices/{id}/photos](#post-devicesidphotos)
  - [Logi zdarzeń (`/logs`, `/event-logs`)](#logi-zdarzeń-logs-event-logs)
    - [GET /devices/{id}/logs (oraz /devices/{id}/event-logs)](#get-devicesidlogs-oraz-devicesidevent-logs)
    - [GET /logs (oraz /event-logs)](#get-logs-oraz-event-logs)
  - [Ogólne](#ogólne)
    - [GET /](#get-)

---

## Format odpowiedzi

Większość endpointów zwraca ustandaryzowaną strukturę odpowiedzi JSON:

```json
{
  "status": "success",
  "data": { ... }
}
```

lub w przypadku operacji modyfikacji/usunięcia:

```json
{
  "status": "success",
  "message": "Komunikat informacyjny"
}
```

---

## Słowniki i typy wyliczeniowe

### `TelemetryPeriod` (okres telemetrii)
Wartość liczbowa dni brana pod uwagę przy filtrowaniu danych telemetrycznych oraz zdjęć:
- `1` – **DAY** (ostatnie 24 godziny / 1 dzień – wartość domyślna)
- `7` – **WEEK** (ostatnie 7 dni)
- `30` – **MONTH** (ostatnie 30 dni)
- `365` – **YEAR** (ostatni rok)

### `Severity` (ważność logu zdarzenia)
Poziom istotności wpisu w dzienniku zdarzeń:
- `1` – **POSITIVE** (sukces, zdarzenie pozytywne)
- `2` – **INFO** (informacja standardowa)
- `3` – **WARNING** (ostrzeżenie)
- `4` – **CRITICAL** (błąd krytyczny)

---

## Dokumentacja Endpointów

### Urządzenia (`/devices`)

#### `GET /devices/{id}`
Pobiera szczegółowe informacje o urządzeniu o podanym identyfikatorze.

- **Parametry ścieżki (Path params):**
  - `id` (`integer`, wymagany) – Identyfikator urządzenia.

- **Przykładowa odpowiedź (`200 OK`):**
  ```json
  {
    "status": "success",
    "data": {
      "device": {
        "id": 1,
        "name": "Doniczka Salon",
        "specification": {
          "sensor_version": "v1.2",
          "pump_installed": true
        }
      }
    }
  }
  ```

---

#### `POST /devices`
Tworzy nowe urządzenie w systemie.

- **Nagłówki:**
  - `Content-Type: application/json`

- **Ciało żądania (Request Body):**
  | Pole | Typ | Wymagane | Opis |
  | :--- | :--- | :--- | :--- |
  | `name` | `string` | Tak | Nazwa urządzenia |
  | `specification` | `object` | Nie | Opcjonalny słownik z dodatkową specyfikacją techniczną |

  ```json
  {
    "name": "Doniczka Kuchnia",
    "specification": {
      "light_type": "full-spectrum"
    }
  }
  ```

- **Przykładowa odpowiedź (`200 OK`):**
  ```json
  {
    "status": "success",
    "data": {
      "device": {
        "id": 2,
        "name": "Doniczka Kuchnia",
        "specification": {
          "light_type": "full-spectrum"
        }
      }
    }
  }
  ```

---

#### `PATCH /devices/{id}`
Aktualizuje dane istniejącego urządzenia.

- **Parametry ścieżki (Path params):**
  - `id` (`integer`, wymagany) – Identyfikator urządzenia do aktualizacji.

- **Nagłówki:**
  - `Content-Type: application/json`

- **Ciało żądania (Request Body):**
  | Pole | Typ | Wymagane | Opis |
  | :--- | :--- | :--- | :--- |
  | `name` | `string` | Tak | Zaktualizowana nazwa urządzenia |
  | `specification` | `object` | Nie | Zaktualizowana specyfikacja |

  ```json
  {
    "name": "Doniczka Kuchnia - Zioła",
    "specification": {
      "light_type": "full-spectrum",
      "firmware_version": "2.0.1"
    }
  }
  ```

- **Przykładowa odpowiedź (`200 OK`):**
  ```json
  {
    "status": "success",
    "data": {
      "device": {
        "id": 2,
        "name": "Doniczka Kuchnia - Zioła",
        "specification": {
          "light_type": "full-spectrum",
          "firmware_version": "2.0.1"
        }
      }
    }
  }
  ```

---

#### `DELETE /devices/{id}`
Usuwa urządzenie o wskazanym identyfikatorze.

- **Parametry ścieżki (Path params):**
  - `id` (`integer`, wymagany) – Identyfikator urządzenia.

- **Przykładowa odpowiedź (`200 OK`):**
  ```json
  {
    "status": "success",
    "message": "Device with id 2 has been deleted."
  }
  ```

---

### Telemetria (`/devices/{id}/telemetry`)

#### `GET /devices/{id}/telemetry`
Pobiera historię pomiarów telemetrii dla wskazanego urządzenia.

- **Parametry ścieżki (Path params):**
  - `id` (`integer`, wymagany) – Identyfikator urządzenia.

- **Parametry zapytania (Query params):**
  - `period` (`integer`, opcjonalny, domyślnie `1`) – Zakres czasu: `1` (dzień), `7` (tydzień), `30` (miesiąc), `365` (rok).
  - `limit` (`integer`, opcjonalny) – Maksymalna liczba zwracanych rekordów.

- **Przykładowa odpowiedź (`200 OK`):**
  ```json
  {
    "status": "success",
    "data": {
      "telemetry": [
        {
          "device_id": 1,
          "temperature": 22.5,
          "air_humidity": 55.0,
          "soil_top_humidity": 45.2,
          "soil_middle_humidity": 50.1,
          "soil_bottom_humidity": 58.7,
          "light_intensity": 850,
          "timestamp": "2026-11-04T10:00:00Z"
        }
      ]
    }
  }
  ```

---

### Zdjęcia roślin (`/devices/{id}/photos`)

#### `GET /devices/{id}/photos`
Pobiera listę zdjęć wykonanych przez dane urządzenie wraz z wygenerowanymi adresami URL (S3).

- **Parametry ścieżki (Path params):**
  - `id` (`integer`, wymagany) – Identyfikator urządzenia.

- **Parametry zapytania (Query params):**
  - `period` (`integer`, opcjonalny, domyślnie `1`) – Zakres czasu: `1` (dzień), `7` (tydzień), `30` (miesiąc), `365` (rok).
  - `limit` (`integer`, opcjonalny) – Maksymalna liczba zwracanych zdjęć.

- **Przykładowa odpowiedź (`200 OK`):**
  ```json
  {
    "status": "success",
    "data": {
      "photos": [
        {
          "id": 1,
          "device_id": 1,
          "path": "photos/1/2026-11-04_10-00-00.jpg",
          "timestamp": "2026-11-04T10:00:00Z",
          "url": "https://bucket-name.s3.region.amazonaws.com/photos/1/2026-11-04_10-00-00.jpg?..."
        }
      ]
    }
  }
  ```

---

#### `POST /devices/{id}/photos`
Zapisuje nowe zdjęcie rośliny w magazynie S3 oraz powiązany wpis w bazie danych.

- **Parametry ścieżki (Path params):**
  - `id` (`integer`, wymagany) – Identyfikator urządzenia.

- **Nagłówki:**
  - `Content-Type: multipart/form-data`

- **Ciało formularza (Form Data):**
  | Pole | Typ | Wymagane | Opis |
  | :--- | :--- | :--- | :--- |
  | `photo` | `file` (binary) | Tak | Plik ze zdjęciem |
  | `timestamp` | `string` (datetime ISO 8601) | Tak | Data i godzina wykonania zdjęcia, np. `2026-11-04T10:00:00Z` |

- **Przykładowa odpowiedź (`200 OK`):**
  ```json
  {
    "status": "success",
    "message": "Plant photo stored successfully."
  }
  ```

---

### Logi zdarzeń (`/logs`, `/event-logs`)

#### `GET /devices/{id}/logs` oraz `/devices/{id}/event-logs`
Zwraca wpisy dziennika zdarzeń powiązane z konkretnym urządzeniem.

- **Parametry ścieżki (Path params):**
  - `id` (`integer`, wymagany) – Identyfikator urządzenia.

- **Parametry zapytania (Query params):**
  - `limit` (`integer`, opcjonalny) – Maksymalna liczba zwracanych logów.

- **Przykładowa odpowiedź (`200 OK`):**
  ```json
  {
    "status": "success",
    "data": {
      "logs": [
        {
          "id": 10,
          "device_id": 1,
          "content": "Podlewanie zostało pomyślnie uruchomione.",
          "severity": 1,
          "timestamp": "2026-11-04T08:30:00Z"
        }
      ],
      "event_logs": [
        {
          "id": 10,
          "device_id": 1,
          "content": "Podlewanie zostało pomyślnie uruchomione.",
          "severity": 1,
          "timestamp": "2026-11-04T08:30:00Z"
        }
      ]
    }
  }
  ```

---

#### `GET /logs` oraz `/event-logs`
Zwraca wpisy dziennika zdarzeń dla wszystkich urządzeń.

- **Parametry zapytania (Query params):**
  - `limit` (`integer`, opcjonalny) – Maksymalna liczba zwracanych logów.

- **Przykładowa odpowiedź (`200 OK`):**
  ```json
  {
    "status": "success",
    "data": {
      "logs": [
        {
          "id": 10,
          "device_id": 1,
          "content": "Niski poziom wilgotności gleby.",
          "severity": 3,
          "timestamp": "2026-11-04T08:00:00Z"
        }
      ],
      "event_logs": [
        {
          "id": 10,
          "device_id": 1,
          "content": "Niski poziom wilgotności gleby.",
          "severity": 3,
          "timestamp": "2026-11-04T08:00:00Z"
        }
      ]
    }
  }
  ```

---

### Ogólne

#### `GET /`
Główny endpoint (root/healthcheck).
- **Zwracana wartość:** `null` / pusty response (status 200).

