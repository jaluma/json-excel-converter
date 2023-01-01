# settings
class SecurityData:
    def __init__(self):
        self.username = b"stanleyjobson"
        self.password = b"swordfish"


class Settings:
    def __init__(self):
        self.docs_url = '/swagger'
        self.redoc_url = '/redoc'
        self.security = SecurityData()


# global instance
settings = Settings()
