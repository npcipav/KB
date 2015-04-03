#!/usr/bin/env python
#


import sqlite3


class DiaryDBHelper:
    """ Database helper. """

    def __init__(self, dbFileName):
        #
        self._connection = sqlite3.connect(dbFileName)
        self._cursor = self._connection.cursor()
        #
        queries = [
            "create table if not exists diary (date text primary key,"
                " text text)",
            "create table if not exists tags (id integer primary key"
                " autoincrement, tag text, msgdate text)",
            ]
        [self._run(query) for query in queries]

    def __del__(self):
        # Normilize the data base and close the date base connection
        # on delete.
        self._cursor.execute("vacuum")
        self._connection.close()

    def _run(self, query):
        print(query)
        self._cursor.execute(query)

    def add(self, date, text, tags):
        try:
            query = ("insert into diary (date, text) values ('{date}',"
                " '{text}')").format(date=date, text=text)
            self._run(query)
            for tag in tags:
                query = ("insert into tags (tag, msgdate) values "
                    "('{tag}', '{date}')").format(tag=tag, date=date)
                self._run(query)
            self._connection.commit()
        except sqlite3.Error: print('sqlite3.Error')

    def delete(self, date):
        try:
            queries = [
                "delete from diary where date='{date}'"
                    .format(date=date),
                "delete from tags where msgdate='{date}'"
                    .format(date=date),
                "commit",
                ]
            [self._run(query) for query in queries]
        except sqlite3.Error: print('sqlite3.Error')

    def find(self, tags=['']):
        """
        Finds records in a data base which satisfy the query tags and
        returns them. If req is empty, returns all records.
        """
        try:
            if tags == ['']:
                query = "select date, text from diary"
                self._run(query)
                return self._cursor.fetchall()
            else:
                for tag in tags:
                    query = ("select date, text from diary where date"
                        " in (select msgdate from tags where tag="
                        "'{tag}')"
                        ).format(tag=tag)
                    self._run(query)
                return self._cursor.fetchall()
        except sqlite3.Error: print('sqlite3.Error')


def test(): pass


if __name__ == '__main__':
    test()
