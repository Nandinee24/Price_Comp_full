from django import forms

class URLForm(forms.Form):
    url = forms.URLField(label='Enter URL', max_length=200, widget=forms.TextInput)
