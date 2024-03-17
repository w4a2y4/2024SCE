from sic_framework.devices import Nao
from sic_framework.devices.common_naoqi.naoqi_text_to_speech import NaoqiTextToSpeechRequest
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys
from openai import OpenAI

from transcript import *
from gui_components import *
from ch1 import ch1
from ch2 import ch2

ROBOT_EXIST = False

class Controller():
    def __init__(self, nao, gpt_client):
        self.nao = nao
        self.gpt_client = gpt_client

    def tts(self, text):
        if self.nao != None:
            self.nao.tts.request(NaoqiTextToSpeechRequest(text, pitch_shift=1.0, volume=1.5, speed=50), block=False)
        print(f"** SPEAKING ** {text}")
        return
    
    def askGpt(self, prompt):
        response = self.gpt_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYS_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )
        print(f"** GPT Response ** {response}")
        self.tts(response.choices[0].message.content)
        return

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller

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
        root.addLayout(self._askGPTLayout())

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
        go_btn = QPushButton("SAY IT")
        go_btn.clicked.connect(self.sendText)
        layout.addWidget(go_btn)
        return layout
    
    def _askGPTLayout(self):
        layout = QHBoxLayout()
        self.gptBox = QLineEdit(self)
        self.gptBox.move(20, 20)
        self.gptBox.resize(280,40)
        layout.addWidget(self.gptBox)
        ask_btn = QPushButton("ASK GPT")
        ask_btn.clicked.connect(self.askGpt)
        layout.addWidget(ask_btn)
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
        self.controller.tts(msg)

    def sendText(self):
        self.controller.tts(self.textbox.text())
        self.textbox.setText("")
    
    def askGpt(self):
        self.controller.askGpt(self.gptBox.text())
        self.gptBox.setText("")


if __name__ == "__main__":

    # setup gpt
    gpt_client = OpenAI()

     # connect to robot
    controller = Controller(Nao(ip='192.168.0.151') if ROBOT_EXIST else None, gpt_client)

    # start gui
    app = QApplication(sys.argv)
    window = MainWindow(controller)
    window.show()

    app.exec()