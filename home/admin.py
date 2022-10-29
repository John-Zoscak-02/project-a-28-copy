from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile, Course, Section, Schedule

class SectionInline(admin.TabularInline):
    model = Section
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields' : ['description']}),
    ]
    inlines = [SectionInline]
    list_display = ('description', 'catalog_number', 'units', 'department')
    search_fields = ['catalog_number', 'description', 'department']
    list_per_page: 100

class FriendsInline(admin.TabularInline):
    model=Profile

class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 1

class ProfileInline(admin.StackedInline):
    model = Profile
    inlines = (FriendsInline, ScheduleInline)
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_friends', 'get_schedule')
    list_select_related = ('profile', )

    def get_friends(self, instance):
        return instance.profile.friends
    get_friends.short_description = 'Friends'

    def get_schedule(self, instance):
        return instance.profile.schedule
    get_schedule.short_description = 'Schedule'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)



admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Course, CourseAdmin)