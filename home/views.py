from django.shortcuts import render
from django.views import generic

from .models import Course, Department, Section, Professor
from django.views.generic.edit import CreateView

import urllib3
import json

# Create your views here.
#class LandingView(generic.ListView):
#    template_name = 'home/landing.html'

#    def get_queryset(self):
#        """
#        Return nothing (right now)
#        """
#        return []


def landing(request):  # We probably want this to be the list view of als the courses
    return render(request, 'home/landing.html')

class AboutUsView(generic.ListView):
    model = Professor
    template_name= 'home/about-us.html'
    def about_us(request): 
        return render(request, 'home/about-us.html')

def deserialize_from_luthers_list():
    http = urllib3.PoolManager()

    depts_r = http.request('GET', "http://luthers-list.herokuapp.com/api/deptlist/?format=json")
    depts = json.loads(depts_r.data.decode('utf-8'))

    for subject in depts:
        dept = Department(subject=subject)
        dept.save()
        sections_r = http.request('GET', "http://luthers-list.herokuapp.com/api/dept/%s/?format=json" % subject)
        sections = json.loads(sections_r.data.decode('utf-8'))

        for s in sections:
            course = Course.objects.get(description=s.description)
            if course == Course.DoesNotExist:
                course = Course(catalog_number=s.catalog_number,
                                description=s.description,
                                units=s.units,
                                department=dept.pk)
                course.save()

            professor = Professor.objects.get(prof_name=s.instructor.name)
            if professor == Professor.DoesNotExist:
                professor = Professor(prof_name=s.instructor.name,
                                description=s.instructor.email)
                professor.save()
            
            section = Section(section_number=s.course_number,
                        wait_list=s.wait_list,
                        wait_cap=s.wait_cap,
                        enrollment_total=s.enrollment_total,
                        enrollment_avaialable=s.enrollment_avaiable,
                        topic=s.topic,
                        course=course.pk,
                        proffessor=professor.pk,
                        days=s.meetings.days,
                        start_time=s.meetings.start_time,
                        end_time=s.meetings.end_time,
                        facility_description=s.meetings.facility_description)
            section.save()




def calendar(request):
    return render(request, 'home/calendar.html')


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'home/course_detail.html'

