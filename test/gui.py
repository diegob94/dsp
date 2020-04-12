import sys

from PySide2.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QSlider, QHBoxLayout, QSizePolicy
from PySide2.QtCore import Slot, Qt
from PySide2.QtGui import QPalette

from packetlib import Packet

class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.button = QPushButton("Send")
        self.layout = QVBoxLayout()
        self.layout.addWidget(SliderGroup())
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        # Connecting the signal
        self.button.clicked.connect(self.magic)
        self.packet = Packet('packet.yaml')
    @Slot()
    def magic(self):
        for slider in self.findChildren(Slider):
            slider_name = slider.objectName()
            slider_value = slider.slider.sliderPosition()
            setattr(self.packet, slider_name, slider_value)
        for i in self.packet.stream:
            print(f"send: 0x{i:X}")
        print()

class SliderGroup(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.layout = QHBoxLayout()
        self.layout.addWidget(Slider("val1", 0, 256 - 1))
        self.layout.addWidget(Slider("val2", -1000, 1000))
        #self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

class Slider(QWidget):
    def __init__(self, name, min_value, max_value):
        QWidget.__init__(self)
        self.setObjectName(name)
        self.slider = QSlider(Qt.Orientation.Vertical)
        self.slider.setMaximum(max_value)
        self.slider.setMinimum(min_value)
        self.label = QLabel(name)
        self.label.setAlignment(Qt.AlignCenter)
        min_width = self.label.fontMetrics().boundingRect(str(min_value)).width()
        max_width = self.label.fontMetrics().boundingRect(str(max_value)).width()
        minimum_width = max(min_width, max_width)
        self.value = QLabel(self.to_string(min_value))
        self.value.setAlignment(Qt.AlignCenter)
        self.value.setMinimumWidth(minimum_width)
        self.value.setText(self.to_string(self.slider.sliderPosition()))
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.slider, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.value, alignment=Qt.AlignHCenter)
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)
        self.slider.valueChanged.connect(self.callback)
    def callback(self, value):
        self.value.setText(self.to_string(value))
    def to_string(self, value):
        return f"{value}"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    #app.setStyleSheet("QLabel { background-color: yellow }");
    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()
    sys.exit(app.exec_())
