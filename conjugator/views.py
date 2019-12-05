from django.shortcuts import render
from .models import Infinitive

def home(request):
    verb_list = Infinitive.objects.order_by('frequency')
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

    context = { 'col_list': col_list, 'page_title': 'Top 100 German Verbs'}
    return render(request, 'conjugator/home.html', context)
