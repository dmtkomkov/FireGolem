from django.db import models
from django.conf import settings

__all__ = ("WorkLog", "LabelGroup", "Label")


class WorkLog(models.Model):
    log = models.CharField(max_length=255)
    labels = models.ManyToManyField(settings.LABEL_MODEL)

    def __unicode__(self):
        return u"{}".format(self.log)


class LabelGroup(models.Model):
    name = models.CharField(unique=True, max_length=64)
    single = models.BooleanField(default=False)

    def __unicode__(self):
        return u"{}".format(self.name)


class Label(models.Model):
    name = models.CharField(unique=True, max_length=64)
    group = models.ForeignKey(settings.LABEL_GROUP_MODEL, related_name='labels', blank=True, null=True)

    def __unicode__(self):
        return u"{}".format(self.name)
