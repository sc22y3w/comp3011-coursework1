import json
from collections import Counter

from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from .models import Pokemon, PokemonTeam, PokemonType


def parse_bool(value):
    """Parse common boolean representations from JSON payloads."""
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        if value in (0, 1):
            return bool(value)
        return None
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in ('true', '1', 'yes', 'on'):
            return True
        if normalized in ('false', '0', 'no', 'off'):
            return False
    return None


def pokemon_api(request):
    """API endpoint that returns all Pokemon data as JSON."""
    queryset = Pokemon.objects.prefetch_related('type', 'abilities').all()

    sort_types_raw = request.GET.get('sort_types') or request.GET.get('sort_type')
    if sort_types_raw:
        requested_types = list(dict.fromkeys(
            t.strip().lower() for t in sort_types_raw.split(',') if t.strip()
        ))
        if not requested_types:
            return JsonResponse({'error': 'sort_type must contain at least one type name'}, status=400)

        available_types = list(PokemonType.objects.values_list('name', flat=True).order_by('name'))
        available_by_normalized = {t.lower(): t for t in available_types}
        unknown_types = sorted({t for t in requested_types if t not in available_by_normalized})
        if unknown_types:
            return JsonResponse(
                {
                    'error': f"Unknown type(s): {', '.join(unknown_types)}",
                    'valid_types': available_types,
                },
                status=400,
            )

        for type_name in requested_types:
            queryset = queryset.filter(type__name__iexact=type_name)

        queryset = queryset.distinct().order_by('id')
    else:
        queryset = queryset.order_by('id')

    pokemon_list = []
    for p in queryset:
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

    public = parse_bool(data.get('public', False))
    if public is None:
        return JsonResponse({'error': 'public must be a boolean value'}, status=400)

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

    team = PokemonTeam.objects.create(name=name, public=public, **pokemon_objects)

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
            'public': t.public,
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

    public = team.public
    if 'public' in data:
        parsed_public = parse_bool(data.get('public'))
        if parsed_public is None:
            return JsonResponse({'error': 'public must be a boolean value'}, status=400)
        public = parsed_public

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
    team.public = public
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

    def get_attack_style(p):
        if p.attack > p.special_attack:
            return 'physical'
        elif p.special_attack > p.attack:
            return 'special'
        else:
            return 'mixed'

    member_details = [
        {
            'name': p.name,
            'types': [t.name for t in p.type.all()],
            'attack': p.attack,
            'special_attack': p.special_attack,
            'attack_style': get_attack_style(p),
        }
        for p in members
    ]

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
            'pokemon_multipliers': [
                {'name': p.name, 'multiplier': multipliers[i]} for i, p in enumerate(members)
            ],
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
        'member_details': member_details,
        'type_analysis': type_analysis,
        'strengths': strengths,
        'weaknesses': weaknesses,
    })


def top_pokemon_usage_api(request):
    """API endpoint that returns the top 10 most-used Pokemon in all teams."""
    slot_fields = [
        'pokemon_1_id', 'pokemon_2_id', 'pokemon_3_id',
        'pokemon_4_id', 'pokemon_5_id', 'pokemon_6_id',
    ]
    usage_counter = Counter()

    for row in PokemonTeam.objects.values_list(*slot_fields):
        usage_counter.update(row)

    if not usage_counter:
        return JsonResponse({'top_pokemon': []})

    pokemon_names = {
        p.id: p.name
        for p in Pokemon.objects.filter(id__in=usage_counter.keys()).only('id', 'name')
    }

    sorted_usage = sorted(
        usage_counter.items(),
        key=lambda item: (-item[1], pokemon_names.get(item[0], ''), item[0]),
    )[:10]

    return JsonResponse({
        'top_pokemon': [
            {
                'pokemon_id': pokemon_id,
                'name': pokemon_names.get(pokemon_id),
                'times_used': count,
            }
            for pokemon_id, count in sorted_usage
        ]
    })


def top_type_usage_api(request):
    """API endpoint that returns Pokemon types sorted by total usage in all teams."""
    slot_fields = [
        'pokemon_1_id', 'pokemon_2_id', 'pokemon_3_id',
        'pokemon_4_id', 'pokemon_5_id', 'pokemon_6_id',
    ]
    usage_counter = Counter()

    for row in PokemonTeam.objects.values_list(*slot_fields):
        usage_counter.update(row)

    if not usage_counter:
        return JsonResponse({'type_usage': []})

    type_counter = Counter()
    pokemon_with_types = Pokemon.objects.filter(id__in=usage_counter.keys()).prefetch_related('type')
    for pokemon in pokemon_with_types:
        appearances = usage_counter.get(pokemon.id, 0)
        for pokemon_type in pokemon.type.all():
            type_counter[pokemon_type.name] += appearances

    sorted_types = sorted(type_counter.items(), key=lambda item: (-item[1], item[0]))

    return JsonResponse({
        'type_usage': [
            {'type': type_name, 'times_used': count}
            for type_name, count in sorted_types
        ]
    })
