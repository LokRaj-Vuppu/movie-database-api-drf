from rest_framework.throttling import UserRateThrottle

class StreamPlatformThrottle(UserRateThrottle):
    scope = 'stream'