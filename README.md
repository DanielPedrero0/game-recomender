# game-recomender
# Game Recommender — Arquitectura de Microservicios

¿Tienes 300 juegos en Steam sin jugar? Yo también. Por eso construí esto.

**Game Recommender** es un sistema backend basado en microservicios que gestiona tu biblioteca personal de videojuegos y te recomienda nuevos títulos automáticamente según tus géneros favoritos, consultando la API oficial de [IGDB](https://api-docs.igdb.com/) (Internet Game Database — más de 200.000 juegos).

---

## Arquitectura

```
┌─────────────────────┐         ┌──────────────────────────┐
│    game-service     │◄────────│   recommender-service    │
│  (Puerto 8001)      │  REST   │   (Puerto 8002)          │
│                     │         │                          │
│  - CRUD biblioteca  │         │  - Llama a game-service  │
│  - Géneros favoritos│         │  - Consulta IGDB API     │
│  - PostgreSQL       │         │  - Devuelve recomend.    │
└─────────────────────┘         └──────────────────────────┘
         │                                   │
         ▼                                   ▼
   [game-db :5432]                  [recommender-db :5433]
         
         ▲─────────────────────────────────────▲
                         │
                  [frontend :8501]
                  Streamlit UI
```

Cada microservicio tiene su **propia base de datos** y se comunican entre sí únicamente a través de HTTP REST — principio core de la arquitectura de microservicios.

---

## Stack tecnológico

- **Python 3.11** + **FastAPI** — framework async de alto rendimiento
- **SQLAlchemy** — ORM para PostgreSQL
- **Pydantic** — validación de datos de entrada y salida
- **PostgreSQL 15** — base de datos relacional (una por servicio)
- **Docker + Docker Compose** — orquestación de contenedores
- **IGDB API** — base de datos oficial de videojuegos (Twitch/Amazon)
- **httpx** — cliente HTTP async para comunicación entre servicios
- **Streamlit** — interfaz web para interactuar con la API

---

## Cómo levantar el proyecto

### Pre-requisitos
- Docker y Docker Compose instalados

### 1. Obtén tus credenciales de IGDB (gratis)
- Regístrate en [dev.twitch.tv](https://dev.twitch.tv/console)
- Crea una nueva aplicación
- Copia tu **Client ID** y genera un **Client Secret**

### 2. Crea el archivo `.env` en la raíz del proyecto
```env
IGDB_CLIENT_ID=tu_client_id
IGDB_CLIENT_SECRET=tu_client_secret
```

### 3. Levanta todo con un comando
```bash
docker-compose up --build
```

### 4. ¡Listo! Servicios disponibles en:

| Servicio | URL | Descripción |
|---|---|---|
| Frontend | http://localhost:8501 | Interfaz web Streamlit |
| game-service docs | http://localhost:8001/docs | API docs interactiva |
| recommender-service docs | http://localhost:8002/docs | API docs interactiva |

---

## 📖 Cómo usarlo

### Opción A — Interfaz web (Streamlit)
Abre `http://localhost:8501` y usa las tres pestañas:
- **Mi Biblioteca** — visualiza y filtra tus juegos
- **Añadir Juego** — añade juegos con género, plataforma y estado
- **Recomendaciones** — obtén sugerencias personalizadas por género

### Opción B — API directa

**Añade un juego:**
```bash
curl -X POST http://localhost:8001/games/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Witcher 3",
    "genre": "RPG",
    "platform": "PC",
    "status": "completado",
    "rating": 9.5
  }'
```

**Actualiza el estado:**
```bash
curl -X PATCH http://localhost:8001/games/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completado", "rating": 9.5}'
```

**Obtén recomendaciones:**
```bash
# Por género favorito automático
curl http://localhost:8002/recommendations/

# Por género concreto
curl http://localhost:8002/recommendations/?genre=FPS
```

El sistema automáticamente:
1. Consulta al `game-service` tus géneros más jugados
2. Traduce el género a la nomenclatura de IGDB (`RPG` → `Role-playing (RPG)`)
3. Busca en IGDB juegos de ese género con rating alto
4. Devuelve una lista de recomendaciones personalizadas

---

##  Estructura del proyecto

```
game-recommender/
├── docker-compose.yml
├── .env                        ← credenciales IGDB (no subir a Git)
├── .gitignore
├── game-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── database/session.py
│       ├── models/game.py
│       ├── schemas/game.py
│       └── routes/games.py
├── recommender-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── services/igdb.py    ← lógica IGDB + comunicación entre servicios
│       └── routes/recommendations.py
└── frontend/
    ├── Dockerfile
    ├── requirements.txt
    └── app.py                  ← interfaz Streamlit
```

---

##  Endpoints

### game-service (`:8001`)
| Método | Endpoint | Descripción |
|---|---|---|
| `POST` | `/games/` | Añade un juego a tu biblioteca |
| `GET` | `/games/` | Lista todos tus juegos (`?status=completado&genre=RPG`) |
| `GET` | `/games/{id}` | Obtiene un juego por id |
| `GET` | `/games/genres/top` | Géneros favoritos ordenados por frecuencia |
| `PATCH` | `/games/{id}` | Actualiza estado, puntuación o género |
| `DELETE` | `/games/{id}` | Elimina un juego |

### recommender-service (`:8002`)
| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/recommendations/` | Recomendaciones según género favorito |
| `GET` | `/recommendations/?genre=FPS` | Recomendaciones por género concreto |

### Géneros soportados
| Tu género | IGDB |
|---|---|
| `RPG` | Role-playing (RPG) |
| `FPS` | Shooter |
| `MOBA` | Strategy |
| `Aventura` | Adventure |
| `Deportes` | Sport |
| `Lucha` | Fighting |
| `Plataformas` | Platform |
| `Puzzles` | Puzzle |
| `Carreras` | Racing |

