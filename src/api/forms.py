from django import forms

class NameForm(forms.Form):
    url = forms.CharField(label='Your hackathon URL', max_length=100,widget=forms.TextInput(attrs={'placeholder': 'Search'}))
    email = forms.CharField(label='Your EMAIL', max_length=100,widget=forms.TextInput(attrs={'placeholder': 'Email'}))