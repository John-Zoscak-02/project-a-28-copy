from django.shortcuts import render
from django.views import generic

from .models import Course, Department, Section, Professor

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
    deserialize_from_luthers_list()
    return render(request, 'home/landing.html')

def deserialize_from_luthers_list():
    http = urllib3.PoolManager()

    depts_r = http.request('GET', "http://luthers-list.herokuapp.com/api/deptlist")
    depts = json.loads(depts_r.data.decode('utf-8'))
    for d in depts:
        dept = Department(subject=d['subject'])
        dept.save()
        sections_r = http.request('GET', "http://luthers-list.herokuapp.com/api/dept/%s" % dept.subject)
        sections = json.loads(sections_r.data.decode('utf-8'))
        for s in sections:
            try: 
                course = Course.objects.get(description=s['description'])
            except Course.DoesNotExist:
                course = Course(catalog_number=s['catalog_number'],
                                description=s['description'],
                                units=s['units'],
                                department=dept)
                course.save()

            try:
                professor = Professor.objects.get(prof_name=s['instructor']['name'])
            except Professor.DoesNotExist:
                professor = Professor(prof_name=s['instructor']['name'],
                                prof_email=s['instructor']['email'])
                professor.save()
            
            print("course number type: ", type(s['course_number']))
            section = Section(section_number=s['course_number'],
                        wait_list=s['wait_list'],
                        wait_cap=s['wait_cap'],
                        enrollment_total=s['enrollment_total'],
                        enrollment_available=s['enrollment_available'],
                        topic=s['topic'],
                        course=course,
                        professor=professor,
                        days=s['meetings'][0]['days'],
                        start_time=s['meetings'][0]['start_time'],
                        end_time=s['meetings'][0]['end_time'],
                        facility_description=s['meetings'][0]['facility_description'])
            section.save()




def calendar(request):
    return render(request, 'home/calendar.html')


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'home/course_detail.html'

