from django.db.utils import IntegrityError
from django.test import Client, TestCase
from django.urls import resolve, reverse

from . import views
from .models import Conjugation, Mood, Tense, Verb


class VerbModelTest(TestCase):

    def setUp(self):
        Verb.objects.create(infinitive='test_infinitive', frequency=1)

    def test_verb_model_str(self):
        verb = Verb.objects.get(infinitive='test_infinitive')
        self.assertEqual(verb.__str__(), verb.infinitive)


class MoodModelTest(TestCase):

    def setUp(self):
        Mood.objects.create(name='test_name')

    def test_mood_model_str(self):
        mood = Mood.objects.get(name='test_name')
        self.assertEqual(mood.__str__(), mood.name)


class TenseModelTest(TestCase):

    def setUp(self):
        Tense.objects.create(name='test_name')

    def test_tense_model_str(self):
        tense = Tense.objects.get(name='test_name')
        self.assertEqual(tense.__str__(), tense.name)


class ConjugationModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        verb = Verb.objects.create(infinitive='test_infinitive', frequency=1)
        mood = Mood.objects.create(name='test_mood')
        tense = Tense.objects.create(name='test_tense')
        Conjugation.objects.create(verb=verb, mood=mood, tense=tense)

    def test_conjugation_model_str(self):
        conjugation = Conjugation.objects.get(pk=1)
        self.assertEqual(conjugation.__str__(),
                         f'{conjugation.verb.infinitive} {conjugation.mood.name} {conjugation.tense.name}')

    def test_unique_constraint(self):
        verb = Verb.objects.get(infinitive='test_infinitive')
        mood = Mood.objects.get(name='test_mood')
        tense = Tense.objects.get(name='test_tense')
        with self.assertRaises(IntegrityError):
            Conjugation.objects.create(verb=verb, mood=mood, tense=tense)


class HomeViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Verb.objects.create(infinitive=f'test_infinitive1', frequency=1)

    def setUp(self):
        self.response = self.client.get(reverse('home'))

    def create_x_verbs(self, stop):
        for i in range(2, stop + 1):
            Verb.objects.create(infinitive=f'test_infinitive{i}', frequency=i)

    def home_view_renders_verbs(self):
        response = self.client.get(reverse('home'))
        verbs = Verb.objects.all()
        for i in range(verbs.count()):
            self.assertContains(response, f'<span class="badge">{verbs[i].frequency}</span>')
            self.assertContains(response, f'{verbs[i].infinitive}')

    def test_home_url_resolves_to_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func, views.home)

    def test_home_view_success_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_home_view_uses_home_template(self):
        self.assertTemplateUsed(self.response, 'conjugator/home.html')

    def test_home_view_brand_rendering(self):
        self.assertContains(self.response, 'Top 100 German Verbs</a>')

    def test_home_view_brand_links_to_home(self):
        self.assertContains(self.response, f'href=\"{reverse("home")}\"')

    def test_home_view_search_form_action_url_links_to_search(self):
        self.assertContains(self.response, f'action="{reverse("search")}"')

    def test_home_view_title(self):
        self.assertContains(self.response, '<title>Top 100 German Verbs</title>')

    def test_home_view_renders_1_verb(self):
        self.home_view_renders_verbs()

    def test_home_view_renders_15_verbs(self):
        self.create_x_verbs(15)
        self.home_view_renders_verbs()

    def test_home_view_renders_100_verbs(self):
        self.create_x_verbs(100)
        self.home_view_renders_verbs()


class AutocompleteViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        for i in range(1, 101):
            Verb.objects.create(infinitive=f'test_infinitive{i}', frequency=i)

    def setUp(self):
        self.response = self.client.get(reverse('autocomplete'))

    def test_autocomplete_url_resolves_to_autocomplete_view(self):
        view = resolve('/autocomplete/')
        self.assertEqual(view.func, views.autocomplete)

    def test_autocomplete_view_success_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_autocomplete_view_renders_all_rows(self):
        self.assertEqual(len(self.response.json()), Verb.objects.count())

    def test_autocomplete_view_renders_json_correctly(self):
        verbs = Verb.objects.all()
        for i in range(verbs.count()):
            self.assertEqual(self.response.json()[i], f'{verbs[i].infinitive}')


class ConjugationViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.verb = Verb.objects.create(
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

        cls.indicative_present = Conjugation.objects.create(
            verb=cls.verb,
            mood=indicative,
            tense=present,
            ich='indicative_present_ich',
            du='indicative_present_du',
            er='indicative_present_er',
            wir='indicative_present_wir',
            ihr='indicative_present_ihr',
            sie='indicative_present_sie'
        )

        cls.indicative_perfect = Conjugation.objects.create(
            verb=cls.verb,
            mood=indicative,
            tense=perfect,
            ich='indicative_perfect_ich',
            du='indicative_perfect_du',
            er='indicative_perfect_er',
            wir='indicative_perfect_wir',
            ihr='indicative_perfect_ihr',
            sie='indicative_perfect_sie'
        )

        cls.indicative_preterite = Conjugation.objects.create(
            verb=cls.verb,
            mood=indicative,
            tense=preterite,
            ich='indicative_preterite_ich',
            du='indicative_preterite_du',
            er='indicative_preterite_er',
            wir='indicative_preterite_wir',
            ihr='indicative_preterite_ihr',
            sie='indicative_preterite_sie'
        )

        cls.indicative_plusquamperfect = Conjugation.objects.create(
            verb=cls.verb,
            mood=indicative,
            tense=plusquamperfect,
            ich='indicative_plusquamperfect_ich',
            du='indicative_plusquamperfect_du',
            er='indicative_plusquamperfect_er',
            wir='indicative_plusquamperfect_wir',
            ihr='indicative_plusquamperfect_ihr',
            sie='indicative_plusquamperfect_sie'
        )

        cls.indicative_future = Conjugation.objects.create(
            verb=cls.verb,
            mood=indicative,
            tense=future,
            ich='indicative_future_ich',
            du='indicative_future_du',
            er='indicative_future_er',
            wir='indicative_future_wir',
            ihr='indicative_future_ihr',
            sie='indicative_future_sie'
        )

        cls.indicative_future_perfect = Conjugation.objects.create(
            verb=cls.verb,
            mood=indicative,
            tense=future_perfect,
            ich='indicative_future_perfect_ich',
            du='indicative_future_perfect_du',
            er='indicative_future_perfect_er',
            wir='indicative_future_perfect_wir',
            ihr='indicative_future_perfect_ihr',
            sie='indicative_future_perfect_sie'
        )

        cls.subjunctive_I_present = Conjugation.objects.create(
            verb=cls.verb,
            mood=subjunctive_I,
            tense=present,
            ich='subjunctive_I_present_ich',
            du='subjunctive_I_present_du',
            er='subjunctive_I_present_er',
            wir='subjunctive_I_present_wir',
            ihr='subjunctive_I_present_ihr',
            sie='subjunctive_I_present_sie'
        )

        cls.subjunctive_I_perfect = Conjugation.objects.create(
            verb=cls.verb,
            mood=subjunctive_I,
            tense=perfect,
            ich='subjunctive_I_perfect_ich',
            du='subjunctive_I_perfect_du',
            er='subjunctive_I_perfect_er',
            wir='subjunctive_I_perfect_wir',
            ihr='subjunctive_I_perfect_ihr',
            sie='subjunctive_I_perfect_sie'
        )

        cls.subjunctive_I_future = Conjugation.objects.create(
            verb=cls.verb,
            mood=subjunctive_I,
            tense=future,
            ich='subjunctive_I_future_ich',
            du='subjunctive_I_future_du',
            er='subjunctive_I_future_er',
            wir='subjunctive_I_future_wir',
            ihr='subjunctive_I_future_ihr',
            sie='subjunctive_I_future_sie'
        )

        cls.subjunctive_I_future_perfect = Conjugation.objects.create(
            verb=cls.verb,
            mood=subjunctive_I,
            tense=future_perfect,
            ich='subjunctive_I_future_perfect_ich',
            du='subjunctive_I_future_perfect_du',
            er='subjunctive_I_future_perfect_er',
            wir='subjunctive_I_future_perfect_wir',
            ihr='subjunctive_I_future_perfect_ihr',
            sie='subjunctive_I_future_perfect_sie'
        )

        cls.subjunctive_II_preterite = Conjugation.objects.create(
            verb=cls.verb,
            mood=subjunctive_II,
            tense=preterite,
            ich='subjunctive_II_preterite_ich',
            du='subjunctive_II_preterite_du',
            er='subjunctive_II_preterite_er',
            wir='subjunctive_II_preterite_wir',
            ihr='subjunctive_II_preterite_ihr',
            sie='subjunctive_II_preterite_sie'
        )

        cls.subjunctive_II_plusquamperfect = Conjugation.objects.create(
            verb=cls.verb,
            mood=subjunctive_II,
            tense=plusquamperfect,
            ich='subjunctive_II_plusquamperfect_ich',
            du='subjunctive_II_plusquamperfect_du',
            er='subjunctive_II_plusquamperfect_er',
            wir='subjunctive_II_plusquamperfect_wir',
            ihr='subjunctive_II_plusquamperfect_ihr',
            sie='subjunctive_II_plusquamperfect_sie'
        )

        cls.subjunctive_II_future = Conjugation.objects.create(
            verb=cls.verb,
            mood=subjunctive_II,
            tense=future,
            ich='subjunctive_II_future_ich',
            du='subjunctive_II_future_du',
            er='subjunctive_II_future_er',
            wir='subjunctive_II_future_wir',
            ihr='subjunctive_II_future_ihr',
            sie='subjunctive_II_future_sie'
        )

        cls.subjunctive_II_future_perfect = Conjugation.objects.create(
            verb=cls.verb,
            mood=subjunctive_II,
            tense=future_perfect,
            ich='subjunctive_II_future_perfect_ich',
            du='subjunctive_II_future_perfect_du',
            er='subjunctive_II_future_perfect_er',
            wir='subjunctive_II_future_perfect_wir',
            ihr='subjunctive_II_future_perfect_ihr',
            sie='subjunctive_II_future_perfect_sie'
        )

        cls.client = Client()
        cls.url = reverse('conjugation', kwargs={'infinitive': f'{cls.verb.infinitive}'})
        cls.response = cls.client.get(cls.url)

    def test_conjugation_url_resolves_to_conjugation_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func, views.conjugation)

    def test_conjugation_view_not_found_status_code(self):
        url = reverse('conjugation', kwargs={'infinitive': 'does_not_exist'})
        no_response = self.client.get(url)
        self.assertEqual(no_response.status_code, 404)

    def test_conjugation_view_success_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_conjugation_view_uses_conjugation_template(self):
        self.assertTemplateUsed(self.response, 'conjugator/conjugation.html')

    def test_conjugation_view_renders_brand(self):
        self.assertContains(self.response, 'Home')

    def test_conjugation_page_title(self):
        self.assertContains(self.response, f'{self.verb.infinitive} conjugation | Top 100 German Verbs')

    def test_conjugation_page_contains_verb_conjugation(self):
        self.assertContains(self.response, self.verb.infinitive)
        self.assertContains(self.response, self.verb.frequency)
        self.assertContains(self.response, self.verb.translation)
        self.assertContains(self.response, self.verb.present_participle)
        self.assertContains(self.response, self.verb.past_participle)

        self.assertContains(self.response, self.indicative_present.ich)
        self.assertContains(self.response, self.indicative_present.du)
        self.assertContains(self.response, self.indicative_present.er)
        self.assertContains(self.response, self.indicative_present.wir)
        self.assertContains(self.response, self.indicative_present.ihr)
        self.assertContains(self.response, self.indicative_present.sie)

        self.assertContains(self.response, self.indicative_perfect.ich)
        self.assertContains(self.response, self.indicative_perfect.du)
        self.assertContains(self.response, self.indicative_perfect.er)
        self.assertContains(self.response, self.indicative_perfect.wir)
        self.assertContains(self.response, self.indicative_perfect.ihr)
        self.assertContains(self.response, self.indicative_perfect.sie)

        self.assertContains(self.response, self.indicative_preterite.ich)
        self.assertContains(self.response, self.indicative_preterite.du)
        self.assertContains(self.response, self.indicative_preterite.er)
        self.assertContains(self.response, self.indicative_preterite.wir)
        self.assertContains(self.response, self.indicative_preterite.ihr)
        self.assertContains(self.response, self.indicative_preterite.sie)

        self.assertContains(self.response, self.indicative_plusquamperfect.ich)
        self.assertContains(self.response, self.indicative_plusquamperfect.du)
        self.assertContains(self.response, self.indicative_plusquamperfect.er)
        self.assertContains(self.response, self.indicative_plusquamperfect.wir)
        self.assertContains(self.response, self.indicative_plusquamperfect.ihr)
        self.assertContains(self.response, self.indicative_plusquamperfect.sie)

        self.assertContains(self.response, self.indicative_future.ich)
        self.assertContains(self.response, self.indicative_future.du)
        self.assertContains(self.response, self.indicative_future.er)
        self.assertContains(self.response, self.indicative_future.wir)
        self.assertContains(self.response, self.indicative_future.ihr)
        self.assertContains(self.response, self.indicative_future.sie)

        self.assertContains(self.response, self.indicative_future_perfect.ich)
        self.assertContains(self.response, self.indicative_future_perfect.du)
        self.assertContains(self.response, self.indicative_future_perfect.er)
        self.assertContains(self.response, self.indicative_future_perfect.wir)
        self.assertContains(self.response, self.indicative_future_perfect.ihr)
        self.assertContains(self.response, self.indicative_future_perfect.sie)

        self.assertContains(self.response, self.subjunctive_I_present.ich)
        self.assertContains(self.response, self.subjunctive_I_present.du)
        self.assertContains(self.response, self.subjunctive_I_present.er)
        self.assertContains(self.response, self.subjunctive_I_present.wir)
        self.assertContains(self.response, self.subjunctive_I_present.ihr)
        self.assertContains(self.response, self.subjunctive_I_present.sie)

        self.assertContains(self.response, self.subjunctive_I_perfect.ich)
        self.assertContains(self.response, self.subjunctive_I_perfect.du)
        self.assertContains(self.response, self.subjunctive_I_perfect.er)
        self.assertContains(self.response, self.subjunctive_I_perfect.wir)
        self.assertContains(self.response, self.subjunctive_I_perfect.ihr)
        self.assertContains(self.response, self.subjunctive_I_perfect.sie)

        self.assertContains(self.response, self.subjunctive_I_future.ich)
        self.assertContains(self.response, self.subjunctive_I_future.du)
        self.assertContains(self.response, self.subjunctive_I_future.er)
        self.assertContains(self.response, self.subjunctive_I_future.wir)
        self.assertContains(self.response, self.subjunctive_I_future.ihr)
        self.assertContains(self.response, self.subjunctive_I_future.sie)

        self.assertContains(self.response, self.subjunctive_I_future_perfect.ich)
        self.assertContains(self.response, self.subjunctive_I_future_perfect.du)
        self.assertContains(self.response, self.subjunctive_I_future_perfect.er)
        self.assertContains(self.response, self.subjunctive_I_future_perfect.wir)
        self.assertContains(self.response, self.subjunctive_I_future_perfect.ihr)
        self.assertContains(self.response, self.subjunctive_I_future_perfect.sie)

        self.assertContains(self.response, self.subjunctive_II_preterite.ich)
        self.assertContains(self.response, self.subjunctive_II_preterite.du)
        self.assertContains(self.response, self.subjunctive_II_preterite.er)
        self.assertContains(self.response, self.subjunctive_II_preterite.wir)
        self.assertContains(self.response, self.subjunctive_II_preterite.ihr)
        self.assertContains(self.response, self.subjunctive_II_preterite.sie)

        self.assertContains(self.response, self.subjunctive_II_plusquamperfect.ich)
        self.assertContains(self.response, self.subjunctive_II_plusquamperfect.du)
        self.assertContains(self.response, self.subjunctive_II_plusquamperfect.er)
        self.assertContains(self.response, self.subjunctive_II_plusquamperfect.wir)
        self.assertContains(self.response, self.subjunctive_II_plusquamperfect.ihr)
        self.assertContains(self.response, self.subjunctive_II_plusquamperfect.sie)

        self.assertContains(self.response, self.subjunctive_II_future.ich)
        self.assertContains(self.response, self.subjunctive_II_future.du)
        self.assertContains(self.response, self.subjunctive_II_future.er)
        self.assertContains(self.response, self.subjunctive_II_future.wir)
        self.assertContains(self.response, self.subjunctive_II_future.ihr)
        self.assertContains(self.response, self.subjunctive_II_future.sie)

        self.assertContains(self.response, self.subjunctive_II_future_perfect.ich)
        self.assertContains(self.response, self.subjunctive_II_future_perfect.du)
        self.assertContains(self.response, self.subjunctive_II_future_perfect.er)
        self.assertContains(self.response, self.subjunctive_II_future_perfect.wir)
        self.assertContains(self.response, self.subjunctive_II_future_perfect.ihr)
        self.assertContains(self.response, self.subjunctive_II_future_perfect.sie)


class SearchViewTest(ConjugationViewTest):

    def test_search_view_url_resolves_to_search_view(self):
        view = resolve('/search/')
        self.assertEqual(view.func, views.search)

    def test_search_view_raises_404_with_empty_search_query(self):
        response = self.client.get(reverse('search'), {'q': ''})
        self.assertEqual(response.status_code, 404)

    def test_search_view_redirect_status_code(self):
        response = self.client.get(reverse('search'), {'q': self.verb.infinitive})
        self.assertEqual(response.status_code, 302)

    def test_search_view_redirects_to_conjugation_url_with_lowercase_query(self):
        response = self.client.get(reverse('search'), {'q': self.verb.infinitive})
        url = reverse('conjugation', kwargs={'infinitive': self.verb.infinitive})
        self.assertRedirects(response, url)

    def test_search_view_redirects_to_conjugation_url_with_non_lowercase_query(self):
        response = self.client.get(reverse('search'), {'q': 'Test_Infinitive'})
        url = reverse('conjugation', kwargs={'infinitive': self.verb.infinitive})
        self.assertRedirects(response, url)

    def test_search_view_redirected_to_home_view_success_status_code(self):
        response = self.client.get(reverse('search'), {'q': 'does_not_exist'}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_search_view_redirected_to_home_view_using_home_template(self):
        response = self.client.get(reverse('search'), {'q': 'does_not_exist'}, follow=True)
        self.assertTemplateUsed(response, 'conjugator/home.html')

    def test_search_view_error_message_available_to_home_view(self):
        response = self.client.get(reverse('search'), {'q': 'does_not_exist'}, follow=True)
        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, 'No verb found matching search query. Please try again.')

    def test_search_view_error_message_rendered_after_redirect(self):
        response = self.client.get(reverse('search'), {'q': 'does_not_exist'}, follow=True)
        self.assertContains(response, 'No verb found matching search query. Please try again.')
