import os
import random
import sys
from uuid import uuid4

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_config.settings")
django.setup()

from pokemon_app.models import Pokemon, PokemonTeam


def run(count=60):
    pokemon_ids = list(Pokemon.objects.values_list("id", flat=True))

    if len(pokemon_ids) < 6:
        raise ValueError(
            "At least 6 Pokemon are required before creating teams. "
            "Run import_pokemon.py first."
        )

    created = 0
    while created < count:
        selected_ids = random.sample(pokemon_ids, 6)

        PokemonTeam.objects.create(
            name=f"Random Team {uuid4().hex}",
            public=bool(random.getrandbits(1)),
            pokemon_1_id=selected_ids[0],
            pokemon_2_id=selected_ids[1],
            pokemon_3_id=selected_ids[2],
            pokemon_4_id=selected_ids[3],
            pokemon_5_id=selected_ids[4],
            pokemon_6_id=selected_ids[5],
        )
        created += 1

    print(f"Created {created} random teams.")


if __name__ == "__main__":
    count = 60
    if len(sys.argv) > 1:
        count = int(sys.argv[1])
    run(count)
