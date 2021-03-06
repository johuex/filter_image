from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog
import form
import time
import numpy as np
import cv2  # для чтение bmp файлов
import matplotlib.pyplot as plt


class MainApp(form.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.image = 0  # исходное изображение
        self.foutname = ""  # путь к фин изо
        self.foutname_2 = ""
        self.final_image = 0  # обработанное изображение
        self.y = 0  # ось вниз
        self.x = 0  # ось вправо
        self.core_size = 0
        self.pushButton.pressed.connect(self.select_image)  # выбрать изображение
        self.pushButton_2.pressed.connect(self.filter)  # начать обработку изображения
        self.pushButton_3.pressed.connect(self.section_graph)  # разрез функции яркости по строке
        self.pushButton_4.pressed.connect(self.brightness)

    def select_image(self):
        """
        выбор изображения пользователем
        :return:
        """
        fname, temp = QFileDialog.getOpenFileName(self, "Open File", "", "Image files (*bmp *jpg)") # путь до картинки
        self.image = cv2.imread(fname, 0)  # матричное представление изображения в ndarray
        self.image = self.image.astype(object)
        self.y, self.x = self.image.shape  # размер картинки
        self.label_9.setText(str(self.x))
        self.label_10.setText(str(self.y))
        image = QtGui.QPixmap(QtGui.QImage(fname, format=None,))  # открываем картинку
        self.original_im.setPixmap(image)  # помещаем картинку в QLabel

    def filter(self):
        """
        выбор фильтра
        :return:
        """
        if type(self.image) is np.ndarray:
            self.final_image = 0
            start = time.time()
            self.core_size = int(self.lineEdit.text())
            self.final_image = np.zeros((self.y, self.x), dtype=object)
            # self.final_image = self.image
            if self.comboBox.currentIndex() == 0:
                '''среднегеометрический'''
                if self.comboBox_2.currentIndex() == 0:
                    self.geometry_filter1()
                    type_filter = "_1x_geom"
                elif self.comboBox_2.currentIndex() == 1:
                    self.geometry_filter2()
                    type_filter = "_2x_geom"
            elif self.comboBox.currentIndex() == 1:
                '''среднегармонический'''
                if self.comboBox_2.currentIndex() == 0:
                    self.garmony_filter1()
                    type_filter = "_1x_garm"
                if self.comboBox_2.currentIndex() == 1:
                    self.garmony_filter2()
                    type_filter = "_2x_garmo"

        finish = time.time()
        self.foutname = type_filter + "_filtered" + ".bmp"
        self.final_image = self.final_image.astype(np.uint8)
        cv2.imwrite(self.foutname, self.final_image)
        image = QtGui.QPixmap(QtGui.QImage(self.foutname, format=None, ))  # открываем картинку
        self.changed_im.setPixmap(image)  # помещаем картинку в QLabel
        self.label_20.setText(str(finish - start))

    def geometry_filter2(self):
        """
        двумерный среднегеометрический фильтр
        :return:
        """
        core = np.zeros((self.core_size, self.core_size), dtype=object)  # ядро
        for i in range(self.core_size//2, self.y - self.core_size//2):
            for j in range(self.core_size//2, self.x - self.core_size//2):
                core = self.image[i-self.core_size//2:i+self.core_size//2+1, j-self.core_size//2:j+self.core_size//2+1]
                core = np.where(core == 0, core + 1, core)
                self.final_image[i, j] = int(np.prod(core) ** (1 / (self.core_size*self.core_size)))

    def geometry_filter1(self):
        """
        одномерный среднегеометрический фильтр
        :return:
        """
        core = np.zeros(self.core_size, dtype=object)  # маска, заполненная нулями
        # np.prod - перемножение всех элементов маски
        for i in range(self.y):
            for j in range(self.core_size//2, self.x - self.core_size//2):  # проход по строкам
                core = self.image[i, j-self.core_size//2:j+self.core_size//2+1]
                core = np.where(core == 0, core + 1, core)
                self.final_image[i, j] = int(np.prod(core) ** (1 / (self.core_size)))

        for i in range(self.x):
            for j in range(self.core_size//2, self.y - self.core_size//2):  # проход по столбцам
                core = self.final_image[j-self.core_size//2:j+self.core_size//2+1, i]
                core = np.where(core == 0, core + 1, core)
                self.final_image[j, i] = int(np.prod(core) ** (1 / (self.core_size)))



    def garmony_filter2(self):
        """
        двумерный среднегармонический фильтр
        :return:
        """
        core = np.zeros((self.core_size, self.core_size), dtype=object)  # ядро
        for i in range(self.core_size // 2, self.y - self.core_size // 2):
            for j in range(self.core_size // 2, self.x - self.core_size // 2):
                core = self.image[i - self.core_size // 2:i + self.core_size // 2 + 1, j - self.core_size // 2:j + self.core_size // 2 + 1]
                core = np.where(core == 0, core + 1, core)
                self.final_image[i, j] = int((self.core_size**2) / (np.sum(1/core)))

    def garmony_filter1(self):
        """
        одномерный среднегармонический фильтр
        :return:
        """
        core = np.zeros(self.core_size, dtype=object)  # маска, заполненная нулями
        # np.prod - перемножение всех элементов маски
        for i in range(self.y):
            for j in range(self.core_size // 2, self.x - self.core_size // 2):  # проход по строкам
                core = self.image[i, j - self.core_size // 2:j + self.core_size // 2 + 1]
                core = np.where(core == 0, core + 1, core)
                self.final_image[i, j] = int((self.core_size) / (np.sum(1/core)))

        for i in range(self.x):
            for j in range(self.core_size // 2, self.y - self.core_size // 2):  # проход по столбцам
                core = self.final_image[j - self.core_size // 2:j + self.core_size // 2 + 1, i]
                core = np.where(core == 0, core + 1, core)
                self.final_image[j, i] = int((self.core_size) / (np.sum(1/core)))


    def section_graph(self):
        """показать разрез функции яркости для n-ой строки"""
        if (type(self.final_image) is np.ndarray):
            plt.subplot(221)
            plt.hist(self.image, color=['blue']*self.x, histtype='stepfilled')
            plt.title("Гистограмма яркости исходного")
            plt.subplot(222)
            plt.hist(self.final_image, color=['blue']*self.x, histtype='stepfilled')
            plt.title("    и обработанного изображения")

            y = self.image[int(self.lineEdit_4.text()), :]  # яркости в строке
            x = np.arange(0, self.x, 1)
            plt.subplot(223)
            plt.plot(x, y)
            plt.title("Разрез функции яркости ")
            plt.xlabel("Пиксель")
            plt.ylabel("Яркость")
            plt.subplot(224)
            y = self.final_image[int(self.lineEdit_4.text()), :]
            plt.plot(x, y)
            plt.title(" по {} строке".format(self.lineEdit_4.text()))
            plt.xlabel("Пиксель")
            plt.ylabel("Яркость")
            plt.show()
            cv2.imread(self.foutname)
            self.foutname_2 =  "line_for_graph.bmp"
            self.final_image = cv2.line(self.final_image, (0, int(self.lineEdit_4.text())), (self.x, int(self.lineEdit_4.text())), (255, 255, 255), 1)
            cv2.imwrite(self.foutname_2, self.final_image)
            image = QtGui.QPixmap(QtGui.QImage(self.foutname_2, format=None, ))  # открываем картинку
            self.changed_im.setPixmap(image)  # помещаем картинку в QLabel

    def brightness(self):
        self.label_16.setText(str(self.image[int(self.lineEdit_2.text()), int(self.lineEdit_3.text())]))
        self.label_17.setText(str(self.final_image[int(self.lineEdit_2.text()), int(self.lineEdit_3.text())]))


app = QtWidgets.QApplication([])
window = MainApp()
window.show()
app.exec_()
