from django.shortcuts import render

from .models import Course, Department, Section, Professor
from django.views.generic.edit import CreateView
from django.views import generic
import urllib3
import json
import numpy as np

# Create your views here.

def landing(request):
    # Department list:
    deptList = [{"subject":"ACCT"},{"subject":"AIRS"},{"subject":"ALAR"},{"subject":"AM"},{"subject":"AMST"},{"subject":"ANTH"},{"subject":"APMA"},{"subject":"ARAB"},{"subject":"ARAD"},{"subject":"ARAH"},{"subject":"ARCH"},{"subject":"ARCY"},{"subject":"ARH"},{"subject":"ARTH"},{"subject":"ARTR"},{"subject":"ARTS"},{"subject":"ASL"},{"subject":"ASTR"},{"subject":"BIMS"},{"subject":"BIOC"},{"subject":"BIOL"},{"subject":"BIOP"},{"subject":"BME"},{"subject":"BUS"},{"subject":"CASS"},{"subject":"CE"},{"subject":"CELL"},{"subject":"CHE"},{"subject":"CHEM"},{"subject":"CHIN"},{"subject":"CHTR"},{"subject":"CLAS"},{"subject":"COGS"},{"subject":"COLA"},{"subject":"COMM"},{"subject":"CONC"},{"subject":"CPE"},{"subject":"CREO"},{"subject":"CS"},{"subject":"DANC"},{"subject":"DEM"},{"subject":"DH"},{"subject":"DRAM"},{"subject":"DS"},{"subject":"EALC"},{"subject":"EAST"},{"subject":"ECE"},{"subject":"ECON"},{"subject":"EDHS"},{"subject":"EDIS"},{"subject":"EDLF"},{"subject":"EDNC"},{"subject":"EGMT"},{"subject":"ELA"},{"subject":"ENCW"},{"subject":"ENGL"},{"subject":"ENGR"},{"subject":"ENTP"},{"subject":"ENWR"},{"subject":"ESL"},{"subject":"ETP"},{"subject":"EURS"},{"subject":"EVAT"},{"subject":"EVEC"},{"subject":"EVGE"},{"subject":"EVHY"},{"subject":"EVSC"},{"subject":"FREN"},{"subject":"GBAC"},{"subject":"GBUS"},{"subject":"GCCS"},{"subject":"GCNL"},{"subject":"GCOM"},{"subject":"GDS"},{"subject":"GERM"},{"subject":"GETR"},{"subject":"GHSS"},{"subject":"GNUR"},{"subject":"GREE"},{"subject":"GSAS"},{"subject":"GSCI"},{"subject":"GSGS"},{"subject":"GSMS"},{"subject":"GSSJ"},{"subject":"GSVS"},{"subject":"HBIO"},{"subject":"HEBR"},{"subject":"HHE"},{"subject":"HIAF"},{"subject":"HIEA"},{"subject":"HIEU"},{"subject":"HILA"},{"subject":"HIME"},{"subject":"HIND"},{"subject":"HISA"},{"subject":"HIST"},{"subject":"HIUS"},{"subject":"HR"},{"subject":"HSCI"},{"subject":"IMP"},{"subject":"INST"},{"subject":"ISBU"},{"subject":"ISHU"},{"subject":"ISIN"},{"subject":"ISLS"},{"subject":"ISSS"},{"subject":"IT"},{"subject":"ITAL"},{"subject":"ITTR"},{"subject":"JAPN"},{"subject":"JPTR"},{"subject":"KICH"},{"subject":"KINE"},{"subject":"KLPA"},{"subject":"KOR"},{"subject":"LAR"},{"subject":"LASE"},{"subject":"LAST"},{"subject":"LATI"},{"subject":"LAW"},{"subject":"LING"},{"subject":"LNGS"},{"subject":"LPPA"},{"subject":"LPPL"},{"subject":"LPPP"},{"subject":"LPPS"},{"subject":"MAE"},{"subject":"MATH"},{"subject":"MDST"},{"subject":"MED"},{"subject":"MESA"},{"subject":"MICR"},{"subject":"MISC"},{"subject":"MSE"},{"subject":"MSP"},{"subject":"MUBD"},{"subject":"MUEN"},{"subject":"MUPF"},{"subject":"MUSI"},{"subject":"NASC"},{"subject":"NCPR"},{"subject":"NESC"},{"subject":"NUCO"},{"subject":"NUIP"},{"subject":"NURS"},{"subject":"PATH"},{"subject":"PC"},{"subject":"PERS"},{"subject":"PETR"},{"subject":"PHAR"},{"subject":"PHIL"},{"subject":"PHS"},{"subject":"PHY"},{"subject":"PHYS"},{"subject":"PLAC"},{"subject":"PLAD"},{"subject":"PLAN"},{"subject":"PLAP"},{"subject":"PLCP"},{"subject":"PLIR"},{"subject":"PLPT"},{"subject":"POL"},{"subject":"PORT"},{"subject":"POTR"},{"subject":"PPL"},{"subject":"PSHM"},{"subject":"PSLP"},{"subject":"PSPA"},{"subject":"PSPM"},{"subject":"PSPS"},{"subject":"PST"},{"subject":"PSYC"},{"subject":"RELA"},{"subject":"RELB"},{"subject":"RELC"},{"subject":"RELG"},{"subject":"RELH"},{"subject":"RELI"},{"subject":"RELJ"},{"subject":"RELS"},{"subject":"RUSS"},{"subject":"RUTR"},{"subject":"SANS"},{"subject":"SARC"},{"subject":"SAST"},{"subject":"SATR"},{"subject":"SEC"},{"subject":"SLAV"},{"subject":"SLTR"},{"subject":"SOC"},{"subject":"SPAN"},{"subject":"STAT"},{"subject":"STS"},{"subject":"SWAH"},{"subject":"SYS"},{"subject":"TURK"},{"subject":"UD"},{"subject":"UNST"},{"subject":"URDU"},{"subject":"USEM"},{"subject":"WGS"}]

    return render(request, 'home/landing.html', {'deptList': deptList})


def friends(request):
    return render(request, 'home/friends.html')


def profile(request):
    return render(request, 'home/profile.html')

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

        try:
            professor = list(filter(lambda professor: professor.prof_name == s['instructor']['name'], professors))[0]
        except:
            professor = Professor(prof_name=s['instructor']['name'],
                            prof_email=s['instructor']['email'])
            professors.append(professor)
        
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
        sections.append(section)

    return courses, professors, sections