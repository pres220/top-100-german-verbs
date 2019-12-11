from django.shortcuts import render, get_object_or_404, redirect
from .models import Verb, Conjugation
from django.db import connection

def home(request):
    verb_list = Verb.objects.order_by('frequency').values('infinitive', 'frequency')
    verb_list_length = verb_list.count()
    col_list = []
    col_length = 10 if verb_list_length >= 10 else verb_list_length

    for i in range(0, verb_list_length, col_length):
        new_col = []
        for j in range(i, i + col_length):
            try:
                new_col.append(verb_list[j])
            except IndexError:
                break
        col_list.append(new_col)

    context = {
        'col_list': col_list,
        'page_title': 'Top 100 German Verbs',
        'brand': 'Top 100 German Verbs'
    }
    return render(request, 'conjugator/home.html', context)

def conjugation(request, infinitive):
    verb = get_object_or_404(Verb, infinitive__iexact=infinitive)
    next_frequency = verb.frequency + 1 if verb.frequency < Verb.objects.count() else 1
    prev_frequency = verb.frequency - 1 if verb.frequency > 1 else Verb.objects.count()
    next_verb = Verb.objects.get(frequency=next_frequency).infinitive
    prev_verb = Verb.objects.get(frequency=prev_frequency).infinitive
    conjugations = Conjugation.objects.filter(infinitive=verb)
    indicative_present = conjugations.get(mood__name='indicative', tense__name='present')
    indicative_perfect = conjugations.get(mood__name='indicative', tense__name='perfect')
    indicative_preterite = conjugations.get(mood__name='indicative', tense__name='preterite')
    indicative_plusquamperfect = conjugations.get(mood__name='indicative', tense__name='plusquamperfect')
    indicative_future = conjugations.get(mood__name='indicative', tense__name='future')
    indicative_future_perfect = conjugations.get(mood__name='indicative', tense__name='future perfect')
    subjunctive_I_present = conjugations.get(mood__name='subjunctive I', tense__name='present')
    subjunctive_I_perfect = conjugations.get(mood__name='subjunctive I', tense__name='perfect')
    subjunctive_I_future = conjugations.get(mood__name='subjunctive I', tense__name='future')
    subjunctive_I_future_perfect = conjugations.get(mood__name='subjunctive I', tense__name='future perfect')
    subjunctive_II_preterite = conjugations.get(mood__name='subjunctive II', tense__name='preterite')
    subjunctive_II_plusquamperfect = conjugations.get(mood__name='subjunctive II', tense__name='plusquamperfect')
    subjunctive_II_future = conjugations.get(mood__name='subjunctive II', tense__name='future')
    subjunctive_II_future_perfect = conjugations.get(mood__name='subjunctive II', tense__name='future perfect')

    context = {
        'verb': verb,
        'next_verb': next_verb,
        'prev_verb': prev_verb,
        'indicative_present': indicative_present,
        'indicative_perfect': indicative_perfect,
        'indicative_preterite': indicative_preterite,
        'indicative_plusquamperfect': indicative_plusquamperfect,
        'indicative_future': indicative_future,
        'indicative_future_perfect': indicative_future_perfect,
        'subjunctive_I_present': subjunctive_I_present,
        'subjunctive_I_perfect': subjunctive_I_perfect,
        'subjunctive_I_future': subjunctive_I_future,
        'subjunctive_I_future_perfect': subjunctive_I_future_perfect,
        'subjunctive_II_preterite': subjunctive_II_preterite,
        'subjunctive_II_plusquamperfect': subjunctive_II_plusquamperfect,
        'subjunctive_II_future': subjunctive_II_future,
        'subjunctive_II_future_perfect': subjunctive_II_future_perfect,
        'page_title': f'{verb.infinitive} conjugation | Top 100 German Verbs'
    }
    return render(request, 'conjugator/conjugation.html', context)


def search(request):
    search_query = request.GET.get('q')
    if search_query:
        result = Verb.objects.filter(infinitive__iexact=search_query).first()
        if result:
            return redirect(f'/verb/{result.pk}/')
        else:
            context = {
                'search_query': search_query,
                'page_title': 'Search failed | Top 100 German Verbs'
            }
            return render(request, 'conjugator/search_result.html', context)
    else:
        return redirect('/')