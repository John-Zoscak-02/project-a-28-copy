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
    return render(request, 'home/landing.html')