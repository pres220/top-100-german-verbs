from django.test import TestCase
from django.db.utils import IntegrityError
from django.urls import reverse
from .models import Verb, Mood, Tense, Conjugation


class VerbModelTest(TestCase):

    def setUp(self):
        Verb.objects.create(
            infinitive='test_infinitive',
            frequency=1,
            translation='test_translation',
            present_participle='test_present_participle',
            past_participle='test_past_participle',
        )

    def test_fields(self):
        verb = Verb.objects.get(infinitive='test_infinitive')
        self.assertTrue(isinstance(verb, Verb))
        self.assertEqual(verb.__str__(), verb.infinitive)
        self.assertEqual(verb.infinitive, 'test_infinitive')
        self.assertEqual(verb.frequency, 1)
        self.assertEqual(verb.translation, 'test_translation')
        self.assertEqual(verb.present_participle, 'test_present_participle')
        self.assertEqual(verb.past_participle, 'test_past_participle')


class MoodModelTest(TestCase):

    def setUp(self):
        Mood.objects.create(name='test_name')

    def test_name(self):
        mood = Mood.objects.get(name='test_name')
        self.assertTrue(isinstance(mood, Mood))
        self.assertEqual(mood.__str__(), mood.name)
        self.assertEqual(mood.name, 'test_name')


class TenseModelTest(TestCase):

    def setUp(self):
        Tense.objects.create(name='test_name')

    def test_name(self):
        tense = Tense.objects.get(name='test_name')
        self.assertTrue(isinstance(tense, Tense))
        self.assertEqual(tense.__str__(), tense.name)
        self.assertEqual(tense.name, 'test_name')


class ConjugationModelTest(TestCase):

    def setUp(self):
        verb = Verb.objects.create(
            infinitive='test_infinitive',
            frequency=1,
            translation='test_translation',
            present_participle='test_present_participle',
            past_participle='test_past_participle',
        )

        mood = Mood.objects.create(name='test_mood')
        tense = Tense.objects.create(name='test_tense')

        Conjugation.objects.create(
            verb=verb,
            mood=mood,
            tense=tense,
            ich='test_ich',
            du='test_du',
            er='test_er',
            wir='test_wir',
            ihr='test_ihr',
            sie='test_sie'
        )

    def test_fields(self):
        conjugation = Conjugation.objects.get(pk=1)
        self.assertTrue(isinstance(conjugation, Conjugation))
        self.assertEqual(conjugation.__str__(),
            f'{conjugation.verb.infinitive} {conjugation.mood.name} {conjugation.tense.name}')
        self.assertEqual(conjugation.verb.infinitive, 'test_infinitive')
        self.assertEqual(conjugation.mood.name, 'test_mood')
        self.assertEqual(conjugation.tense.name, 'test_tense')
        self.assertEqual(conjugation.ich, 'test_ich')
        self.assertEqual(conjugation.du, 'test_du')
        self.assertEqual(conjugation.er, 'test_er')
        self.assertEqual(conjugation.wir, 'test_wir')
        self.assertEqual(conjugation.ihr, 'test_ihr')
        self.assertEqual(conjugation.sie, 'test_sie')

    def test_unique_constraint(self):
        verb = Verb.objects.get(infinitive='test_infinitive')
        mood = Mood.objects.get(name='test_mood')
        tense = Tense.objects.get(name='test_tense')
        with self.assertRaises(IntegrityError):
            Conjugation.objects.create(
                verb=verb,
                mood=mood,
                tense=tense,
                ich='test_ich2',
                du='test_du2',
                er='test_er2',
                wir='test_wir2',
                ihr='test_ihr2',
                sie='test_sie2'
            )


class HomeViewTest(TestCase):

    def setUp(self):
        for i in range(1, 12):
            Verb.objects.create(
                infinitive=f'test_infinitive{i}',
                frequency=i,
            )

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conjugator/home.html')
        for i in range(1, 12):
            self.assertContains(response, f'test_infinitive{i}')


class AutocompleteViewTest(TestCase):

    def setUp(self):
        for i in range(1, 101):
            Verb.objects.create(
                infinitive=f'test_infinitive{i}',
                frequency=i,
            )

    def test_autocomplete_json(self):
        response = self.client.get(reverse('autocomplete'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), Verb.objects.count())
        for i in range(1, 101):
            self.assertEqual(response.json()[i-1], f'test_infinitive{i}')


class ConjugationViewTest(TestCase):

    def setUp(self):
        verb = Verb.objects.create(
            infinitive='test_infinitive',
            frequency=1,
            translation='test_translation',
            present_participle='test_present_participle',
            past_participle='test_past_participle',
        )

        indicative = Mood.objects.create(name='indicative')
        subjunctive_I = Mood.objects.create(name='subjunctive I')
        subjunctive_II = Mood.objects.create(name='subjunctive II')

        present = Tense.objects.create(name='present')
        perfect = Tense.objects.create(name='perfect')
        preterite = Tense.objects.create(name='preterite')
        plusquamperfect = Tense.objects.create(name='plusquamperfect')
        future = Tense.objects.create(name='future')
        future_perfect = Tense.objects.create(name='future perfect')

        Conjugation.objects.create(
            verb=verb,
            mood=indicative,
            tense=present,
            ich='indicative_present_ich',
            du='indicative_present_du',
            er='indicative_present_er',
            wir='indicative_present_wir',
            ihr='indicative_present_ihr',
            sie='indicative_present_sie'
        )

        Conjugation.objects.create(
            verb=verb,
            mood=indicative,
            tense=perfect,
            ich='indicative_perfect_ich',
            du='indicative_perfect_du',
            er='indicative_perfect_er',
            wir='indicative_perfect_wir',
            ihr='indicative_perfect_ihr',
            sie='indicative_perfect_sie'
        )

        Conjugation.objects.create(
            verb=verb,
            mood=indicative,
            tense=preterite,
            ich='indicative_preterite_ich',
            du='indicative_preterite_du',
            er='indicative_preterite_er',
            wir='indicative_preterite_wir',
            ihr='indicative_preterite_ihr',
            sie='indicative_preterite_sie'
        )

        Conjugation.objects.create(
            verb=verb,
            mood=indicative,
            tense=plusquamperfect,
            ich='indicative_plusquamperfect_ich',
            du='indicative_plusquamperfect_du',
            er='indicative_plusquamperfect_er',
            wir='indicative_plusquamperfect_wir',
            ihr='indicative_plusquamperfect_ihr',
            sie='indicative_plusquamperfect_sie'
        )

        Conjugation.objects.create(
            verb=verb,
            mood=indicative,
            tense=future,
            ich='indicative_future_ich',
            du='indicative_future_du',
            er='indicative_future_er',
            wir='indicative_future_wir',
            ihr='indicative_future_ihr',
            sie='indicative_future_sie'
        )

        Conjugation.objects.create(
            verb=verb,
            mood=indicative,
            tense=future_perfect,
            ich='indicative_future_perfect_ich',
            du='indicative_future_perfect_du',
            er='indicative_future_perfect_er',
            wir='indicative_future_perfect_wir',
            ihr='indicative_future_perfect_ihr',
            sie='indicative_future_perfect_sie'
        )

        Conjugation.objects.create(
            verb=verb,
            mood=subjunctive_I,
            tense=present,
            ich='subjunctive_I_present_ich',
            du='subjunctive_I_present_du',
            er='subjunctive_I_present_er',
            wir='subjunctive_I_present_wir',
            ihr='subjunctive_I_present_ihr',
            sie='subjunctive_I_present_sie'
        )

        Conjugation.objects.create(
            verb=verb,
            mood=subjunctive_I,
            tense=perfect,
            ich='subjunctive_I_perfect_ich',
            du='subjunctive_I_perfect_du',
            er='subjunctive_I_perfect_er',
            wir='subjunctive_I_perfect_wir',
            ihr='subjunctive_I_perfect_ihr',
            sie='subjunctive_I_perfect_sie'
        )

        Conjugation.objects.create(
            verb=verb,
            mood=subjunctive_I,
            tense=future,
            ich='subjunctive_I_future_ich',
            du='subjunctive_I_future_du',
            er='subjunctive_I_future_er',
            wir='subjunctive_I_future_wir',
            ihr='subjunctive_I_future_ihr',
            sie='subjunctive_I_future_sie'
        )

        Conjugation.objects.create(
            verb=verb,
            mood=subjunctive_I,
            tense=future_perfect,
            ich='subjunctive_I_future_perfect_ich',
            du='subjunctive_I_future_perfect_du',
            er='subjunctive_I_future_perfect_er',
            wir='subjunctive_I_future_perfect_wir',
            ihr='subjunctive_I_future_perfect_ihr',
            sie='subjunctive_I_future_perfect_sie'
        )

        Conjugation.objects.create(
            verb=verb,
            mood=subjunctive_II,
            tense=preterite,
            ich='subjunctive_II_preterite_ich',
            du='subjunctive_II_preterite_du',
            er='subjunctive_II_preterite_er',
            wir='subjunctive_II_preterite_wir',
            ihr='subjunctive_II_preterite_ihr',
            sie='subjunctive_II_preterite_sie'
        )

        Conjugation.objects.create(
            verb=verb,
            mood=subjunctive_II,
            tense=plusquamperfect,
            ich='subjunctive_II_plusquamperfect_ich',
            du='subjunctive_II_plusquamperfect_du',
            er='subjunctive_II_plusquamperfect_er',
            wir='subjunctive_II_plusquamperfect_wir',
            ihr='subjunctive_II_plusquamperfect_ihr',
            sie='subjunctive_II_plusquamperfect_sie'
        )

        Conjugation.objects.create(
            verb=verb,
            mood=subjunctive_II,
            tense=future,
            ich='subjunctive_II_future_ich',
            du='subjunctive_II_future_du',
            er='subjunctive_II_future_er',
            wir='subjunctive_II_future_wir',
            ihr='subjunctive_II_future_ihr',
            sie='subjunctive_II_future_sie'
        )

        Conjugation.objects.create(
            verb=verb,
            mood=subjunctive_II,
            tense=future_perfect,
            ich='subjunctive_II_future_perfect_ich',
            du='subjunctive_II_future_perfect_du',
            er='subjunctive_II_future_perfect_er',
            wir='subjunctive_II_future_perfect_wir',
            ihr='subjunctive_II_future_perfect_ihr',
            sie='subjunctive_II_future_perfect_sie'
        )

    def test_detail_page_not_created_for_nonexisting_verb(self):
        url = reverse('conjugation', kwargs={'infinitive':'does_not_exist'})
        no_response = self.client.get(url)
        self.assertEqual(no_response.status_code, 404)

    def test_detail_page_created_for_existing_verb(self):
        url = reverse('conjugation', kwargs={'infinitive':'test_infinitive'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conjugator/conjugation.html')

    def test_detail_page_contains_conjugation(self):
        url = reverse('conjugation', kwargs={'infinitive':'test_infinitive'})
        response = self.client.get(url)
        self.assertContains(response, 'test_infinitive')
        self.assertContains(response, '1st')
        self.assertContains(response, 'test_translation')
        self.assertContains(response, 'test_present_participle')
        self.assertContains(response, 'test_past_participle')

        self.assertContains(response, 'indicative_present_ich')
        self.assertContains(response, 'indicative_present_du')
        self.assertContains(response, 'indicative_present_er')
        self.assertContains(response, 'indicative_present_wir')
        self.assertContains(response, 'indicative_present_ihr')
        self.assertContains(response, 'indicative_present_sie')

        self.assertContains(response, 'indicative_perfect_ich')
        self.assertContains(response, 'indicative_perfect_du')
        self.assertContains(response, 'indicative_perfect_er')
        self.assertContains(response, 'indicative_perfect_wir')
        self.assertContains(response, 'indicative_perfect_ihr')
        self.assertContains(response, 'indicative_perfect_sie')

        self.assertContains(response, 'indicative_preterite_ich')
        self.assertContains(response, 'indicative_preterite_du')
        self.assertContains(response, 'indicative_preterite_er')
        self.assertContains(response, 'indicative_preterite_wir')
        self.assertContains(response, 'indicative_preterite_ihr')
        self.assertContains(response, 'indicative_preterite_sie')

        self.assertContains(response, 'indicative_plusquamperfect_ich')
        self.assertContains(response, 'indicative_plusquamperfect_du')
        self.assertContains(response, 'indicative_plusquamperfect_er')
        self.assertContains(response, 'indicative_plusquamperfect_wir')
        self.assertContains(response, 'indicative_plusquamperfect_ihr')
        self.assertContains(response, 'indicative_plusquamperfect_sie')

        self.assertContains(response, 'indicative_future_ich')
        self.assertContains(response, 'indicative_future_du')
        self.assertContains(response, 'indicative_future_er')
        self.assertContains(response, 'indicative_future_wir')
        self.assertContains(response, 'indicative_future_ihr')
        self.assertContains(response, 'indicative_future_sie')

        self.assertContains(response, 'indicative_future_perfect_ich')
        self.assertContains(response, 'indicative_future_perfect_du')
        self.assertContains(response, 'indicative_future_perfect_er')
        self.assertContains(response, 'indicative_future_perfect_wir')
        self.assertContains(response, 'indicative_future_perfect_ihr')
        self.assertContains(response, 'indicative_future_perfect_sie')

        self.assertContains(response, 'subjunctive_I_present_ich')
        self.assertContains(response, 'subjunctive_I_present_du')
        self.assertContains(response, 'subjunctive_I_present_er')
        self.assertContains(response, 'subjunctive_I_present_wir')
        self.assertContains(response, 'subjunctive_I_present_ihr')
        self.assertContains(response, 'subjunctive_I_present_sie')

        self.assertContains(response, 'subjunctive_I_perfect_ich')
        self.assertContains(response, 'subjunctive_I_perfect_du')
        self.assertContains(response, 'subjunctive_I_perfect_er')
        self.assertContains(response, 'subjunctive_I_perfect_wir')
        self.assertContains(response, 'subjunctive_I_perfect_ihr')
        self.assertContains(response, 'subjunctive_I_perfect_sie')

        self.assertContains(response, 'subjunctive_I_future_ich')
        self.assertContains(response, 'subjunctive_I_future_du')
        self.assertContains(response, 'subjunctive_I_future_er')
        self.assertContains(response, 'subjunctive_I_future_wir')
        self.assertContains(response, 'subjunctive_I_future_ihr')
        self.assertContains(response, 'subjunctive_I_future_sie')

        self.assertContains(response, 'subjunctive_I_future_perfect_ich')
        self.assertContains(response, 'subjunctive_I_future_perfect_du')
        self.assertContains(response, 'subjunctive_I_future_perfect_er')
        self.assertContains(response, 'subjunctive_I_future_perfect_wir')
        self.assertContains(response, 'subjunctive_I_future_perfect_ihr')
        self.assertContains(response, 'subjunctive_I_future_perfect_sie')

        self.assertContains(response, 'subjunctive_II_preterite_ich')
        self.assertContains(response, 'subjunctive_II_preterite_du')
        self.assertContains(response, 'subjunctive_II_preterite_er')
        self.assertContains(response, 'subjunctive_II_preterite_wir')
        self.assertContains(response, 'subjunctive_II_preterite_ihr')
        self.assertContains(response, 'subjunctive_II_preterite_sie')

        self.assertContains(response, 'subjunctive_II_plusquamperfect_ich')
        self.assertContains(response, 'subjunctive_II_plusquamperfect_du')
        self.assertContains(response, 'subjunctive_II_plusquamperfect_er')
        self.assertContains(response, 'subjunctive_II_plusquamperfect_wir')
        self.assertContains(response, 'subjunctive_II_plusquamperfect_ihr')
        self.assertContains(response, 'subjunctive_II_plusquamperfect_sie')

        self.assertContains(response, 'subjunctive_II_future_ich')
        self.assertContains(response, 'subjunctive_II_future_du')
        self.assertContains(response, 'subjunctive_II_future_er')
        self.assertContains(response, 'subjunctive_II_future_wir')
        self.assertContains(response, 'subjunctive_II_future_ihr')
        self.assertContains(response, 'subjunctive_II_future_sie')

        self.assertContains(response, 'subjunctive_II_future_perfect_ich')
        self.assertContains(response, 'subjunctive_II_future_perfect_du')
        self.assertContains(response, 'subjunctive_II_future_perfect_er')
        self.assertContains(response, 'subjunctive_II_future_perfect_wir')
        self.assertContains(response, 'subjunctive_II_future_perfect_ihr')
        self.assertContains(response, 'subjunctive_II_future_perfect_sie')


class SearchViewTest(ConjugationViewTest):

    def test_empty_search_query_redirect(self):
        response = self.client.get(reverse('search'), {'q':''} )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_lowercase_search_query_redirect(self):
        response = self.client.get(reverse('search'), {'q':'test_infinitive'})
        self.assertEqual(response.status_code, 302)
        url = reverse('conjugation', kwargs={'infinitive':'test_infinitive'})
        self.assertRedirects(response, url)

    def test_nonlowercase_search_query_redirect(self):
        response = self.client.get(reverse('search'), {'q':'Test_Infinitive'})
        self.assertEqual(response.status_code, 302)
        url = reverse('conjugation', kwargs={'infinitive':'test_infinitive'})
        self.assertRedirects(response, url)

    def test_search_query_does_not_exist(self):
        response = self.client.get(reverse('search'), {'q':'does_not_exist'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'conjugator/search_result.html')
        self.assertContains(response, 'does_not_exist')
