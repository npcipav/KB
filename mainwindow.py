#!/usr/bin/env python
#


from PyQt4 import QtGui, QtCore

from editrecwindow import EditRecWindow


def RecordView(rec):
    """
    Imagine that it creates instance of RecordView class inherited by
    QtGui.QListWidgetItem from Record. It has date and text properties.
    """
    self = QtGui.QListWidgetItem()
    # self.__class__ = 'RecordView'
    # self.__bases__ = 'QtGui.QListWidgetItem'
    self.date = rec.date
    self.text = rec.text
    self.tags = ' '.join(rec.tags)
    #
    self.setText(
        self.date +
        ':\n' + self.text +
        '\ntags: ' + (self.tags or 'None')
        )
    return self


class MainWindow(QtGui.QWidget):
    """ Class is used like observer by DiaryManager. """

    def __init__(self, model=None, parent=None):
        QtGui.QWidget.__init__(self, parent)
        #
        self.setWindowTitle('KB')
        self.resize(700, 500)
        self.__createWidgets()
        self.__createConnections()
        self._wnds = []
        #
        if not model:
            QtGui.qApp.quit()
        self._model = model
        model.addObserver(self)

    def __createWidgets(self):
        # widgets
        self._addRecButton = QtGui.QPushButton('Add')
        self._editRecButton = QtGui.QPushButton('Edit')
        self._delRecButton = QtGui.QPushButton('Delete')
        self._searchLineEdit = QtGui.QLineEdit()
        self._searchButton = QtGui.QPushButton('Search')
        self._recList = QtGui.QListWidget()
        # layouts
        recControlLayout = QtGui.QHBoxLayout()
        recControlLayout.addWidget(self._addRecButton)
        recControlLayout.addWidget(self._editRecButton)
        recControlLayout.addWidget(self._delRecButton)
        recControlLayout.addWidget(self._searchLineEdit)
        recControlLayout.addWidget(self._searchButton)
        recListLayout = QtGui.QVBoxLayout()
        recListLayout.addWidget(self._recList)
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(recControlLayout)
        mainLayout.addLayout(recListLayout)
        self.setLayout(mainLayout)
        # styles
        sp = QtGui.QSizePolicy()
        sp.setHorizontalPolicy(QtGui.QSizePolicy.Expanding)
        self._searchLineEdit.setSizePolicy(sp)
        sp = QtGui.QSizePolicy()
        sp.setHorizontalPolicy(QtGui.QSizePolicy.Fixed)
        self._delRecButton.setSizePolicy(sp)
        self._recList.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection
            )
        self._recList.setWordWrap(True)

    def __createConnections(self):
        self.connect(
            self._addRecButton, QtCore.SIGNAL('clicked()'),
            self._onClickAddRecButton
            )
        self.connect(
            self._editRecButton, QtCore.SIGNAL('clicked()'),
            self._onClickEditRecButton
            )
        self.connect(
            self._delRecButton, QtCore.SIGNAL('clicked()'),
            self._onClickDelRecButton
            )
        self.connect(
            self._searchButton, QtCore.SIGNAL('clicked()'),
            self._onClickSearchButton
            )

    def _onClickAddRecButton(self):
        wnd = EditRecWindow(model=self._model)
        wnd.show()
        self._wnds.append(wnd)

    def _onClickEditRecButton(self):
        for i in range(self._recList.count()):
            item = self._recList.item(i)
            if item.isSelected():
                oldDate = item.date
                oldText = item.text
                wnd = EditRecWindow(
                    model=self._model, oldDate=oldDate, oldText=oldText
                    )
                wnd.show()
                self._wnds.append(wnd)

    def _onClickDelRecButton(self):
        selectedItems = []
        for i in range(self._recList.count()):
            item = self._recList.item(i)
            if item.isSelected():
                selectedItems.append(item.date)
        self._model.delRecs(selectedItems)

    def _onClickSearchButton(self):
        query = self._searchLineEdit.text()
        query.replace(',', ' ').replace('.', ' ').replace('!', ' ') \
             .replace('?', ' ')
        self._model.updateTags(query.split(' '))

    def updateRecList(self, recs):
        """
        Updates records list on display. It's used by
        DiaryManager like observer's handler method.
        """
        self._recList.clear()
        for rec in recs:
            self._recList.addItem(RecordView(rec))


__all__ = [MainWindow]


def test(): pass


if __name__ == '__main__':
    test()
