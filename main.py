from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog
import form


class MainApp(form.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.image = 0
        self.fname = ""
        self.final_image = 0
        self.pushButton.pressed.connect(self.select_image) # выбрать изображение
        self.pushButton_2.pressed.connect(self.filter)  # начать обработку изображения
        self.pushButton_3.pressed.connect(self.section_graph)  # разрез функции яркости по строке

    def select_image(self):
        """
        выбор изображения пользователем
        :return:
        """
        fname, temp = QFileDialog.getOpenFileName(self, "Open File", "", "Image files (*bmp)") # путь до картинки
        self.image = QtGui.QPixmap(QtGui.QImage(fname, format=None,))  # открываем картинку
        self.original_im.setPixmap(self.image)  # помещаем картинку в QLabel

    def filter(self):
        """
        выбор фильтра согласно выбору пользователя
        :return:
        """
        if self.radioButton_3:
            '''среднегеометрический'''
            if self.radioButton:
                '''одномерный'''
                type_filter = "_1x_geom"
            if self.radioButton_2:
                '''двумерный'''
                type_filter = "_2x_geom"
        if self.radioButton_4:
            '''среднегармонический'''
            if self.radioButton:
                '''одномерный'''
                type_filter = "_1x_garm"
            if self.radioButton_2:
                '''двумерный'''
                type_filter = "_2x_garmo"

        self.changed_im.pixmap().save(self.fname + type_filter + "_filtered")  # сохранить изображение
        self.image = QtGui.QPixmap(QtGui.QImage("/" + self.fname + type_filter + "_filtered", format=None, ))  # открываем картинку
        self.changed_im.setPixmap(self.image)  # помещаем картинку в QLabel

    def geometry_filter2(self):
        """
        двумерный среднегеометрический фильтр
        :return:
        """
        pass

    def geometry_filter1(self):
        """
        одномерный среднегеометрический фильтр
        :return:
        """
        pass

    def garmony_filter2(self):
        """
        двумерный среднегармонический фильтр
        :return:
        """
        pass

    def garmony_filter1(self):
        """
        одномерный среднегармонический фильтр
        :return:
        """
        pass

    def show_gist(self):
        """показать гистограмму яркости обработанного изображения"""
        pass

    def section_graph(self):
        """показать разрез функции яркости для n-ой строки"""
        pass


app = QtWidgets.QApplication([])
window = MainApp()
window.show()
app.exec_()
