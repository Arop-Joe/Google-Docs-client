from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Document(models.Model):
	name = models.CharField(max_length=200)
	link = models.CharField(max_length=1000, unique=True)
	creation_date = models.DateField(default=now)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.name
