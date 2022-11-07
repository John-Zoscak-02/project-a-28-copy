from pyexpat import model
from django.db import models

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# We will be able to get this information from the SIS scraper when we have access to that
# To Do: the specifics of all of this will need to change, this is just an outline and example

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    friends_with = models.ForeignKey("self", on_delete=models.CASCADE, related_name='friends', null=True)

    def __str__(self):  # __unicode__ for Python 2
        return str(self.user)

@receiver(post_save, sender=User)
def watchlist_create(sender, instance=None, created=False, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class AboutUs(models.Model):
    contact = models.TextField(max_length=1000)
    def __str__(self):
        return "Prof=%s Email=%s" % (self.prof_name, self.prof_email)

class Department(models.Model):
    subject = models.CharField(max_length=4)

    def __str__(self):
        return self.subject

class Course(models.Model):
    catalog_number = models.CharField(max_length=4)
    description = models.CharField(max_length=64)
    units = models.CharField(max_length=1)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

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

    @property
    def classes_by_time(self):
        by_time = {}
        for cls in self.classes.all():
            start_time = cls.start_time
            end_time = cls.end_time
            if start_time:
                scale = ((float(end_time[:2]) - float(start_time[:2])) + 
                        (float(end_time[3:5]) - float(start_time[3:5])))
                translate = float(start_time[3:5]) / 60
                t=''
                if float(start_time[:2]) < 12:
                    t = (str(start_time[:2])+"am", scale, translate)
                else:
                    t = (str(start_time[:2])+"pm", scale, translate)

                if t in by_time:
                    by_time[t].append((cls, (scale, translate)))
                else:
                    by_time[t] = []
                    by_time[t].append((cls, (scale, translate)))
        return by_time


