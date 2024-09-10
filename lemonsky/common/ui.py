from typing import Tuple

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


MESSAGEBOX_TYPE = Tuple[str, int]


class NewMessageBox(QMessageBox):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)

    def setup_ui(self, title: str, text: str, button0: MESSAGEBOX_TYPE = None, button1: MESSAGEBOX_TYPE = None):
        self.setWindowTitle(title)
        self.setText(text)

        if button0:
            self.addButton(*button0)
        else:
            self.addButton(QMessageBox.Ok)

        if button1:
            self.addButton(*button1)

    def information(self, title: str, text: str, button0: MESSAGEBOX_TYPE = None, button1: MESSAGEBOX_TYPE = None):
        self.setIcon(QMessageBox.Icon.Information)
        self.setup_ui(title, text, button0=button0, button1=button1)
        return self.exec_()

    def warning(self, title: str, text: str, button0: MESSAGEBOX_TYPE = None, button1: MESSAGEBOX_TYPE = None):
        self.setIcon(QMessageBox.Icon.Warning)
        self.setup_ui(title, text, button0=button0, button1=button1)
        return self.exec_()

    def critical(self, title: str, text: str, button0: MESSAGEBOX_TYPE = None, button1: MESSAGEBOX_TYPE = None):
        self.setIcon(QMessageBox.Icon.Critical)
        self.setup_ui(title, text, button0=button0, button1=button1)
        return self.exec_()

    def question(self, title: str, text: str, button0: MESSAGEBOX_TYPE = None, button1: MESSAGEBOX_TYPE = None):
        self.setIcon(QMessageBox.Icon.Question)
        self.setup_ui(title, text, button0=button0, button1=button1)
        return self.exec_()
