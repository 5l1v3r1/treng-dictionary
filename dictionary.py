from gui import appGUI
from dictionaries import cambridge
from dictionaries import tureng
from PyQt5 import QtCore, QtGui, QtWidgets

class dictionary(QtWidgets.QMainWindow, appGUI.Ui_MainWindow):
    def __init__(self, parent=None):
        super(dictionary,self).__init__(parent)

        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('gui/icon.png'))
        
        with open('gui/style.css') as f:
            style = f.read()

        self.setStyleSheet(style)
        appGUI.Ui_MainWindow()
        self.lineEdit.returnPressed.connect(self.translateIt)
        self.pushButton.clicked.connect(self.translateIt)
        
    def clear(self):
        print('worked')

    def reTranslateTreng(self,x,y):        
        word = self.trTable.item(x, y)
        word = word.text()
        self.lineEdit.setText(word)
        self.translateIt()

    def reTranslateCamb(self,x,y):
        word = self.cmTable.item(x, y)
        word = word.text()        
        self.lineEdit.setText(word)
        self.translateIt()

    def translateIt(self):
        unknown = self.lineEdit.text()
        if unknown == '':
            unknown = 'Stay Home'
            self.lineEdit.setText('Stay Home :)')
        unknown = unknown.lower()
        wordTr = tureng.get_result(unknown)
        wordCm = cambridge.getTranslate(unknown)

        if 'suggestions' not in wordTr:
            wordTr = tureng.translate(unknown)
            pass
        
        else:
            trSuggestList = list(wordTr.values())
            wordTr=False # flag for suggestion

        dR=[213,210,159] # dark row color
        lR=[233,232,204] # light row color

        ######################################################
        ################ TURENG WORKSPACE ####################
        ######################################################

        if self.trLayout.count()>0:
            self.trTable.setColumnCount(2)
            self.trTable.setRowCount(0)
        else:    
            self.trTable = QtWidgets.QTableWidget(self.trFrame)
            self.trTable.setObjectName("trTable")
            self.trLayout.addWidget(self.trTable)
            self.trTable.setColumnCount(2)
            self.trTable.setRowCount(0)
            self.trTable.setSelectionMode(0)
            self.trTable.setFocusPolicy(0)
            self.trTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            self.trTable.verticalHeader().setVisible(False)
            self.trTable.horizontalHeader().setStretchLastSection(True)

            # Strech first column
            header = QtWidgets.QHeaderView(QtCore.Qt.Horizontal, self.trTable)
            self.trTable.setHorizontalHeader(header)
            header.setVisible(False)
            header.setSectionResizeMode(0,QtWidgets.QHeaderView.Stretch)

        try:
            self.trTable.cellDoubleClicked.disconnect()
        except:
            pass
        
        if wordTr==False: #check result is suggestions
            suggestions = trSuggestList[0]
            self.trTable.setColumnCount(1)
            for word in suggestions:
                newRow = self.trTable.rowCount()+1
                currentRow = newRow-1
                self.trTable.setRowCount(newRow)
                self.trTable.setItem(currentRow,0, QtWidgets.QTableWidgetItem(word))
                self.trTable.item(currentRow,0).setBackground((QtGui.QColor(dR[0],dR[1],dR[2])))
            self.trTable.cellDoubleClicked.connect(self.reTranslateTreng)

        else:
            for i in range(0, len(wordTr)):
                if self.trTable.rowCount() == 0:
                    self.trTable.setRowCount(self.trTable.rowCount() + 1)
                    tempRow = self.trTable.rowCount() - 1
                    self.trTable.setSpan(tempRow, 0, 1, 2)
                    self.trTable.setItem(tempRow, 0, QtWidgets.QTableWidgetItem(wordTr[i][1]))
                    self.trTable.item(tempRow,0).setBackground((QtGui.QColor(dR[0],dR[1],dR[2])))

                    self.trTable.setRowCount(self.trTable.rowCount() + 1)
                    tempRow = self.trTable.rowCount() - 1
                    self.trTable.setItem(tempRow, 0, QtWidgets.QTableWidgetItem(wordTr[i][2]))
                    self.trTable.setItem(tempRow, 1, QtWidgets.QTableWidgetItem(wordTr[i][3]))
                    self.trTable.item(tempRow,0).setBackground((QtGui.QColor(lR[0],lR[1],lR[2])))
                    self.trTable.item(tempRow,1).setBackground((QtGui.QColor(lR[0],lR[1],lR[2])))

                elif wordTr[i][1] == wordTr[i - 1][1]:
                    self.trTable.setRowCount(self.trTable.rowCount() + 1)
                    tempRow = self.trTable.rowCount() - 1
                    self.trTable.setItem(tempRow, 0, QtWidgets.QTableWidgetItem(wordTr[i][2]))
                    self.trTable.setItem(tempRow, 1, QtWidgets.QTableWidgetItem(wordTr[i][3]))
                    self.trTable.item(tempRow,0).setBackground((QtGui.QColor(lR[0],lR[1],lR[2])))
                    self.trTable.item(tempRow,1).setBackground((QtGui.QColor(lR[0],lR[1],lR[2])))

                elif wordTr[i][1] != wordTr[i - 1][1]:
                    self.trTable.setRowCount(self.trTable.rowCount() + 1)
                    tempRow = self.trTable.rowCount() - 1
                    self.trTable.setSpan(tempRow, 0, 1, 2)
                    self.trTable.setItem(tempRow, 0, QtWidgets.QTableWidgetItem(wordTr[i][1]))
                    self.trTable.item(tempRow,0).setBackground((QtGui.QColor(dR[0],dR[1],dR[2])))

                    self.trTable.setRowCount(self.trTable.rowCount() + 1)
                    tempRow = self.trTable.rowCount() - 1
                    self.trTable.setItem(tempRow, 0, QtWidgets.QTableWidgetItem(wordTr[i][2]))
                    self.trTable.setItem(tempRow, 1, QtWidgets.QTableWidgetItem(wordTr[i][3]))
                    self.trTable.item(tempRow,0).setBackground((QtGui.QColor(lR[0],lR[1],lR[2])))
                    self.trTable.item(tempRow,1).setBackground((QtGui.QColor(lR[0],lR[1],lR[2])))
            self.trTable.cellDoubleClicked.connect(self.reTranslateTreng)

        #########################################################
        ################ CAMBRIDGE WORKSPACE ####################
        #########################################################
        if self.cmLayout.count()>0:
            self.cmTable.setColumnCount(1)
            self.cmTable.setRowCount(0)
        
        else:          
            self.cmTable = QtWidgets.QTableWidget(self.cmFrame)
            self.cmTable.setObjectName("cmTable")            
            self.cmLayout.addWidget(self.cmTable)
            self.cmTable.setColumnCount(1)
            self.cmTable.setRowCount(0)
            self.cmTable.setSelectionMode(0)
            self.cmTable.setFocusPolicy(0)
            self.cmTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
            self.cmTable.verticalHeader().setVisible(False)
            self.cmTable.horizontalHeader().setVisible(False)
            self.cmTable.horizontalHeader().setStretchLastSection(True)

        try:
            self.cmTable.cellDoubleClicked.disconnect()
        except:
            pass

        if wordCm==False: #check result is suggestions
            suggestions = cambridge.getSuggestions(unknown)
            for word in suggestions:
                newRow = self.cmTable.rowCount()+1
                currentRow = newRow-1
                self.cmTable.setRowCount(newRow)
                self.cmTable.setItem(currentRow,0, QtWidgets.QTableWidgetItem(word))
                self.cmTable.item(currentRow,0).setBackground((QtGui.QColor(dR[0],dR[1],dR[2])))
            self.cmTable.cellDoubleClicked.connect(self.reTranslateCamb)

        else:
            # write meanings to table
            for sentence in wordCm.keys():
                newRow = self.cmTable.rowCount()+1
                currentRow = newRow-1
                self.cmTable.setRowCount(newRow)

                # alternative word wrapper with changing row height
                if len(sentence) > 38:
                    rowHeight = ((len(sentence)//38)+1)*24
                    self.cmTable.setRowHeight(currentRow, rowHeight)
                    
                self.cmTable.setItem(currentRow,0, QtWidgets.QTableWidgetItem(sentence))
                self.cmTable.item(currentRow,0).setBackground((QtGui.QColor(dR[0],dR[1],dR[2])))

                # write examples to table
                for example in wordCm[sentence]:
                    newRow = self.cmTable.rowCount() + 1
                    currentRow = newRow-1
                    self.cmTable.setRowCount(newRow)
                    
                    ## alternative word wrapper with changing row height
                    if len(example) > 38:
                        rowHeight = ((len(example)//38)+1)*24
                        self.cmTable.setRowHeight(currentRow, rowHeight)

                    self.cmTable.setItem(currentRow,0, QtWidgets.QTableWidgetItem(example))
                    self.cmTable.item(currentRow,0).setBackground((QtGui.QColor(lR[0],lR[1],lR[2])))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    appUI = dictionary()
    appUI.show()
    sys.exit(app.exec_())