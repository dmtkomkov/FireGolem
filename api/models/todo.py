from django.db import models
from datetime import datetime
from django.conf import settings

from django.db.models import Sum

__all__ = ("Area", "Project", "Task", "TaskStatus", "WorkLog")


class TaskManager(models.Manager):
    def get_queryset(self):
        return super(models.Manager, self).get_queryset().filter(deleted=False)


class Area(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u"%s" % self.name

    @property
    def count(self):
        # Exclude cancelled and closed tasks
        return Task.objects.filter(area=self.id).exclude(status__in=(21, 22)).count()


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u"%s" % self.name

    @property
    def count(self):
        # Exclude cancelled and closed tasks
        return Task.objects.filter(project=self.id).exclude(status__in=(21, 22)).count()


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

    objects = TaskManager()

    @property
    def logged(self):
        task_logs = WorkLog.objects.filter(task=self.id).filter(post__deleted=False)
        return task_logs.aggregate(Sum('log'))['log__sum'] or 0  # Do not return None in case of no logs

    def __unicode__(self):
        return u"%s" % self.name


class TaskStatus(models.Model):
    status = models.CharField(max_length=10, unique=True)
    icon = models.CharField(max_length=20, blank=True, null=True)

    def __unicode__(self):
        return u"%s" % self.status

    @property
    def count(self):
        return Task.objects.filter(status=self.id).count()


class WorkLog(models.Model):
    task = models.ForeignKey(settings.TASK_MODEL)
    log = models.PositiveSmallIntegerField(default=0)
    post = models.ForeignKey(settings.POST_MODEL)

    def __unicode__(self):
        return u"%s" % self.comment.title
