from django import forms

class InitForm(forms.Form):
    client_id = forms.CharField(label='Client ID', max_length=140)
    client_secret = forms.CharField(label='Client Secret', max_length=140)
    website_url = forms.CharField(label='Website URL', max_length=140)