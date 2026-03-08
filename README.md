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
      "id": 1,
      "name": "Bulbasaur",
      "types": ["grass", "poison"],
      "abilities": ["overgrow", "chlorophyll"],
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
      "against_fight": 0.5,
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

## Pages

| Route | Description |
|-------|-------------|
| `/pokemon/` | Web page displaying all Pokémon in a searchable table |
| `/admin/` | Django admin panel |
