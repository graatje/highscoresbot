from enum import Enum


class PermissionLevel(Enum):
    UNAUTHORIZED = 0
    LOGGED_IN = 1
    ADMINISTRATOR = 2

    def __eq__(self, other):
        if type(other) != PermissionLevel:
            return False
        return other.value == self.value

    def __lt__(self, other):
        if type(other) != PermissionLevel:
            return False
        return self.value < other.value

    def __gt__(self, other):
        if type(other) != PermissionLevel:
            return False
        return self.value > other.value

    def __le__(self, other):
        if type(other) != PermissionLevel:
            return False
        return self.value <= other.value

    def __ge__(self, other):
        if type(other) != PermissionLevel:
            return False
        return self.value >= other.value
