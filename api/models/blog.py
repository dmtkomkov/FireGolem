from django.db import models
from datetime import datetime
from django.conf import settings

from django.db.models import Manager
from api.managers import ExistingManager

__all__ = 'Post',


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    deleted = models.BooleanField(default=False)
    objects = ExistingManager()
    all_objects = Manager()

    def __unicode__(self):
        return u"%s" % self.title
