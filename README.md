# Pokémon App

A Django web application that serves Pokémon data via a REST API and displays it in a web interface.

## API Endpoints

### Get All Pokémon

```
GET /api/pokemon/
```

Returns a list of all Pokémon with their stats, types, abilities, and type matchup multipliers.

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
| `405 Method Not Allowed` | Request used an unsupported HTTP method (only `GET` is supported) |
| `500 Internal Server Error` | An unexpected server error occurred |

### Create a Pokémon Team

```
POST /api/team/create/
```

Creates a new Pokémon team with 6 Pokémon.

#### Request Format

**Content-Type:** `application/json`

```json
{
  "name": string,
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
| `404 Not Found` | A referenced Pokémon ID does not exist | `{"error": "Pokemon with id <id> does not exist"}` |
| `405 Method Not Allowed` | Request used an unsupported HTTP method (only `POST` is supported) | Empty |
| `409 Conflict` | A team with the given name already exists | `{"error": "A team with this name already exists"}` |
| `500 Internal Server Error` | An unexpected server error occurred | Empty |

#### Error Response Format

**Content-Type:** `application/json`

```json
{
  "error": string
}
```

### Get All Teams

```
GET /api/teams/
```

Returns a list of all Pokémon teams and their members.

#### Response Format

**Content-Type:** `application/json`

```json
{
  "teams": [
    {
      "id": int,
      "name": string,
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

Updates an existing Pokémon team's name and members.

#### Request Format

**Content-Type:** `application/json`

```json
{
  "name": string,
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
| `404 Not Found` | Team or referenced Pokémon ID does not exist | `{"error": "<message>"}` |
| `405 Method Not Allowed` | Request used an unsupported HTTP method (only `PUT` is supported) | Empty |
| `409 Conflict` | Another team with the given name already exists | `{"error": "A team with this name already exists"}` |
| `500 Internal Server Error` | An unexpected server error occurred | Empty |

#### Error Response Format

**Content-Type:** `application/json`

```json
{
  "error": string
}
```

## Pages

| Route | Description |
|-------|-------------|
| `/pokemon/` | Web page displaying all Pokémon in a searchable table |
| `/teams/` | Web page displaying all created Pokémon teams |
| `/team/create/` | Web page for creating a new Pokémon team |
| `/team/<id>/edit/` | Web page for editing an existing Pokémon team |
| `/admin/` | Django admin panel |
