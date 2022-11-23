from datetime import datetime
from multiprocessing import context
from urllib import request
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Course, Department, Relationship, Section, Schedule, Profile, Comment
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from django.views import generic
import urllib3
import json
import numpy as np
from .forms import CommentForm, SearchForm
from django.contrib.auth.models import User
from django.db.models import Q
from home.utils import group_by_course, get_events, search_for_section, group_by_schools, get_section
from .forms import ProfileModelForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

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
def add_comment(request, pk):
    profile = Profile.objects.get(id=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST,instance=profile)
        if form.is_valid():
            body = form.cleaned_data['content']
            c = Comment(profile = profile, user = request.user, content = body, date = datetime.now())
            c.save()
            return redirect(request.path_info)
        else:
            messages.info(request, 'Invalid Input!')
            return redirect(request.path_info)
    else:
        form = CommentForm()
    #all_comments = Comment.objects.filter(profile=profile).count()
    context = {
        'form' : form,
        'profile': profile,
    }
    return render(request, 'home/comments.html', context)



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
        return context

    def post(self, request, **kwargs):
        current_user_profile = request.user.profile
        schedule = get_object_or_404(Schedule, profile=current_user_profile)
        data = request.POST
        print(data)
        section_data = data['class_remove']
        print(section_data)
        section = Section.objects.get(section_number=section_data[7:12])
        schedule.classes.remove(section)
        schedule.save()
                
        context = self.get_context_data(kwargs=kwargs)
        return render(request, self.template_name, context)
        #return redirect('home:profile_view')

class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'home/profile_list.html'
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

            if 'section_add' in request.POST:
                current_user_profile = request.user.profile
                try:
                    schedule = Schedule.objects.get(profile=current_user_profile)
                except Schedule.DoesNotExist:
                    schedule = Schedule.objects.create(profile=current_user_profile)
                    schedule.save()
                
                csv_section_data = json.loads(request.POST['section_add'].replace('\'', '"'))
                print(csv_section_data)

                dept_json = get_department_json(csv_section_data['Mnemonic'])

                for section in dept_json:
                    if section['course_number'] == csv_section_data['ClassNumber']:
                        print(section)

                # section = get_section(section_data)

                # retval = add_to_schedule(section, schedule)

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

def get_section(section_data):
    subject = section_data['subject']
    try:
        department = Department.objects.get(subject=subject)
    except Department.DoesNotExist:
        department = Department.objects.create(subject=subject)
        department.save()

    catalog_number = section_data['catalog_number']
    description = section_data['description']
    units = section_data['units']
    try:
        course = Course.objects.get(department=department, catalog_number=catalog_number)
    except Course.DoesNotExist:
        course = Course.objects.create(catalog_number=catalog_number, description=description, units=units, department=department)
        course.save()

    section_number = section_data['course_number']
    wait_list = section_data['wait_list']
    wait_cap = section_data['wait_cap']
    enrollment_total = section_data['enrollment_total']
    enrollment_available = section_data['enrollment_available']
    topic = section_data['topic']
    prof_name = section_data['instructor']['name']
    prof_email = section_data['instructor']['email']
    if len(section_data['meetings']) == 0:
        meeting = {"days": "-",
                    "start_time": "",
                    "end_time": "",
                    "facility_description": "-"}
    else:
        meeting = section_data['meetings'][0]
    days = meeting['days']
    start_time = meeting['start_time']
    end_time = meeting['end_time']
    facility_description = meeting['facility_description']
    try:
        section = Section.objects.get(course=course, section_number=section_number)
    except Section.DoesNotExist:
        section = Section.objects.create(
            section_number=section_number,
            wait_list=wait_list,
            wait_cap=wait_cap,
            enrollment_total=enrollment_total,
            enrollment_available=enrollment_available,
            topic=topic,
            course=course,
            prof_name=prof_name,
            prof_email=prof_email,
            days=days,
            start_time=start_time,
            end_time=end_time,
            facility_description=facility_description,
        )
        section.save()

    return section


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
            print(schedule)
        except Schedule.DoesNotExist:
            schedule = Schedule.objects.create(profile=current_user_profile)
            schedule.save()
        data = request.POST
        section_data = json.loads(data['section_add'].replace('\'', '"'))

        section = get_section(section_data)

        interval = [float(section.start_time[:2]) + float(section.start_time[3:5]) / 60,
                    float(section.end_time[:2]) + float(section.end_time[3:5]) / 60]
        days = {section.days[i:i+2] for i in range(0, len(section.days), 2)}

        context = self.get_queryset()
        
        conflicts = False
        for other_section in schedule.classes.all():
            other_interval = [float(other_section.start_time[:2]) + float(other_section.start_time[3:5]) / 60,
                              float(other_section.end_time[:2]) + float(other_section.end_time[3:5]) / 60]
            other_days = {other_section.days[i:i+2] for i in range(0, len(other_section.days), 2)}

            if days.intersection(other_days):
                if max(0, min(interval[1], other_interval[1])) - max(interval[0], other_interval[0]) > 0:
                    conflicts = True
        
        if not conflicts:
            schedule.classes.add(section)
                
        return redirect('home:dept_detail', self.kwargs['dept'])
