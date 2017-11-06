from django.db import models
from datetime import datetime
from django.conf import settings

__all__ = ("Area", "Project", "Task", "TaskStatus", "WorkLog")


class Area(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u"%s" % self.name

    @property
    def count(self):
        return Task.objects.filter(status=self.id).count()


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u"%s" % self.name

    @property
    def count(self):
        return Task.objects.filter(status=self.id).count()


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(default=datetime.now)
    updated = models.DateTimeField(default=datetime.now)
    status = models.ForeignKey(settings.TASK_STATUS_MODEL, default=1)
    estimation = models.PositiveSmallIntegerField(default=0)
    area = models.ForeignKey(settings.AREA_MODEL, models.SET_NULL, blank=True, null=True)
    project = models.ForeignKey(settings.PROJECT_MODEL, models.SET_NULL, blank=True, null=True)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return u"%s" % self.name


class TaskStatus(models.Model):
    status = models.CharField(max_length=10, unique=True)

    def __unicode__(self):
        return u"%s" % self.status

    @property
    def count(self):
        return Task.objects.filter(status=self.id).count()


class WorkLog(models.Model):
    task = models.ForeignKey(settings.TASK_MODEL)
    log = models.PositiveSmallIntegerField(default=0)
    comment = models.ForeignKey(settings.POST_MODEL)  # TODO: change name comment -> post

    def __unicode__(self):
        return u"%s" % self.comment.title
