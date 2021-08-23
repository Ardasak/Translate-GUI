from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import sys
import os
import wx
from wx.core import GetClientDisplayRect, MenuEvent
import textblob
class UI_Window(QWidget):
    def __init__(self, parent=None):
        super(UI_Window, self).__init__(parent)
        self.init()
        self.state = None
        self.diller = {
            "German": "de",
            "Turkish": "tr",
            "English": "en",
            "French": "fr",
            "Italian": "it",
            "Japanese": "ja",
            "Dutch": "nl",
            "Spanish": "es",
            "Chinese": "zh",
            "Korean": "ko",
        }
        app = wx.App(False)
        
        self.width, self.height = wx.GetDisplaySize()
        self.setGeometry(
            round((self.width / 2) - 600), round((self.height / 2) - 300), 1200, 600
        )

    def init(self):
        self.liste = [
            "--- Choose ---",
            "German",
            "Turkish",
            "English",
            "French",
            "Italian",
            "Japanese",
            "Dutch",
            "Spanish",
            "Chinese",
            "Korean",
        ]
        self.to_combobox = QComboBox()
        self.to_combobox.addItems(self.liste)
        self.to_combobox.currentIndexChanged.connect(self.on_to_combobox_changed)
        self.from_combobox = QComboBox()
        self.from_combobox.addItems(self.liste)
        self.from_combobox.currentIndexChanged.connect(self.on_from_combobox_changed)
        self.to_textarea = QTextEdit()
        self.to_textarea.setReadOnly(True)
        self.from_textarea = QTextEdit()
        self.translate_button = QPushButton("Translate")
        self.translate_button.clicked.connect(self.translate)
        self.switch_button = QPushButton("Switch")
        self.switch_button.clicked.connect(self.switch)
        self.h_box = QHBoxLayout()

        self.setLayout(self.h_box)
        self.yerlesim()
        self.show()

    def on_from_combobox_changed(self):
        self.from_dil = self.diller.get(self.from_combobox.currentText())
        if self.state!=1:
            self.from_textarea.clear()
        

    def on_to_combobox_changed(self):
        self.to_dil = self.diller.get(self.to_combobox.currentText())
        if self.state!=1:
            self.to_textarea.clear()
        
    def translate(self):
        message_box = QMessageBox()
        if(self.to_combobox.currentText()!="--- Choose ---" and self.from_combobox.currentText()!="--- Choose ---"):
            try:
                mytext=textblob.TextBlob(self.from_textarea.toPlainText())
                translated = mytext.translate(from_lang=self.from_dil,to=self.to_dil)
                self.to_textarea.setText(str(translated))
            except textblob.exceptions.NotTranslated:
                message_box.setText("An error occured while translating.")
                message_box.setWindowTitle("Warning!")
                message_box.setIcon(QMessageBox.Warning)
                if(self.from_textarea.toPlainText()==""):
                    message_box.setText("You can't leave the text area empty.")
                else:
                    message_box.setDetailedText("Make sure you chose both languages correctly, the program will occur an error if you write something in Japanese but choose Spanish. Try again!")
                message_box.exec()
        else:
            message_box.setText("Please choose both of the languages.")
            message_box.setWindowTitle("Warning!")
            message_box.setIcon(QMessageBox.Warning)
            message_box.exec()
    def switch(self):
        self.state=1
        if(self.to_combobox.currentText()!=self.from_combobox.currentText()):
            gecici = self.from_combobox.currentText()
            self.from_combobox.setCurrentText(self.to_combobox.currentText())
            self.to_combobox.setCurrentText(gecici)
            gecici = self.from_textarea.toPlainText()
            self.from_textarea.setText(self.to_textarea.toPlainText())
            self.to_textarea.setText(gecici)
        self.state=0
    def yerlesim(self):

        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.from_combobox)
        self.v_layout.addWidget(self.from_textarea)
        self.v_layout1 = QVBoxLayout()
        self.v_layout.addWidget(self.to_combobox)
        self.v_layout.addWidget(self.to_textarea)
        self.v_layout2 = QVBoxLayout()
        self.v_layout2.addStretch()
        self.v_layout2.addWidget(self.switch_button)
        self.v_layout2.addWidget(self.translate_button)
        self.v_layout2.addStretch()
        self.h_box1 = QHBoxLayout()
        self.h_box1.addLayout(self.v_layout)
        self.h_box1.addLayout(self.v_layout1)
        self.h_box1.addLayout(self.v_layout2)
        self.main_v_box = QVBoxLayout()
        self.main_v_box.addLayout(self.h_box1)
        self.h_box.addLayout(self.main_v_box)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = UI_Window()
    sys.exit(app.exec_())
