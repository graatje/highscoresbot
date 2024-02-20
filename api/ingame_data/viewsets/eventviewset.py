from rest_framework import viewsets

from api.ingame_data.models import Event, Eventname
from api.ingame_data.serializers.eventserializer import EventSerializer


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    ALLOWED_EVENTS = [
        Eventname.objects.get(name="swarm"),
        Eventname.objects.get(name="goldrush"),
        Eventname.objects.get(name="arceusaltar"),
        Eventname.objects.get(name="kyogrealtar"),
        Eventname.objects.get(name="honey"),
        Eventname.objects.get(name="tournament"),
        Eventname.objects.get(name="worldblessing"),

    ]
    queryset = Event.objects.all().order_by("-time")
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = Event.objects.filter(eventname__in=self.ALLOWED_EVENTS).order_by("-time")

        return queryset
