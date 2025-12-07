# Mood to Makan 🍽️✨

**Mood to Makan** is an intelligent food recommendation platform that helps users discover what to eat based on their current mood. By leveraging AI and vector search, it connects users with local UMKM (MSMEs) offering dishes that match their emotional state and cravings.

## 🚀 Features

-   **Mood-Based Search**: Describe how you feel (e.g., "Sad and need comfort food", "Celebrating with friends"), and get personalized food recommendations.
-   **AI-Powered Descriptions**: Automatically generate appetizing descriptions and "mood tags" for food items using AI.
-   **UMKM Dashboard**: Dedicated portal for business owners to manage their stores, menus, and view analytics.
-   **User Reviews**: Community-driven ratings and reviews for dishes.
-   **Personalized Recommendations**: Suggestions based on past order history and taste preferences.

## 🛠️ Tech Stack

### Backend
-   **Framework**: FastAPI (Python)
-   **Database**: PostgreSQL with `pgvector` extension (for semantic search)
-   **ORM**: SQLAlchemy
-   **Migrations**: Alembic
-   **AI/LLM**: LangChain (Integration with OpenAI / Google Gemini)
-   **Package Manager**: uv

### Frontend
-   **Framework**: Nuxt 3 (Vue.js)
-   **Styling**: Tailwind CSS
-   **State Management**: Pinia
-   **HTTP Client**: Nuxt `useFetch`

### Infrastructure
-   **Containerization**: Docker & Docker Compose

## 📋 Prerequisites

-   [Docker Desktop](https://www.docker.com/products/docker-desktop/)
-   [Node.js](https://nodejs.org/) (v18+)
-   [Python](https://www.python.org/) (v3.10+)
-   [uv](https://github.com/astral-sh/uv) (Fast Python package installer)

## ⚙️ Installation & Setup

### Option 1: Run with Docker (Recommended)

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd mood-to-makan
    ```

2.  **Environment Setup**
    -   Create a `.env` file in the `backend/` directory based on `backend/example.env`.
    -   Create a `.env` file in the `frontend/` directory based on `frontend/.env.example`.
    -   Ensure you have valid API keys for OpenAI or Gemini if you want to use AI features.

3.  **Start the Application**
    ```bash
    docker-compose up -d --build
    ```
    -   Frontend: http://localhost:3000
    -   Backend API: http://localhost:8007
    -   API Docs: http://localhost:8007/docs

### Option 2: Run Locally

#### Database Setup
You need a PostgreSQL instance running with the `pgvector` extension. You can use the docker service for just the DB:
```bash
docker-compose up -d db
```

#### Backend Setup
1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```
2.  Install dependencies:
    ```bash
    uv sync
    ```
3.  Run Migrations:
    ```bash
    uv run alembic upgrade head
    ```
4.  Start the server:
    ```bash
    uv run uvicorn app.main:app --reload
    ```
    The backend will run on `http://localhost:8000`.

#### Frontend Setup
1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2.  Setup Environment Variables:
    -   Create a `.env` file based on `.env.example`.
3.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm run dev
    ```
    The frontend will run on `http://localhost:3000`.

## 🗄️ Database Seeding

To populate the database with initial data (categories, sample foods, etc.):

```bash
cd backend
uv run python init/seed_all_tables.py
```

## 🐘 Database Migrations (Alembic)

We use Alembic for database schema migrations.

### Common Commands

**1. Create a new migration (after changing models)**
```bash
cd backend
uv run alembic revision --autogenerate -m "describe_your_change"
```

**2. Apply migrations (update database)**
```bash
cd backend
uv run alembic upgrade head
```

**3. Rollback last migration**
```bash
cd backend
uv run alembic downgrade -1
```

## 📂 Project Structure

```
mood-to-makan/
├── backend/                # FastAPI Application
│   ├── app/
│   │   ├── api/            # API Routes
│   │   ├── core/           # Config & Security
│   │   ├── models/         # Database Models
│   │   ├── schemas/        # Pydantic Schemas
│   │   └── services/       # Business Logic (AI, S3, etc.)
│   ├── alembic/            # Database Migrations
│   └── init/               # Seeding Scripts
├── frontend/               # Nuxt 3 Application
│   ├── app/
│   │   ├── components/     # Vue Components
│   │   ├── pages/          # Application Routes
│   │   └── stores/         # Pinia State Stores
│   └── server/             # Nuxt Server Routes
└── docker-compose.yml      # Docker Orchestration
```

## 🔑 Environment Variables

### Backend (`backend/.env`)

```ini
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/mood2makan
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Configuration (Choose one or both)
OPENROUTER_API_KEY=sk-or-...
GEMINI_API_KEY=AIza...
```

### Frontend (`frontend/.env`)

```ini
API_URL=http://localhost:8000/api/v1
HOST=0.0.0.0
PORT=3000
NUXT_API_PROXY_TARGET=http://localhost:8000/api/v1
```