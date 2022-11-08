from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Department, Relationship, Section, Profile, Schedule
from django.views.generic.edit import CreateView
from django.views import generic
import urllib3
import json
import numpy as np
from .forms import SearchForm
from django.contrib.auth.models import User
from django.db.models import Q
from home.utils import group_by_course, get_events, search_for_section

#from google.oauth2 import service_account
#import googleapiclient.discovery

#CAL_ID = 'c_8dc9a28038e69f7797ebdada5d7a0742a88425879517b38502e62af3ae0976a9@group.calendar.google.com'
#SCOPES = ['https://www.googleapis.com/auth/calendar']
#SERVICE_ACCOUNT_FILE = './google-credentials.json'

#credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
#service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

mnemonic_map= { "AAS":"African-American and African Studies","ACCT":"Accounting","ADAP":"Advisor Approval - Self-Directed Major Requirement","AIRS":"Air Science","ALAR":"Architecture and Landscape Architecture","AM":"Applied Mechanics","AMST":"American Studies","ANTH":"Anthropology","APMA":"Applied Mathematics","ARAB":"Arabic","ARAD":"Arts Administration","ARAH":"History of Art and Architecture","ARCH":"Architecture","ARCY":"Archaeology","ARH":"Architectural History","ARTH":"History of Art","ARTR":"Arabic in Translation","ARTS":"Studio Art","ASL":"American Sign Language","ASTR":"Astronomy","BENG":"Bengali","BETR":"Bengali in Translation","BIMS":"Biomedical Sciences","BIOC":"Biochemistry","BIOE":"Bioethics","BIOL":"Biology","BIOM":"Biomedical Engineering","BIOP":"Biophysics","BME":"Biomedical Engineering","BUS":"Business","CASS":"College Arts Scholars Seminar","CCFA":"Common Course-Humanities","CCLT":"Common Course-Literature","CCSC":"Common Course-Sciences","CCSS":"Common Course-Social Sciences","CE":"Civil Engineering","CELL":"Cell Biology","CHE":"Chemical Engineering","CHEM":"Chemistry","CHIN":"Chinese","CHTR":"Chinese in Translation","CJ":"Criminal Justice","CLAS":"Classics","COGS":"Cognitive Science","COLA":"College Advising Seminar","COMM":"Commerce","CONC":"Business Fundamentals", "CREO":"Creole", "CPE":"Computer Engineering","CPLT":"Comparative Literature","CS":"Computer Science","CZ":"Czech","DANC":"Dance","DEM":"Democarcy","DH":"Digital Humanities", "DS":"Data Science", "DRAM":"Drama","EALC":"East Asian Languages, Literatures, and Cultures","EAST":"East Asian Studies","ECE":"Electrical and Computer Engineering","ECON":"Economics","EDHS":"Education-Human Services","EDIS":"Education-Curriculum, Instruction, & Special Ed","EDLF":"Education-Leadership, Foundations, and Policy","EDNC":"Education Non-Credit","EGMT":"Engagement", "ELA":"Occupation in Liberal Arts","ENAM":"English-American Literature to 1900","ENCR":"English-Criticism","ENCW":"English Creative Writing","ENEC":"English-Restoration and Eighteenth-Century Lit","ENGL":"English-Miscellaneous","ENGN":"English-Genre Studies","ENGR":"Engineering","ENLS":"English-Language Study","ENLT":"English-Introductory Seminar in Literature","ENMC":"English-Modern & Contemporary Literature","ENMD":"English-Medieval Literature","ENNC":"English-Nineteenth-Century British Literature","ENPG":"English-Pedagogy","ENPW":"English-Poetry Writing","ENRN":"English-Renaissance Literature","ENSP":"English-Special Topics in Literature","ENTP":"Entrepenuership", "ENWR":"English-Academic, Professional, & Creative Writing","EP":"Engineering Physics","ESL":"English as a Second Language","ETP":"Enviromental Thought and Practice","EVAT":"Environmental Sciences-Atmospheric Sciences","EVEC":"Environmental Sciences-Ecology","EVGE":"Environmental Sciences-Geosciences","EVHY":"Environmental Sciences-Hydrology","EURS":"European Studies", "EVSC":"Environmental Sciences","FREN":"French","FRLN":"Foreign Language Exempt Modified","FRTR":"French in Translation","GBAC":"Enterprise Analytics", "GBUS":"Graduate Business", "GCCS":"Global Commerce", "GCNL":"Clinical Nurse Leader","GCOM":"Graduate Commerce","GDS":"Global Development Studies","GERM":"German","GETR":"German in Translation","GHSS":"Graduage Humanities and Social Studies", "GNUR":"Graduate Nursing","GREE":"Greek","GSAS":"Graduate Arts & Sciences","GSCI":"Graduate Sciences", "GSGS":"Global Studies", "GSMS":"Global Studies-Middle East and South Asia", "GSSJ":"Global Studies-Securities and Justice", "GSVS":"Global Studies-Enviroments and Sustainability", "HBIO":"Human Biology","HEBR":"Hebrew","HETR":"Hebrew in Translation","HHE":"", "HIAF":"History-African History","HIEA":"History-East Asian History","HIEU":"History-European History","HILA":"History-Latin American History","HIME":"History-Middle Eastern History","HIND":"Hindi","HISA":"History-South Asian History","HIST":"History-General History","HIUS":"History-United States History","HR":"Human Resources","HSCI":"College Science Scholars Seminar","HUMS":"Humanistic Studies","IHGC":"Humanities and Global Cultures","IMP":"Interdisciplinary Thesis","INST":"Interdisciplinary Studies","IS":"Interdisciplinary Studies","ISAS":"Interdisciplinary Studies-Analytical Skills","ISBU":"Interdisciplinary Studies-Business","ISCI":"Interdisciplinary Studies-Critical Issues","ISCP":"Interdisciplinary Studies-Capstone Project","ISCS":"Interdisciplinary Studies-Capstone Project","ISED":"Interdisciplinary Studies-Invidualized Education","ISGE":"Interdisiplinary Studies-General Elective","ISHU":"Interdisiplinary Studies-Humanities","ISIN":"Interdisciplinary Studies-Individualized Other","ISIR":"Interdisciplinary Studies-Independent Research","ISIT":"Interdisciplinary Studies-Information Technology","ISLS":"Interdisciplinary Studies-Liberal Studies Seminar","ISPS":"Interdisciplinary Studies-Proseminar","ISSS":"Interdisciplinary Studies-Social Sciences","IT":"Informational Technology","ITAL":"Italian","ITTR":"Italian in Translation","JAPN":"Japanese","JPTR":"Japanese in Translation","JWST":"Jewish Studies","KICH":"Maya Kich", "KINE":"Kinesiology","KLPA":"Lifetime Physical Activity", "KOR":"Korean","KRTR":"Korean in Translation","LAR":"Landscape Architecture","LASE":"Liberal Arts Seminar","LAST":"Latin American Studies","LATI":"Latin","LAW":"Law","LING":"Linguistics","LNGS":"General Linguistics","LPPA":"Leadership and Public Policy-Evaluation and Analysis", "LPPL":"Leadership and Public Policy-Leadership", "LPPP":"Leadership and Public Policy-Policy", "LPPS":"Leadership and Public Policy-Substantive", "MAE":"Mechanical & Aerospace Engineering","MATH":"Mathematics","MDST":"Media Studies","MED":"Medicine","MESA":"Middle Eastern & South Asian Languages & Cultures","MEST":"Middle Eastern Studies","MICR":"Microbiology","MISC":"Military Science","MSE":"Materials Science and Engineering","MSP":"Medieval Studies","MUBD":"Music-Marching Band","MUEN":"Music-Ensembles","MUPF":"Music-Private Performance Instruction","MUSI":"Music","NASC":"Naval Science","NCAM":"Non-Credit Association Management","NCAR":"Non-Credit Architecture & Environment Design","NCBM":"Non-Credit Business and Management","NCBS":"Non-Credit Biological Sciences","HCCJ":"NC-Criminal Justice","NCCS":"Non-Credit Computer and Information Sciences","NCED":"Non-Credit Education","NCEL":"Non-Credit English Literature","NCEN":"Non-Credit Engineering","NCFA":"Non-Credit Fine and Applied Arts","NCFL":"Non-Credit Foreign Language","NCFP":"Non-Credit Financial Planning","NCHP":"Non-Credit Health Professions","HCIC":"NC-Intellegence Community","NCIS":"Non-Credit Interdisciplinary Studies","NCLA":"Non-Credit Law","NCLE":"Non-Credit Letters","NCLS":"Non-Credit Library Sciences","NCPD":"Non-Credit Personal Development","NCPH":"Non-Credit Physical Sciences","NCPR":"Non-Credit Professional Review","NCPS":"Non-Credit Psychology","NCSS":"Non-Credit Social Sciences","NCTH":"Non-Credit Theology","NESC":"Neuroscience","NRES":"Undergraduate Non-Resident","NRGA":"Graduate Non-Resident","NUCO":"Nursing Core","NUIP":"Nursing Interprofessional","NURS":"Nursing","NW":"Non-Western Perspectives","PASH":"Pashto","PATH":"Pathology","PAVS":"Pavilion Seminars","PC":"Procurement and Contracts Management","PERS":"Persian","PETR":"Persian in Translation","PHAR":"Pharmacology","PHIL":"Philosophy","PHS":"Public Health Sciences","PHSE":"Public Health Sciences Ethics","PHY":"Physiology","PHYE":"Physical Education","PHYS":"Physics","PLAC":"Planning Application","PLAD":"Politics-Departmental Seminar","PLAN":"Urban and Environmental Planning","PLAP":"Politics-American Politics","PLCP":"Politics-Comparative Politics","PLIR":"Politics-International Relations","PLPT":"Politics-Political Theory","PLSK":"Personal Skills","POL":"Polish","PORT":"Portuguese","POTR":"Portuguese in Translation","PPL":"Political Philosophy, Policy, and Law","PPOL":"Public Policy","PSCJ":"Professional Studies-Criminal Justice","PSED":"Professional Studies-Education","PSEW":"Professional Studies-Education Web-Based","PSHM":"PS-Health Sciences Management","PSHP":"Professional Studies-Health Policy","PSHS":"PS-Health Science","PSLP":"Professional Studies-Leadership","PSLS":"Professional Studies-Leadership Skills","PSMT":"Professional Studies-MT","PSPA":"Professional Studies-Public Administration", "PSPS":"Professional Studies-Public Science", "PSPL":"Professional Studies-Political Leadership","PSPM":"Professional Studies-Project Management","PSSP":"Professional Studies-Spanish","PSSS":"Professional Studies-Social Sciences","PSTS":"Professional Studies-Technology and Society","PST":"Political and Social Thought","PSWD":"Professional Studies-Workforce Development","PSYC":"Psychology","RELA":"Religion-African Religions","RELB":"Religion-Buddhism","RELC":"Religion-Christianity","RELG":"Religion-General Religion","RELH":"Religion-Hinduism","RELI":"Religion-Islam","RELJ":"Religion-Judaism","RELS":"Religion-Special Topic","RUSS":"Russian","RUTR":"Russian in Translation","SANS":"Sanskrit","SARC":"Architecture School","SAST":"South Asian Studies","SATR":"South Asian Literature in Translation","SEC":"Security", "SEMS":"Semester at Sea","SLAV":"Slavic","SLFK":"Slavic Folklore & Oral Literature","SLTR":"Slavic in Translation","SOC":"Sociology","SOSC":"Social Science Elective","SPAN":"Spanish","SPTR":"Spanish in Translation","SRBC":"Serbo-Croatian","STAT":"Statistics","STS":"Science, Technology, and Society","SURG":"Surgery","SWAG":"Studies in Women and Gender","SWAH":"Swahili","SWR":"Second Writing Requirement","SYS":"Systems & Information Engineering","TBTN":"Tibetan","TMP":"Technology, Management, and Policy","TURK":"Turkish","UD":"Urban Design", "UKR":"Ukrainian","UNST":"University Studies","URDU":"Urdu","USEM":"University Seminar","WGS":"Women and Gender Studies","YIDD":"Yiddish","YITR":"Yiddish in Translation","ZFOR":"Study Abroad"}

def profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)
    context = {'qs' : qs}
    return render(request, 'home/profile_list.html', context)

class ProfileListView(generic.ListView):
    model = Profile
    template_name = 'home/profile_list.html'
    # context_object_name = 'qs'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)

        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True
        return context

def invite_profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)
    context = {'qs' : qs}
    return render(request, 'home/to_invite_list.html', context)

def my_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    context = {'profile': profile, 'friends': profiles_list_view}

    # Create Events
    #events = get_events(Profile.objects.get(pk=pk).schedule.classes.all())
    #for event in events:
    #    service.events().insert(calendarId=CAL_ID, body=event).execute()
    #render = render(request, 'home/profile.html')
    #for event in events:
        #service.events().
    #return render

    return render(request, 'home/profile.html', context)

def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitations_received(profile)
    results = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(results) == 0:
        is_empty = True
    context = {'qs' : results,
    'is_empty': is_empty,
    }
    return render(request, 'home/friends.html', context)

def send_invitation(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('home:my_profile_view')

def remove_from_friends(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get((Q(sender=sender) & Q(receiver=receiver)) | Q(sender=receiver) & Q(receiver=sender))
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('home:my_profile_view')

def accept_invitation(request):
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status == 'accepted'
            rel.save()
    return redirect('home:friends')

def reject_invitation(request):
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        receiver = Profile.objects.get(user=request.user)
        sender = Profile.objects.get(pk=pk)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('home:friends')



def landing(request):
    # Department list:

    deptList = [{"subject":"ACCT"},{"subject":"AIRS"},{"subject":"ALAR"},{"subject":"AM"},{"subject":"AMST"},{"subject":"ANTH"},{"subject":"APMA"},{"subject":"ARAB"},{"subject":"ARAD"},{"subject":"ARAH"},{"subject":"ARCH"},{"subject":"ARCY"},{"subject":"ARH"},{"subject":"ARTH"},{"subject":"ARTR"},{"subject":"ARTS"},{"subject":"ASL"},{"subject":"ASTR"},{"subject":"BIMS"},{"subject":"BIOC"},{"subject":"BIOL"},{"subject":"BIOP"},{"subject":"BME"},{"subject":"BUS"},{"subject":"CASS"},{"subject":"CE"},{"subject":"CELL"},{"subject":"CHE"},{"subject":"CHEM"},{"subject":"CHIN"},{"subject":"CHTR"},{"subject":"CLAS"},{"subject":"COGS"},{"subject":"COLA"},{"subject":"COMM"},{"subject":"CONC"},{"subject":"CPE"},{"subject":"CREO"},{"subject":"CS"},{"subject":"DANC"},{"subject":"DEM"},{"subject":"DH"},{"subject":"DRAM"},{"subject":"DS"},{"subject":"EALC"},{"subject":"EAST"},{"subject":"ECE"},{"subject":"ECON"},{"subject":"EDHS"},{"subject":"EDIS"},{"subject":"EDLF"},{"subject":"EDNC"},{"subject":"EGMT"},{"subject":"ELA"},{"subject":"ENCW"},{"subject":"ENGL"},{"subject":"ENGR"},{"subject":"ENTP"},{"subject":"ENWR"},{"subject":"ESL"},{"subject":"ETP"},{"subject":"EURS"},{"subject":"EVAT"},{"subject":"EVEC"},{"subject":"EVGE"},{"subject":"EVHY"},{"subject":"EVSC"},{"subject":"FREN"},{"subject":"GBAC"},{"subject":"GBUS"},{"subject":"GCCS"},{"subject":"GCNL"},{"subject":"GCOM"},{"subject":"GDS"},{"subject":"GERM"},{"subject":"GETR"},{"subject":"GHSS"},{"subject":"GNUR"},{"subject":"GREE"},{"subject":"GSAS"},{"subject":"GSCI"},{"subject":"GSGS"},{"subject":"GSMS"},{"subject":"GSSJ"},{"subject":"GSVS"},{"subject":"HBIO"},{"subject":"HEBR"},{"subject":"HHE"},{"subject":"HIAF"},{"subject":"HIEA"},{"subject":"HIEU"},{"subject":"HILA"},{"subject":"HIME"},{"subject":"HIND"},{"subject":"HISA"},{"subject":"HIST"},{"subject":"HIUS"},{"subject":"HR"},{"subject":"HSCI"},{"subject":"IMP"},{"subject":"INST"},{"subject":"ISBU"},{"subject":"ISHU"},{"subject":"ISIN"},{"subject":"ISLS"},{"subject":"ISSS"},{"subject":"IT"},{"subject":"ITAL"},{"subject":"ITTR"},{"subject":"JAPN"},{"subject":"JPTR"},{"subject":"KICH"},{"subject":"KINE"},{"subject":"KLPA"},{"subject":"KOR"},{"subject":"LAR"},{"subject":"LASE"},{"subject":"LAST"},{"subject":"LATI"},{"subject":"LAW"},{"subject":"LING"},{"subject":"LNGS"},{"subject":"LPPA"},{"subject":"LPPL"},{"subject":"LPPP"},{"subject":"LPPS"},{"subject":"MAE"},{"subject":"MATH"},{"subject":"MDST"},{"subject":"MED"},{"subject":"MESA"},{"subject":"MICR"},{"subject":"MISC"},{"subject":"MSE"},{"subject":"MSP"},{"subject":"MUBD"},{"subject":"MUEN"},{"subject":"MUPF"},{"subject":"MUSI"},{"subject":"NASC"},{"subject":"NCPR"},{"subject":"NESC"},{"subject":"NUCO"},{"subject":"NUIP"},{"subject":"NURS"},{"subject":"PATH"},{"subject":"PC"},{"subject":"PERS"},{"subject":"PETR"},{"subject":"PHAR"},{"subject":"PHIL"},{"subject":"PHS"},{"subject":"PHY"},{"subject":"PHYS"},{"subject":"PLAC"},{"subject":"PLAD"},{"subject":"PLAN"},{"subject":"PLAP"},{"subject":"PLCP"},{"subject":"PLIR"},{"subject":"PLPT"},{"subject":"POL"},{"subject":"PORT"},{"subject":"POTR"},{"subject":"PPL"},{"subject":"PSHM"},{"subject":"PSLP"},{"subject":"PSPA"},{"subject":"PSPM"},{"subject":"PSPS"},{"subject":"PST"},{"subject":"PSYC"},{"subject":"RELA"},{"subject":"RELB"},{"subject":"RELC"},{"subject":"RELG"},{"subject":"RELH"},{"subject":"RELI"},{"subject":"RELJ"},{"subject":"RELS"},{"subject":"RUSS"},{"subject":"RUTR"},{"subject":"SANS"},{"subject":"SARC"},{"subject":"SAST"},{"subject":"SATR"},{"subject":"SEC"},{"subject":"SLAV"},{"subject":"SLTR"},{"subject":"SOC"},{"subject":"SPAN"},{"subject":"STAT"},{"subject":"STS"},{"subject":"SWAH"},{"subject":"SYS"},{"subject":"TURK"},{"subject":"UD"},{"subject":"UNST"},{"subject":"URDU"},{"subject":"USEM"},{"subject":"WGS"}]
    deptList = [{"subject": dept["subject"], "name":mnemonic_map[dept["subject"]]} for dept in deptList]

    return render(request, 'home/landing.html', {'deptList': deptList})


def search_page(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            department = form.cleaned_data['department']
            course_number = form.cleaned_data['course_number']
            days = form.cleaned_data['days']
            search_data = search_for_section({'department': department, 'catalog_number': course_number, 'days': days})

            return render(request, 'home/search.html', {'form': form, 'search_data': search_data})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchForm()

    return render(request, 'home/search.html', {'form': form, 'search_data': None})


def friends(request):
    return render(request, 'home/friends.html')

def about_us(request):
    return render(request, 'home/about-us.html')

class CourseDetailView(generic.ListView):
    model = Course
    template_name = 'home/course_detail.html'

    @staticmethod
    def get_queryset(request):
        return render(request, 'home/course_detail.html')

class DeptDetailView(generic.ListView):
    model = Course
    template_name = 'home/department_list.html'

    def get_queryset(self):
        # courses, professors, sections = deserialize_department(self.kwargs['dept'])
        courses_json = group_by_course(self.kwargs['dept'])
        return {'courses_json': courses_json, 'dept': self.kwargs['dept']}

    def post(self, request, **kwargs):
        current_user_profile = request.user.profile
        schedule = Schedule.objects.get(profile=current_user_profile)
        data = request.POST
        section_number = int(data.get('section_add'))
        section = Section.objects.get(section_number=section_number)
        scheduled_sections = schedule.classes.all()

        interval = [float(section.start_time[:2]) + float(section.start_time[3:5]) / 60,
                    float(section.end_time[:2]) + float(section.end_time[3:5]) / 60]
        days = {section.days[i:i+2] for i in range(0, len(section.days), 2)}

        context = self.get_queryset()
        
        conflicts = False
        for other_section in scheduled_sections:
            other_interval = [float(other_section.start_time[:2]) + float(other_section.start_time[3:5]) / 60,
                              float(other_section.end_time[:2]) + float(other_section.end_time[3:5]) / 60]
            other_days = {other_section.days[i:i+2] for i in range(0, len(other_section.days), 2)}

            if days.intersection(other_days):
                if max(0, min(interval[1], other_interval[1])) - max(interval[0], other_interval[0]) > 0:
                    conflicts = True
        
        if not conflicts:
            schedule.classes.add(section)
                
        return render(request, self.template_name, context)
