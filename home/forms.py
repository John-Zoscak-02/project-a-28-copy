from django import forms


class SearchForm(forms.Form):
    class_name = forms.CharField(label='Class Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
