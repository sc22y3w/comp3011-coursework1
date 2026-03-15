# Pokémon App

A Django web application that serves Pokémon data via a REST API and displays it in a web interface.

## API Endpoints

### Authentication Note

Non-browser clients can register and log in directly using JSON API calls.
The frontend web pages at `/register/` and `/login/` also use these same API endpoints via JavaScript `fetch`.

### Register

```
POST /api/auth/register/
```

**Content-Type:** `application/json`

```json
{
  "username": "misty",
  "password": "staryu123"
}
```

Response codes:

- `201 Created` on success
- `400 Bad Request` when required fields are missing or JSON is invalid
- `409 Conflict` when username already exists

### Login

```
POST /api/auth/login/
```

**Content-Type:** `application/json`

```json
{
  "username": "misty",
  "password": "staryu123"
}
```

Response codes:

- `200 OK` on success
- `400 Bad Request` when required fields are missing or JSON is invalid
- `401 Unauthorized` for invalid credentials

The following protected endpoints require a logged-in user:

- `POST /api/team/create/`
- `PUT /api/team/<id>/edit/`
- `DELETE /api/team/<id>/delete/`

If a request is made without being logged in, the API returns:

- `401 Unauthorized`
- `{"error": "Authentication credentials were not provided"}`

### Get All Pokémon

```
GET /api/pokemon/
```

Returns a list of all Pokémon with their stats, types, abilities, and type matchup multipliers.

Optional query parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `sort_type` | string | Filter Pokémon to only those matching a single type (e.g. `fire`). |
| `sort_types` | comma-separated strings | Filter Pokémon to only those matching all listed types (e.g. `fire,flying`). |

Example:

```
GET /api/pokemon/?sort_types=fire,flying
```

#### Response Format

**Content-Type:** `application/json`

```json
{
  "pokemon": [
    {
      "id": int,
      "name": string,
      "types": [string],
      "abilities": [string],
      "hp": int,
      "attack": int,
      "defense": int,
      "special_attack": int,
      "special_defense": int,
      "speed": int,
      "against_bug": float,
      "against_dark": float,
      "against_dragon": float,
      "against_electric": float,
      "against_fairy": float,
      "against_fight": float,
      "against_fire": float,
      "against_flying": float,
      "against_ghost": float,
      "against_grass": float,
      "against_ground": float,
      "against_ice": float,
      "against_normal": float,
      "against_poison": float,
      "against_psychic": float,
      "against_rock": float,
      "against_steel": float,
      "against_water": float
    }
  ]
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique identifier for the Pokémon |
| `name` | string | Name of the Pokémon |
| `types` | array of strings | The Pokémon's type(s) |
| `abilities` | array of strings | The Pokémon's abilities |
| `hp` | integer | Hit Points stat |
| `attack` | integer | Attack stat |
| `defense` | integer | Defense stat |
| `special_attack` | integer | Special Attack stat |
| `special_defense` | integer | Special Defense stat |
| `speed` | integer | Speed stat |
| `against_*` | float | Damage multiplier against the specified type (e.g. `2.0` = double damage, `0.5` = half damage) |

#### Response Codes

| Status Code | Description |
|-------------|-------------|
| `200 OK` | Successfully retrieved Pokémon data |
| `400 Bad Request` | Unknown type(s) provided in filter parameter |
| `405 Method Not Allowed` | Request used an unsupported HTTP method (only `GET` is supported) |
| `500 Internal Server Error` | An unexpected server error occurred |

### Create a Pokémon Team

```
POST /api/team/create/
```

Creates a new Pokémon team with 6 Pokémon. The team is automatically assigned to the authenticated user as its owner.

#### Request Format

**Content-Type:** `application/json`

```json
{
  "name": string,
  "public": bool,
  "pokemon_1": int,
  "pokemon_2": int,
  "pokemon_3": int,
  "pokemon_4": int,
  "pokemon_5": int,
  "pokemon_6": int
}
```

#### Request Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique name for the team |
| `public` | boolean | No | Whether the team is publicly visible. Defaults to `false` if omitted. |
| `pokemon_1` | integer | Yes | ID of the 1st Pokémon |
| `pokemon_2` | integer | Yes | ID of the 2nd Pokémon |
| `pokemon_3` | integer | Yes | ID of the 3rd Pokémon |
| `pokemon_4` | integer | Yes | ID of the 4th Pokémon |
| `pokemon_5` | integer | Yes | ID of the 5th Pokémon |
| `pokemon_6` | integer | Yes | ID of the 6th Pokémon |

#### Response Codes

| Status Code | Description | Response Body |
|-------------|-------------|---------------|
| `201 Created` | Team successfully created | Empty |
| `400 Bad Request` | Invalid JSON, missing fields, or invalid field values | `{"error": "<message>"}` |
| `401 Unauthorized` | User is not logged in | `{"error": "Authentication credentials were not provided"}` |
| `404 Not Found` | A referenced Pokémon ID does not exist | `{"error": "Pokemon with id <id> does not exist"}` |
| `405 Method Not Allowed` | Request used an unsupported HTTP method (only `POST` is supported) | Empty |
| `409 Conflict` | A team with the given name already exists | `{"error": "A team with this name already exists"}` |
| `500 Internal Server Error` | An unexpected server error occurred | Empty |

### Get All Teams

```
GET /api/teams/
```

Returns a list of all Pokémon teams, including visibility, owner, and team members.

#### Response Format

**Content-Type:** `application/json`

```json
{
  "teams": [
    {
      "id": int,
      "name": string,
      "public": bool,
      "owner": string | null,
      "pokemon": [
        {"id": int, "name": string},
        {"id": int, "name": string},
        {"id": int, "name": string},
        {"id": int, "name": string},
        {"id": int, "name": string},
        {"id": int, "name": string}
      ]
    }
  ]
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique identifier for the team |
| `name` | string | Name of the team |
| `public` | boolean | Whether the team is publicly visible |
| `owner` | string or null | Username of the team's owner, or `null` if unowned |
| `pokemon` | array of objects | The 6 Pokémon in the team, each with `id` (integer) and `name` (string) |

#### Response Codes

| Status Code | Description |
|-------------|-------------|
| `200 OK` | Successfully retrieved teams |
| `405 Method Not Allowed` | Request used an unsupported HTTP method (only `GET` is supported) |
| `500 Internal Server Error` | An unexpected server error occurred |

### Edit a Pokémon Team

```
PUT /api/team/<id>/edit/
```

Updates an existing Pokémon team's name, members, and visibility. Only the team's owner can edit it.

#### Request Format

**Content-Type:** `application/json`

```json
{
  "name": string,
  "public": bool,
  "pokemon_1": int,
  "pokemon_2": int,
  "pokemon_3": int,
  "pokemon_4": int,
  "pokemon_5": int,
  "pokemon_6": int
}
```

#### Request Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique name for the team |
| `public` | boolean | No | Whether the team is publicly visible. If omitted, current value is kept. |
| `pokemon_1` | integer | Yes | ID of the 1st Pokémon |
| `pokemon_2` | integer | Yes | ID of the 2nd Pokémon |
| `pokemon_3` | integer | Yes | ID of the 3rd Pokémon |
| `pokemon_4` | integer | Yes | ID of the 4th Pokémon |
| `pokemon_5` | integer | Yes | ID of the 5th Pokémon |
| `pokemon_6` | integer | Yes | ID of the 6th Pokémon |

#### Response Format

**Content-Type:** `application/json`

```json
{
  "message": "Team updated successfully"
}
```

#### Response Codes

| Status Code | Description | Response Body |
|-------------|-------------|---------------|
| `200 OK` | Team successfully updated | `{"message": "Team updated successfully"}` |
| `400 Bad Request` | Invalid JSON, missing fields, or invalid field values | `{"error": "<message>"}` |
| `401 Unauthorized` | User is not logged in | `{"error": "Authentication credentials were not provided"}` |
| `403 Forbidden` | Authenticated user is not the team's owner | `{"error": "You do not have permission to edit this team"}` |
| `404 Not Found` | Team or referenced Pokémon ID does not exist | `{"error": "<message>"}` |
| `405 Method Not Allowed` | Request used an unsupported HTTP method (only `PUT` is supported) | Empty |
| `409 Conflict` | Another team with the given name already exists | `{"error": "A team with this name already exists"}` |
| `500 Internal Server Error` | An unexpected server error occurred | Empty |

### Delete a Pokémon Team

```
DELETE /api/team/<id>/delete/
```

Deletes a Pokémon team. Only the team's owner can delete it.

#### Response Codes

| Status Code | Description | Response Body |
|-------------|-------------|---------------|
| `200 OK` | Team successfully deleted | `{"message": "Team deleted successfully"}` |
| `401 Unauthorized` | User is not logged in | `{"error": "Authentication credentials were not provided"}` |
| `403 Forbidden` | Authenticated user is not the team's owner | `{"error": "You do not have permission to delete this team"}` |
| `404 Not Found` | Team with the given ID does not exist | `{"error": "Team not found"}` |
| `405 Method Not Allowed` | Request used an unsupported HTTP method (only `DELETE` is supported) | Empty |
| `500 Internal Server Error` | An unexpected server error occurred | Empty |

### Analyse Team Effectiveness

```
GET /api/team/<id>/analysis/
```

Analyses a team's effectiveness against each of the 18 Pokémon types by aggregating the `against_*` multipliers of all 6 team members.

#### Response Format

**Content-Type:** `application/json`

```json
{
  "team": string,
  "members": [string],
  "member_details": [
    {
      "name": string,
      "types": [string],
      "attack": int,
      "special_attack": int,
      "attack_style": string
    }
  ],
  "type_analysis": {
    "<type>": {
      "pokemon_multipliers": [{"name": string, "multiplier": float}],
      "average_multiplier": float,
      "best_pokemon": {"name": string, "multiplier": float},
      "worst_pokemon": {"name": string, "multiplier": float},
      "rating": string
    }
  },
  "strengths": [string],
  "weaknesses": [string]
}
```

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `team` | string | Name of the team |
| `members` | array of strings | Names of the 6 Pokémon in the team |
| `member_details` | array of objects | Per-member stats including types, attack values, and attack style (`physical`, `special`, or `mixed`) |
| `type_analysis` | object | Per-type breakdown (keys are type names, e.g. `bug`, `fire`) |
| `type_analysis.<type>.pokemon_multipliers` | array | Each team member's damage multiplier against this type |
| `type_analysis.<type>.average_multiplier` | float | Mean multiplier across all 6 members (rounded to 3 d.p.) |
| `type_analysis.<type>.best_pokemon` | object | Team member with the lowest (most resistant) multiplier |
| `type_analysis.<type>.worst_pokemon` | object | Team member with the highest (most vulnerable) multiplier |
| `type_analysis.<type>.rating` | string | One of: `very resistant` (≤0.5), `resistant` (≤1.0), `neutral` (≤1.5), `vulnerable` (≤2.0), `very vulnerable` (>2.0) |
| `strengths` | array of strings | Types the team is resistant to (avg < 1.0), sorted best first |
| `weaknesses` | array of strings | Types the team is vulnerable to (avg > 1.0), sorted worst first |

#### Response Codes

| Status Code | Description | Response Body |
|-------------|-------------|---------------|
| `200 OK` | Analysis successfully computed | See response format above |
| `404 Not Found` | Team with the given ID does not exist | `{"error": "Team not found"}` |
| `405 Method Not Allowed` | Request used an unsupported HTTP method (only `GET` is supported) | Empty |
| `500 Internal Server Error` | An unexpected server error occurred | Empty |

### Top 10 Most Used Pokémon

```
GET /api/stats/top-pokemon/
```

Returns the top 10 Pokémon most frequently added to team slots across all teams.

#### Response Format

**Content-Type:** `application/json`

```json
{
  "top_pokemon": [
    {
      "pokemon_id": int,
      "name": string,
      "times_used": int
    }
  ]
}
```

#### Response Codes

| Status Code | Description |
|-------------|-------------|
| `200 OK` | Successfully retrieved usage data |
| `405 Method Not Allowed` | Request used an unsupported HTTP method (only `GET` is supported) |
| `500 Internal Server Error` | An unexpected server error occurred |

### Most Used Pokémon Types

```
GET /api/stats/top-types/
```

Returns Pokémon types sorted by how often they appear in team slots (highest first).

#### Response Format

**Content-Type:** `application/json`

```json
{
  "type_usage": [
    {
      "type": string,
      "times_used": int
    }
  ]
}
```

#### Response Codes

| Status Code | Description |
|-------------|-------------|
| `200 OK` | Successfully retrieved type usage data |
| `405 Method Not Allowed` | Request used an unsupported HTTP method (only `GET` is supported) |
| `500 Internal Server Error` | An unexpected server error occurred |

## Pages

| Route | Description |
|-------|-------------|
| `/pokemon/` | Web page displaying all Pokémon in a searchable table |
| `/teams/` | Web page displaying all created Pokémon teams |
| `/team/create/` | Web page for creating a new Pokémon team |
| `/team/<id>/edit/` | Web page for editing an existing Pokémon team |
| `/team/<id>/analysis/` | Web page showing the team's type effectiveness analysis |
| `/admin/` | Django admin panel |
