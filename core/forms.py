from django import forms


class RegistrationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
    phone = forms.CharField()
    is_customer = forms.CharField()
    is_admin = forms.CharField()


class VehicleForm(forms.Form):
    plate = forms.CharField()
    model = forms.CharField()
    capacity = forms.IntegerField()


