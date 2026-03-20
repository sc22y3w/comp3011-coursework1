# Pokemon App

A Django web application for browsing Pokemon data, building teams, and analysing team effectiveness. It exposes a REST API and provides a Bootstrap-based web frontend.

## Prerequisites

- Python 3.10+
- pip

## Setup & Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd comp3011-coursework1
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux / macOS
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**

   ```bash
   cd django_project
   python manage.py migrate
   ```


7. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

   The app is now available at `http://localhost:8000/`.

## Running Tests

```bash
cd django_project
python manage.py test pokemon_app
```

This runs the full API test suite (41 test cases covering authentication, Pokemon listing, team CRUD, analysis, and statistics).

## Frontend Pages

| Route | Auth Required | Description |
|-------|---------------|-------------|
| `/` | No | Homepage — public teams with search and type filtering |
| `/login/` | No | Login page |
| `/register/` | No | Registration page |
| `/pokemon/` | No | Searchable, filterable Pokemon table |
| `/team/create/` | Yes | Create a new 6-Pokemon team |
| `/team/<id>/edit/` | Yes | Edit an existing team |
| `/team/<id>/analysis/` | No | Team type effectiveness analysis |
| `/teams/` | Yes | View and manage your teams |
| `/global-stats/` | No | Top Pokemon and type usage statistics |
| `/admin/` | Yes (staff) | Django admin panel |

## API Documentation

Full API documentation — including all endpoints, parameters, request/response formats, example `curl` commands, authentication flow, and error codes — is available in **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)**...

## Used Scripts
1. **Import the Pokemon dataset:**

   The `pokemon.csv` file contains 801 Pokemon. Import it into the SQLite database:

   ```bash
   python import_pokemon.py
   ```

   This creates `PokemonType`, `Ability`, and `Pokemon` records. The script is idempotent and can be safely re-run.

2. **Populate sample teams:**

   ```bash
   python populate_random_teams.py
   ```
