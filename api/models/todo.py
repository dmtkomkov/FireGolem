from django.db import models
from datetime import datetime
from django.conf import settings

from .managers import ExistingManager

__all__ = ("Task",)


# class Area(models.Model):
#     name = models.CharField(max_length=255, unique=True)
#     description = models.TextField(blank=True, null=True)
#
#     def __unicode__(self):
#         return u"%s" % self.name
#
#     @property
#     def count(self):
#         # Exclude cancelled and closed tasks
#         return Task.objects.filter(area=self.id).exclude(status__in=(21, 22)).count()


# class Project(models.Model):
#     name = models.CharField(max_length=255, unique=True)
#     description = models.TextField(blank=True, null=True)
#
#     def __unicode__(self):
#         return u"%s" % self.name
#
#     @property
#     def count(self):
#         # Exclude cancelled and closed tasks
#         return Task.objects.filter(project=self.id).exclude(status__in=(21, 22)).count()


class Task(models.Model):
    name = models.CharField(max_length=255)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    created_date = models.DateTimeField(default=datetime.now)
    completed_date = models.DateTimeField(blank=True, null=True)
    deleted = models.BooleanField(default=False)
    objects = ExistingManager()

    def __unicode__(self):
        return u"%s" % self.name


# class TaskStatus(models.Model):
#     status = models.CharField(max_length=10, unique=True)
#     icon = models.CharField(max_length=20, blank=True, null=True)
#
#     def __unicode__(self):
#         return u"%s" % self.status
#
#     @property
#     def count(self):
#         return Task.objects.filter(status=self.id).count()
#
#
# class WorkLog(models.Model):
#     task = models.ForeignKey(settings.TASK_MODEL)
#     log = models.PositiveSmallIntegerField(default=0)
#     post = models.ForeignKey(settings.POST_MODEL)
#
#     def __unicode__(self):
#         return u"{}: {}".format(self.task, self.log)
