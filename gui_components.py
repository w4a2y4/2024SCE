from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def TitleLabel(text):
    label = QLabel(text)
    font = QFont()
    font.setBold(True)
    font.setPointSize(20)
    label.setFont(font)
    return label

def SeperatorLine():
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    return line