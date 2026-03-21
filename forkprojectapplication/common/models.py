import uuid

from django.db import models
from django.db.models import Manager
from django.utils import timezone


# Create your models here.    
class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class TimeStampMixin(models.Model):
    creation_time = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_time = models.DateTimeField(null=True)
    deleter_id = models.IntegerField(null=True)
    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def delete(self):
        self.deleted_time = timezone.now()
        self.is_deleted = True
        self.save()
    
    def restore(self):
        self.is_deleted = False
        self.save()

    class Meta:
        abstract = True


class ModifierMixin(models.Model):
    creator_id = models.IntegerField()
    last_modifier_id = models.IntegerField()

    class Meta:
        abstract = True


class CustomBaseModel(TimeStampMixin, SoftDeleteMixin, ModifierMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True