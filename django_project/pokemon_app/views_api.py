from django.http import JsonResponse
from .models import Pokemon


def pokemon_api(request):
    """API endpoint that returns all Pokemon data as JSON."""
    pokemon_list = []
    for p in Pokemon.objects.prefetch_related('type', 'abilities').all():
        pokemon_list.append({
            'id': p.id,
            'name': p.name,
            'types': [t.name for t in p.type.all()],
            'abilities': [a.name for a in p.abilities.all()],
            'hp': p.hp,
            'attack': p.attack,
            'defense': p.defense,
            'special_attack': p.special_attack,
            'special_defense': p.special_defense,
            'speed': p.speed,
            'against_bug': p.against_bug,
            'against_dark': p.against_dark,
            'against_dragon': p.against_dragon,
            'against_electric': p.against_electric,
            'against_fairy': p.against_fairy,
            'against_fight': p.against_fight,
            'against_fire': p.against_fire,
            'against_flying': p.against_flying,
            'against_ghost': p.against_ghost,
            'against_grass': p.against_grass,
            'against_ground': p.against_ground,
            'against_ice': p.against_ice,
            'against_normal': p.against_normal,
            'against_poison': p.against_poison,
            'against_psychic': p.against_psychic,
            'against_rock': p.against_rock,
            'against_steel': p.against_steel,
            'against_water': p.against_water,
        })
    return JsonResponse({'pokemon': pokemon_list})
