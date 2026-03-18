# API Documentation

All API endpoints are prefixed with `/api/` and return JSON responses with `Content-Type: application/json`.

---

## Authentication

The API uses Django's session-based authentication. On successful login, the server sets a `sessionid` cookie which must be included in subsequent requests to protected endpoints. Non-browser clients can register and log in using the JSON endpoints below. The frontend pages at `/register/` and `/login/` also consume these same endpoints via JavaScript `fetch`.

### Register

```
POST /api/auth/users/
```

Creates a new user account.

**Content-Type:** `application/json`

**Request Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `username` | string | Yes | Desired username |
| `password` | string | Yes | Password (must pass Django's validators: min 8 chars, not common, not entirely numeric) |

**Example Request:**

```bash
curl -X POST http://localhost:8000/api/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "misty", "password": "staryu123"}'
```

**Example Response (201 Created):**

```json
{
  "message": "Registration successful",
  "username": "misty"
}
```

**Error Responses:**

| Status Code | Description | Example Response Body |
|-------------|-------------|----------------------|
| `400 Bad Request` | Missing fields, invalid JSON, or weak password | `{"error": "Password does not meet requirements", "details": ["This password is too short."]}` |
| `409 Conflict` | Username already taken | `{"error": "Username already exists"}` |

---

### Login

```
POST /api/auth/sessions/
```

Authenticates a user and creates a session. On success, the response includes a `Set-Cookie` header with the `sessionid`.

**Content-Type:** `application/json`

**Request Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `username` | string | Yes | Username |
| `password` | string | Yes | Password |

**Example Request:**

```bash
curl -X POST http://localhost:8000/api/auth/sessions/ \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"username": "misty", "password": "staryu123"}'
```

**Example Response (200 OK):**

```json
{
  "message": "Login successful",
  "username": "misty"
}
```

**Error Responses:**

| Status Code | Description | Example Response Body |
|-------------|-------------|----------------------|
| `400 Bad Request` | Missing fields or invalid JSON | `{"error": "username and password are required"}` |
| `401 Unauthorized` | Invalid credentials | `{"error": "Invalid username or password"}` |

---

### Logout

```
POST /api/auth/sessions/logout/
```

Destroys the current session. **Requires authentication.**

**Example Request:**

```bash
curl -X POST http://localhost:8000/api/auth/sessions/logout/ \
  -b cookies.txt
```

**Example Response (200 OK):**

```json
{
  "message": "Logout successful"
}
```

**Error Responses:**

| Status Code | Description | Example Response Body |
|-------------|-------------|----------------------|
| `401 Unauthorized` | Not logged in | `{"error": "Authentication credentials were not provided"}` |

---

## Protected Endpoints

The following endpoints require a logged-in user (session cookie). If a request is made without authentication, the API returns:

- **Status:** `401 Unauthorized`
- **Body:** `{"error": "Authentication credentials were not provided"}`

Protected endpoints:
- `POST /api/teams/`
- `PUT /api/teams/<id>/`
- `DELETE /api/teams/<id>/`
- `POST /api/auth/sessions/logout/`

---

## Pokemon

### List All Pokemon

```
GET /api/pokemon/
```

Returns a paginated list of all Pokemon with their stats, types, abilities, and type-effectiveness multipliers.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `sort_type` | string | Filter to Pokemon matching a single type (e.g. `fire`). |
| `sort_types` | comma-separated strings | Filter to Pokemon matching **all** listed types (e.g. `fire,flying`). |
| `limit` | integer | Maximum number of results to return (must be >= 1). |
| `offset` | integer | Number of results to skip (must be >= 0, default `0`). |

**Example Request:**

```bash
curl "http://localhost:8000/api/pokemon/?sort_types=fire,flying&limit=2&offset=0"
```

**Example Response (200 OK):**

```json
{
  "count": 3,
  "limit": 2,
  "offset": 0,
  "pokemon": [
    {
      "id": 6,
      "name": "Charizard",
      "types": ["Fire", "Flying"],
      "abilities": ["Blaze", "Solar Power"],
      "hp": 78,
      "attack": 84,
      "defense": 78,
      "special_attack": 109,
      "special_defense": 85,
      "speed": 100,
      "against_bug": 0.25,
      "against_dark": 1.0,
      "against_dragon": 1.0,
      "against_electric": 2.0,
      "against_fairy": 0.5,
      "against_fighting": 0.5,
      "against_fire": 0.5,
      "against_flying": 1.0,
      "against_ghost": 1.0,
      "against_grass": 0.25,
      "against_ground": 0.0,
      "against_ice": 1.0,
      "against_normal": 1.0,
      "against_poison": 1.0,
      "against_psychic": 1.0,
      "against_rock": 4.0,
      "against_steel": 0.5,
      "against_water": 2.0
    }
  ]
}
```

**Response Fields:**

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

**Error Responses:**

| Status Code | Description | Example Response Body |
|-------------|-------------|----------------------|
| `400 Bad Request` | Unknown type(s), or invalid `limit`/`offset` | `{"error": "Unknown type(s): fairy", "valid_types": ["Bug", "Dark", ...]}` |
| `405 Method Not Allowed` | Unsupported HTTP method | — |

---

## Teams

### List Teams

```
GET /api/teams/
```

Returns a list of Pokemon teams. **Authenticated users** see all public teams plus their own private teams. **Unauthenticated users** see only public teams.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `types` | comma-separated strings | Filter teams whose Pokemon collectively cover **all** listed types. For example, `types=fire,water` returns teams that have at least one Fire-type and at least one Water-type Pokemon. |

**Example Request:**

```bash
curl "http://localhost:8000/api/teams/?types=fire,water"
```

**Example Response (200 OK):**

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

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `teams` | array | List of team objects |
| `teams[].id` | integer | Unique team identifier |
| `teams[].name` | string | Team name |
| `teams[].public` | boolean | Whether the team is publicly visible |
| `teams[].owner` | string or null | Username of the owner, or `null` if unowned |
| `teams[].pokemon` | array | The 6 Pokemon in the team, each with `id`, `name`, and `types` |

**Error Responses:**

| Status Code | Description | Example Response Body |
|-------------|-------------|----------------------|
| `400 Bad Request` | Unknown type(s) in `types` parameter | `{"error": "Unknown type(s): fairy", "valid_types": ["Bug", "Dark", ...]}` |
| `405 Method Not Allowed` | Unsupported HTTP method | — |

---

### Get a Single Team

```
GET /api/teams/<id>/
```

Returns a single team by its ID. No authentication required.

**Example Request:**

```bash
curl http://localhost:8000/api/teams/1/
```

**Example Response (200 OK):**

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

**Error Responses:**

| Status Code | Description | Example Response Body |
|-------------|-------------|----------------------|
| `404 Not Found` | Team does not exist | `{"error": "Team not found"}` |
| `405 Method Not Allowed` | Unsupported HTTP method | — |

---

### Create a Team

```
POST /api/teams/
```

Creates a new Pokemon team with 6 Pokemon. **Requires authentication.** The team is automatically assigned to the authenticated user.

**Content-Type:** `application/json`

**Request Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique name for the team |
| `public` | boolean | No | Whether the team is publicly visible (default: `false`) |
| `pokemon_1` | integer | Yes | ID of the 1st Pokemon |
| `pokemon_2` | integer | Yes | ID of the 2nd Pokemon |
| `pokemon_3` | integer | Yes | ID of the 3rd Pokemon |
| `pokemon_4` | integer | Yes | ID of the 4th Pokemon |
| `pokemon_5` | integer | Yes | ID of the 5th Pokemon |
| `pokemon_6` | integer | Yes | ID of the 6th Pokemon |

**Example Request:**

```bash
curl -X POST http://localhost:8000/api/teams/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "name": "My Fire Team",
    "public": true,
    "pokemon_1": 4,
    "pokemon_2": 5,
    "pokemon_3": 6,
    "pokemon_4": 37,
    "pokemon_5": 38,
    "pokemon_6": 77
  }'
```

**Example Response (201 Created):**

```json
{
  "id": 1,
  "name": "My Fire Team"
}
```

**Error Responses:**

| Status Code | Description | Example Response Body |
|-------------|-------------|----------------------|
| `400 Bad Request` | Invalid JSON, missing fields, or invalid values | `{"error": "pokemon_3 is required"}` |
| `401 Unauthorized` | Not logged in | `{"error": "Authentication credentials were not provided"}` |
| `404 Not Found` | Pokemon ID does not exist | `{"error": "Pokemon with id 999 does not exist"}` |
| `409 Conflict` | Team name already exists | `{"error": "A team with this name already exists"}` |
| `405 Method Not Allowed` | Unsupported HTTP method | — |

---

### Edit a Team

```
PUT /api/teams/<id>/
```

Updates an existing Pokemon team. **Requires authentication.** Only the team's owner can edit it.

**Content-Type:** `application/json`

**Request Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique name for the team |
| `public` | boolean | No | Whether the team is publicly visible (if omitted, current value is kept) |
| `pokemon_1` | integer | Yes | ID of the 1st Pokemon |
| `pokemon_2` | integer | Yes | ID of the 2nd Pokemon |
| `pokemon_3` | integer | Yes | ID of the 3rd Pokemon |
| `pokemon_4` | integer | Yes | ID of the 4th Pokemon |
| `pokemon_5` | integer | Yes | ID of the 5th Pokemon |
| `pokemon_6` | integer | Yes | ID of the 6th Pokemon |

**Example Request:**

```bash
curl -X PUT http://localhost:8000/api/teams/1/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "name": "My Fire Team v2",
    "public": false,
    "pokemon_1": 4,
    "pokemon_2": 5,
    "pokemon_3": 6,
    "pokemon_4": 37,
    "pokemon_5": 38,
    "pokemon_6": 77
  }'
```

**Example Response (200 OK):**

```json
{
  "message": "Team updated successfully"
}
```

**Error Responses:**

| Status Code | Description | Example Response Body |
|-------------|-------------|----------------------|
| `400 Bad Request` | Invalid JSON, missing fields, or invalid values | `{"error": "Team name is required"}` |
| `401 Unauthorized` | Not logged in | `{"error": "Authentication credentials were not provided"}` |
| `403 Forbidden` | Not the team's owner | `{"error": "You do not have permission to edit this team"}` |
| `404 Not Found` | Team or Pokemon ID does not exist | `{"error": "Team not found"}` |
| `409 Conflict` | Another team with the given name exists | `{"error": "A team with this name already exists"}` |
| `405 Method Not Allowed` | Unsupported HTTP method | — |

---

### Delete a Team

```
DELETE /api/teams/<id>/
```

Deletes a Pokemon team. **Requires authentication.** Only the team's owner can delete it.

**Example Request:**

```bash
curl -X DELETE http://localhost:8000/api/teams/1/ \
  -b cookies.txt
```

**Example Response (204 No Content):**

Empty response body.

**Error Responses:**

| Status Code | Description | Example Response Body |
|-------------|-------------|----------------------|
| `401 Unauthorized` | Not logged in | `{"error": "Authentication credentials were not provided"}` |
| `403 Forbidden` | Not the team's owner | `{"error": "You do not have permission to delete this team"}` |
| `404 Not Found` | Team does not exist | `{"error": "Team not found"}` |
| `405 Method Not Allowed` | Unsupported HTTP method | — |

---

## Team Analysis

### Analyse Team Effectiveness

```
GET /api/teams/<id>/analysis/
```

Analyses a team's effectiveness against each of the 18 Pokemon types by aggregating the `against_*` multipliers of all 6 team members.

**Example Request:**

```bash
curl http://localhost:8000/api/teams/1/analysis/
```

**Example Response (200 OK):**

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
      "pokemon_multipliers": [
        {"name": "Charmander", "multiplier": 0.5},
        {"name": "Charmeleon", "multiplier": 0.5},
        {"name": "Charizard", "multiplier": 0.25},
        {"name": "Vulpix", "multiplier": 0.5},
        {"name": "Ninetales", "multiplier": 0.5},
        {"name": "Ponyta", "multiplier": 0.5}
      ],
      "average_multiplier": 0.458,
      "best_pokemon": {"name": "Charizard", "multiplier": 0.25},
      "worst_pokemon": {"name": "Charmander", "multiplier": 0.5},
      "rating": "very resistant"
    }
  },
  "strengths": ["bug", "fairy", "fire", "grass", "ice", "steel"],
  "weaknesses": ["ground", "rock", "water"]
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `team` | string | Name of the team |
| `members` | array of strings | Names of the 6 Pokemon |
| `member_details` | array of objects | Per-member stats: types, attack, special_attack, and attack_style (`physical`, `special`, or `mixed`) |
| `type_analysis` | object | Per-type breakdown keyed by type name |
| `type_analysis.<type>.pokemon_multipliers` | array | Each member's damage multiplier against this type |
| `type_analysis.<type>.average_multiplier` | float | Mean multiplier across all 6 members (3 d.p.) |
| `type_analysis.<type>.best_pokemon` | object | Member with the lowest (most resistant) multiplier |
| `type_analysis.<type>.worst_pokemon` | object | Member with the highest (most vulnerable) multiplier |
| `type_analysis.<type>.rating` | string | One of: `very resistant` (<= 0.5), `resistant` (<= 1.0), `neutral` (<= 1.5), `vulnerable` (<= 2.0), `very vulnerable` (> 2.0) |
| `strengths` | array of strings | Types the team is resistant to (avg < 1.0), sorted best first |
| `weaknesses` | array of strings | Types the team is vulnerable to (avg > 1.0), sorted worst first |

**Error Responses:**

| Status Code | Description | Example Response Body |
|-------------|-------------|----------------------|
| `404 Not Found` | Team does not exist | `{"error": "Team not found"}` |
| `405 Method Not Allowed` | Unsupported HTTP method | — |

---

## Statistics

### Top 10 Most Used Pokemon

```
GET /api/stats/top-pokemon/
```

Returns the 10 Pokemon most frequently added to team slots across all teams.

**Example Request:**

```bash
curl http://localhost:8000/api/stats/top-pokemon/
```

**Example Response (200 OK):**

```json
{
  "top_pokemon": [
    {
      "pokemon_id": 6,
      "name": "Charizard",
      "times_used": 15
    },
    {
      "pokemon_id": 150,
      "name": "Mewtwo",
      "times_used": 12
    }
  ]
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `top_pokemon` | array | Up to 10 Pokemon, sorted by usage (descending) |
| `top_pokemon[].pokemon_id` | integer | Pokemon ID |
| `top_pokemon[].name` | string | Pokemon name |
| `top_pokemon[].times_used` | integer | Number of team slots this Pokemon appears in |

**Error Responses:**

| Status Code | Description |
|-------------|-------------|
| `405 Method Not Allowed` | Unsupported HTTP method |

---

### Most Used Pokemon Types

```
GET /api/stats/top-types/
```

Returns Pokemon types sorted by how often they appear in team slots (highest first). Each team slot's Pokemon contributes all of its types to the count.

**Example Request:**

```bash
curl http://localhost:8000/api/stats/top-types/
```

**Example Response (200 OK):**

```json
{
  "type_usage": [
    {
      "type": "Water",
      "times_used": 42
    },
    {
      "type": "Fire",
      "times_used": 38
    }
  ]
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `type_usage` | array | All types with at least one usage, sorted descending |
| `type_usage[].type` | string | Type name |
| `type_usage[].times_used` | integer | Total appearances in team slots |

**Error Responses:**

| Status Code | Description |
|-------------|-------------|
| `405 Method Not Allowed` | Unsupported HTTP method |