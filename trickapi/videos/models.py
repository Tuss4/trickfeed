from django.db import models


YT = "YT"
IG = "IG"
VN = "VN"

VIDEO_TYPES = (
    (YT, "YouTube"),
    (IG, "Instagram"),
    (VN, "Vine"),
)

YT_URL = "https://www.youtube.com/watch?v={0}"


class Video(models.Model):

    video_type = models.CharField(
        max_length=2, choices=VIDEO_TYPES, default=YT)
    title = models.CharField(max_length=255)
    video_id = models.CharField(max_length=50, unique=True, db_index=True)
    thumbnail_url = models.CharField(max_length=255)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

    def __unicode__(self):
        return "{0} - {1}".format(self.title, self.video_type)
