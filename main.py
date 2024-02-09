import sys
from typing import List

from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox

from design import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, *args, **kwargs) -> None:
        super(MainWindow, self).__init__(parent, *args, **kwargs)
        self.setupUi(self)

        canvas = QtGui.QPixmap(100, 100)
        canvas.fill(Qt.GlobalColor.white)
        self.label.setPixmap(canvas)
        self.last_x, self.last_y = None, None

        self.save_btn.triggered.connect(self.save)
        self.clear_btn.triggered.connect(self.clear)

    def mouseMoveEvent(self, e):
        if self.last_x is None:
            self.last_x = int(e.position().x())
            self.last_y = int(e.position().y())
            return

        canvas = self.label.pixmap()
        painter = QtGui.QPainter(canvas)
        painter.drawLine(self.last_x, self.last_y - 22, int(e.position().x()), int(e.position().y() - 22))
        painter.end()
        self.label.setPixmap(canvas)

        self.last_x = int(e.position().x())
        self.last_y = int(e.position().y())

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None

    def save(self) -> None:
        dlg = QMessageBox(self)

        try:
            canvas = self.label.pixmap()
            array = self.pixmap_to_array(canvas)

            with open('1.txt', 'w', encoding='utf-8') as file:
                file.write(''.join(array))

            dlg.setText("Успешно сохранено")
        except Exception as _:
            dlg.setText("Что-то пошло не так!")

        dlg.exec()

    @staticmethod
    def pixmap_to_array(canvas) -> List[str]:
        array: List[str] = []
        pixmap: QtGui.QImage = canvas.toImage()

        for y in range(100):
            for x in range(100):
                color = pixmap.pixel(x, y)

                if color == QtGui.QColor(255, 255, 255):
                    array.append('w')
                else:
                    array.append('b')

        return array

    def clear(self) -> None:
        canvas = self.label.pixmap()
        canvas.fill(Qt.GlobalColor.white)
        self.label.setPixmap(canvas)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
