from django.db.models import Manager


class ExistingManager(Manager):
    def get_queryset(self):
        return super(Manager, self).get_queryset().filter(deleted=False)
