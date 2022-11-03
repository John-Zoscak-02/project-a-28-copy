from django import forms


class SearchForm(forms.Form):
    class_name = forms.CharField(label='Class Name', max_length=100)
