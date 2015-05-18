#!/usr/bin/env python
#


class Settings:
    """ Keeps application settings. """

    def __init__(self):
        self._dbFileName = ''

    def getDbFileName(self):
        return self._dbFileName

    def setDbFileName(self, name):
        self._dbFileName = name

settings = Settings()
