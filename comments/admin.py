from django.contrib import admin

# Register your models here.
from .models import Comment

# customizing the Comment admin in detail
class CommentModelAdmin(admin.ModelAdmin):
	"""docstring for CommentModelAdmin"""
	list_display = ['user', 'content_type', 'timestamp', 'content']
	list_display_links = ['content']
	list_filter = ['timestamp', 'user', 'content_type']
	search_fields = ['content']
	class Meta:
		model = Comment


admin.site.register(Comment, CommentModelAdmin)