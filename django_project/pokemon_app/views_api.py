import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from .models import Pokemon, PokemonTeam


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


@require_http_methods(["POST"])
def create_team_api(request):
    """API endpoint to create a PokemonTeam."""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    name = data.get('name')
    if not name:
        return JsonResponse({'error': 'Team name is required'}, status=400)

    if PokemonTeam.objects.filter(name=name).exists():
        return JsonResponse({'error': 'A team with this name already exists'}, status=409)

    pokemon_ids = []
    for i in range(1, 7):
        pid = data.get(f'pokemon_{i}')
        if pid is None:
            return JsonResponse({'error': f'pokemon_{i} is required'}, status=400)
        try:
            pid = int(pid)
        except (ValueError, TypeError):
            return JsonResponse({'error': f'pokemon_{i} must be a valid integer'}, status=400)
        pokemon_ids.append(pid)

    pokemon_objects = {}
    for i, pid in enumerate(pokemon_ids, start=1):
        try:
            pokemon_objects[f'pokemon_{i}'] = Pokemon.objects.get(id=pid)
        except Pokemon.DoesNotExist:
            return JsonResponse({'error': f'Pokemon with id {pid} does not exist'}, status=404)

    team = PokemonTeam.objects.create(name=name, **pokemon_objects)

    return HttpResponse(status=201)


def teams_api(request):
    """API endpoint that returns all teams as JSON."""
    teams = PokemonTeam.objects.select_related(
        'pokemon_1', 'pokemon_2', 'pokemon_3',
        'pokemon_4', 'pokemon_5', 'pokemon_6',
    ).all()
    team_list = []
    for t in teams:
        team_list.append({
            'id': t.id,
            'name': t.name,
            'pokemon': [
                {'id': getattr(t, f'pokemon_{i}').id, 'name': getattr(t, f'pokemon_{i}').name}
                for i in range(1, 7)
            ],
        })
    return JsonResponse({'teams': team_list})


@require_http_methods(["PUT"])
def edit_team_api(request, team_id):
    """API endpoint to edit an existing PokemonTeam."""
    try:
        team = PokemonTeam.objects.get(id=team_id)
    except PokemonTeam.DoesNotExist:
        return JsonResponse({'error': 'Team not found'}, status=404)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    name = data.get('name')
    if not name:
        return JsonResponse({'error': 'Team name is required'}, status=400)

    if PokemonTeam.objects.filter(name=name).exclude(id=team_id).exists():
        return JsonResponse({'error': 'A team with this name already exists'}, status=409)

    pokemon_ids = []
    for i in range(1, 7):
        pid = data.get(f'pokemon_{i}')
        if pid is None:
            return JsonResponse({'error': f'pokemon_{i} is required'}, status=400)
        try:
            pid = int(pid)
        except (ValueError, TypeError):
            return JsonResponse({'error': f'pokemon_{i} must be a valid integer'}, status=400)
        pokemon_ids.append(pid)

    for i, pid in enumerate(pokemon_ids, start=1):
        try:
            pokemon = Pokemon.objects.get(id=pid)
        except Pokemon.DoesNotExist:
            return JsonResponse({'error': f'Pokemon with id {pid} does not exist'}, status=404)
        setattr(team, f'pokemon_{i}', pokemon)

    team.name = name
    team.save()

    return JsonResponse({'message': 'Team updated successfully'})


@require_http_methods(["DELETE"])
def delete_team_api(request, team_id):
    """API endpoint to delete a PokemonTeam."""
    try:
        team = PokemonTeam.objects.get(id=team_id)
    except PokemonTeam.DoesNotExist:
        return JsonResponse({'error': 'Team not found'}, status=404)

    team.delete()
    return JsonResponse({'message': 'Team deleted successfully'})


def team_analysis_api(request, team_id):
    """API endpoint that analyses a team's effectiveness against each Pokemon type.

    For each of the 18 types, returns per-Pokemon multipliers, the team average,
    the best and worst matchups, and an overall rating.
    """
    try:
        team = PokemonTeam.objects.select_related(
            'pokemon_1', 'pokemon_2', 'pokemon_3',
            'pokemon_4', 'pokemon_5', 'pokemon_6',
        ).get(id=team_id)
    except PokemonTeam.DoesNotExist:
        return JsonResponse({'error': 'Team not found'}, status=404)

    TYPES = [
        'bug', 'dark', 'dragon', 'electric', 'fairy', 'fight',
        'fire', 'flying', 'ghost', 'grass', 'ground', 'ice',
        'normal', 'poison', 'psychic', 'rock', 'steel', 'water',
    ]

    members = [getattr(team, f'pokemon_{i}') for i in range(1, 7)]

    type_analysis = {}
    for t in TYPES:
        field = f'against_{t}'
        multipliers = [getattr(p, field) for p in members]
        avg = sum(multipliers) / len(multipliers)
        best_idx = multipliers.index(min(multipliers))
        worst_idx = multipliers.index(max(multipliers))

        if avg <= 0.5:
            rating = 'very resistant'
        elif avg <= 1.0:
            rating = 'resistant'
        elif avg <= 1.5:
            rating = 'neutral'
        elif avg <= 2.0:
            rating = 'vulnerable'
        else:
            rating = 'very vulnerable'

        type_analysis[t] = {
            'pokemon_multipliers': {
                p.name: multipliers[i] for i, p in enumerate(members)
            },
            'average_multiplier': round(avg, 3),
            'best_pokemon': {'name': members[best_idx].name, 'multiplier': multipliers[best_idx]},
            'worst_pokemon': {'name': members[worst_idx].name, 'multiplier': multipliers[worst_idx]},
            'rating': rating,
        }

    strengths = sorted(
        [t for t in TYPES if type_analysis[t]['average_multiplier'] < 1.0],
        key=lambda t: type_analysis[t]['average_multiplier'],
    )
    weaknesses = sorted(
        [t for t in TYPES if type_analysis[t]['average_multiplier'] > 1.0],
        key=lambda t: type_analysis[t]['average_multiplier'],
        reverse=True,
    )

    return JsonResponse({
        'team': team.name,
        'members': [p.name for p in members],
        'type_analysis': type_analysis,
        'strengths': strengths,
        'weaknesses': weaknesses,
    })
