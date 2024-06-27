from django import forms

class SearchForm(forms.Form):
    keyword = forms.CharField(label='Search Keyword', max_length=100)
    first_page = forms.IntegerField(label='First Page', min_value=1)
    last_page = forms.IntegerField(label='Last Page', min_value=1)
