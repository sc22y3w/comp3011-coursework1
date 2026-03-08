from django.contrib import admin
from .models import PokemonType, Ability, Pokemon

admin.site.register(PokemonType)
admin.site.register(Ability)


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_types', 'hp', 'attack', 'defense')

    def get_types(self, obj):
        return ', '.join(t.name for t in obj.type.all())
    get_types.short_description = 'Type'
