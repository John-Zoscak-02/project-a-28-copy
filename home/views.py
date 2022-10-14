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
    return render(request, 'home/landing.html')


'''
This function will construct/identify a department instance(s) from the subject parameter, query the lutherlist api 
    for the subject parameter, then construct/identify all relevant courses and thier respective sections. It 
    will then save all this into the database. 

param: subject (<string>) - the department subject to deserialize

return: nothing

Results can be seen under the Home/Courses page in the django admin portal

NOTE: if you load too many courses (~290), the database will fill up and you will have problems loading any more
    You can avoid problems by clearing the saved courses in the admin portal 
'''
def deserialize_department(subject):
    http = urllib3.PoolManager()

    try: 
        dept = Department.objects.get(subject=subject)
    except Department.DoesNotExist:
        dept = Department(subject=subject)
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




def calendar(request):
    return render(request, 'home/calendar.html')


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'home/course_detail.html'

