from registration.models import UserProfile
from django.contrib.auth.models import User
from django import forms

cities = (
	('test', 'test'),
	)

class SocialForm(forms.Form):
    phone = forms.RegexField(regex=r'^\d{10}$')
    class Meta:
        model = UserProfile
        fields = ('city','phone')
        widgets = {
            'city': forms.Select(choices=cities),
        }

class UserProfileForm(forms.ModelForm):
    phone = forms.RegexField(regex=r'^\d{10}$')
    class Meta:
        model = UserProfile
        fields = ('name', 'email_id','city','phone')
        widgets = {
            'city': forms.Select(choices=cities),
        }        