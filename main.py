from sic_framework.devices import Nao
from sic_framework.devices.common_naoqi.naoqi_text_to_speech import NaoqiTextToSpeechRequest
from sic_framework.devices.common_naoqi.naoqi_motion_recorder import PlayRecording, NaoqiMotionRecording
from sic_framework.devices.common_naoqi.naoqi_stiffness import Stiffness
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys
from openai import OpenAI

from transcript import *
from gui_components import *
from ch1 import ch1
from ch2 import ch2

ROBOT_EXIST = False
IP = '192.168.1.103'

class Controller():
    def __init__(self, nao, gpt_client):
        self.nao = nao
        self.gpt_client = gpt_client
        self.chain = ["RArm"]
        self.wave_motion = NaoqiMotionRecording.load("wave.motion")

    def tts(self, text):
        print(f"** SPEAKING ** {text}")
        if self.nao == None:
            return
        self.nao.tts.request(\
            NaoqiTextToSpeechRequest(text, pitch_shift=1.0, volume=1.5, speed=100), block=False)
        return
    
    def askGpt(self, prompt):
        response = self.gpt_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYS_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )
        # print(f"** GPT Response ** {response}")
        self.tts(response.choices[0].message.content)
        return
    
    def flipTablet(self):
        print("** ARM MOTION **")
        if self.nao == None:
            return
        # play pre-recorded motions
        self.nao.stiffness.request(Stiffness(.95, self.chain))
        self.nao.motion_record.request(PlayRecording(self.wave_motion))
        self.nao.stiffness.request(Stiffness(.0, self.chain))
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
        layout.addWidget(self.setTtsBtn(FIRST_GREETING))
        layout.addWidget(self.setTtsBtn(START_READ))
        layout.addWidget(HorizontalSeperatorLine())
        layout.addWidget(QLabel("2nd time"))
        layout.addWidget(self.setTtsBtn(SECOND_GREETING))
        layout.addWidget(self.setTtsBtn(CH1_SHORT_SUMMARY))
        layout.addWidget(self.setTtsBtn(CH1_LONG_SUMMARY))
        layout.addWidget(self.setTtsBtn(CONTINUE_READ))
        layout.addStretch()
        return layout
    
    def _readingLayout(self):
        layout = QVBoxLayout()
        layout.addWidget(TitleLabel("Phase 2: Reading"))
        layout.addWidget(QLabel("Robot reads"))
        layout.addLayout(self._chapterContents(ch1))
        layout.addLayout(self._chapterContents(ch2))
        layout.addWidget(HorizontalSeperatorLine())
        layout.addWidget(QLabel("Ask in-between questions"))
        layout.addLayout(self._inBetweenQuestions(ch1))
        layout.addLayout(self._inBetweenQuestions(ch2))
        layout.addWidget(HorizontalSeperatorLine())
        layout.addWidget(QLabel("Answer random questions"))
        layout.addWidget(self.setTtsBtn(DEFAULT_ANSWER))
        layout.addStretch()
        return layout
    
    def _chapterContents(self, chapter):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(chapter.title))
        layout.addWidget(self.setTtsBtn(CH1_FULL_TEXT))
        for i, p in enumerate(chapter.paragraphs):
            layout.addWidget(self.setTtsBtn((f"P{str(i)}", p)))
        return layout
    
    def _inBetweenQuestions(self, chapter):
        layout = QVBoxLayout()
        questions = QHBoxLayout()
        questions.addWidget(QLabel(f"{chapter.title} - Q"))
        answers = QHBoxLayout()
        answers.addWidget(QLabel(f"{chapter.title} - A"))
        for i, qa in enumerate(chapter.questions):
            questions.addWidget(self.setTtsBtn((str(i), qa[0])))
            answers.addWidget(self.setTtsBtn((str(i), qa[1])))
        layout.addLayout(questions)
        layout.addLayout(answers)
        return layout
    
    def _farewellLayout(self):
        layout = QVBoxLayout()
        layout.addWidget(TitleLabel("Phase 3: Farewell & Feedback"))
        layout.addWidget(self.setTtsBtn(END_SESSION))
        layout.addWidget(self.setTtsBtn(FEEDBACK_PAGE))
        layout.addWidget(self.setTtsBtn(FEEDBACK_QUESTIONS))
        layout.addWidget(self.setTtsBtn(FAREWELL))
        # append motion layout
        layout.addWidget(HorizontalSeperatorLine())
        layout.addLayout(self._motionLayout())
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
    
    def _motionLayout(self):
        layout = QVBoxLayout()
        layout.addWidget(TitleLabel("Recorded motions"))
        flip_btn = QPushButton("FLIP TABLET")
        flip_btn.clicked.connect(self.controller.flipTablet)
        layout.addWidget(flip_btn)
        return layout

    def setTtsBtn(self, kvp: tuple):
        (k, v) = kvp
        btn = QPushButton(k)
        btn.setProperty("msg", v)
        btn.clicked.connect(self.tts)
        return btn

    def tts(self):
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
    controller = Controller(Nao(ip=IP) if ROBOT_EXIST else None, gpt_client)

    # start gui
    app = QApplication(sys.argv)
    window = MainWindow(controller)
    window.show()

    app.exec()