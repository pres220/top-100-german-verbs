from django.contrib import admin
from .models import Verb


class VerbAdmin(admin.ModelAdmin):
    list_display = ('infinitive', 'frequency', 'translation')
    ordering = ['frequency']

    fieldsets = (
        (None, {
            'fields': ('infinitive', 'frequency', 'translation', 'past_participle')
        }),
        ('Present Tense Conjugation', {
            'fields': ('present_ich', 'present_du', 'present_er', 'present_wir', 'present_ihr', 'present_sie')
        }),
        ('Present Perfect Tense Conjugation', {
            'fields': ('perfect_ich', 'perfect_du', 'perfect_er', 'perfect_wir', 'perfect_ihr', 'perfect_sie')
        }),
        ('Simple Past Tense Conjugation', {
            'fields': ('past_ich', 'past_du', 'past_er', 'past_wir', 'past_ihr', 'past_sie')
        }),
    )

admin.site.register(Verb, VerbAdmin)