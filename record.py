#!/usr/bin/env python
#


class Record:
    """ Just record in a diary. """

    def __init__(self, date, text):
        self.date = date
        self.text = text
        self.__createTags()

    def __createTags(self):
        text = self.text
        text.replace('.', ' ').replace(',', ' ').replace('!', ' ') \
            .replace('?', ' ')
        self.tags = [
            word for word in text.split(' ') if word.startswith('#')
            ]


def test(): pass


if __name__ == '__main__':
    test()
