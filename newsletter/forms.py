from django import forms

from newsletter.models import Newsletter

class NewsletterForm(forms.ModelForm):
	"""docstring for NewsletterForm"""
	class Meta:
		model = Newsletter
		fields = ['full_name', 'email']
	#def __init__(self, arg):
	#	super(NewsletterForm, self).__init__()
	#	self.arg = arg
		