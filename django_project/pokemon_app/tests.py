from django.test import TestCase

from .models import Pokemon, PokemonType


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
