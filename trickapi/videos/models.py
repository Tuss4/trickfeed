from django.db import models
from eswrapper.mixins import ESWrapperMixin
from eswrapper.managers import ESManager
from .managers import ESVideoManager


YT = "YT"
IG = "IG"
VN = "VN"

VIDEO_TYPES = (
    (YT, "YouTube"),
    (IG, "Instagram"),
    (VN, "Vine"),
)

YT_URL = "https://www.youtube.com/watch?v={}"


class Video(ESWrapperMixin, models.Model):

    video_type = models.CharField(
        max_length=2, choices=VIDEO_TYPES, default=YT)
    title = models.CharField(max_length=255)
    video_id = models.CharField(max_length=50, unique=True, db_index=True)
    thumbnail_url = models.CharField(max_length=255)
    date_added = models.DateField(auto_now_add=True)

    es_objects = ESVideoManager()

    class Meta:
        ordering = ['-date_added']

    def __unicode__(self):
        return "{0} - {1}".format(self.video_id, self.video_type)

    @property
    def get_video_url(self):
        if self.video_type == YT:
            return YT_URL.format(self.video_id)
        return ""

    # Overriding get_document_body to add a custom key/val for get_video_url
    def get_document_body(self):
        doc_dict = super(Video, self).get_document_body()
        doc_dict['video_url'] = self.get_video_url
        return doc_dict
