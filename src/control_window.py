import multiprocessing
import multiprocessing.connection
from event_system import Event
import sys
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QListWidget, QPushButton, QInputDialog, QDialog, QLabel, QLineEdit, QVBoxLayout, QComboBox, QMessageBox, QListWidgetItem
from event_system import EventSystem
from igs_math import Vector2


class ObjectDialog(QDialog):

    def __init__(self, conn: multiprocessing.connection.Connection):
        super().__init__()
        self.__conn = conn
        label = QLabel('Create new object:')
        self.obj_coords_input = QLineEdit()
        self.obj_coords_input.setPlaceholderText('Object coordinates')
        self.obj_name = QLineEdit()
        self.obj_name.setPlaceholderText('Object name')

        ok_button = QPushButton('OK')
        cancel_button = QPushButton('Cancel')
        ok_button.clicked.connect(self.createObject)
        cancel_button.clicked.connect(self.reject)

        self.obj_type = QComboBox()
        self.obj_type.addItem("Point")
        self.obj_type.addItem("Line")
        self.obj_type.addItem("Polygon")

        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(self.obj_type)
        layout.addWidget(self.obj_name)
        layout.addWidget(self.obj_coords_input)
        layout.addWidget(ok_button)
        layout.addWidget(cancel_button)

    def createObject(self):
        obj_type = self.obj_type.currentText()

        coords: str = self.obj_coords_input.text()
        coords.split(',')
        match obj_type:
            case 'Line':
                pass
            case 'Polygon':
                pass
            case 'Point':
                pass

        self.accept()


class ControlWindow(QMainWindow):

    def poll_conn(self):
        if self.__conn.poll():
            message = self.__conn.recv()
            match message[0]:
                case Event.DRAWABLE_ADDED:
                    item = QListWidgetItem(str(message[1].name))
                    item.setData(1, message[1])
                    self.list_widget.addItem(item)
                case Event.DRAWABLE_REMOVED:
                    for i in range(self.list_widget.count()):
                        if self.list_widget.item(i).data(1) == message[1]:
                            self.list_widget.takeItem(i)
                            return

    def __init__(self, conn: multiprocessing.connection.Connection):
        super().__init__()
        self.__conn = conn
        self.setWindowTitle("List Widget Example")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)  # type: ignore
        self.setFixedSize(200, 600)
        self.resize(200, 600)
        main_widget = QWidget(self)
        grid = QGridLayout(main_widget)
        self.setCentralWidget(main_widget)

        self.list_widget = QListWidget()
        self.conn_poll_timer = QTimer()
        self.conn_poll_timer.start()
        self.conn_poll_timer.timeout.connect(self.poll_conn)
        remove_button = QPushButton('remove', self)
        remove_button.clicked.connect(self.remove_item)

        first_row = QWidget(self)
        first_row_layout = QGridLayout(first_row)
        first_row_layout.addWidget(self.list_widget, 0, 0)
        first_row_layout.addWidget(remove_button, 1, 0)

        second_row = QWidget(self)
        second_row_layout = QGridLayout(second_row)
        button_zoom_in = QPushButton('+', self)
        button_movew_up = QPushButton('UP', self)
        button_zoom_out = QPushButton('-', self)
        button_movew_left = QPushButton('LEFT', self)
        button_movew_right = QPushButton('RIGHT', self)
        button_movew_down = QPushButton('DOWN', self)

        button_zoom_in.clicked.connect(
            lambda: self.__conn.send((Event.ZOOM_WINDOW, Vector2(125, 125))))
        button_zoom_out.clicked.connect(
            lambda: self.__conn.send((Event.ZOOM_WINDOW, Vector2(-125, -125))))
        button_movew_up.clicked.connect(
            lambda: self.__conn.send((Event.MOVE_WINDOW, Vector2(0, 100)))
        )
        button_movew_down.clicked.connect(
            lambda: self.__conn.send((Event.MOVE_WINDOW, Vector2(0, -100)))
        )
        button_movew_left.clicked.connect(
            lambda: self.__conn.send((Event.MOVE_WINDOW, Vector2(-100, 0)))
        )
        button_movew_right.clicked.connect(
            lambda: self.__conn.send((Event.MOVE_WINDOW, Vector2(100, 0)))
        )

        second_row_layout.addWidget(button_zoom_in, 0, 0)
        second_row_layout.addWidget(button_movew_up, 0, 1)
        second_row_layout.addWidget(button_zoom_out, 0, 2)
        second_row_layout.addWidget(button_movew_left, 1, 0)
        second_row_layout.addWidget(button_movew_right, 1, 2)
        second_row_layout.addWidget(button_movew_down, 2, 1)

        third_row = QWidget(self)
        third_row_layout = QGridLayout(third_row)

        add_obj_button = QPushButton('add object', self)
        add_obj_button.clicked.connect(self.add_item)
        third_row_layout.addWidget(add_obj_button, 0, 0)

        grid.addWidget(first_row, 0, 0)
        grid.addWidget(second_row, 1, 0)
        grid.addWidget(third_row, 2, 0)

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
        ObjectDialog(self.__conn).exec()

    def remove_item(self):
        if self.list_widget.count() == 0 or self.list_widget.currentItem() == None:
            return
        selectedItem: QListWidgetItem = self.list_widget.currentItem()
        self.__conn.send((Event.REMOVE_DRAWALBE, selectedItem.data(1)))


def create_control_window(conn: multiprocessing.connection.Connection):
    app = QApplication(sys.argv)
    control_window = ControlWindow(conn)
    control_window.show()
    app.exec()
