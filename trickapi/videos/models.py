from django.db import models


YT = 0
IG = 1
VN = 2

VIDEO_TYPES = (
    (YT, "YouTube"),
    (IG, "Instagram"),
    (VN, "Vine"),
)


class Video(models.Model):

    video_type = models.CharField()
