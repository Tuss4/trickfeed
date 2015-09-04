from rest_framework import serializers


class RegisterTrickerSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField()
