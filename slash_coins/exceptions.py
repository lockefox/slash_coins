"""exceptions.py: custom exceptions for specific cases"""
class SlashCoinsException(Exception):
    """base Exception class for project exceptions"""
    pass

class UnknownChatPlatform(SlashCoinsException):
    """got a request and don't know what to do with it"""
    pass
