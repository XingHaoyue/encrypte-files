from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton,
                             QTextEdit, QVBoxLayout, QHBoxLayout, QFileDialog)
from cryptography.hazmat.primitives import serialization

from key import *
import os
import chardet

class DecipheringBar(QWidget):
    def __init__(self, parent=None):
        super(DecipheringBar, self).__init__(parent)

        self.label1 = QLabel("请选择解密文件：")
        self.file = QTextEdit()
        self.select1 = QPushButton("选择文件")
        self.label2 = QLabel("请选择密钥文件：")
        self.key = QTextEdit()
        self.select2 = QPushButton("选择文件")
        self.tip = QTextEdit()
        self.begin = QPushButton("开始解密")

        self.index = None

        self.setlay()
        self.init()

    def setlay(self):
        lay1 = QHBoxLayout()
        lay1.addWidget(self.file)
        lay1.addWidget(self.select1)

        lay2 = QHBoxLayout()
        lay2.addWidget(self.key)
        lay2.addWidget(self.select2)

        layout = QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addLayout(lay1)
        layout.addWidget(self.label2)
        layout.addLayout(lay2)
        layout.addWidget(self.tip)
        layout.addWidget(self.begin)

        self.setLayout(layout)

    def init(self):
        self.file.setReadOnly(True)
        self.key.setReadOnly(True)
        self.select1.clicked.connect(self.get_file)
        self.select2.clicked.connect(self.get_key)
        self.begin.clicked.connect(self.begin_deciphering)

    def get_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "选择文件", "",
                                                  "All Files (*)", options=options)
        if fileName:
            self.file.setText(fileName)
            self.file_path = fileName
            self.filename = os.path.basename(fileName)

    def get_key(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "选择文件", "",
                                                  "*.dat", options=options)
        if fileName:
            self.key.setText(fileName)
            self.key_path = fileName
        try:
            self.index = AllMethods.generate_method(fileName)
        except:
            self.key.setText("密钥文件不合法！")


    def begin_deciphering(self):
        if self.index == 0:
            try:
                res = AllMethods.aes_decrypt(self.key_path, self.file_path)
                with open(f"de_{self.filename}", 'wb') as f:
                    f.write(res)
                self.tip.append("AES解密成功！")
                self.tip.append("解密文件已保存！")
            except:
                self.tip.setText("解密失败！")

        elif self.index == 1:
            try:
                res = AllMethods.ecc_decrypt(self.key_path, self.file_path)
                with open(f"de_{self.filename}", 'wb') as f:
                    f.write(res)
                self.tip.append("ECC解密成功！")
                self.tip.append("解密文件已保存！")
            except:
                self.tip.setText("解密失败！")

        else:
            self.tip.setText("请选择密钥文件！")
