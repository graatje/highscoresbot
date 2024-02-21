from api.ingame_data.models import Event
from rest_framework import serializers


class EventSerializer(serializers.HyperlinkedModelSerializer):
    eventname = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = Event
        fields = ["id", "eventname", "data", "time"]
