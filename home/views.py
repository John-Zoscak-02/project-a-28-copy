from django.shortcuts import render

from .models import Course, Department, Section, Professor
from django.views.generic.edit import CreateView
from django.views import generic
import urllib3
import json
import numpy as np

# Create your views here.
#class LandingView(generic.ListView):
#    template_name = 'home/landing.html'

#    def get_queryset(self):
#        """
#        Return nothing (right now)
#        """
#        return []


def landing(request): 
    return render(request, 'home/landing.html')

class AboutUsView(generic.ListView):
    model = Professor
    template_name= 'home/about-us.html'
    def about_us(request): 
        return render(request, 'home/about-us.html')

class CalendarView(generic.ListView):
    model = Professor
    template_name= 'home/calendar.html'
    def about_us(request): 
        return render(request, 'home/calendar.html')

class CourseDetailView(generic.ListView):
    model = Course
    template_name= 'home/course_detail.html'
    def about_us(request): 
        return render(request, 'home/course_detail.html')

'''
This function will construct/identify department instances for all the mnemonics in luthers list, then 
    construct/identify all relevant courses and thier respective sections. It will then save all this 
    into the database. 

#NOTE: This function is only a proof of concept. It takes about 3 minutes to run and saves 2501 sections. 

return: nothing

Results can be seen under the Home/Courses page in the django admin portal
'''
def deserialize_from_luthers_list():
    http = urllib3.PoolManager()

    depts_r = http.request('GET', "http://luthers-list.herokuapp.com/api/deptlist/?format=json")
    depts = json.loads(depts_r.data.decode('utf-8'))

    for subject in depts:
        mnemonic = subject['subject']
        try: 
            dept = Department.objects.get(subject=mnemonic)
        except Department.DoesNotExist:
            dept = Department(subject=mnemonic)
            dept.save() # we can remove this when we are querying the api and rendering on the fly
        
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
                course.save() # we can remove this when we are querying the api and rendering on the fly

            try:
                professor = Professor.objects.get(prof_name=s['instructor']['name'])
            except Professor.DoesNotExist:
                professor = Professor(prof_name=s['instructor']['name'],
                                prof_email=s['instructor']['email'])
                professor.save() # we can remove this when we are querying the api and rendering on the fly
            
            if (len(s['meetings']) == 0):
                #raise Exception("Having a problem with meeting %d in %s %s"  % (s['course_number'], dept.subject, course.catalog_number))
                meeting = {"days": "-",
                           "start_time": "",
                           "end_time": "",
                           "facility_description": "-"}
            else:
                meeting = s['meetings'][0]
            #print("Course Number: ", s['course_number'], dept.subject, meeting)
            section = Section(section_number=s['course_number'],
                        wait_list=s['wait_list'],
                        wait_cap=s['wait_cap'],
                        enrollment_total=s['enrollment_total'],
                        enrollment_available=s['enrollment_available'],
                        topic=s['topic'],
                        course=course,
                        professor=professor,
                        days=meeting["days"],
                        start_time=meeting["start_time"],
                        end_time=meeting["end_time"],
                        facility_description=meeting["facility_description"])
            section.save() # we can remove this when we are querying the api and rendering on the fly


'''
This function will construct/identify a department instance(s) from the subject parameter, query the lutherlist api 
    for the subject parameter, then construct/identify all relevant courses and thier respective sections. It 
    will then save all this into the database.
    
We should change this function at some point to return the models that constructs/identifies. (For on the fly rendering)

param: subject (<string>) - the department subject to deserialize

return: nothing

Results can be seen under the Home/Courses page in the django admin portal
'''
def deserialize_department(subject):
    http = urllib3.PoolManager()

    courses = np.array([])
    sections = []
    
    dept = Department(subject=subject)

    sections_r = http.request('GET', "http://luthers-list.herokuapp.com/api/dept/%s" % dept.subject)
    sections = json.loads(sections_r.data.decode('utf-8'))
    for s in sections:
        try: 
            course = courses[courses['description'] == s['description'])]
        except Course.DoesNotExist:
            course = Course(catalog_number=s['catalog_number'],
                            description=s['description'],
                            units=s['units'],
                            department=dept)
            course.save() # we can remove this when we are querying the api and rendering on the fly

        try:
            professor = Professor.objects.get(prof_name=s['instructor']['name'])
        except Professor.DoesNotExist:
            professor = Professor(prof_name=s['instructor']['name'],
                            prof_email=s['instructor']['email'])
            professor.save() # we can remove this when we are querying the api and rendering on the fly
        
        if (len(s['meetings']) == 0):
            raise Exception("Having a problem with meeting %d in %s %s"  % (s['course_number'], dept.subject, course.catalog_number))
        meeting = s['meetings'][0]
        #print("Course Number: ", s['course_number'], dept.subject, meeting)
        section = Section(section_number=s['course_number'],
                    wait_list=s['wait_list'],
                    wait_cap=s['wait_cap'],
                    enrollment_total=s['enrollment_total'],
                    enrollment_available=s['enrollment_available'],
                    topic=s['topic'],
                    course=course,
                    professor=professor,
                    days=meeting["days"],
                    start_time=meeting["start_time"],
                    end_time=meeting["end_time"],
                    facility_description=meeting["facility_description"])
        section.save() # we can remove this when we are querying the api and rendering on the fly
