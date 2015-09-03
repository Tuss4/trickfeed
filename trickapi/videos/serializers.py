from rest_framework import serializers
from .models import Video


class VideoSerializer(serializers.ModelSerializer):

    video_url = serializers.Field(source='get_video_url')

    class Meta:
        model = Video
