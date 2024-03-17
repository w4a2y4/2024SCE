from sic_framework.devices import Nao
from sic_framework.devices.common_naoqi.naoqi_text_to_speech import NaoqiTextToSpeechRequest
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from transcript import *
from gui_components import *
import sys
from ch1 import ch1
from ch2 import ch2

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

        layout = QHBoxLayout()
        layout.addLayout(self._greetingsLayout())
        layout.addWidget(VerticalSeperatorLine())
        layout.addLayout(self._readingLayout())
        layout.addWidget(VerticalSeperatorLine())
        layout.addLayout(self._farewellLayout())

        root = QVBoxLayout()
        root.addLayout(layout)
        root.addWidget(HorizontalSeperatorLine())
        root.addLayout(self._freeInputLayout())

        widget = QWidget()
        widget.setLayout(root)
        self.setCentralWidget(widget)
    
    def _greetingsLayout(self):
        layout = QVBoxLayout()
        layout.addWidget(TitleLabel("Phase 1: Greetings"))
        layout.addWidget(QLabel("1st time"))
        layout.addWidget(self.setBtn(FIRST_GREETING))
        layout.addWidget(self.setBtn(START_READ))
        layout.addWidget(HorizontalSeperatorLine())
        layout.addWidget(QLabel("2nd time"))
        layout.addWidget(self.setBtn(SECOND_GREETING))
        layout.addWidget(self.setBtn(CH1_SHORT_SUMMARY))
        layout.addWidget(self.setBtn(CH1_LONG_SUMMARY))
        layout.addWidget(self.setBtn(CONTINUE_READ))
        layout.addStretch()
        return layout
    
    def _readingLayout(self):
        layout = QVBoxLayout()
        layout.addWidget(TitleLabel("Phase 2: Reading"))
        layout.addWidget(QLabel("robot reads"))
        layout.addWidget(self.setBtn(CH1_FULL_TEXT))
        layout.addWidget(self.setBtn(CH2_FULL_TEXT))
        layout.addWidget(HorizontalSeperatorLine())
        layout.addWidget(QLabel("ask in-between questions"))
        layout.addLayout(self._inBetweenQuestions(ch1))
        layout.addLayout(self._inBetweenQuestions(ch2))
        layout.addWidget(HorizontalSeperatorLine())
        layout.addWidget(QLabel("answer random questions"))
        layout.addWidget(self.setBtn(DEFAULT_ANSWER))
        layout.addStretch()
        return layout
    
    def _inBetweenQuestions(self, chapter):
        layout = QVBoxLayout()
        layout.addWidget(QLabel(chapter.title))
        questions = QHBoxLayout()
        questions.addWidget(QLabel("Q:"))
        answers = QHBoxLayout()
        answers.addWidget(QLabel("A:"))
        for i, qa in enumerate(chapter.questions):
            questions.addWidget(self.setBtn((str(i), qa[0])))
            answers.addWidget(self.setBtn((str(i), qa[1])))
        layout.addLayout(questions)
        layout.addLayout(answers)
        return layout
    
    def _farewellLayout(self):
        layout = QVBoxLayout()
        layout.addWidget(TitleLabel("Phase 3: Farewell & Feedback"))
        layout.addWidget(self.setBtn(END_SESSION))
        layout.addWidget(self.setBtn(FEEDBACK_PAGE))
        layout.addWidget(self.setBtn(FEEDBACK_QUESTIONS))
        layout.addWidget(self.setBtn(FAREWELL))
        layout.addStretch()
        return layout
    
    def _freeInputLayout(self):
        layout = QHBoxLayout()
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280,40)
        layout.addWidget(self.textbox)
        go_btn = QPushButton("GO")
        go_btn.clicked.connect(self.sendText)
        layout.addWidget(go_btn)
        return layout

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