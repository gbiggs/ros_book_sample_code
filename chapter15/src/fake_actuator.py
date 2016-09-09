#!/usr/bin/env python

from PySide.QtCore import Qt
from PySide.QtGui import QApplication, QVBoxLayout, QPushButton, QSlider, \
                         QDial, QGroupBox
import sys
import threading


class ActualFakeActuator(object):
    def __init__(self, callback=None):
        self.callback = callback

        self.app = QApplication(sys.argv)

        self.vlayout = QVBoxLayout()

        self.button = QPushButton('light')
        self.button.pressed.connect(self._button_callback)
        self.button.setCheckable(True)
        self.button.setChecked(True)
        self.button.setStyleSheet('background-color: white')
        self.vlayout.addWidget(self.button)

        self.slider = QSlider()
        self.slider.setOrientation(Qt.Horizontal)
        self.vlayout.addWidget(self.slider)

        self.dial = QDial()
        self.dial.setNotchesVisible(True)
        self.dial.setWrapping(True)
        self.vlayout.addWidget(self.dial)

        self.quit = QPushButton('Quit')
        self.quit.clicked.connect(self.app.quit)
        self.vlayout.addWidget(self.quit)

        self.group = QGroupBox('Fake Actuator')
        self.group.setLayout(self.vlayout)

    def _button_callback(self):
        if self.button.isChecked():
            self.button.setStyleSheet('background-color: red')
        else:
            self.button.setStyleSheet('background-color: white')

    def light_on(self):
        return self.button.isChecked()

    def toggle_light(self, on):
        self.button.setChecked(on)

    def volume(self):
        return self.slider.value()

    def set_volume(self, value):
        self.slider.setValue(value)

    def position(self):
        return self.dial.value()

    def set_position(self, value):
        self.dial.setValue(value)

    def run(self):
        self.group.show()
        self.app.exec_()


class FakeActuator(object):
    def __init__(self):
        thread = threading.Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def run(self):
        self.actuator = ActualFakeActuator()
        self.actuator.run()

    @property
    def light_on(self):
        return self.actuator.light_on()

    def toggle_light(self, on):
        return self.actuator.toggle_light(on)

    @property
    def volume(self):
        return self.actuator.volume()

    @volume.setter
    def volume(self, value):
        self.actuator.set_volume(value)

    @property
    def position(self):
        return self.actuator.position()

    def set_position(self, value):
        return self.actuator.set_position(value)


if __name__ == '__main__':
    a = FakeActuator()
    a.run()
