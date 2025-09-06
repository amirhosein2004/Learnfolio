from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

# Custom throttle class for anonymous users with a specific rate limit scope
class CustomAnonThrottle(AnonRateThrottle):
    scope = 'custom_action'

# Custom throttle class for authenticated users with a specific rate limit scope
class CustomUserThrottle(UserRateThrottle):
    scope = 'custom_action'

# Custom throttle class for token refresh requests for authenticated users
class TokenRefreshUserThrottle(UserRateThrottle):
    scope = 'token_refresh_user'
