from django.test import TestCase
from django.urls import reverse
from django.db import IntegrityError

from home.views import profiles_list_view
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
    def test_friends_error(self):
        """
        If page results in 200 error, site is running
        """
        response = self.client.get('profile')
        self.assertEquals(response.status_code, 200)
    def test_friend_error2(self):
        """
        If random url is input in, test fails
        """
        response = self.client.get('/friends/random')
        self.assertEquals(response.status_code, 404)
    
    def test_friends_error3(self):
        """
        If page redirects to friends, it's good
        """
        response = self.client.get('/friends/accept/')
        self.assertEquals(response.client.request, 302)

    def test_friends_error4(self):
        """
        If page redirects to friends, it's good
        """
        response = self.client.get('/friends/reject/')
        self.assertEquals(response.status_code, 302)