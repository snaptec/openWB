class SkodaConfigException(Exception):
    """Raised when Skoda Connect API client is configured incorrectly"""

    def __init__(self, status):
        """Initialize exception"""
        super(SkodaConfigException, self).__init__(status)
        self.status = status

class SkodaAuthenticationException(Exception):
    """Raised when credentials are invalid during authentication"""

    def __init__(self, status):
        """Initialize exception"""
        super(SkodaAuthenticationException, self).__init__(status)
        self.status = status

class SkodaAccountLockedException(Exception):
    """Raised when account is locked from too many login attempts"""

    def __init__(self, status):
        """Initialize exception"""
        super(SkodaAccountLockedException, self).__init__(status)
        self.status = status

class SkodaTokenExpiredException(Exception):
    """Raised when server reports that the access token has expired"""

    def __init__(self, status):
        """Initialize exception"""
        super(SkodaTokenExpiredException, self).__init__(status)
        self.status = status

class SkodaException(Exception):
    """Raised when an unknown error occurs during API interaction"""

    def __init__(self, status):
        """Initialize exception"""
        super(SkodaException, self).__init__(status)
        self.status = status

class SkodaThrottledException(Exception):
    """Raised when the API throttles the connection"""

    def __init__(self, status):
        """Initialize exception"""
        super(SkodaThrottledException, self).__init__(status)
        self.status = status

class SkodaEULAException(Exception):
    """Raised when EULA must be accepted before login"""

    def __init__(self, status):
        """Initialize exception"""
        super(SkodaEULAException, self).__init__(status)
        self.status = status

class SkodaLoginFailedException(Exception):
    """Raised when login fails for an unknown reason"""

    def __init__(self, status):
        """Initialize exception"""
        super(SkodaLoginFailedException, self).__init__(status)
        self.status = status

class SkodaInvalidRequestException(Exception):
    """Raised when an unsupported request is made"""

    def __init__(self, status):
        """Initialize exception"""
        super(SkodaInvalidRequestException, self).__init__(status)
        self.status = status

class SkodaRequestInProgressException(Exception):
    """Raised when a request fails because another request is already in progress"""

    def __init__(self, status):
        """Initialize exception"""
        super(SkodaRequestInProgressException, self).__init__(status)
        self.status = status
