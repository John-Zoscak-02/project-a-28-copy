from django.shortcuts import render
from django.views import generic

from .models import Course

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


def calendar(request):
    return render(request, 'home/calendar.html')


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'home/course_detail.html'

