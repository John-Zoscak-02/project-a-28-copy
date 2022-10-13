from django.test import TestCase

# Create your tests here.
import datetime

from django.test import TestCase
from django.utils import timezone

#from .models import Question
from django.urls import reverse
# def create_question(question_text, days):
#     """
#     Create a question with the given `question_text` and published the
#     given number of `days` offset to now (negative for questions published
#     in the past, positive for questions that have yet to be published).
#     """
#     time = timezone.now() + datetime.timedelta(days=days)
#     return Question.objects.create(question_text=question_text, pub_date=time)


class GoogleLoginViewTests(TestCase):
    def test_page_error(self):
        """
        If page results in 200 error, site is running
        """
        response = self.client.get('/accounts/login/')
        self.assertEquals(response.status_code, 200)
    def test_page_error2(self):
        """
        If random url is input in, test fails
        """
        response = self.client.get('/accounts/random')
        self.assertEquals(response.status_code, 404)
    