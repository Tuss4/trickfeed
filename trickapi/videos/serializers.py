from rest_framework import serializers
from .models import Video, YT, VIDEO_TYPES


class VideoSerializer(serializers.ModelSerializer):

    video_url = serializers.SerializerMethodField()

    class Meta:
        model = Video

    def get_video_url(self, obj):
        return obj.get_video_url


class CreateVideoSerializer(serializers.Serializer):

    video_type = serializers.ChoiceField(choices=VIDEO_TYPES, default=YT)
    title = serializers.CharField()
    video_id = serializers.CharField()
    thumbnail_url = serializers.URLField()
