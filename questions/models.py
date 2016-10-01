from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.template.defaultfilters import truncatechars
from django.utils.text import Truncator
from django.core.urlresolvers import reverse

# Create your models here.
from accounts.models import MyUser
from videos.models import Video

class QuestionManager(models.Manager):
    """docstring for QuestionManager"""
    def all(self):
        return super(QuestionManager, self).filter(active=True).filter(parent=None)
        
    def recent(self):
        try:
        	limit_to = settings.RECENT_COMMENT_NUMBER
        except:
        	limit_to = 6
        return self.get_queryset().filter(active=True).filter(parent=None)[:limit_to]

    def create_question(self, user=None, text=None, destination=None, video=None, parent=None):
        if not destination:
            raise ValueError("Must have a destination for new comment")

        if not user:
            raise ValueError("Must have a user for every comment")

        question = self.model(
            user = user,
            destination = destination,
            text = text,
        )
        if video is not None:
            question.video = video
        if parent is not None:
            question.parent = parent
        question.save(using=self._db)
        return question


class Question(models.Model):
    """docstring for Question"""
    user = models.ForeignKey(MyUser)
    parent = models.ForeignKey("self", null=True, blank=True)
    destination = models.CharField(max_length=300)
    text = models.TextField()
    video = models.ForeignKey(Video, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    active = models.BooleanField(default=True)

    objects = QuestionManager()

    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('question_thread', kwargs={'id':self.id})

    @property
    def get_instance_location(self):
        return self.destination

    @property
    def get_question(self):
        return self.text

    @property
    def is_child(self):
        if self.parent is not None:
            return True
        else:
            return False

    def get_children(self):
        if self.is_child:
            return None
        else:
            return Question.objects.filter(parent=self)

    def get_affected_users(self):
        """
        it needs to be a parent and have children,
        the children, in effect, are the affected users.
        """
        question_children = self.get_children()
        if question_children is not None:
            users = []
            for question in question_children:
                if question.user in users:
                    pass
                else:
                    users.append(question.user)
            return users
        return None
