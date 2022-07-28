from rest_framework import serializers

from api.models import TargetURL


class TargetURLSerializer(serializers.ModelSerializer):
    full_url = serializers.URLField()
    lifetime = serializers.IntegerField()
    short_url = serializers.URLField()

    class Meta:
        model = TargetURL
        fields = ('full_url', 'lifetime', 'short_url')
