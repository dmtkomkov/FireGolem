from django.db import models
from datetime import datetime
from django.conf import settings

__all__ = 'Post',


class PostManager(models.Manager):
    def get_queryset(self):
        return super(models.Manager, self).get_queryset().filter(deleted=False)


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    deleted = models.BooleanField(default=False)

    objects = PostManager()

    def __unicode__(self):
        return u"%s" % self.title
