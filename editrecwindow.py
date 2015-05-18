#!/usr/bin/env python
#


from PyQt4 import QtGui, QtCore
from datetime import datetime

from record import Record


class EditRecWindow(QtGui.QWidget):
    """ Window is used to edit or create records. """

    def __init__(self, oldDate='', oldText='', model=None, parent=None):
        QtGui.QWidget.__init__(self, parent)
        #
        self._editModeOn = (oldText != '' and oldDate != '')
        self._oldText = oldText
        self._oldDate = oldDate
        #
        self.setWindowTitle('Editor')
        self.resize(600, 400)
        self.__createWidgets()
        self.__createConnections()
        #
        if not model:
            QtGui.qApp.quit()
        self._model = model

    def __createWidgets(self):
        # widgets
        self._addRecButton = QtGui.QPushButton('Ok')
        self._newRecTextEdit = QtGui.QTextEdit()
        if self._editModeOn:
            self._newRecTextEdit.insertPlainText(self._oldText)
        # layouts
        vb = QtGui.QVBoxLayout()
        vb.addWidget(self._addRecButton)
        vb.addWidget(self._newRecTextEdit)
        self.setLayout(vb)
        # styles

    def __createConnections(self):
        self.connect(
            self._addRecButton, QtCore.SIGNAL('clicked()'),
            self._onClickAddRecButton
            )

    def _onClickAddRecButton(self):
        date = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        text = str(self._newRecTextEdit.toPlainText())
        if text == '':
            self.close()
            return
        self._newRecTextEdit.clear()
        if self._editModeOn:
            self._model.editRec(self._oldDate, Record(date, text))
        else:
            self._model.addRec(Record(date, text))
        self.close()
