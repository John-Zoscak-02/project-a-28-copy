from django import forms


class SearchForm(forms.Form):
    department = forms.CharField(label='Department Abbreviation', widget=forms.TextInput(attrs={'class': 'form-control'}))
    course_number = forms.CharField(label='Course Number', widget=forms.TextInput(attrs={'class': 'form-control'}))
    days = forms.CharField(label='Days', widget=forms.TextInput(attrs={'class': 'form-control'}))
