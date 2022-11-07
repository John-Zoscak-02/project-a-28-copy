from django.test import TestCase
from django.urls import reverse
from django.db import IntegrityError
from .models import Course, Department, Relationship, Section, Professor, Profile
from django.core.cache import cache
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

class ProfileManagerTests(TestCase):
    def test_no_self_follow(self):
        self.assertEqual(True)