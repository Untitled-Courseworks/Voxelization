import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtCore

from PyQt5.QtWidgets import QFileDialog
import MeshToVoxel
import ReadObj
from Visualization import get_model
from ConvertToFile import convert
from Visual_2_0 import ShowModel
import pygame

import WindowMenu.WinMenu as WM  # Это наш конвертированный файл дизайна


class ExampleApp(QtWidgets.QMainWindow, WM.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.current_file_path = ""
        self.result = None
        self.InitProgram()

    def closeEvent(self, *args, **kwargs):
        quit()

    def InitProgram(self):
        self.button_Save.setEnabled(False)
        self.button_Show.setEnabled(False)
        self.button_FileChoose.clicked.connect(self.FileChoose)
        self.button_Reset.clicked.connect(self.Reset)
        self.button_Show.clicked.connect(self.Show)
        self.button_Save.clicked.connect(self.Save)
        # self.button_Show.hide()  # Из-за наличия багов убрал

    def FileChoose(self):
        self.current_file_path = QFileDialog.getOpenFileName(self, "File Choose", "/home", "*.obj")[0]
        if self.current_file_path != "":
            self.label_FilePath.setText(self.current_file_path)
            self.button_Save.setEnabled(True)
            self.button_Show.setEnabled(True)
        else:
            self.label_FilePath.setText("Выберите файл типа *.obj")
            self.button_Save.setEnabled(False)
            self.button_Show.setEnabled(False)

    def Reset(self):
        self.doubleSpinBox_VoxelSize.setValue(1.000)
        self.label_FilePath.setText("")
        self.current_file_path = ""
        self.result = None
        self.button_Save.setEnabled(False)
        self.button_Show.setEnabled(False)
        self.button_FileChoose.setEnabled(True)

    def Save(self):
        file_name = QFileDialog.getSaveFileName(self, "File Save", "/", "*.pcd")[0]
        if file_name != "" and file_name is not None:
            self.Voxelization()
            convert(file_name, self.result, float(self.doubleSpinBox_VoxelSize.value()))

    def Show(self):
        self.Voxelization()
        ShowModel(self.result, float(self.doubleSpinBox_VoxelSize.value()), [[i[0] for i in self.model[1]], [i[1] for i in self.model[1]]], False)

    def Voxelization(self):
        self.model = ReadObj.read_file(self.current_file_path)
        self.result = MeshToVoxel.get_voxel_model(self.model[0], self.model[1], float(self.doubleSpinBox_VoxelSize.value()))
        self.button_FileChoose.setEnabled(False)


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
