from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Video
from eswrapper.script import create_document, update_document

@receiver(post_save, sender=Video)
def document_handler(sender, **kwargs):
    if not kwargs.get('created'):
        update_document(kwargs.get('instance'))
    else:
        create_document(kwargs.get('instance'))
