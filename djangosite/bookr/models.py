from django.db import models
from django.contrib.auth.models import User

#idk about on_delete, might have made some mistakes there.
#probably helps that there is no way to delete users
class Book(models.Model):
	picture = models.ImageField()
	seller = models.ForeignKey(User, on_delete=models.CASCADE)
	price = models.FloatField()
	condition = models.CharField(max_length=100)
	isbn = models.BigIntegerField()

class Seller(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.ImageField()
	phone = models.CharField(max_length=20)

class Review(models.Model):
	#these related_names might cause issues?????!?!?!?!!!
	rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='raters')
	ratee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratees')
	stars = models.IntegerField()
	text = models.CharField(max_length=500)