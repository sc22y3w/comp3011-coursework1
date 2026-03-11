from django.test import TestCase

from .models import Pokemon, PokemonTeam, PokemonType


class PokemonApiSortingTests(TestCase):
	def create_pokemon(self, name, types):
		pokemon = Pokemon.objects.create(
			name=name,
			hp=50,
			attack=50,
			defense=50,
			special_attack=50,
			special_defense=50,
			speed=50,
		)
		pokemon.type.set(types)
		return pokemon

	def test_sort_by_single_type_moves_matching_pokemon_first(self):
		fire = PokemonType.objects.create(name='fire')
		water = PokemonType.objects.create(name='water')
		grass = PokemonType.objects.create(name='grass')

		self.create_pokemon('Bulbasaur', [grass])
		self.create_pokemon('Charmander', [fire])
		self.create_pokemon('Squirtle', [water])
		self.create_pokemon('Vulpix', [fire])

		response = self.client.get('/api/pokemon/?sort_type=fire')

		self.assertEqual(response.status_code, 200)
		payload = response.json()
		self.assertEqual(
			[pokemon['name'] for pokemon in payload['pokemon']],
			['Charmander', 'Vulpix', 'Bulbasaur', 'Squirtle'],
		)

	def test_sort_by_unknown_type_returns_400(self):
		fire = PokemonType.objects.create(name='fire')
		self.create_pokemon('Charmander', [fire])

		response = self.client.get('/api/pokemon/?sort_type=unknown')

		self.assertEqual(response.status_code, 400)
		payload = response.json()
		self.assertIn('Unknown type(s): unknown', payload['error'])
		self.assertEqual(payload['valid_types'], ['fire'])


class GlobalStatsApiTests(TestCase):
	def create_pokemon(self, name, types):
		pokemon = Pokemon.objects.create(
			name=name,
			hp=50,
			attack=50,
			defense=50,
			special_attack=50,
			special_defense=50,
			speed=50,
		)
		pokemon.type.set(types)
		return pokemon

	def setUp(self):
		fire = PokemonType.objects.create(name='fire')
		water = PokemonType.objects.create(name='water')
		grass = PokemonType.objects.create(name='grass')
		poison = PokemonType.objects.create(name='poison')
		electric = PokemonType.objects.create(name='electric')
		normal = PokemonType.objects.create(name='normal')

		self.charmander = self.create_pokemon('Charmander', [fire])
		self.squirtle = self.create_pokemon('Squirtle', [water])
		self.bulbasaur = self.create_pokemon('Bulbasaur', [grass, poison])
		self.pikachu = self.create_pokemon('Pikachu', [electric])
		self.eevee = self.create_pokemon('Eevee', [normal])

		PokemonTeam.objects.create(
			name='Team A',
			pokemon_1=self.charmander,
			pokemon_2=self.charmander,
			pokemon_3=self.charmander,
			pokemon_4=self.squirtle,
			pokemon_5=self.bulbasaur,
			pokemon_6=self.pikachu,
		)
		PokemonTeam.objects.create(
			name='Team B',
			pokemon_1=self.charmander,
			pokemon_2=self.squirtle,
			pokemon_3=self.squirtle,
			pokemon_4=self.squirtle,
			pokemon_5=self.pikachu,
			pokemon_6=self.eevee,
		)
		PokemonTeam.objects.create(
			name='Team C',
			pokemon_1=self.squirtle,
			pokemon_2=self.pikachu,
			pokemon_3=self.pikachu,
			pokemon_4=self.pikachu,
			pokemon_5=self.eevee,
			pokemon_6=self.eevee,
		)

	def test_top_pokemon_usage_returns_ranked_top_10(self):
		response = self.client.get('/api/stats/top-pokemon/')

		self.assertEqual(response.status_code, 200)
		payload = response.json()
		self.assertEqual(
			payload['top_pokemon'],
			[
				{'pokemon_id': self.pikachu.id, 'name': 'Pikachu', 'times_used': 5},
				{'pokemon_id': self.squirtle.id, 'name': 'Squirtle', 'times_used': 5},
				{'pokemon_id': self.charmander.id, 'name': 'Charmander', 'times_used': 4},
				{'pokemon_id': self.eevee.id, 'name': 'Eevee', 'times_used': 3},
				{'pokemon_id': self.bulbasaur.id, 'name': 'Bulbasaur', 'times_used': 1},
			],
		)

	def test_top_type_usage_returns_ranked_types(self):
		response = self.client.get('/api/stats/top-types/')

		self.assertEqual(response.status_code, 200)
		payload = response.json()
		self.assertEqual(
			payload['type_usage'],
			[
				{'type': 'electric', 'times_used': 5},
				{'type': 'water', 'times_used': 5},
				{'type': 'fire', 'times_used': 4},
				{'type': 'normal', 'times_used': 3},
				{'type': 'grass', 'times_used': 1},
				{'type': 'poison', 'times_used': 1},
			],
		)
