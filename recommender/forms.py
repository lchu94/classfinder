import json
from django import forms
from django.contrib.auth.models import User
from recommender.models import UserProfile, CompleteEnrollmentData
from dal import autocomplete


"""
Import all majors at MIT. Returns a list of tuples of the majors
"""
def get_mit_majors():
	majors = []
	with open('recommender/static/recommender/degree_requirements.json', 'r') as f:
		data = json.load(f)

	for major in data:
		majors.append((major, major))
	return sorted(majors, key=lambda tup: tup[0])



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
	majors = get_mit_majors()
	major1 = forms.ChoiceField(choices=majors, initial="None")
	major2 = forms.ChoiceField(choices=majors, initial="None")
	semester = forms.ChoiceField(choices=[(x, x) for x in range(1, 9)])
	classes = forms.CharField(max_length=256)
	# classes = autocomplete.ModelSelect2Multiple(url='user-autocomplete')

	class Meta:
		model = UserProfile
		fields = ('major1', 'major2', 'semester', 'classes')
		# widgets = {
  #           'classes': autocomplete.ModelSelect2Multiple(
  #           	'recommender:classes-autocomplete'
  #           )
  #       }


class GetPopularClassesForm(forms.Form):
	majors = get_mit_majors()
	major = forms.ChoiceField(choices=majors, initial="None")
	semester = forms.ChoiceField(choices=[(x, x) for x in range(1, 17)])


class GetSubjectForm(forms.Form):
	class_name = forms.CharField(max_length=256)	# TODO: divide by course and make dropdowns?


class KeywordsForm(forms.Form):
	keywords = forms.CharField(max_length=256)
