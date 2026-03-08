from django.db import models

class PokemonType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
      
class Ability(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
      
class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    type = models.ManyToManyField(PokemonType, related_name='pokemon_type')
    abilities = models.ManyToManyField(Ability, related_name='pokemon_abilities')
    against_bug = models.FloatField(default=1.0)
    against_dark = models.FloatField(default=1.0)
    against_dragon = models.FloatField(default=1.0)
    against_electric = models.FloatField(default=1.0)
    against_fairy = models.FloatField(default=1.0)
    against_fight = models.FloatField(default=1.0)
    against_fire = models.FloatField(default=1.0)
    against_flying = models.FloatField(default=1.0)
    against_ghost = models.FloatField(default=1.0)
    against_grass = models.FloatField(default=1.0)
    against_ground = models.FloatField(default=1.0)
    against_ice = models.FloatField(default=1.0)
    against_normal = models.FloatField(default=1.0)
    against_poison = models.FloatField(default=1.0)
    against_psychic = models.FloatField(default=1.0)
    against_rock = models.FloatField(default=1.0)
    against_steel = models.FloatField(default=1.0)
    against_water = models.FloatField(default=1.0)
    
    hp = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    special_attack = models.IntegerField()
    special_defense = models.IntegerField()
    speed = models.IntegerField()

    def __str__(self):
        return self.name


class PokemonTeam(models.Model):
    name = models.CharField(max_length=100)
    pokemon_1 = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='team_slot_1')
    pokemon_2 = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='team_slot_2')
    pokemon_3 = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='team_slot_3')
    pokemon_4 = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='team_slot_4')
    pokemon_5 = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='team_slot_5')
    pokemon_6 = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='team_slot_6')

    def __str__(self):
        return self.name