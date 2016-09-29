from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.

#share_string = quote_plus(instance.content)
#Post.objects.get(id=instance.id)
#comments = Comment.objects.filter_by_instance(instance)

class CommentManager(models.Manager):
	def all(self):
		qs = super(CommentManager, self).filter(parent=None)
		return qs


	"""docstring for CommentManager"""
	def filter_by_instance(self, instance):
		content_type = ContentType.objects.get_for_model(instance.__class__)
		obj_id = instance.id
		try:
			limit_to = settings.RECENT_COMMENT_NUMBER
		except:
			limit_to = 6

		qs=super(CommentManager, self).filter(content_type=content_type, object_id=obj_id).filter(parent=None)[:limit_to]
		#comments = Comment.objects.filter_by_instance(instance)
		return qs




class Comment(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	active = models.BooleanField(default=True)
	content_object = GenericForeignKey('content_type', 'object_id')
	parent = models.ForeignKey("self", null=True, blank=True)

	content = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)


	objects = CommentManager()

	class Meta:
		ordering = ['-timestamp']

	def __unicode__(self):
		return str(self.user.username)


	#def __init__(self, arg):
	#	super(Comment, self).__init__()
	#	self.arg = arg

	def get_absolute_url(self):
		return reverse("comments:thread", kwargs={"id": self.id})
		pass

	def children(self): #replies to parent comment
		return Comment.objects.filter(parent=self)

	@property
	def is_parent(self):
		if self.parent is not None:
			return False
		return True
