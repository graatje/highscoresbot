# import datetime
# import re
#
#
#
# class WorldBlessing(TimedEvent):
#     """
#     This event triggers 2 minutes before the expiring of the worldblessing.
#     """
#     def __init__(self):
#         """
#         calls the superclass init.
#         """
#         self.EVENTNAME = "worldblessing"
#         super(WorldBlessing, self).__init__(datetime.timedelta(minutes=30))
#
#     def makeMessage(self) -> str:
#         """
#         Makes the message that gets sent to the recipients.
#         :return: the message
#         """
#         return "world blessing expiring in 2 minutes!"
#
#     def __bool__(self):
#         now = datetime.datetime.now()
#         return self.activationtime is not None and not self.hasCooldown() and self.activationtime <= now <= \
#                (self.activationtime + datetime.timedelta(minutes=3))
