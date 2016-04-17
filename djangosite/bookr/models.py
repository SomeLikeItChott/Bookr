from django.db import models
from django.contrib.auth.models import User

#idk about on_delete, might have made some mistakes there.
#probably helps that there is no way to delete users
class Book(models.Model):
	title = models.CharField(max_length=200, default='No title found')
	author = models.CharField(max_length=200, default='No authors found')
	picture = models.ImageField()
	seller = models.ForeignKey(User, on_delete=models.CASCADE)
	price = models.FloatField()
	condition = models.CharField(max_length=100)
	isbn = models.BigIntegerField()

class Seller(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.ImageField()

class Contact(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	PHONE = 'PH'
	EMAIL = 'EM'
	CONTACT_TYPE_CHOICES = (
		(PHONE, 'Phone'),
		(EMAIL, 'Email'),
	)
	contact_type = models.CharField(max_length=2, choices=CONTACT_TYPE_CHOICES, default=PHONE)
	contact_text = models.CharField(max_length=40)

class Review(models.Model):
	#these related_names might cause issues?????!?!?!?!!!
	rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='raters')
	ratee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratees')
	stars = models.IntegerField()
	text = models.CharField(max_length=500)