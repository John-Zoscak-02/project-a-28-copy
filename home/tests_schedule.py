from django.test import TestCase

# Create your tests here.
import datetime

from django.test import TestCase
from django.utils import timezone
from django.contrib import auth

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

class ScheduleViewTests(TestCase):
    def test_NoLogin_Schedule(self):
        self.assertTrue(1)

