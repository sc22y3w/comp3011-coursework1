import os
import sys
import csv
import ast

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_config.settings")
django.setup()

from pokemon_app.models import PokemonType, Ability, Pokemon

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "pokemon.csv")


def run():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    # --- 1. Create PokemonTypes ---
    type_names = set()
    for row in reader:
        if row["type1"]:
            type_names.add(row["type1"].strip())
        if row["type2"]:
            type_names.add(row["type2"].strip())

    type_objs = {}
    for name in sorted(type_names):
        obj, _ = PokemonType.objects.get_or_create(name=name)
        type_objs[name] = obj
    print(f"Created/found {len(type_objs)} types.")

    # --- 2. Create Abilities ---
    ability_names = set()
    for row in reader:
        abilities = ast.literal_eval(row["abilities"])
        for a in abilities:
            ability_names.add(a.strip())

    ability_objs = {}
    for name in sorted(ability_names):
        obj, _ = Ability.objects.get_or_create(name=name)
        ability_objs[name] = obj
    print(f"Created/found {len(ability_objs)} abilities.")

    # --- 3. Create Pokemon ---
    created = 0
    for row in reader:
        pokemon, is_new = Pokemon.objects.get_or_create(
            name=row["name"],
            defaults={
                "against_bug": float(row["against_bug"]),
                "against_dark": float(row["against_dark"]),
                "against_dragon": float(row["against_dragon"]),
                "against_electric": float(row["against_electric"]),
                "against_fairy": float(row["against_fairy"]),
                "against_fight": float(row["against_fight"]),
                "against_fire": float(row["against_fire"]),
                "against_flying": float(row["against_flying"]),
                "against_ghost": float(row["against_ghost"]),
                "against_grass": float(row["against_grass"]),
                "against_ground": float(row["against_ground"]),
                "against_ice": float(row["against_ice"]),
                "against_normal": float(row["against_normal"]),
                "against_poison": float(row["against_poison"]),
                "against_psychic": float(row["against_psychic"]),
                "against_rock": float(row["against_rock"]),
                "against_steel": float(row["against_steel"]),
                "against_water": float(row["against_water"]),
                "hp": int(row["hp"]),
                "attack": int(row["attack"]),
                "defense": int(row["defense"]),
                "special_attack": int(row["sp_attack"]),
                "special_defense": int(row["sp_defense"]),
                "speed": int(row["speed"]),
            },
        )

        # Set types
        types = []
        if row["type1"]:
            types.append(type_objs[row["type1"].strip()])
        if row["type2"]:
            types.append(type_objs[row["type2"].strip()])
        pokemon.type.set(types)

        # Set abilities
        abilities = ast.literal_eval(row["abilities"])
        pokemon.abilities.set([ability_objs[a.strip()] for a in abilities])

        if is_new:
            created += 1

    print(f"Created {created} pokemon ({len(reader)} total rows).")


if __name__ == "__main__":
    run()
