from .models import Course, Department, Section, Profile
import urllib3
import json

from datetime import datetime
from datetime import timedelta
import pytz

def get_events(value):
    events = []

    switcher = {
    "Su" : 0,
    "Mo" : 1,
    "Tu" : 2,
    "We" : 3,
    "Th" : 4,
    "Fr" : 5,
    "Sa" : 6 }

    for class_event in value:
        days_str = class_event.days
        days = [days_str[i:i+2] for i in range(0, len(days_str), 2)]

        today = datetime.now().astimezone(pytz.timezone('America/New_York')).date()
        sunday = today - timedelta(days=(today.weekday()+1)%7)
        sunday_anchor = datetime(sunday.year, sunday.month, sunday.day)
        #print("anchor: ", sunday_anchor)
        if class_event.start_time and class_event.end_time:
            for day in days:
                starttime_delta = timedelta(days=switcher.get(day, 0), hours=int(class_event.start_time[:2]), minutes=int(class_event.start_time[3:5]))
                endtime_delta = timedelta(days=switcher.get(day, 0), hours=int(class_event.end_time[:2]), minutes=int(class_event.end_time[3:5]))
                
                start = sunday_anchor + starttime_delta
                end = sunday_anchor + endtime_delta
                summary = "%s: %s" % (class_event.course.department.subject, class_event.course.catalog_number)
                description = class_event.course.description
                location = class_event.facility_description
                print(start.strftime("%Y-%m-%dT%H:%M:00.00Z"), end.strftime("%Y-%m-%dT%H:%M:00.00Z"))
            
                events.append({
                    'summary': summary,
                    'description': description,
                    'location': location, 
                    'start': {
                        'dateTime': start.strftime("%Y-%m-%dT%H:%M:00.00Z"),
                        'timeZone': 'America/New_York',
                    },
                    'end': {
                        'dateTime': end.strftime("%Y-%m-%dT%H:%M:00.00Z"),
                        'timeZone': 'America/New_York',
                    },
                })
    return events


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
            
            if len(s['meetings']) == 0:
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
                        prof_name=s['instructor']['name'],
                        prof_email=s['instructor']['email'],
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

return: list of courses, professors, and sections

Results can be seen under the Home/Courses page in the django admin portal
'''
def deserialize_department(subject):
    http = urllib3.PoolManager()

    courses = []
    professors = []
    sections = []
    
    dept = Department(subject=subject)

    sections_r = http.request('GET', "http://luthers-list.herokuapp.com/api/dept/%s" % dept.subject)
    sections_map = json.loads(sections_r.data.decode('utf-8'))
    for s in sections_map:
         
        try:
            course = list(filter(lambda course: course.description == s['description'], courses))[0]
        except: 
            course = Course(catalog_number=s['catalog_number'],
                            description=s['description'],
                            units=s['units'],
                            department=dept)
            courses.append(course)

        #try:
        #    professor = list(filter(lambda professor: professor.prof_name == s['instructor']['name'], professors))[0]
        #except:
        #    professor = Professor(prof_name=s['instructor']['name'],
        #                    prof_email=s['instructor']['email'])
        #    professors.append(professor)
        
        if len(s['meetings']) == 0:
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
                    prof_name=s['instructor']['name'],
                    prof_email=s['instructor']['email'],
                    days=meeting["days"],
                    start_time=meeting["start_time"],
                    end_time=meeting["end_time"],
                    facility_description=meeting["facility_description"])
        sections.append(section)

    return courses, professors, sections


def get_department_json(subject):
    http = urllib3.PoolManager()
    dept = Department(subject=subject)
    dept_r = http.request('GET', "http://luthers-list.herokuapp.com/api/dept/%s" % dept.subject)
    dept_json = json.loads(dept_r.data.decode('utf-8'))
    return dept_json


def group_by_course(subject):
    dept_json = get_department_json(subject)
    courses = {}
    courses_set = set()
    for section in dept_json:
        if courses_set.__contains__(section['catalog_number']):
            courses[subject+section['catalog_number'] + ' - ' + section['description']].append(section)
        else:
            courses_set.add(section['catalog_number'])
            courses[subject + section['catalog_number'] + ' - ' + section['description']] = []
            courses[subject + section['catalog_number'] + ' - ' + section['description']].append(section)
    return courses

