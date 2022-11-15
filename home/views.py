from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Department, Relationship, Section, Profile, Schedule
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from django.views import generic
import urllib3
import json
import numpy as np
from .forms import SearchForm
from django.contrib.auth.models import User
from django.db.models import Q
from home.utils import group_by_course, get_events, search_for_section, group_by_schools, get_section
from .forms import ProfileModelForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }

    return render(request, 'home/profile.html', context)

@login_required
def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitations_received(profile)
    results = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(results) == 0:
        is_empty = True

    context = {
        'qs': results,
        'is_empty': is_empty,
    }

    return render(request, 'home/friends.html', context)

@login_required
def accept_invitation(request):
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('home:friends')

@login_required
def reject_invitation(request):
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        receiver = Profile.objects.get(user=request.user)
        sender = Profile.objects.get(pk=pk)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('home:friends')

@login_required
def invite_profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)

    context = {'qs': qs}

    return render(request, 'home/to_invite_list.html', context)

@login_required
def profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)

    context = {'qs': qs}

    return render(request, 'home/profile_list.html', context)

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'home/profile.html'

    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    profile = Profile.objects.get(user=self.request.user)
    #    rel_r = Relationship.objects.filter(sender=profile)
    #    rel_s = Relationship.objects.filter(receiver=profile)
    #    rel_receiver = []
    #    rel_sender = []
    #    for item in rel_r:
    #        rel_receiver.append(item.receiver.user)
    #    for item in rel_s:
    #        rel_sender.append(item.sender.user)
    #    context["rel_receiver"] = rel_receiver
    #    context["rel_sender"] = rel_sender
    #    return context

    def post(self, request, **kwargs):
        current_user_profile = request.user.profile
        schedule = Schedule.objects.get(profile=current_user_profile)
        data = request.POST
        print(data)
        section_data = data['class_remove']
        print(section_data)
        section = Section.objects.get(section_number=section_data[7:12])
        schedule.classes.remove(section)
        schedule.save()
                
        #context = self.get_context_data(kwargs=kwargs)
        #return render(request, self.template_name, context)
        return redirect('home:profile_view')

class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'home/profile_list.html'
    # context_object_name = 'qs'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
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

@login_required
def send_invitation(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('home:profile_view')
    
@login_required
def remove_from_friends(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('home:profile_view')

def landing(request):
    schools = group_by_schools()

    return render(request, 'home/landing.html', {'schools': schools})


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
            instructor = form.cleaned_data['instructor']
            search_data = search_for_section({'department': department, 'catalog_number': course_number, 'days': days, 'instructor': instructor})

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
        try:
            schedule = Schedule.objects.get(profile=current_user_profile)
        except Schedule.DoesNotExist:
            schedule = Schedule.objects.create(profile=current_user_profile)
            schedule.save()
        data = request.POST
        section_data = json.loads(data['section_add'].replace('\'', '"'))

        section = get_section(section_data)
        scheduled_sections = schedule.classes.all()

        interval = [float(section.start_time[:2]) + float(section.start_time[3:5]) / 60,
                    float(section.end_time[:2]) + float(section.end_time[3:5]) / 60]
        days = {section.days[i:i+2] for i in range(0, len(section.days), 2)}
        
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
                
        return redirect('home:dept_detail', self.kwargs['dept'])
