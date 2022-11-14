from .models import Course, Department, Section, Profile
import urllib3
import json

import pandas as pd
from datetime import datetime
from datetime import timedelta
import pytz
import csv

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


mnemonic_map= { "AAS":"African-American and African Studies","ACCT":"Accounting","ADAP":"Advisor Approval - Self-Directed Major Requirement","AIRS":"Air Science","ALAR":"Architecture and Landscape Architecture","AM":"Applied Mechanics","AMST":"American Studies","ANTH":"Anthropology","APMA":"Applied Mathematics","ARAB":"Arabic","ARAD":"Arts Administration","ARAH":"History of Art and Architecture","ARCH":"Architecture","ARCY":"Archaeology","ARH":"Architectural History","ARTH":"History of Art","ARTR":"Arabic in Translation","ARTS":"Studio Art","ASL":"American Sign Language","ASTR":"Astronomy","BENG":"Bengali","BETR":"Bengali in Translation","BIMS":"Biomedical Sciences","BIOC":"Biochemistry","BIOE":"Bioethics","BIOL":"Biology","BIOM":"Biomedical Engineering","BIOP":"Biophysics","BME":"Biomedical Engineering","BUS":"Business","CASS":"College Arts Scholars Seminar","CCFA":"Common Course-Humanities","CCLT":"Common Course-Literature","CCSC":"Common Course-Sciences","CCSS":"Common Course-Social Sciences","CE":"Civil Engineering","CELL":"Cell Biology","CHE":"Chemical Engineering","CHEM":"Chemistry","CHIN":"Chinese","CHTR":"Chinese in Translation","CJ":"Criminal Justice","CLAS":"Classics","COGS":"Cognitive Science","COLA":"College Advising Seminar","COMM":"Commerce","CONC":"Business Fundamentals", "CREO":"Creole", "CPE":"Computer Engineering","CPLT":"Comparative Literature","CS":"Computer Science","CZ":"Czech","DANC":"Dance","DEM":"Democarcy","DH":"Digital Humanities", "DS":"Data Science", "DRAM":"Drama","EALC":"East Asian Languages, Literatures, and Cultures","EAST":"East Asian Studies","ECE":"Electrical and Computer Engineering","ECON":"Economics","EDHS":"Education-Human Services","EDIS":"Education-Curriculum, Instruction, & Special Ed","EDLF":"Education-Leadership, Foundations, and Policy","EDNC":"Education Non-Credit","EGMT":"Engagement", "ELA":"Occupation in Liberal Arts","ENAM":"English-American Literature to 1900","ENCR":"English-Criticism","ENCW":"English Creative Writing","ENEC":"English-Restoration and Eighteenth-Century Lit","ENGL":"English-Miscellaneous","ENGN":"English-Genre Studies","ENGR":"Engineering","ENLS":"English-Language Study","ENLT":"English-Introductory Seminar in Literature","ENMC":"English-Modern & Contemporary Literature","ENMD":"English-Medieval Literature","ENNC":"English-Nineteenth-Century British Literature","ENPG":"English-Pedagogy","ENPW":"English-Poetry Writing","ENRN":"English-Renaissance Literature","ENSP":"English-Special Topics in Literature","ENTP":"Entrepenuership", "ENWR":"English-Academic, Professional, & Creative Writing","EP":"Engineering Physics","ESL":"English as a Second Language","ETP":"Enviromental Thought and Practice","EVAT":"Environmental Sciences-Atmospheric Sciences","EVEC":"Environmental Sciences-Ecology","EVGE":"Environmental Sciences-Geosciences","EVHY":"Environmental Sciences-Hydrology","EURS":"European Studies", "EVSC":"Environmental Sciences","FREN":"French","FRLN":"Foreign Language Exempt Modified","FRTR":"French in Translation","GBAC":"Enterprise Analytics", "GBUS":"Graduate Business", "GCCS":"Global Commerce", "GCNL":"Clinical Nurse Leader","GCOM":"Graduate Commerce","GDS":"Global Development Studies","GERM":"German","GETR":"German in Translation","GHSS":"Graduage Humanities and Social Studies", "GNUR":"Graduate Nursing","GREE":"Greek","GSAS":"Graduate Arts & Sciences","GSCI":"Graduate Sciences", "GSGS":"Global Studies", "GSMS":"Global Studies-Middle East and South Asia", "GSSJ":"Global Studies-Securities and Justice", "GSVS":"Global Studies-Enviroments and Sustainability", "HBIO":"Human Biology","HEBR":"Hebrew","HETR":"Hebrew in Translation","HHE":"", "HIAF":"History-African History","HIEA":"History-East Asian History","HIEU":"History-European History","HILA":"History-Latin American History","HIME":"History-Middle Eastern History","HIND":"Hindi","HISA":"History-South Asian History","HIST":"History-General History","HIUS":"History-United States History","HR":"Human Resources","HSCI":"College Science Scholars Seminar","HUMS":"Humanistic Studies","IHGC":"Humanities and Global Cultures","IMP":"Interdisciplinary Thesis","INST":"Interdisciplinary Studies","IS":"Interdisciplinary Studies","ISAS":"Interdisciplinary Studies-Analytical Skills","ISBU":"Interdisciplinary Studies-Business","ISCI":"Interdisciplinary Studies-Critical Issues","ISCP":"Interdisciplinary Studies-Capstone Project","ISCS":"Interdisciplinary Studies-Capstone Project","ISED":"Interdisciplinary Studies-Invidualized Education","ISGE":"Interdisiplinary Studies-General Elective","ISHU":"Interdisiplinary Studies-Humanities","ISIN":"Interdisciplinary Studies-Individualized Other","ISIR":"Interdisciplinary Studies-Independent Research","ISIT":"Interdisciplinary Studies-Information Technology","ISLS":"Interdisciplinary Studies-Liberal Studies Seminar","ISPS":"Interdisciplinary Studies-Proseminar","ISSS":"Interdisciplinary Studies-Social Sciences","IT":"Informational Technology","ITAL":"Italian","ITTR":"Italian in Translation","JAPN":"Japanese","JPTR":"Japanese in Translation","JWST":"Jewish Studies","KICH":"Maya Kich", "KINE":"Kinesiology","KLPA":"Lifetime Physical Activity", "KOR":"Korean","KRTR":"Korean in Translation","LAR":"Landscape Architecture","LASE":"Liberal Arts Seminar","LAST":"Latin American Studies","LATI":"Latin","LAW":"Law","LING":"Linguistics","LNGS":"General Linguistics","LPPA":"Leadership and Public Policy-Evaluation and Analysis", "LPPL":"Leadership and Public Policy-Leadership", "LPPP":"Leadership and Public Policy-Policy", "LPPS":"Leadership and Public Policy-Substantive", "MAE":"Mechanical & Aerospace Engineering","MATH":"Mathematics","MDST":"Media Studies","MED":"Medicine","MESA":"Middle Eastern & South Asian Languages & Cultures","MEST":"Middle Eastern Studies","MICR":"Microbiology","MISC":"Military Science","MSE":"Materials Science and Engineering","MSP":"Medieval Studies","MUBD":"Music-Marching Band","MUEN":"Music-Ensembles","MUPF":"Music-Private Performance Instruction","MUSI":"Music","NASC":"Naval Science","NCAM":"Non-Credit Association Management","NCAR":"Non-Credit Architecture & Environment Design","NCBM":"Non-Credit Business and Management","NCBS":"Non-Credit Biological Sciences","HCCJ":"NC-Criminal Justice","NCCS":"Non-Credit Computer and Information Sciences","NCED":"Non-Credit Education","NCEL":"Non-Credit English Literature","NCEN":"Non-Credit Engineering","NCFA":"Non-Credit Fine and Applied Arts","NCFL":"Non-Credit Foreign Language","NCFP":"Non-Credit Financial Planning","NCHP":"Non-Credit Health Professions","HCIC":"NC-Intellegence Community","NCIS":"Non-Credit Interdisciplinary Studies","NCLA":"Non-Credit Law","NCLE":"Non-Credit Letters","NCLS":"Non-Credit Library Sciences","NCPD":"Non-Credit Personal Development","NCPH":"Non-Credit Physical Sciences","NCPR":"Non-Credit Professional Review","NCPS":"Non-Credit Psychology","NCSS":"Non-Credit Social Sciences","NCTH":"Non-Credit Theology","NESC":"Neuroscience","NRES":"Undergraduate Non-Resident","NRGA":"Graduate Non-Resident","NUCO":"Nursing Core","NUIP":"Nursing Interprofessional","NURS":"Nursing","NW":"Non-Western Perspectives","PASH":"Pashto","PATH":"Pathology","PAVS":"Pavilion Seminars","PC":"Procurement and Contracts Management","PERS":"Persian","PETR":"Persian in Translation","PHAR":"Pharmacology","PHIL":"Philosophy","PHS":"Public Health Sciences","PHSE":"Public Health Sciences Ethics","PHY":"Physiology","PHYE":"Physical Education","PHYS":"Physics","PLAC":"Planning Application","PLAD":"Politics-Departmental Seminar","PLAN":"Urban and Environmental Planning","PLAP":"Politics-American Politics","PLCP":"Politics-Comparative Politics","PLIR":"Politics-International Relations","PLPT":"Politics-Political Theory","PLSK":"Personal Skills","POL":"Polish","PORT":"Portuguese","POTR":"Portuguese in Translation","PPL":"Political Philosophy, Policy, and Law","PPOL":"Public Policy","PSCJ":"Professional Studies-Criminal Justice","PSED":"Professional Studies-Education","PSEW":"Professional Studies-Education Web-Based","PSHM":"PS-Health Sciences Management","PSHP":"Professional Studies-Health Policy","PSHS":"PS-Health Science","PSLP":"Professional Studies-Leadership","PSLS":"Professional Studies-Leadership Skills","PSMT":"Professional Studies-MT","PSPA":"Professional Studies-Public Administration", "PSPS":"Professional Studies-Public Science", "PSPL":"Professional Studies-Political Leadership","PSPM":"Professional Studies-Project Management","PSSP":"Professional Studies-Spanish","PSSS":"Professional Studies-Social Sciences","PSTS":"Professional Studies-Technology and Society","PST":"Political and Social Thought","PSWD":"Professional Studies-Workforce Development","PSYC":"Psychology","RELA":"Religion-African Religions","RELB":"Religion-Buddhism","RELC":"Religion-Christianity","RELG":"Religion-General Religion","RELH":"Religion-Hinduism","RELI":"Religion-Islam","RELJ":"Religion-Judaism","RELS":"Religion-Special Topic","RUSS":"Russian","RUTR":"Russian in Translation","SANS":"Sanskrit","SARC":"Architecture School","SAST":"South Asian Studies","SATR":"South Asian Literature in Translation","SEC":"Security", "SEMS":"Semester at Sea","SLAV":"Slavic","SLFK":"Slavic Folklore & Oral Literature","SLTR":"Slavic in Translation","SOC":"Sociology","SOSC":"Social Science Elective","SPAN":"Spanish","SPTR":"Spanish in Translation","SRBC":"Serbo-Croatian","STAT":"Statistics","STS":"Science, Technology, and Society","SURG":"Surgery","SWAG":"Studies in Women and Gender","SWAH":"Swahili","SWR":"Second Writing Requirement","SYS":"Systems & Information Engineering","TBTN":"Tibetan","TMP":"Technology, Management, and Policy","TURK":"Turkish","UD":"Urban Design", "UKR":"Ukrainian","UNST":"University Studies","URDU":"Urdu","USEM":"University Seminar","WGS":"Women and Gender Studies","YIDD":"Yiddish","YITR":"Yiddish in Translation","ZFOR":"Study Abroad"}
def group_by_schools():
    schools_dict = {}
    try:
        schools = pd.read_csv("static/schools.csv") 
    except (FileNotFoundError, FileExistsError):
        return None

    #print(schools.columns.values)
    for school in schools.columns.values:
        schools_dict[school] = list()
        for mnemonic in schools[school]:
            name = mnemonic_map.get(mnemonic, None)
            if (name):
                schools_dict[school].append({'mnemonic':mnemonic, 'name':mnemonic_map[mnemonic]})
    #for school, subjects in schools_dict:
    #    print(school)
    #    for subject in subjects:
    #        print("    ", subject.mnemonic, subject.name)
    print(schools_dict)
    return schools_dict
    


def search_for_section(search_criteria):
    try:
        csvfile = open('static/searchData.csv')
    except (FileNotFoundError, FileExistsError):
        return None
    valid_search_criteria = ['department', 'catalog_number', 'instructor', 'days', 'description']
    if not all(crit in valid_search_criteria for crit in search_criteria):
        return None
    sections = []
    reader = csv.DictReader(csvfile)
    criteria_to_column = {'department': 'Mnemonic',
                          'catalog_number': 'Number',
                          'instructor': 'Instructor',
                          'days': 'Days',
                          'description': 'Title',}
    for row in reader:
        valid = True
        for crit in search_criteria:
            if not search_criteria[crit].lower() in row[criteria_to_column[crit]].lower():
                valid = False
        if valid:
            sections.append(row)

    return sections
