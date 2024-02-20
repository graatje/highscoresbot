from rest_framework import viewsets

from api.ingame_data.models import Event
from api.ingame_data.serializers.eventserializer import EventSerializer


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
