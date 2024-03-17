from sic_framework.devices import Nao
from sic_framework.devices.common_naoqi.naoqi_text_to_speech import NaoqiTextToSpeechRequest
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from buttons import *
from gui_components import *
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
    def __init__(self, tts):
        super().__init__()

        self.tts = tts

        layout = QVBoxLayout()

        layout.addWidget(TitleLabel("Phase 1: Greetings"))
        layout.addLayout(self._greetingsLayout())
        layout.addWidget(SeperatorLine())

        layout.addWidget(TitleLabel("Phase 2: Reading"))
        layout.addLayout(self._readingLayout())
        layout.addWidget(SeperatorLine())
        
        layout.addWidget(TitleLabel("Phase 3: Farewell & Feedback"))
        layout.addLayout(self._farewellLayout())
        layout.addWidget(SeperatorLine())
        
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
    
    def _greetingsLayout(self):
        layout = QHBoxLayout()
        col1 = QVBoxLayout()
        col1.addWidget(QLabel("1st time"))
        col1.addWidget(self.setBtn(FIRST_GREETING))
        col1.addWidget(self.setBtn(START_READ))
        col1.addStretch()
        col2 = QVBoxLayout()
        col2.addWidget(QLabel("2nd time"))
        col2.addWidget(self.setBtn(SECOND_GREETING))
        col2.addWidget(self.setBtn(CH1_SHORT_SUMMARY))
        col2.addWidget(self.setBtn(CH1_LONG_SUMMARY))
        col2.addWidget(self.setBtn(CONTINUE_READ))
        col2.addStretch()
        layout.addLayout(col1)
        layout.addLayout(col2)
        return layout
    
    def _readingLayout(self):
        # TODO
        return QHBoxLayout()
    
    def _farewellLayout(self):
        # TODO
        return QHBoxLayout()

    def setBtn(self, kvp: tuple):
        (k, v) = kvp
        btn = QPushButton(k)
        btn.setProperty("msg", v)
        btn.clicked.connect(self.onClick)
        return btn

    def onClick(self):
        widget = self.sender()
        msg = widget.property("msg")
        self.tts(msg)

    def sendText(self):
        self.tts(self.textbox.text())
        self.textbox.setText("")


if __name__ == "__main__":
    # connect to robot
    controller = NaoController(Nao(ip='192.168.0.151') if ROBOT_EXIST else None)

    # start gui
    app = QApplication(sys.argv)
    window = MainWindow(controller.tts)
    window.show()

    app.exec()





