#!/usr/bin/env python
#
# KB.
#


import sys
from PyQt4 import QtGui, QtCore

from settings import settings
from diarymanager import DiaryManager
from mainwindow import MainWindow


def main():
    #
    app = QtGui.QApplication(sys.argv)
    settings.setDbFileName('diary.sqlite')
    diary = DiaryManager()
    wnd = MainWindow(diary)
    wnd.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
