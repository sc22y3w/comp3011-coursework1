# Pokemon App

A Django web application that serves Pokemon data via a REST API and displays it in a web interface.

## API Endpoints

All API endpoints are prefixed with `/api/` and return JSON responses with `Content-Type: application/json`.

### Authentication

Non-browser clients can register and log in directly using JSON API calls.
The frontend web pages at `/register/` and `/login/` also use these same API endpoints via JavaScript `fetch`.

#### Register

```
POST /api/auth/users/
```

**Content-Type:** `application/json`

```json
{
  "username": "misty",
  "password": "staryu123"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `username` | string | Yes | Desired username |
| `password` | string | Yes | Password (must pass Django's validators: min 8 chars, not common, not entirely numeric) |

**Response Codes:**

| Status Code | Description | Response Body |
|-------------|-------------|---------------|
| `201 Created` | Account created | `{"message": "Registration successful", "username": "misty"}` |
| `400 Bad Request` | Missing fields, invalid JSON, or weak password | `{"error": "<message>"}` |
| `409 Conflict` | Username already exists | `{"error": "Username already exists"}` |

---

#### Login

```
POST /api/auth/sessions/
```

**Content-Type:** `application/json`

```json
{
  "username": "misty",
  "password": "staryu123"
}
```

**Response Codes:**

| Status Code | Description | Response Body |
|-------------|-------------|---------------|
| `200 OK` | Logged in, session cookie set | `{"message": "Login successful", "username": "misty"}` |
| `400 Bad Request` | Missing fields or invalid JSON | `{"error": "<message>"}` |
| `401 Unauthorized` | Invalid credentials | `{"error": "Invalid username or password"}` |

---

#### Logout

```
POST /api/auth/sessions/logout/
```

Destroys the current session. Requires authentication.

**Response Codes:**

| Status Code | Description | Response Body |
|-------------|-------------|---------------|
| `200 OK` | Logged out | `{"message": "Logout successful"}` |
| `401 Unauthorized` | Not logged in | `{"error": "Authentication credentials were not provided"}` |

---

### Protected Endpoints

The following endpoints require a logged-in user (session cookie). If a request is made without authentication, the API returns:

- `401 Unauthorized`
- `{"error": "Authentication credentials were not provided"}`

Protected endpoints:
- `POST /api/teams/`
- `PUT /api/teams/<id>/`
- `DELETE /api/teams/<id>/`
- `POST /api/auth/sessions/logout/`

---

### Get All Pokemon

```
GET /api/pokemon/
```

Returns a list of all Pokemon with their stats, types, abilities, and type matchup multipliers.

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `sort_type` | string | Filter Pokemon to only those matching a single type (e.g. `fire`). |
| `sort_types` | comma-separated strings | Filter Pokemon to only those matching **all** listed types (e.g. `fire,flying`). |
| `limit` | integer | Maximum number of results to return (must be >= 1). |
| `offset` | integer | Number of results to skip (must be >= 0, default `0`). |

Example:

```
GET /api/pokemon/?sort_types=fire,flying&limit=10&offset=0
```

#### Response Format

**Content-Type:** `application/json`

```json
{
  "count": 801,
  "limit": 10,
  "offset": 0,
  "pokemon": [
    {
      "id": 1,
      "name": "Bulbasaur",
      "types": ["Grass", "Poison"],
      "abilities": ["Overgrow", "Chlorophyll"],
      "hp": 45,
      "attack": 49,
      "defense": 49,
      "special_attack": 65,
      "special_defense": 65,
      "speed": 45,
      "against_bug": 1.0,
      "against_dark": 1.0,
      "against_dragon": 1.0,
      "against_electric": 0.5,
      "against_fairy": 0.5,
      "against_fighting": 0.5,
      "against_fire": 2.0,
      "against_flying": 2.0,
      "against_ghost": 1.0,
      "against_grass": 0.25,
      "against_ground": 1.0,
      "against_ice": 2.0,
      "against_normal": 1.0,
      "against_poison": 1.0,
      "against_psychic": 2.0,
      "against_rock": 1.0,
      "against_steel": 1.0,
      "against_water": 0.5
    }
  ]
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `count` | integer | Total number of matching Pokemon (before pagination) |
| `limit` | integer or null | The limit applied, or `null` if no limit was set |
| `offset` | integer | The offset applied |
| `pokemon` | array | List of Pokemon objects |
| `pokemon[].id` | integer | Unique identifier |
| `pokemon[].name` | string | Pokemon name |
| `pokemon[].types` | array of strings | The Pokemon's type(s) |
| `pokemon[].abilities` | array of strings | The Pokemon's abilities |
| `pokemon[].hp` | integer | Hit Points stat |
| `pokemon[].attack` | integer | Attack stat |
| `pokemon[].defense` | integer | Defense stat |
| `pokemon[].special_attack` | integer | Special Attack stat |
| `pokemon[].special_defense` | integer | Special Defense stat |
| `pokemon[].speed` | integer | Speed stat |
| `pokemon[].against_*` | float | Damage multiplier against the specified type (e.g. `2.0` = double damage, `0.5` = half damage) |

#### Response Codes

| Status Code | Description |
|-------------|-------------|
| `200 OK` | Successfully retrieved Pokemon data |
| `400 Bad Request` | Unknown type(s), or invalid `limit`/`offset` value |
| `405 Method Not Allowed` | Request used an unsupported HTTP method (only `GET` is supported) |

---

### Get All Teams

```
GET /api/teams/
```

Returns a list of Pokemon teams. **Authenticated users** see all public teams plus their own private teams. **Unauthenticated users** see only public teams.

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `types` | comma-separated strings | Filter teams to only those whose Pokemon collectively cover **all** listed types. For example, `types=fire,water,fairy` returns teams that have at least one Fire-type Pokemon, at least one Water-type Pokemon, **and** at least one Fairy-type Pokemon — they do not need to be the same Pokemon. |

Example:

```
GET /api/teams/?types=fire,water,fairy
```

#### Response Format

**Content-Type:** `application/json`

```json
{
  "teams": [
    {
      "id": 1,
      "name": "My Fire Team",
      "public": true,
      "owner": "misty",
      "pokemon": [
        {"id": 4, "name": "Charmander", "types": ["Fire"]},
        {"id": 5, "name": "Charmeleon", "types": ["Fire"]},
        {"id": 6, "name": "Charizard", "types": ["Fire", "Flying"]},
        {"id": 37, "name": "Vulpix", "types": ["Fire"]},
        {"id": 38, "name": "Ninetales", "types": ["Fire"]},
        {"id": 77, "name": "Ponyta", "types": ["Fire"]}
      ]
    }
  ]
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `teams` | array | List of team objects |
| `teams[].id` | integer | Unique identifier for the team |
| `teams[].name` | string | Name of the team |
| `teams[].public` | boolean | Whether the team is publicly visible |
| `teams[].owner` | string or null | Username of the team's owner, or `null` if unowned |
| `teams[].pokemon` | array of objects | The 6 Pokemon in the team, each with `id`, `name`, and `types` |
| `teams[].pokemon[].types` | array of strings | The Pokemon's type(s) |

#### Response Codes

| Status Code | Description |
|-------------|-------------|
| `200 OK` | Successfully retrieved teams |
| `400 Bad Request` | Unknown type(s) in the `types` parameter (response includes `valid_types` list) |
| `405 Method Not Allowed` | Request used an unsupported HTTP method |

---

### Get a Single Team

```
GET /api/teams/<id>/
```

Returns a single team by its ID. No authentication required.

#### Response Format

Same structure as a single item in the `GET /api/teams/` response:

```json
{
  "id": 1,
  "name": "My Fire Team",
  "public": true,
  "owner": "misty",
  "pokemon": [
    {"id": 4, "name": "Charmander"},
    {"id": 5, "name": "Charmeleon"},
    {"id": 6, "name": "Charizard"},
    {"id": 37, "name": "Vulpix"},
    {"id": 38, "name": "Ninetales"},
    {"id": 77, "name": "Ponyta"}
  ]
}
```

#### Response Codes

| Status Code | Description |
|-------------|-------------|
| `200 OK` | Successfully retrieved team |
| `404 Not Found` | Team with the given ID does not exist |
| `405 Method Not Allowed` | Request used an unsupported HTTP method |

---

### Create a Pokemon Team

```
POST /api/teams/
```

Creates a new Pokemon team with 6 Pokemon. Requires authentication. The team is automatically assigned to the authenticated user as its owner.

#### Request Format

**Content-Type:** `application/json`

```json
{
  "name": "My Fire Team",
  "public": true,
  "pokemon_1": 4,
  "pokemon_2": 5,
  "pokemon_3": 6,
  "pokemon_4": 37,
  "pokemon_5": 38,
  "pokemon_6": 77
}
```

#### Request Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique name for the team |
| `public` | boolean | No | Whether the team is publicly visible. Defaults to `false` if omitted. |
| `pokemon_1` | integer | Yes | ID of the 1st Pokemon |
| `pokemon_2` | integer | Yes | ID of the 2nd Pokemon |
| `pokemon_3` | integer | Yes | ID of the 3rd Pokemon |
| `pokemon_4` | integer | Yes | ID of the 4th Pokemon |
| `pokemon_5` | integer | Yes | ID of the 5th Pokemon |
| `pokemon_6` | integer | Yes | ID of the 6th Pokemon |

#### Response Codes

| Status Code | Description | Response Body |
|-------------|-------------|---------------|
| `201 Created` | Team successfully created | `{"id": 1, "name": "My Fire Team"}` |
| `400 Bad Request` | Invalid JSON, missing fields, or invalid field values | `{"error": "<message>"}` |
| `401 Unauthorized` | User is not logged in | `{"error": "Authentication credentials were not provided"}` |
| `404 Not Found` | A referenced Pokemon ID does not exist | `{"error": "Pokemon with id <id> does not exist"}` |
| `405 Method Not Allowed` | Request used an unsupported HTTP method | |
| `409 Conflict` | A team with the given name already exists | `{"error": "A team with this name already exists"}` |

---

### Edit a Pokemon Team

```
PUT /api/teams/<id>/
```

Updates an existing Pokemon team. Requires authentication. Only the team's owner can edit it.

#### Request Format

**Content-Type:** `application/json`

```json
{
  "name": "My Fire Team v2",
  "public": false,
  "pokemon_1": 4,
  "pokemon_2": 5,
  "pokemon_3": 6,
  "pokemon_4": 37,
  "pokemon_5": 38,
  "pokemon_6": 77
}
```

#### Request Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique name for the team |
| `public` | boolean | No | Whether the team is publicly visible. If omitted, current value is kept. |
| `pokemon_1` | integer | Yes | ID of the 1st Pokemon |
| `pokemon_2` | integer | Yes | ID of the 2nd Pokemon |
| `pokemon_3` | integer | Yes | ID of the 3rd Pokemon |
| `pokemon_4` | integer | Yes | ID of the 4th Pokemon |
| `pokemon_5` | integer | Yes | ID of the 5th Pokemon |
| `pokemon_6` | integer | Yes | ID of the 6th Pokemon |

#### Response Codes

| Status Code | Description | Response Body |
|-------------|-------------|---------------|
| `200 OK` | Team successfully updated | `{"message": "Team updated successfully"}` |
| `400 Bad Request` | Invalid JSON, missing fields, or invalid field values | `{"error": "<message>"}` |
| `401 Unauthorized` | User is not logged in | `{"error": "Authentication credentials were not provided"}` |
| `403 Forbidden` | Authenticated user is not the team's owner | `{"error": "You do not have permission to edit this team"}` |
| `404 Not Found` | Team or referenced Pokemon ID does not exist | `{"error": "<message>"}` |
| `405 Method Not Allowed` | Request used an unsupported HTTP method | |
| `409 Conflict` | Another team with the given name already exists | `{"error": "A team with this name already exists"}` |

---

### Delete a Pokemon Team

```
DELETE /api/teams/<id>/
```

Deletes a Pokemon team. Requires authentication. Only the team's owner can delete it.

#### Response Codes

| Status Code | Description | Response Body |
|-------------|-------------|---------------|
| `204 No Content` | Team successfully deleted | Empty |
| `401 Unauthorized` | User is not logged in | `{"error": "Authentication credentials were not provided"}` |
| `403 Forbidden` | Authenticated user is not the team's owner | `{"error": "You do not have permission to delete this team"}` |
| `404 Not Found` | Team with the given ID does not exist | `{"error": "Team not found"}` |
| `405 Method Not Allowed` | Request used an unsupported HTTP method | |

---

### Analyse Team Effectiveness

```
GET /api/teams/<id>/analysis/
```

Analyses a team's effectiveness against each of the 18 Pokemon types by aggregating the `against_*` multipliers of all 6 team members.

#### Response Format

**Content-Type:** `application/json`

```json
{
  "team": "My Fire Team",
  "members": ["Charmander", "Charmeleon", "Charizard", "Vulpix", "Ninetales", "Ponyta"],
  "member_details": [
    {
      "name": "Charmander",
      "types": ["Fire"],
      "attack": 52,
      "special_attack": 60,
      "attack_style": "special"
    }
  ],
  "type_analysis": {
    "bug": {
      "pokemon_multipliers": [{"name": "Charmander", "multiplier": 0.5}],
      "average_multiplier": 0.583,
      "best_pokemon": {"name": "Charmander", "multiplier": 0.5},
      "worst_pokemon": {"name": "Ponyta", "multiplier": 1.0},
      "rating": "resistant"
    }
  },
  "strengths": ["bug", "fairy", "fire", "grass", "ice", "steel"],
  "weaknesses": ["ground", "rock", "water"]
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `team` | string | Name of the team |
| `members` | array of strings | Names of the 6 Pokemon in the team |
| `member_details` | array of objects | Per-member stats including types, attack values, and attack style (`physical`, `special`, or `mixed`) |
| `type_analysis` | object | Per-type breakdown (keys are type names, e.g. `bug`, `fire`) |
| `type_analysis.<type>.pokemon_multipliers` | array | Each team member's damage multiplier against this type |
| `type_analysis.<type>.average_multiplier` | float | Mean multiplier across all 6 members (rounded to 3 d.p.) |
| `type_analysis.<type>.best_pokemon` | object | Team member with the lowest (most resistant) multiplier |
| `type_analysis.<type>.worst_pokemon` | object | Team member with the highest (most vulnerable) multiplier |
| `type_analysis.<type>.rating` | string | One of: `very resistant` (avg <= 0.5), `resistant` (avg <= 1.0), `neutral` (avg <= 1.5), `vulnerable` (avg <= 2.0), `very vulnerable` (avg > 2.0) |
| `strengths` | array of strings | Types the team is resistant to (avg < 1.0), sorted best first |
| `weaknesses` | array of strings | Types the team is vulnerable to (avg > 1.0), sorted worst first |

#### Response Codes

| Status Code | Description |
|-------------|-------------|
| `200 OK` | Analysis successfully computed |
| `404 Not Found` | Team with the given ID does not exist |
| `405 Method Not Allowed` | Request used an unsupported HTTP method (only `GET` is supported) |

---

### Top 10 Most Used Pokemon

```
GET /api/stats/top-pokemon/
```

Returns the top 10 Pokemon most frequently added to team slots across all teams.

#### Response Format

**Content-Type:** `application/json`

```json
{
  "top_pokemon": [
    {
      "pokemon_id": 6,
      "name": "Charizard",
      "times_used": 15
    }
  ]
}
```

#### Response Codes

| Status Code | Description |
|-------------|-------------|
| `200 OK` | Successfully retrieved usage data |
| `405 Method Not Allowed` | Request used an unsupported HTTP method (only `GET` is supported) |

---

### Most Used Pokemon Types

```
GET /api/stats/top-types/
```

Returns Pokemon types sorted by how often they appear in team slots (highest first).

#### Response Format

**Content-Type:** `application/json`

```json
{
  "type_usage": [
    {
      "type": "Water",
      "times_used": 42
    }
  ]
}
```

#### Response Codes

| Status Code | Description |
|-------------|-------------|
| `200 OK` | Successfully retrieved type usage data |
| `405 Method Not Allowed` | Request used an unsupported HTTP method (only `GET` is supported) |

---

## Frontend Pages

| Route | Auth Required | Description |
|-------|---------------|-------------|
| `/` | No | Homepage displaying public teams |
| `/login/` | No | Login page (redirects if already authenticated) |
| `/register/` | No | Registration page (redirects if already authenticated) |
| `/pokemon/` | No | Searchable, filterable Pokemon table |
| `/team/create/` | Yes | Create a new Pokemon team |
| `/team/<id>/edit/` | Yes | Edit an existing Pokemon team |
| `/team/<id>/analysis/` | No | Team type effectiveness analysis |
| `/teams/` | Yes | View and manage your teams |
| `/global-stats/` | No | Top Pokemon and type usage statistics |
| `/admin/` | Yes (staff) | Django admin panel |
