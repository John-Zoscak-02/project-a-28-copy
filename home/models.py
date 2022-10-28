from django.db import models

# Create your models here.

# We will be able to get this information from the SIS scraper when we have access to that
# To Do: the specifics of all of this will need to change, this is just an outline and example

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
    average_rating = models.DecimalField()
    average_gpa = models.DecimalField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.department} {self.catalog_number} - {self.description} ({self.units} units)"

class Review(models.Model):
    rating = models.IntegerField(max_length=1)
    has_text = models.BooleanField()
    text = models.TextField(max_length=10_000)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

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


