#!/usr/bin/env python
#


from settings import settings
from diarydbhelper import DiaryDBHelper
from record import Record


def castTupleToRecord(tpl):
    # 1 - date; 2 - text.
    return Record(tpl[0], tpl[1])


class DiaryManager:
    """
    Diary message manager. Implements a Observable interface from
    Observer disign pattern.
    """

    def __init__(self):
        fileName = settings.getDbFileName()
        self._db = DiaryDBHelper(fileName)
        self._observers = []
        # Init msgs.
        self._recs = list(map(castTupleToRecord, self._db.find()))

    def addRec(self, rec):
        """ Adds record. """
        self._db.add(rec.date, rec.text, rec.tags)
        self._recs = list(map(castTupleToRecord, self._db.find()))
        self._notifyObservers()

    def editRec(self, oldDate, rec):
        """ Substitutes record with date as oldDate to rec. """
        self.delRecs([oldDate, ])
        self.addRec(rec)

    def delRecs(self, dates):
        """ Deletes records by date. """
        for date in dates:
            self._db.delete(date)
        self._recs = list(map(castTupleToRecord, self._db.find()))
        self._notifyObservers()

    def updateTags(self, tags):
        """ Updates displayed message list by tags. """
        self._recs = []
        self._recs = list(map(castTupleToRecord, self._db.find(tags)))
        self._notifyObservers()

    def addObserver(self, observer):
        """
        One of observable method, see the Observer Disign Pattern for
        details.
        """
        self._observers.append(observer)
        self._notifyObservers()

    def deleteObserver(self, observer):
        """
        One of observable method, see the Observer Disign Pattern for
        details.
        """
        self._observer.pop(observer)

    def _notifyObservers(self):
        # One of observable method, see the Observer Disign Pattern for
        # details.
        for o in self._observers:
            o.updateRecList(self._recs)


__all__ = [DiaryManager]


def test(): pass


if __name__ == '__main__':
    test()
