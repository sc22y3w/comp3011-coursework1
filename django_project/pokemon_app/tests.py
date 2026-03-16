import json

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Ability, Pokemon, PokemonTeam, PokemonType


class ApiTestBase(TestCase):
    """Shared setUp for all API test classes."""

    @classmethod
    def setUpTestData(cls):
        cls.type_fire = PokemonType.objects.create(name='Fire')
        cls.type_water = PokemonType.objects.create(name='Water')
        cls.type_grass = PokemonType.objects.create(name='Grass')
        cls.type_electric = PokemonType.objects.create(name='Electric')

        cls.ability_blaze = Ability.objects.create(name='Blaze')
        cls.ability_torrent = Ability.objects.create(name='Torrent')

        pokemon_defaults = dict(
            hp=50, attack=60, defense=50,
            special_attack=70, special_defense=50, speed=65,
            against_bug=1.0, against_dark=1.0, against_dragon=1.0,
            against_electric=1.0, against_fairy=1.0, against_fighting=1.0,
            against_fire=0.5, against_flying=1.0, against_ghost=1.0,
            against_grass=0.5, against_ground=2.0, against_ice=1.0,
            against_normal=1.0, against_poison=1.0, against_psychic=1.0,
            against_rock=2.0, against_steel=1.0, against_water=2.0,
        )

        cls.pokemon = []
        names = ['Charmander', 'Squirtle', 'Bulbasaur', 'Pikachu', 'Eevee', 'Jigglypuff']
        for i, name in enumerate(names):
            p = Pokemon.objects.create(name=name, **pokemon_defaults)
            if i % 2 == 0:
                p.type.add(cls.type_fire)
                p.abilities.add(cls.ability_blaze)
            else:
                p.type.add(cls.type_water)
                p.abilities.add(cls.ability_torrent)
            cls.pokemon.append(p)

        cls.user1 = User.objects.create_user(username='ash', password='P@ssw0rd123!')
        cls.user2 = User.objects.create_user(username='misty', password='P@ssw0rd123!')

        cls.public_team = PokemonTeam.objects.create(
            name='Team Rocket', owner=cls.user1, public=True,
            pokemon_1=cls.pokemon[0], pokemon_2=cls.pokemon[1],
            pokemon_3=cls.pokemon[2], pokemon_4=cls.pokemon[3],
            pokemon_5=cls.pokemon[4], pokemon_6=cls.pokemon[5],
        )
        cls.private_team = PokemonTeam.objects.create(
            name='Secret Team', owner=cls.user1, public=False,
            pokemon_1=cls.pokemon[0], pokemon_2=cls.pokemon[1],
            pokemon_3=cls.pokemon[2], pokemon_4=cls.pokemon[3],
            pokemon_5=cls.pokemon[4], pokemon_6=cls.pokemon[5],
        )

    def _login(self, username='ash', password='P@ssw0rd123!'):
        self.client.post('/api/auth/sessions/', json.dumps({
            'username': username, 'password': password,
        }), content_type='application/json')

    def _team_payload(self, **overrides):
        payload = {
            'name': 'New Team',
            'public': True,
            'pokemon_1': self.pokemon[0].id,
            'pokemon_2': self.pokemon[1].id,
            'pokemon_3': self.pokemon[2].id,
            'pokemon_4': self.pokemon[3].id,
            'pokemon_5': self.pokemon[4].id,
            'pokemon_6': self.pokemon[5].id,
        }
        payload.update(overrides)
        return payload


class RegisterApiTest(ApiTestBase):

    def test_register_success(self):
        resp = self.client.post('/api/auth/users/', json.dumps({
            'username': 'newuser', 'password': 'Str0ngP@ss!',
        }), content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(data['username'], 'newuser')
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_missing_username(self):
        resp = self.client.post('/api/auth/users/', json.dumps({
            'password': 'Str0ngP@ss!',
        }), content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_missing_password(self):
        resp = self.client.post('/api/auth/users/', json.dumps({
            'username': 'newuser',
        }), content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_duplicate_username(self):
        resp = self.client.post('/api/auth/users/', json.dumps({
            'username': 'ash', 'password': 'Str0ngP@ss!',
        }), content_type='application/json')
        self.assertEqual(resp.status_code, 409)

    def test_weak_password(self):
        resp = self.client.post('/api/auth/users/', json.dumps({
            'username': 'newuser', 'password': '123',
        }), content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_invalid_json(self):
        resp = self.client.post('/api/auth/users/', 'not json',
                                content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_get_not_allowed(self):
        resp = self.client.get('/api/auth/users/')
        self.assertEqual(resp.status_code, 405)


class LoginApiTest(ApiTestBase):

    def test_login_success(self):
        resp = self.client.post('/api/auth/sessions/', json.dumps({
            'username': 'ash', 'password': 'P@ssw0rd123!',
        }), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['username'], 'ash')

    def test_wrong_credentials(self):
        resp = self.client.post('/api/auth/sessions/', json.dumps({
            'username': 'ash', 'password': 'wrong',
        }), content_type='application/json')
        self.assertEqual(resp.status_code, 401)

    def test_missing_fields(self):
        resp = self.client.post('/api/auth/sessions/', json.dumps({
            'username': 'ash',
        }), content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_invalid_json(self):
        resp = self.client.post('/api/auth/sessions/', '{bad',
                                content_type='application/json')
        self.assertEqual(resp.status_code, 400)


class LogoutApiTest(ApiTestBase):

    def test_logout_success(self):
        self._login()
        resp = self.client.post('/api/auth/sessions/logout/')
        self.assertEqual(resp.status_code, 200)

    def test_logout_unauthenticated(self):
        resp = self.client.post('/api/auth/sessions/logout/')
        self.assertEqual(resp.status_code, 401)


class PokemonApiTest(ApiTestBase):

    def test_get_all_pokemon(self):
        resp = self.client.get('/api/pokemon/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['count'], 6)
        self.assertEqual(len(data['pokemon']), 6)
        first = data['pokemon'][0]
        self.assertIn('name', first)
        self.assertIn('types', first)
        self.assertIn('hp', first)

    def test_pagination_limit_offset(self):
        resp = self.client.get('/api/pokemon/?limit=2&offset=1')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['count'], 6)
        self.assertEqual(data['limit'], 2)
        self.assertEqual(data['offset'], 1)
        self.assertEqual(len(data['pokemon']), 2)

    def test_filter_by_type(self):
        resp = self.client.get('/api/pokemon/?sort_types=Fire')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(all('Fire' in p['types'] for p in data['pokemon']))

    def test_invalid_type_name(self):
        resp = self.client.get('/api/pokemon/?sort_types=Unicorn')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('error', resp.json())

    def test_invalid_limit(self):
        resp = self.client.get('/api/pokemon/?limit=abc')
        self.assertEqual(resp.status_code, 400)

    def test_negative_offset(self):
        resp = self.client.get('/api/pokemon/?offset=-1')
        self.assertEqual(resp.status_code, 400)

    def test_zero_limit(self):
        resp = self.client.get('/api/pokemon/?limit=0')
        self.assertEqual(resp.status_code, 400)


class TeamsApiTest(ApiTestBase):

    def test_get_public_teams_unauthenticated(self):
        resp = self.client.get('/api/teams/')
        data = resp.json()
        self.assertEqual(resp.status_code, 200)
        names = [t['name'] for t in data['teams']]
        self.assertIn('Team Rocket', names)
        self.assertNotIn('Secret Team', names)

    def test_get_teams_authenticated_includes_own_private(self):
        self._login()
        resp = self.client.get('/api/teams/')
        data = resp.json()
        names = [t['name'] for t in data['teams']]
        self.assertIn('Team Rocket', names)
        self.assertIn('Secret Team', names)

    def test_get_teams_other_user_no_private(self):
        self._login('misty', 'P@ssw0rd123!')
        resp = self.client.get('/api/teams/')
        names = [t['name'] for t in resp.json()['teams']]
        self.assertNotIn('Secret Team', names)

    def test_create_team_success(self):
        self._login()
        resp = self.client.post('/api/teams/',
                                json.dumps(self._team_payload()),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()['name'], 'New Team')

    def test_create_team_missing_name(self):
        self._login()
        payload = self._team_payload()
        del payload['name']
        resp = self.client.post('/api/teams/', json.dumps(payload),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_create_team_duplicate_name(self):
        self._login()
        resp = self.client.post('/api/teams/',
                                json.dumps(self._team_payload(name='Team Rocket')),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 409)

    def test_create_team_missing_pokemon(self):
        self._login()
        payload = self._team_payload()
        del payload['pokemon_3']
        resp = self.client.post('/api/teams/', json.dumps(payload),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_create_team_invalid_pokemon_id(self):
        self._login()
        resp = self.client.post('/api/teams/',
                                json.dumps(self._team_payload(pokemon_1=9999)),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 404)

    def test_create_team_unauthenticated(self):
        resp = self.client.post('/api/teams/',
                                json.dumps(self._team_payload()),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 401)

    def test_create_team_invalid_json(self):
        self._login()
        resp = self.client.post('/api/teams/', '{bad',
                                content_type='application/json')
        self.assertEqual(resp.status_code, 400)


class TeamDetailApiTest(ApiTestBase):

    def test_get_team(self):
        resp = self.client.get(f'/api/teams/{self.public_team.id}/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['name'], 'Team Rocket')
        self.assertEqual(len(data['pokemon']), 6)

    def test_get_team_not_found(self):
        resp = self.client.get('/api/teams/9999/')
        self.assertEqual(resp.status_code, 404)

    def test_put_update_own_team(self):
        self._login()
        resp = self.client.put(
            f'/api/teams/{self.public_team.id}/',
            json.dumps(self._team_payload(name='Updated Team')),
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 200)

    def test_put_other_users_team(self):
        self._login('misty', 'P@ssw0rd123!')
        resp = self.client.put(
            f'/api/teams/{self.public_team.id}/',
            json.dumps(self._team_payload(name='Hacked')),
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 403)

    def test_put_unauthenticated(self):
        resp = self.client.put(
            f'/api/teams/{self.public_team.id}/',
            json.dumps(self._team_payload(name='Nope')),
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 401)

    def test_put_duplicate_name(self):
        self._login()
        resp = self.client.put(
            f'/api/teams/{self.public_team.id}/',
            json.dumps(self._team_payload(name='Secret Team')),
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 409)

    def test_put_invalid_pokemon_id(self):
        self._login()
        resp = self.client.put(
            f'/api/teams/{self.public_team.id}/',
            json.dumps(self._team_payload(name='Team Rocket', pokemon_1=9999)),
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 404)

    def test_delete_own_team(self):
        self._login()
        resp = self.client.delete(f'/api/teams/{self.private_team.id}/')
        self.assertEqual(resp.status_code, 204)
        self.assertFalse(PokemonTeam.objects.filter(id=self.private_team.id).exists())

    def test_delete_other_users_team(self):
        self._login('misty', 'P@ssw0rd123!')
        resp = self.client.delete(f'/api/teams/{self.public_team.id}/')
        self.assertEqual(resp.status_code, 403)

    def test_delete_unauthenticated(self):
        resp = self.client.delete(f'/api/teams/{self.public_team.id}/')
        self.assertEqual(resp.status_code, 401)


class TeamAnalysisApiTest(ApiTestBase):

    def test_analysis_success(self):
        resp = self.client.get(f'/api/teams/{self.public_team.id}/analysis/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['team'], 'Team Rocket')
        self.assertEqual(len(data['members']), 6)
        self.assertIn('type_analysis', data)
        self.assertIn('strengths', data)
        self.assertIn('weaknesses', data)
        self.assertIn('member_details', data)
        bug_analysis = data['type_analysis']['bug']
        self.assertIn('average_multiplier', bug_analysis)
        self.assertIn('best_pokemon', bug_analysis)
        self.assertIn('worst_pokemon', bug_analysis)
        self.assertIn('rating', bug_analysis)

    def test_analysis_team_not_found(self):
        resp = self.client.get('/api/teams/9999/analysis/')
        self.assertEqual(resp.status_code, 404)


class TopPokemonUsageApiTest(ApiTestBase):

    def test_top_pokemon(self):
        resp = self.client.get('/api/stats/top-pokemon/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('top_pokemon', data)
        self.assertTrue(len(data['top_pokemon']) > 0)
        first = data['top_pokemon'][0]
        self.assertIn('pokemon_id', first)
        self.assertIn('name', first)
        self.assertIn('times_used', first)

    def test_top_pokemon_empty(self):
        PokemonTeam.objects.all().delete()
        resp = self.client.get('/api/stats/top-pokemon/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['top_pokemon'], [])


class TopTypeUsageApiTest(ApiTestBase):

    def test_top_types(self):
        resp = self.client.get('/api/stats/top-types/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('type_usage', data)
        self.assertTrue(len(data['type_usage']) > 0)
        first = data['type_usage'][0]
        self.assertIn('type', first)
        self.assertIn('times_used', first)

    def test_top_types_empty(self):
        PokemonTeam.objects.all().delete()
        resp = self.client.get('/api/stats/top-types/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['type_usage'], [])
