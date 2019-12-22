from django.contrib import admin

from .models import Conjugation, Mood, Tense, Verb


class ConjugationInline(admin.StackedInline):
    model = Conjugation
    extra = 0


class ConjugationAdmin(admin.ModelAdmin):
    ordering = ['id']
    search_fields = ['verb__infinitive']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('verb', 'mood', 'tense')


class VerbAdmin(admin.ModelAdmin):
    list_display = ('infinitive', 'frequency', 'translation')
    search_fields = ['infinitive']
    inlines = [ConjugationInline]


admin.site.register(Verb, VerbAdmin)
admin.site.register(Mood)
admin.site.register(Tense)
admin.site.register(Conjugation, ConjugationAdmin)
