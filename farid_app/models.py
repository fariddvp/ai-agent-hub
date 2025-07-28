from django.db import models
import uuid

# Create your models here.
class DbBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Conversation(DbBaseModel):
    conversation_log = models.JSONField(default=dict)
    title = models.CharField(max_length=500, default=None, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True, db_index=True)
    is_deleted = models.BooleanField(default=False)
