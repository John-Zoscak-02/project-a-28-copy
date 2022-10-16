from django.shortcuts import render
from django.views import generic

# Create your views here.
#class LandingView(generic.ListView):
#    template_name = 'home/landing.html'

#    def get_queryset(self):
#        """
#        Return nothing (right now)
#        """
#        return []


def landing(request):
    # Department list:
    deptList = [{"subject":"ACCT"},{"subject":"AIRS"},{"subject":"ALAR"},{"subject":"AM"},{"subject":"AMST"},{"subject":"ANTH"},{"subject":"APMA"},{"subject":"ARAB"},{"subject":"ARAD"},{"subject":"ARAH"},{"subject":"ARCH"},{"subject":"ARCY"},{"subject":"ARH"},{"subject":"ARTH"},{"subject":"ARTR"},{"subject":"ARTS"},{"subject":"ASL"},{"subject":"ASTR"},{"subject":"BIMS"},{"subject":"BIOC"},{"subject":"BIOL"},{"subject":"BIOP"},{"subject":"BME"},{"subject":"BUS"},{"subject":"CASS"},{"subject":"CE"},{"subject":"CELL"},{"subject":"CHE"},{"subject":"CHEM"},{"subject":"CHIN"},{"subject":"CHTR"},{"subject":"CLAS"},{"subject":"COGS"},{"subject":"COLA"},{"subject":"COMM"},{"subject":"CONC"},{"subject":"CPE"},{"subject":"CREO"},{"subject":"CS"},{"subject":"DANC"},{"subject":"DEM"},{"subject":"DH"},{"subject":"DRAM"},{"subject":"DS"},{"subject":"EALC"},{"subject":"EAST"},{"subject":"ECE"},{"subject":"ECON"},{"subject":"EDHS"},{"subject":"EDIS"},{"subject":"EDLF"},{"subject":"EDNC"},{"subject":"EGMT"},{"subject":"ELA"},{"subject":"ENCW"},{"subject":"ENGL"},{"subject":"ENGR"},{"subject":"ENTP"},{"subject":"ENWR"},{"subject":"ESL"},{"subject":"ETP"},{"subject":"EURS"},{"subject":"EVAT"},{"subject":"EVEC"},{"subject":"EVGE"},{"subject":"EVHY"},{"subject":"EVSC"},{"subject":"FREN"},{"subject":"GBAC"},{"subject":"GBUS"},{"subject":"GCCS"},{"subject":"GCNL"},{"subject":"GCOM"},{"subject":"GDS"},{"subject":"GERM"},{"subject":"GETR"},{"subject":"GHSS"},{"subject":"GNUR"},{"subject":"GREE"},{"subject":"GSAS"},{"subject":"GSCI"},{"subject":"GSGS"},{"subject":"GSMS"},{"subject":"GSSJ"},{"subject":"GSVS"},{"subject":"HBIO"},{"subject":"HEBR"},{"subject":"HHE"},{"subject":"HIAF"},{"subject":"HIEA"},{"subject":"HIEU"},{"subject":"HILA"},{"subject":"HIME"},{"subject":"HIND"},{"subject":"HISA"},{"subject":"HIST"},{"subject":"HIUS"},{"subject":"HR"},{"subject":"HSCI"},{"subject":"IMP"},{"subject":"INST"},{"subject":"ISBU"},{"subject":"ISHU"},{"subject":"ISIN"},{"subject":"ISLS"},{"subject":"ISSS"},{"subject":"IT"},{"subject":"ITAL"},{"subject":"ITTR"},{"subject":"JAPN"},{"subject":"JPTR"},{"subject":"KICH"},{"subject":"KINE"},{"subject":"KLPA"},{"subject":"KOR"},{"subject":"LAR"},{"subject":"LASE"},{"subject":"LAST"},{"subject":"LATI"},{"subject":"LAW"},{"subject":"LING"},{"subject":"LNGS"},{"subject":"LPPA"},{"subject":"LPPL"},{"subject":"LPPP"},{"subject":"LPPS"},{"subject":"MAE"},{"subject":"MATH"},{"subject":"MDST"},{"subject":"MED"},{"subject":"MESA"},{"subject":"MICR"},{"subject":"MISC"},{"subject":"MSE"},{"subject":"MSP"},{"subject":"MUBD"},{"subject":"MUEN"},{"subject":"MUPF"},{"subject":"MUSI"},{"subject":"NASC"},{"subject":"NCPR"},{"subject":"NESC"},{"subject":"NUCO"},{"subject":"NUIP"},{"subject":"NURS"},{"subject":"PATH"},{"subject":"PC"},{"subject":"PERS"},{"subject":"PETR"},{"subject":"PHAR"},{"subject":"PHIL"},{"subject":"PHS"},{"subject":"PHY"},{"subject":"PHYS"},{"subject":"PLAC"},{"subject":"PLAD"},{"subject":"PLAN"},{"subject":"PLAP"},{"subject":"PLCP"},{"subject":"PLIR"},{"subject":"PLPT"},{"subject":"POL"},{"subject":"PORT"},{"subject":"POTR"},{"subject":"PPL"},{"subject":"PSHM"},{"subject":"PSLP"},{"subject":"PSPA"},{"subject":"PSPM"},{"subject":"PSPS"},{"subject":"PST"},{"subject":"PSYC"},{"subject":"RELA"},{"subject":"RELB"},{"subject":"RELC"},{"subject":"RELG"},{"subject":"RELH"},{"subject":"RELI"},{"subject":"RELJ"},{"subject":"RELS"},{"subject":"RUSS"},{"subject":"RUTR"},{"subject":"SANS"},{"subject":"SARC"},{"subject":"SAST"},{"subject":"SATR"},{"subject":"SEC"},{"subject":"SLAV"},{"subject":"SLTR"},{"subject":"SOC"},{"subject":"SPAN"},{"subject":"STAT"},{"subject":"STS"},{"subject":"SWAH"},{"subject":"SYS"},{"subject":"TURK"},{"subject":"UD"},{"subject":"UNST"},{"subject":"URDU"},{"subject":"USEM"},{"subject":"WGS"}]

    return render(request, 'home/landing.html', {'deptList': deptList})


def friends(request):
    return render(request, 'home/friends.html')


def profile(request):
    return render(request, 'home/profile.html')
