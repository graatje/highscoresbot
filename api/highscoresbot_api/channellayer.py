from channels.layers import InMemoryChannelLayer


class ChannelLayer(InMemoryChannelLayer):
    def __init__(self, **kwargs):
        super().__init__(group_expiry=864000, **kwargs)
