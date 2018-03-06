from django import forms


class contactForm(forms.Form):
    first_name = forms.CharField(required=True, max_length=100)
    last_name = forms.CharField(required=True, max_length=100)
    email = forms.EmailField(required=True, max_length=200)
    comment = forms.CharField(required=True, widget=forms.Textarea)
