class Config:

    def __init__(self):
        # Will change to OS Environment Variable
        self.__secret_key = '0bb1f5b6e04b74510b76edaa429ae385'

    @property
    def secret_key(self):
        return self.__secret_key
