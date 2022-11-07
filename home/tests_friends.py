import email
from django.test import TestCase
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.models import User
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
class BaseTestCase(TestCase):
    def setUp(self):
        """
        Setup some initial users
        """
        self.user_pw = "test"
        self.user_bob = self.create_user("bob", "bob@bob.com", self.user_pw)
        self.user_steve = self.create_user("steve", "steve@steve.com", self.user_pw)
        self.user_susan = self.create_user("susan", "susan@susan.com", self.user_pw)
        self.user_amy = self.create_user("amy", "amy@amy.amy.com", self.user_pw)
        cache.clear()

    def tearDown(self):
        cache.clear()
        self.client.logout()

    def create_user(self, username, email_address, password):
        user = User.objects.create_user(username, email_address, password)
        return user

    def assertResponse200(self, response):
        self.assertEqual(response.status_code, 200)

    def assertResponse302(self, response):
        self.assertEqual(response.status_code, 302)

    def assertResponse403(self, response):
        self.assertEqual(response.status_code, 403)

    def assertResponse404(self, response):
        self.assertEqual(response.status_code, 404)


class ProfileManagerTests(BaseTestCase):
    def test_friends_error(self):
        """
        If page results in 200 error, site is running
        """
        response = self.client.get('/friends')
        self.assertEquals(response.status_code, 301)
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
        self.assertEquals(response.status_code, 302)

    def test_friendship_request(self):
        self.assertNotEqual(Profile.objects.get_all_profiles(self.user_bob), [])


    def test_user_not_in_profiles(self):
        results = Profile.objects.get_all_profiles(self.user_bob)
        self.assertEqual(len(results), 3)
        self.assertTrue(Profile.objects.filter(id=self.user_amy.id).exists())
        self.assertFalse(Profile.objects.filter(id=self.user_bob.id).exists())
        
    def test_user_not_in_profiles(self):
        results = Profile.objects.get_all_profiles_to_invite(self.user_bob)
        self.assertEqual(len(results), 3)
        self.assertTrue(Profile.objects.filter(id=self.user_amy.id).exists())
        self.assertFalse(Profile.objects.filter(id=self.user_bob.id).exists())

    def test_for_correct_fields(self):
        email = self.user_amy.get_email_field_name
        username = self.user_amy.get_username
        self.assertEquals(email, "amy@amy.amy.com")
        self.assertEquals(username, "amy")