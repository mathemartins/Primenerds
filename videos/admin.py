from django.contrib import admin

# Register your models here.
from videos.models import Video, Category, TaggedItem
from django.contrib.contenttypes.admin import GenericTabularInline

class TaggedItemInline(GenericTabularInline):
    """docstring for TaggedItem"""
    model = TaggedItem

class VideoInline(admin.TabularInline):
	model = Video

class VideoModelAdmin(admin.ModelAdmin):
    """docstring for VideoModelAdmin"""
    inlines = [TaggedItemInline]
    list_display = ['__unicode__','title', 'category', 'share_message', 'slug','embed_code']
    list_display_links = ['title']
    list_filter = ['title']
    search_fields = ['title']

    prepopulated_fields = {
        "slug":["title"],
    }

    class Meta:
        model = Video


    #def __init__(self, arg):
    #    super(VideoModelAdmin, self).__init__()
    #    self.arg = arg

class CategoryModelAdmin(admin.ModelAdmin):
    """docstring for CategoryModelAdmin"""
    inlines = [VideoInline, TaggedItemInline]
    list_display = ['title', 'description']
    list_display_links = ['title']
    list_filter = ['title']
    search_fields = ['title']

    class Meta:
        model = Category


    #def __init__(self, arg):
    #    super(CategoryModelAdmin, self).__init__()
    #    self.arg = arg


admin.site.register(Video, VideoModelAdmin)
admin.site.register(Category, CategoryModelAdmin)
admin.site.register(TaggedItem)
