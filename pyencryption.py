from PyQt5.QtWidgets import (QWidget, QTabWidget, QLabel, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QFileDialog)

from key import *


class EncryptionBar(QWidget):
    def __init__(self, parent=None):
        super(EncryptionBar, self).__init__(parent)

        self.label1 = QLabel("请选择加密文件：")
        self.file = QTextEdit()
        self.select = QPushButton("选择文件")
        self.label2 = QLabel("请选择加密方式：")
        self.method = Encryption()
        self.create = QPushButton("生成")
        self.clear = QPushButton("清空")
        self.tip = QTextEdit()
        self.begin = QPushButton("开始加密")
        self.file_path = None

        self.setlay()
        self.init()

    def setlay(self):
        lay1 = QHBoxLayout()
        lay1.addWidget(self.file)
        lay1.addWidget(self.select)

        lay2 = QHBoxLayout()
        lay2.addWidget(self.create)
        lay2.addWidget(self.clear)

        layout = QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addLayout(lay1)
        layout.addWidget(self.label2)
        layout.addWidget(self.method)
        layout.addLayout(lay2)
        layout.addWidget(self.tip)
        layout.addWidget(self.begin)

        self.setLayout(layout)

    def init(self):
        self.file.setReadOnly(True)
        self.select.clicked.connect(self.generate_file)
        self.create.clicked.connect(self.create_key)
        self.clear.clicked.connect(self.clear_all)
        self.begin.clicked.connect(self.begin_encrypte)

    def generate_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "All Files (*)", options=options)
        if fileName:
            self.file.setText(fileName)
            self.file_path = fileName
            self.filename = os.path.basename(fileName)

    def generate_method(self):
        return self.method.currentIndex()


    def create_key(self):
        index = self.generate_method()
        if index == 0:
            self.method.aes.text.append("正在生成密钥...")
            try:
                self.method.aes.key = AllMethods.gen_aes_key()
                self.method.aes.text.append(self.method.aes.key.hex())
            except:
                self.methon.ase.text.append("密钥生成失败！")
        elif index == 1:
            self.method.ecc.text1.append("正在生成公钥...")
            self.method.ecc.text2.append("正在生成私钥...")
            try:
                self.method.ecc.pu_key, self.method.ecc.pr_key = AllMethods.gen_ecc_key()
                temp1 = self.method.ecc.pu_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                            format=serialization.PublicFormat.SubjectPublicKeyInfo)
                temp2 = self.method.ecc.pr_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                             format=serialization.PrivateFormat.PKCS8,
                                                             encryption_algorithm=serialization.NoEncryption())
                self.method.ecc.text1.append(temp1.decode('utf-8'))
                self.method.ecc.text2.append(temp2.decode('utf-8'))
            except:
                self.method.ecc.text2("公钥生成失败！")
                self.method.ecc.text2("密钥生成失败！")

    def clear_all(self):
        self.method.aes.text.clear()
        self.method.ecc.text1.clear()
        self.method.ecc.text2.clear()
        self.tip.clear()

    def begin_encrypte(self):
        index = self.generate_method()
        self.tip.append("正在加密...")
        if index == 0:
            try:
                iv, ciphertext = AllMethods.aes_encrypt(self.method.aes.key, self.file_path)
                with open(f"key_of_{os.path.splitext(self.filename)[0]}.dat", 'wb') as f:
                    f.write("AES".encode())
                    f.writelines([b'\n', base64.b64encode(self.method.aes.key), b'\n', base64.b64encode(iv)])

                with open(f"en_{self.filename}", 'wb') as f:
                    f.write(ciphertext)
                self.tip.append("AES加密成功！")
            except:
                self.tip.append("AES加密失败！")
        elif index == 1:
            try:
                encrypted_file = AllMethods.ecc_encrypt(self.method.ecc.pu_key, self.file_path)
                pem1 = self.method.ecc.pr_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
                pem2 = self.method.ecc.pu_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
                with open(f"key_of_{os.path.splitext(self.filename)[0]}.dat", 'wb') as f:
                    f.write("ECC".encode())
                    f.writelines([b'\n', pem1, pem2])
                with open(f"en_{self.filename}", 'wb') as f:
                    f.write(encrypted_file)
                self.tip.append("ECC加密成功！")
            except:
                self.tip.append("ECC加密失败！")
        else:
            pass


class Encryption(QTabWidget):
    def __init__(self, parent=None):
        super(Encryption, self).__init__(parent)

        self.aes = AES()
        self.ecc = ECC()

        self.addTab(self.aes, "AES")
        self.addTab(self.ecc, "ECC")


class AES(QWidget):
    def __init__(self, parent=None):
        super(AES, self).__init__(parent)

        self.label = QLabel("AES密钥：")
        self.text = QTextEdit()
        self.text.setReadOnly(True)
        self.key = None

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.text)

        self.setLayout(layout)

    def aes_key(self):
        return self.key


class ECC(QWidget):
    def __init__(self, parent=None):
        super(ECC, self).__init__(parent)

        self.label1 = QLabel("ECC公钥：")
        self.text1 = QTextEdit()
        self.text1.setReadOnly(True)
        self.label2 = QLabel("ECC私钥：")
        self.text2 = QTextEdit()
        self.text2.setReadOnly(True)
        self.pu_key = None
        self.pr_key = None

        layout = QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.text1)
        layout.addWidget(self.label2)
        layout.addWidget(self.text2)

        self.setLayout(layout)
