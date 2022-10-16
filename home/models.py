from django.db import models

# Create your models here.

# We will be able to get this information from the SIS scraper when we have access to that
# To Do: the specifics of all of this will need to change, this is just an outline and example

class Professor(models.Model):
    prof_name = models.CharField(max_length=200)
    prof_email = models.CharField(max_length=24)

class Department(models.Model):
    subject = models.CharField(max_length=4)

    def __str__(self):
        return "subject: %s" % (self.subject)

class Course(models.Model):
    catalog_number = models.CharField(max_length=4)
    description = models.CharField(max_length=64)
    units = models.CharField(max_length=1)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return "description: %s\n - %s %s" % (self.description, self.department, self.catalog_number)

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
        return "number: %d\ntopic: %s" % (self.section_number, self.topic)


