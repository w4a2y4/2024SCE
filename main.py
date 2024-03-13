from sic_framework.devices import Nao
from sic_framework.devices.common_naoqi.naoqi_text_to_speech import NaoqiTextToSpeechRequest
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QPushButton, QWidget, QGridLayout, QLineEdit

from buttons import *
import sys

ROBOT_EXIST = False

class NaoController():
    def __init__(self, nao):
        self.nao = nao

    def tts(self, text):
        if self.nao != None:
            self.nao.tts.request(NaoqiTextToSpeechRequest(text, pitch_shift=1.0, volume=1.5, speed=50), block=False)
        print(f"**SPEAKING** {text}")
        return

class MainWindow(QMainWindow):
    def __init__(self, listener):
        super().__init__()

        self.listener = listener
        self.n_times_clicked = 0

        layout = QGridLayout()
        # predefined btns
        # TODO: better layout for easier flow control
        for kvp in BUTTONS:
            (k, v) = kvp
            btn = QPushButton(k)
            btn.setProperty("msg", v)
            btn.clicked.connect(self.onClick)
            layout.addWidget(btn)
        
        # input box
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280,40)
        layout.addWidget(self.textbox)
        go_btn = QPushButton("GO")
        go_btn.clicked.connect(self.sendText)
        layout.addWidget(go_btn)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def onClick(self):
        widget = self.sender()
        msg = widget.property("msg")
        self.listener(msg)

    def sendText(self):
        self.listener(self.textbox.text())
        self.textbox.setText("")


if __name__ == "__main__":
    # connect to robot    
    controller = NaoController(Nao(ip='192.168.0.151') if ROBOT_EXIST else None)

    # start gui
    app = QApplication(sys.argv)
    window = MainWindow(controller.tts)
    window.show()

    app.exec()





