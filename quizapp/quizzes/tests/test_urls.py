from django.test import TestCase, Client
from quizzes.views import quiz
from django.urls import reverse, resolve
from quizzes.models import Quiz


class QuizzesUrlsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_quiz = Quiz.objects.create(
            name='TEST',
            topic='test',
            number_of_questions=5,
            number_of_answers=5,
            time=6,
            score=80,
            difficulty='easy'
        )

    def test_quiz_url_is_resolved(self):
        url = reverse('quiz')
        self.assertEqual(resolve(url).func, quiz)

    def test_quiz_data_is_response(self):
        response = self.client.get(f'/quizzes/{self.test_quiz.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_quiz_data_view_is_response(self):
        response = self.client.get(f'/quizzes/{self.test_quiz.pk}/data/')
        self.assertEqual(response.status_code, 200)
