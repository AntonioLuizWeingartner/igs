import multiprocessing
import multiprocessing.connection
from event_system import Event
import sys
from PyQt5.QtCore import (
    Qt,
    QThread,
    pyqtSignal,
    QTimer,
)
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
    QListWidget,
    QPushButton,
    QInputDialog,
    QDialog,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QComboBox,
    QMessageBox,
    QListWidgetItem,
    QTextEdit,
    QRadioButton,
)
from event_system import EventSystem
from igs_math import Vector2
from drawable import (
    ScaleParameters,
    TranslateParameters,
    RotateParameters,
    DrawableObject,
    Rotation,
)


class ManageObjectWindow(QMainWindow):

    def __init__(self, obj: QListWidgetItem, conn: multiprocessing.connection.Connection):
        super().__init__()
        self.__object = obj
        self.__conn = conn
        self.setWindowTitle("Object Manager")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setFixedSize(400, 500)
        self.resize(200, 600)
        main_widget = QWidget(self)
        grid = QGridLayout(main_widget)
        self.setCentralWidget(main_widget)

        self.__rotation = Rotation.FROM_CENTER_OF_WORLD
        first_row = QWidget(self)
        rotation_label = QLabel('Rotação')
        self.rotate_from_center = QRadioButton(
            'Rotacionar em torno do centro do mundo', self)
        self.rotate_from_center.clicked.connect(self.switch_rotation)
        self.rotate_from_object = QRadioButton(
            'Rotacionar em torno do centro do objeto', self)
        self.rotate_from_object.clicked.connect(self.switch_rotation)
        self.rotate_from_point = QRadioButton(
            'Rotacionar em torno de um ponto qualquer', self)
        self.rotate_from_point.clicked.connect(self.switch_rotation)
        angle_label = QLabel('Ângulo: ')
        self.angle_input = QTextEdit('')
        rotate_x_label = QLabel('X:')
        self.rotate_x_input = QTextEdit('')
        rotate_y_label = QLabel('Y:')
        self.rotate_y_input = QTextEdit('')
        rotation_button = QPushButton('Rotacionar', self)
        rotation_button.clicked.connect(self.rotate_obj)
        first_row_layout = QGridLayout(first_row)
        first_row_layout.addWidget(rotation_label, 0, 0, 1, 2)
        first_row_layout.addWidget(self.rotate_from_center, 1, 0, 1, 2)
        first_row_layout.addWidget(self.rotate_from_object, 2, 0, 1, 2)
        first_row_layout.addWidget(self.rotate_from_point, 3, 0, 1, 2)
        first_row_layout.addWidget(angle_label, 4, 0)
        first_row_layout.addWidget(self.angle_input, 4, 1)
        first_row_layout.addWidget(rotate_x_label, 5, 0)
        first_row_layout.addWidget(self.rotate_x_input, 5, 1)
        first_row_layout.addWidget(rotate_y_label, 6, 0)
        first_row_layout.addWidget(self.rotate_y_input, 6, 1)
        first_row_layout.addWidget(rotation_button, 7, 0, 1, 2)

        second_row = QWidget(self)
        translation_label = QLabel('Translação')
        translation_x_label = QLabel('X:')
        self.translation_x_input = QTextEdit('')
        translation_y_label = QLabel('Y:')
        self.translation_y_input = QTextEdit('')
        translation_button = QPushButton('Translacionar', self)
        translation_button.clicked.connect(self.translate_obj)
        second_row_layout = QGridLayout(second_row)
        second_row_layout.addWidget(translation_label, 0, 0, 1, 2)
        second_row_layout.addWidget(translation_x_label, 1, 0)
        second_row_layout.addWidget(self.translation_x_input, 1, 1)
        second_row_layout.addWidget(translation_y_label, 2, 0)
        second_row_layout.addWidget(self.translation_y_input, 2, 1)
        second_row_layout.addWidget(translation_button, 3, 0, 1, 2)

        third_row = QWidget(self)
        scaling_label = QLabel('Escalanomento')
        scaling_x_value_label = QLabel('X:')
        self.scaling_x_value_input = QTextEdit('')
        scaling_y_value_label = QLabel('Y:')
        self.scaling_y_value_input = QTextEdit('')
        scaling_button = QPushButton('Escalar', self)
        scaling_button.clicked.connect(self.scale_obj)
        third_row_layout = QGridLayout(third_row)
        third_row_layout.addWidget(scaling_label, 0, 0, 1, 2)
        third_row_layout.addWidget(scaling_x_value_label, 1, 0)
        third_row_layout.addWidget(self.scaling_x_value_input, 1, 1)
        third_row_layout.addWidget(scaling_y_value_label, 2, 0)
        third_row_layout.addWidget(self.scaling_y_value_input, 2, 1)
        third_row_layout.addWidget(scaling_button, 3, 0, 1, 2)

        grid.addWidget(first_row, 0, 0, 2, 1)
        grid.addWidget(second_row, 2, 0)
        grid.addWidget(third_row, 3, 0)

    def scale_obj(self):
        try:
            x = int(self.scaling_x_value_input.toPlainText())
            y = int(self.scaling_y_value_input.toPlainText())
            obj: DrawableObject = self.__object.data(1)
            self.__conn.send(
                (Event.DRAWABLE_SCALED, ScaleParameters(obj, x, y)))
        except:
            print('No value given')

    def translate_obj(self):
        try:
            x = int(self.translation_x_input.toPlainText())
            y = int(self.translation_y_input.toPlainText())
            obj: DrawableObject = self.__object.data(1)
            self.__conn.send((Event.DRAWABLE_TRANSLATED,
                              TranslateParameters(obj, x, y)))
        except:
            print('No value given')

    def rotate_obj(self):
        try:
            angle = int(self.angle_input.toPlainText())
        except:
            print('No value given')
            return
        obj: DrawableObject = self.__object.data(1)
        try:
            x = int(self.rotate_x_input.toPlainText())
            y = int(self.rotate_y.input.toPlainText())
        except:
            x = 0
            y = 0
        self.__conn.send(
            (Event.DRAWABLE_ROTATED, RotateParameters(obj, angle, self.__rotation, x, y)))

    def switch_rotation(self):
        if self.rotate_from_center.isChecked():
            self.__rotation = Rotation.FROM_CENTER_OF_WORLD
        if self.rotate_from_object.isChecked():
            self.__rotation = Rotation.FROM_CENTER_OF_OBJECT
        if self.rotate_from_point.isChecked():
            self.__rotation = Rotation.FROM_ARBITRARY_POINT

    def add_item(self):
        message_box = QMessageBox()
        message_box.setWindowTitle("Information")
        message_box.setText(
            "Not implemented yet. Click on the main window to add a new object, use F1 to change object type.\
                \n You can also use the WASD keys to move around and +- to zoom \
                \n in order to draw a wireframe/polygon you must place at least 3 points and ctrl+click")
        message_box.setIcon(QMessageBox.Information)
        message_box.exec()
        return

    def remove_item(self):
        pass


def create_control_window(conn: multiprocessing.connection.Connection):
    app = QApplication(sys.argv)
    control_window = ControlWindow(conn)
    control_window.show()
    app.exec()
