from django.contrib import admin

# Register your models here.

from newsletter.forms import NewsletterForm
from newsletter.models import Newsletter

class NewsletterAdmin(admin.ModelAdmin):
	"""docstring for NewsletterAdmin"""
	list_display = ['__unicode__', 'timestamp', 'updated']
	list_filter = ["updated", "timestamp"]
	search_fields = ["full_name"]
	form = NewsletterForm
	#class Meta:
	#	model = Newsletter

	#def __init__(self, arg):
	#	super(NewsletterAdmin, self).__init__()
	#	self.arg = arg


admin.site.register(Newsletter, NewsletterAdmin)