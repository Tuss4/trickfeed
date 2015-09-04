from rest_framework import serializers
from .models import Video, YT, VIDEO_TYPES, YT_URL


class VideoSerializer(serializers.ModelSerializer):

    video_url = serializers.SerializerMethodField()

    class Meta:
        model = Video

    def get_video_url(self, obj):
        if obj.video_type == YT:
            return YT_URL.format(obj.video_id)
        return ""



class CreateVideoSerializer(serializers.Serializer):

    video_type = serializers.ChoiceField(choices=VIDEO_TYPES, default=YT)
    title = serializers.CharField()
    video_id = serializers.CharField()
    thumbnail_url = serializers.URLField()
