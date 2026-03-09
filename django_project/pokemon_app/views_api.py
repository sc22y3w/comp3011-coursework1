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
