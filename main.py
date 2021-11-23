import sqlite3
import sys

import PyQt5
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.pushButton.clicked.connect(self.table_get_data)
        self.table_get_data()
    
    def table_get_data(self):
        allcoffies = {}
        conn = sqlite3.connect('coffee.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coffee")
        rows = cursor.fetchall()
        for i in rows:
            coffee_name = i[1]
            coffee_price = i[5]
            coffee_id = i[0]
            coffee_roast = cursor.execute("SELECT name FROM roast WHERE id = ?", (i[2],)).fetchone()[0]
            coffee_hammering = cursor.execute("SELECT name FROM hammering WHERE id = ?", (i[3],)).fetchone()[0]
            coffee_taste = i[4]
            allcoffies[coffee_id] = [coffee_name, coffee_price, coffee_roast, coffee_hammering, coffee_taste]
        cursor.close()
        conn.close()
        model_for_table = PyQt5.QtGui.QStandardItemModel(self.tableView)
        model_for_table.setHorizontalHeaderLabels(['Название', 'Цена', 'Прожарка', 'Молотость', 'Вкус'])
        for i in allcoffies:
            model_for_table.appendRow([PyQt5.QtGui.QStandardItem(allcoffies[i][0]), PyQt5.QtGui.QStandardItem(str(allcoffies[i][1])), PyQt5.QtGui.QStandardItem(allcoffies[i][2]), PyQt5.QtGui.QStandardItem(allcoffies[i][3]), PyQt5.QtGui.QStandardItem(allcoffies[i][4])])
        self.tableView.setModel(model_for_table)
        self.tableView.resizeColumnsToContents()
        self.tableView.resizeRowsToContents()
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setEditTriggers(PyQt5.QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView.setColumnWidth(0, 200)
        self.tableView.setColumnWidth(1, 200)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())