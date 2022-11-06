from django.contrib import admin

from .models import Department, Course, Section, Profile, Relationship
from django.contrib.auth.models import Group





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

admin.site.register(Profile)
admin.site.register(Relationship)
admin.site.register(Course, CourseAdmin)
