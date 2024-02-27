import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QAbstractTableModel, QVariant


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent):
        return len(self._data)

    def columnCount(self, parent):
        if self._data:
            return len(self._data[0])
        return 0

    def data(self, index, role):
        if not index.isValid():
            return QVariant()

        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._data[index.row()][index.column()])

        return QVariant()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TableView Example")

        # Crear datos de ejemplo
        data = [
            ["Name", "Age", "Gender"],
            ["John", "30", "Male"],
            ["Lisa", "25", "Female"],
            ["David", "40", "Male"]
        ]

        # Crear modelo de tabla y asignarlo a la vista de tabla
        self.model = TableModel(data)
        self.table_view = QTableView()
        self.table_view.setModel(self.model)

        # Configurar la vista de tabla
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.verticalHeader().setVisible(False)

        # Agregar la vista de tabla al diseño principal
        layout = QVBoxLayout()
        layout.addWidget(self.table_view)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
