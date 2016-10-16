from django import forms


class SearchMovieForm(forms.Form):
    title = forms.CharField()
