from django.db import models
from django.conf import settings
from datetime import date

__all__ = ("WorkLog", "LabelGroup", "Label")


class WorkLog(models.Model):
    log = models.CharField(max_length=255)
    labels = models.ManyToManyField(settings.LABEL_MODEL)
    date = models.DateField(default=date.today)
    duration = models.IntegerField(default=30)

    def __unicode__(self):
        return u"{}".format(self.log)


class LabelGroup(models.Model):
    name = models.CharField(unique=True, max_length=64)
    color = models.CharField(max_length=7, default='#ffffff')

    def __unicode__(self):
        return u"{}".format(self.name)


class Label(models.Model):
    name = models.CharField(unique=True, max_length=64)
    group = models.ForeignKey(settings.LABEL_GROUP_MODEL, related_name='labels', blank=True, null=True,
                              on_delete=models.CASCADE)

    def __unicode__(self):
        return u"{}".format(self.name)
