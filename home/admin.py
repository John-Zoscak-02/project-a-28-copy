from django.contrib import admin

from .models import Department, Course, Section, User
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

ADDITIONAL_USER_FIELDS = (
    (None, {'fields': ('username',)}),
)

class MyUserAdmin(UserAdmin):
    model = User
    add_fieldsets = UserAdmin.add_fieldsets + ADDITIONAL_USER_FIELDS
    fieldsets = UserAdmin.fieldsets + ADDITIONAL_USER_FIELDS
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

admin.site.unregister(User)
admin.site.register(Course, CourseAdmin)
admin.site.register(User, MyUserAdmin)