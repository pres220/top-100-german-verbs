from django.contrib import admin
from .models import Verb, Mood, Tense, Conjugation


class ConjugationInline(admin.StackedInline):
    model = Conjugation
    extra = 0

class ConjugationAdmin(admin.ModelAdmin):
    ordering = ['id']
    search_fields = ['verb__infinitive']

class VerbAdmin(admin.ModelAdmin):
    list_display = ('infinitive', 'frequency', 'translation')
    search_fields = ['infinitive']
    inlines = [ConjugationInline]


admin.site.register(Verb, VerbAdmin)
admin.site.register(Mood)
admin.site.register(Tense)
admin.site.register(Conjugation, ConjugationAdmin)