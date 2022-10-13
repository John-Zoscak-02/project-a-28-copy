from django.db import models

# Create your models here.

# We will be able to get this information from the SIS scraper when we have access to that
# To Do: the specifics of all of this will need to change, this is just an outline and example


class Course(models.Model):
    course_name = models.CharField(max_length=200)
    dept_name = models.CharField(max_length=200)
    dept_abbreviation = models.CharField(max_length=200)
    course_number = models.IntegerField


    def __str__(self):
        return self.course_name


class Professor(models.Model):
    prof_name = models.CharField(max_length=200)


