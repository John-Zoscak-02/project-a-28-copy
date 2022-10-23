from django.contrib import admin

from .models import Department, Course, Section, Profile
from django.contrib.auth.models import User, Group
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class SectionInline(admin.TabularInline):
    model = Section
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    model = User
    fieldsets = [
        (None, {'fields' : ['description']}),
    ]
    inlines = [SectionInline]
    list_display = ('description', 'catalog_number', 'units', 'department')
    search_fields = ['catalog_number', 'description', 'department']
    list_per_page: 100

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = (ProfileInline, )
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.unregister(Group)
