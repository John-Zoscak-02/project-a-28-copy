from django.db import models

# Create your models here.

# We will be able to get this information from the SIS scraper when we have access to that
# To Do: the specifics of all of this will need to change, this is just an outline and example

class Professor(models.Model):
    prof_name = models.CharField(max_length=200)

class Department(models.Model):
    subject = models.CharField(max_length=4)

    def __str__(self):
        return "subject: %s" % (self.suject)

class Course(models.Model):
    catalog_number = models.IntegerField
    description = models.CharField(max_length=64)
    units = models.IntegerField
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return "description: %s\ncatalog_number: %d\nsections: %s" % (self.description, self.catalog_number, self.sections)

class Section(models.Model):
    section_number = models.IntegerField
    wait_list = models.IntegerField
    wait_cap = models.IntegerField
    enrollment_total = models.IntegerField
    enrollment_available= models.IntegerField
    topic = models.CharField(max_length=64)
    question = models.ForeignKey(Course, on_delete=models.CASCADE)
    proffessor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    def __str__(self):
        return "number: %d\ntopic: %s" % (self.section_name, self.topic)


