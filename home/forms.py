from django import forms
from .models import Profile
class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('major', )

DAY_CHOICES = [
    ('', 'Any Day'),
    ('MoWeFr', 'Monday, Wednesday, Friday'),
    ('TuTh', 'Tuesday, Thursday'),
    ('MoWe', 'Monday, Wednesday'),
    ('Mo', 'Monday'),
    ('Tu', 'Tuesday'),
    ('We', 'Wednesday'),
    ('Th', 'Thursday'),
    ('Fr', 'Friday')
]
class SearchForm(forms.Form):
    department = forms.CharField(label='Department Abbreviation', widget=forms.TextInput(attrs={'class': 'form-control'}))
    course_number = forms.CharField(label='Course Number', widget=forms.TextInput(attrs={'class': 'form-control'}))
    instructor = forms.CharField(label='Instructor (not required)',required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    days = forms.CharField(label='Days', initial='', required=False, widget=forms.Select(choices=DAY_CHOICES, attrs={'class': 'form-control'}))
