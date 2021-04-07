import sys

from PyQt5 import QtGui, QtCore, uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication


class Toast(QMainWindow):
    """Auto-closing window"""

    def __init__(self, msg, timeout, parent=None):
        self.msg = msg
        self.timeout = timeout

        QMainWindow.__init__(self)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.X11BypassWindowManagerHint
        )
        self.setGeometry(
            QtWidgets.QStyle.alignedRect(
                QtCore.Qt.LeftToRight,
                QtCore.Qt.AlignCenter,
                QtCore.QSize(400, 100),
                QtWidgets.qApp.desktop().availableGeometry(),
            )
        )
        self.label = QtWidgets.QLabel(self.msg, self)
        self.label.move(150, 30)
        self.label.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.setWindowOpacity(0.8)
        self.setStyleSheet(
            f"background-color: #0A0E14; "
            f"color: #fff;"
            f"font-size: 30px;"
            f"text-align: center;"
        )

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.close)
        self._timer.start(self.timeout)

    def mousePressEvent(self, event):
        QtWidgets.qApp.quit()


def show_toast(msg, timeout=2000):
    app = QApplication(sys.argv)
    toast = Toast(msg, timeout)
    toast.show()
    app.exec_()
