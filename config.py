class Config( object ):
    """
    Common Configuration

    """
    URL_ROOT = 'v1'

class DevelopmentConfig( Config ):
    DEBUG = True

app_config = {
    'development': DevelopmentConfig
}