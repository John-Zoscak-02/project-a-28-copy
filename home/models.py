from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# We will be able to get this information from the SIS scraper when we have access to that
# To Do: the specifics of all of this will need to change, this is just an outline and example

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()

class Profile(models.Model):
    first = 1
    second = 2
    third = 3
    fourth = 4
    grad_student = 5
    other = 6
    ROLE_CHOICES = (
        (first, 'First Year'),
        (second, 'Second Year'),
        (third, 'Thrid Year'),
        (fourth, 'Fourth Year'),
        (grad_student, 'Graduate Student'),
        (other, 'Other'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)
    major = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True
    )
    def __str__(self):
        return self.user.username

class Calendar(models.Model):
    date = models.DateField()

    def __str__(self):
        return "Date: %s" % (self.date)

class AboutUs(models.Model):
    contact = models.TextField(max_length=1000)

class Professor(models.Model):
    prof_name = models.CharField(max_length=200)
    prof_email = models.CharField(max_length=24)

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
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    days = models.CharField(max_length=128)
    start_time = models.CharField(max_length=128)
    end_time = models.CharField(max_length=128)
    facility_description = models.CharField(max_length=128)


    def __str__(self):
        return "number=%d course=%s" % (self.section_number, self.course)


