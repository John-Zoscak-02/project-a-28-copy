from email.policy import default
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify

from django.db.models import Q

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# We will be able to get this information from the SIS scraper when we have access to that
# To Do: the specifics of all of this will need to change, this is just an outline and example

# Friends feature created by adjusting https://github.com/hellopyplane/Social-Network/blob/master/profiles/models.py to fit our needs


class ProfileManager(models.Manager):
    def get_all_profiles_to_invite(self,sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))
        accepted = set([])
        for rel in qs:
            if rel.status == 'accepted':
                accepted.add(rel.receiver)
                accepted.add(rel.sender)

        available = [profile for profile in profiles if profile not in accepted]
        return available
    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles
        
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    major = models.CharField(max_length=200, blank=True)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    objects = ProfileManager()
    
    def get_friends(self):
        return self.friends.all()
    
    def get_friends_no(self):
        return self.friends.all().count()

    def __str__(self):
        return str(self.user)
        
STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted'),
)

class RelationshipManager(models.Manager):
    def invitations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        return qs

class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()
    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add = True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    
    class Meta:
        ordering = ['date']
    def __str__(self):
        return 'Comment by {} on {}'.format(self.user.username, self.date)

class Department(models.Model):
    subject = models.CharField(max_length=4)

    def __str__(self):
        return self.subject



class Course(models.Model):
    catalog_number = models.CharField(max_length=4)
    description = models.CharField(max_length=64)
    units = models.CharField(max_length=1)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.department} {self.catalog_number} - {self.description} ({self.units} units)"

class Section(models.Model):
    section_number = models.IntegerField(default=0)
    wait_list = models.IntegerField(default=0)
    wait_cap = models.IntegerField(default=0)
    enrollment_total = models.IntegerField(default=0)
    enrollment_available= models.IntegerField(default=0)
    topic = models.CharField(max_length=64)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    prof_name = models.CharField(max_length=200)
    prof_email = models.CharField(max_length=24)
    days = models.CharField(max_length=128)
    start_time = models.CharField(max_length=128)
    end_time = models.CharField(max_length=128)
    facility_description = models.CharField(max_length=128)

    def intersect(self, time, day):
        return day in self.days and float(self.start_time[:5]) <= float(time[:5]) <= float(self.end_time[:5])

    def __str__(self):
        return "number=%d course=%s" % (self.section_number, self.course)

class Schedule(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='schedule', null=True)
    classes = models.ManyToManyField(Section, related_name='schedules')

    def get_translate(self, cls):
        return str(50 * (float(cls.start_time[:2]) - 8) + (((float(cls.start_time[3:5])) / 60) * 50))
    
    def get_scale(self, cls):
        return str(50 * (float(cls.end_time[:2]) - float(cls.start_time[:2])) + (((float(cls.end_time[3:5]) - float(cls.start_time[3:5])) / 60) * 50))

    @property
    def classes_by_day(self):
        by_day = {}
        for cls in self.classes.all():
            days = {cls.days[i:i+2] for i in range(0, len(cls.days), 2)}
            for day in days:
                if not (day in by_day):
                    by_day[day] = []
                by_day[day].append((cls, self.get_translate(cls), self.get_scale(cls)))

        return by_day

