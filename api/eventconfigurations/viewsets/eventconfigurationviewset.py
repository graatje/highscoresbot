from rest_framework import viewsets
from api.eventconfigurations.models.eventconfiguration import Eventconfiguration
from api.eventconfigurations.serializers.eventconfigurationserializer import EventconfigurationSerializer


class EventconfigurationViewSet(viewsets.ModelViewSet):
    queryset = Eventconfiguration.objects.all()
    serializer_class = EventconfigurationSerializer
