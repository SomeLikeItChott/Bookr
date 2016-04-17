from django import forms

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