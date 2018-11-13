from django import forms


class Test(forms.Form):
    your_name = forms.CharField(label='Your Name', max_length=100)
    your_soname = forms.TextInput
