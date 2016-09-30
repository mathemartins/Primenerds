from __future__ import unicode_literals
import urllib2

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify

# Create your models here.
from videos.utils import get_vid_for_direction
# MVC - Model View Controller

class VideoQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True)

    def has_embed(self):
        return self.filter(embed_code__isnull=False).exclude(embed_code__exact="")

class VideoManager(models.Manager):
    """docstring for get_featured"""
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)

    def get_featured(self, user, kabc=None):
        #return super (VideoManager, self).filter(featured=True)
        return self.get_queryset().active().featured()

    def all(self):
        return self.get_queryset().active().has_embed()


DEFAULT_MESSAGE = "Yet another awesome package from primenerds."

class Video(models.Model):
    """docstring for Video"""
    title = models.CharField(max_length=200)
    embed_code = models.CharField(max_length=500)
    tags = GenericRelation("TaggedItem", null=True, blank=True)
    share_message = models.TextField(default=DEFAULT_MESSAGE)
    order = models.PositiveIntegerField(default=1)
    slug = models.SlugField(null=True, blank=True)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    free_preview = models.BooleanField(default=False)
    category = models.ForeignKey("Category", default=1)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)

    objects = VideoManager()

    class Meta:
        unique_together = ('slug', 'category')
        ordering = ['order', 'timestamp']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse ("video_detail", kwargs = {"vid_slug":self.slug, "cat_slug":self.category.slug})

    def get_share_link(self):
        full_url_address = "%s%s" %(settings.FULL_DOMAIN_NAME, self.get_absolute_url())
        return full_url_address

    # instance method of itself
    def get_share_message(self):
        full_url_address = "%s%s" %(settings.FULL_DOMAIN_NAME, self.get_absolute_url())
        return urllib2.quote("%s %s" %(self.share_message, full_url_address))

    def get_next_url(self):
        video = get_vid_for_direction(self, "next")
        if video is not None:
            return video.get_absolute_url()
        return None

    def get_previous_url(self):
        video = get_vid_for_direction(self, "previous")
        if video is not None:
            return video.get_absolute_url()
        return None

    @property
    def has_preview(self):
        if self.free_preview:
            return True
        return False

def video_post_save_reciever(sender, instance, created, *args, **kwargs):
    print "signal sent"
    if created:
        slug_title = slugify(instance.title)
        new_slug = "%s %s %s" %(instance.title, instance.category.slug, instance.id)
        try:
            obj_exits = Video.objects.get(slug=slug_title, category=instance.category)
            instance.slug = slugify(new_slug)
            instance.save()
            print "models exists, new slug generated !!"
        except Video.DoesNotExist:
            instance.slug = slug_title
            instance.save()
            print "slug and model created !!"
        except Video.MultipleObjectsReturned:
            instance.slug = slugify(new_slug)
            instance.save()
            print "multiple models already exists, new slug generated !!"
        except:
            pass
post_save.connect(video_post_save_reciever, sender=Video)

class CategoryQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True)

class CategoryManager(models.Manager):
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)

    def get_featured(self):
        return self.get_queryset().active().featured()

    def all(self):
        return self.get_queryset().active()

class Category(models.Model):
    """docstring for Category"""
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=10000, null=True, blank=True)
    tags = GenericRelation("TaggedItem", null=True, blank=True)
    image = models.ImageField(upload_to="video_images/", null=True, blank=True)
    slug = models.SlugField(unique=True)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    objects = CategoryManager()

    class Meta:
        ordering = ['title', 'timestamp']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse ("project_detail", kwargs = {"cat_slug":self.slug})

    def get_image_url(self):
        return "%s%s" %(settings.MEDIA_URL, self.image)

    def get_description(self):
        return self.description

def category_post_save_reciever(sender, instance, created, *args, **kwargs):
    print "signal sent"
    if created:
        slug_title = slugify(instance.title)
        new_slug = "%s %s %s" %(instance.title, instance.slug, instance.id)
        try:
            obj_exits = Category.objects.get(slug=slug_title)
            instance.slug = slugify(new_slug)
            instance.save()
            print "models exists, new slug generated !!"
        except Category.DoesNotExist:
            instance.slug = slug_title
            instance.save()
            print "slug and model created !!"
        except Category.MultipleObjectsReturned:
            instance.slug = slugify(new_slug)
            instance.save()
            print "multiple models already exists, new slug generated !!"
        except:
            pass
post_save.connect(category_post_save_reciever, sender=Category)

TAG_CHOICES = (
    ("Python", "Django"),
    ("Php", "laravel"),
    ("Bootstrap", "Bootstrap"),
    ("Swift", "Swift"),
)

class TaggedItem(models.Model):
    tag = models.SlugField(choices=TAG_CHOICES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('tag', 'content_type', 'object_id')

    def __unicode__(self):              # __str__ on Python 3
        return self.tag
