import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from ui_file import Ui_MainWindow
import os


# Наследуемся от виджета из PyQt5.QtWidgets и от класса с интерфейсом
class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # Вызываем метод для загрузки интерфейса из класса Ui_MainWindow,
        # остальное без изменений
        self.setupUi(self)
        self.setGeometry(600, 600, 600, 600)
        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.run1)
        self.pushButton_3.clicked.connect(self.run2)

    def run(self):
        fullname = os.path.join('dist', "level1.exe")
        os.startfile(fullname)

    def run1(self):
        fullname = os.path.join('dist', "level2.exe")
        os.startfile(fullname)

    def run2(self):
        fullname = os.path.join('dist', "level3.exe")
        os.startfile(fullname)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())