from django.db import models
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return u"%s" % self.title

class Domain(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return u"%s" % self.name

class Aria(models.Model):
    name = models.CharField(max_length=255)
    domain = models.ForeignKey(settings.DOMAIN_MODEL)

    def __unicode__(self):
        return u"%s" % self.name

class Project(models.Model):
    name = models.CharField(max_length=255)
    aria = models.ForeignKey(settings.ARIA_MODEL)

    def __unicode__(self):
        return u"%s" % self.name

class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(default=datetime.now)
    updated = models.DateTimeField(default=datetime.now)
    status = models.ForeignKey(settings.TASK_STATUS_MODEL)
    parent = models.ForeignKey(settings.TASK_MODEL, null=True, blank=True)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return u"%s" % self.name


class TaskStatus(models.Model):
    status = models.CharField(max_length=10, unique=True)

    def __unicode__(self):
        return u"%s" % self.status


class WorkLog(models.Model):
    task = models.ForeignKey(settings.TASK_MODEL)
    log = models.PositiveSmallIntegerField(default=0)
    comment = models.ForeignKey(settings.POST_MODEL)

    def __unicode__(self):
        return u"%s %s %s" % (self.log, self.task.name, self.comment.title)
