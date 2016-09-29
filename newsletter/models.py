from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Newsletter(models.Model):
	"""docstring for Newsletter"""
	email = models.EmailField()
	full_name = models.CharField(max_length=100, blank=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __unicode__(self):
		return self.email

	#def __init__(self, arg):
	#	super(Newsletter, self).__init__()
	#	self.arg = arg
		