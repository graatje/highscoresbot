from api.eventconfigurations.models.eventconfiguration import Eventconfiguration
from rest_framework import serializers


class EventconfigurationSerializer(serializers.HyperlinkedModelSerializer):
    eventname = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = Eventconfiguration
    #    fields = ["id", "eventname", "guild", "channel", "pingrole", "time_in_channel", "failed_sends"]
