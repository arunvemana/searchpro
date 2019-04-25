from django import forms


class SearchForm(forms.Form):
    Search_String = forms.CharField()

