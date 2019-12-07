from django.contrib import admin
from .models import Verb, Mood, Tense, Conjugation


class VerbAdmin(admin.ModelAdmin):
    list_display = ('infinitive', 'frequency', 'translation')
    ordering = ['frequency']

    fieldsets = (
        (None, {
            'fields': ('infinitive', 'frequency', 'translation', 'present_participle', 'past_participle')
        }),
    )

class ConjugationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Verb, VerbAdmin)
admin.site.register(Mood)
admin.site.register(Tense)
admin.site.register(Conjugation)