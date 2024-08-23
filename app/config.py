
class Config:
    DEBUG = False

class DefaultConfig(Config):
    DEBUG = True

config = {
    'default': DefaultConfig
}