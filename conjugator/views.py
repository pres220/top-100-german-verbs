from django.contrib import messages
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Conjugation, Verb


def home(request):
    """
    Renders home.html with a list of lists with each list representing a
    Bootstrap column 10 verbs long.
    """
    verbs = Verb.objects.values('infinitive', 'frequency')
    col_size = 10
    col_list = [verbs[i:i+col_size] for i in range(0, len(verbs), col_size)]
    return render(request, 'conjugator/home.html', {'col_list': col_list})


def conjugation(request, infinitive):
    """
    Renders conjugation.html with the current verb's conjugation pattern.
    """
    verb = get_object_or_404(Verb, infinitive__iexact=infinitive)
    next_frequency = verb.frequency + 1 if verb.frequency < Verb.objects.count() else 1
    prev_frequency = verb.frequency - 1 if verb.frequency > 1 else Verb.objects.count()
    next_verb = Verb.objects.get(frequency=next_frequency).infinitive
    prev_verb = Verb.objects.get(frequency=prev_frequency).infinitive
    conjugations = Conjugation.objects.filter(verb=verb).select_related('mood', 'tense').order_by('id')
    indicative = conjugations.filter(mood__name='indicative')
    subjunctive_I = conjugations.filter(mood__name='subjunctive I')
    subjunctive_II = conjugations.filter(mood__name='subjunctive II')
    conjugations_grouped_by_mood = [indicative, subjunctive_I, subjunctive_II]
    context = {
        'verb': verb,
        'next_verb': next_verb,
        'prev_verb': prev_verb,
        'conjugations_grouped_by_mood': conjugations_grouped_by_mood
    }
    return render(request, 'conjugator/conjugation.html', context)


def search(request):
    """
    Searches the Verb table for a verb matching the search query. If a match is
    found redirects to the conjugation view. Otherwise redirects to home with an
    error message.
    """
    search_query = request.GET.get('q')
    if search_query:
        try:
            verb = Verb.objects.get(infinitive__iexact=search_query)
        except Verb.DoesNotExist:
            messages.error(request, f"No verb found matching search query. Please try again.")
            return redirect('home')
        return redirect(reverse('conjugation', kwargs={'infinitive': verb.infinitive}))
    else:
        raise Http404()


def autocomplete(request):
    """
    Creates a list of all infinitives and renders as JSON to be consumed by the
    the third party autocomplete feature (auto-complete.js).
    """
    autocomplete_list = list(Verb.objects.values_list('infinitive', flat=True))
    return JsonResponse(autocomplete_list, safe=False)
