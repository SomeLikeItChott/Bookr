from django import forms
from django.db import models

class AddContactForm(forms.Form):
	TYPES = (
		('PH', 'Phone'),
		('EM', 'Email'),
	)
	contact_type = forms.ChoiceField(choices=TYPES)
	contact_text = forms.CharField(label='Add new contact info', max_length=40)

class SellForm(forms.Form):
	price = forms.FloatField(label='Price')
	condition = forms.CharField(label='Condition',max_length=100)
	isbn = forms.IntegerField(label='ISBN')
	image = forms.ImageField(required=False)

class RatingForm(forms.Form):
	ONE = 1
	TWO = 2
	THREE = 3
	FOUR = 4
	FIVE = 5
	STAR_CHOICES = (
		(ONE, '★☆☆☆☆'),
		(TWO, '★★☆☆☆'),
		(THREE, '★★★☆☆'),
		(FOUR, '★★★★☆'),
		(FIVE, '★★★★★'),
	)
	stars = forms.ChoiceField(choices=STAR_CHOICES)
	text = forms.CharField(widget=forms.Textarea, label='Comment')

