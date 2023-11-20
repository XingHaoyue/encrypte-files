from PyQt5.QtWidgets import QWidget, QLabel, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog
from key import AllMethods

class CheckBar(QWidget):
    def __init__(self, parent=None):
        super(CheckBar, self).__init__(parent)

        self.label1 = QLabel("请选择原始文件：")
        self.file1 = QTextEdit()
        self.select1 = QPushButton("选择文件")
        self.select1.clicked.connect(self.generate_file1)

        self.label2 = QLabel("请选择解密文件：")
        self.file2 = QTextEdit()
        self.select2 = QPushButton("选择文件")
        self.select2.clicked.connect(self.generate_file2)

        self.resout = QTextEdit()
        self.check = QPushButton("检查")
        self.check.clicked.connect(self.check_file)

        self.file_path1 = None
        self.file_path2 = None

        self.HASH1 = None
        self.HASH2 = None

        self.setlay()

    def setlay(self):
        lay1 = QHBoxLayout()
        lay1.addWidget(self.file1)
        lay1.addWidget(self.select1)

        lay2 = QHBoxLayout()
        lay2.addWidget(self.file2)
        lay2.addWidget(self.select2)

        layout = QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addLayout(lay1)
        layout.addWidget(self.label2)
        layout.addLayout(lay2)
        layout.addWidget(self.resout)
        layout.addWidget(self.check)

        self.setLayout(layout)

    def generate_file1(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "All Files (*)", options=options)
        if fileName:
            self.file1.setText(fileName)
            self.file_path1 = fileName
            self.HASH1 = AllMethods.get_file_hash(self.file_path1)
            self.file1.append("文件哈希值为：")
            self.file1.append(self.HASH1)
    def generate_file2(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "All Files (*)", options=options)
        if fileName:
            self.file2.setText(fileName)
            self.file_path2 = fileName
            self.HASH2 = AllMethods.get_file_hash(self.file_path2)
            self.file2.append("文件哈希值为：")
            self.file2.append(self.HASH2)

    def check_file(self):
        if self.HASH1 == self.HASH2:
            self.resout.setText("文件完整")
        else:
            self.resout.setText("文件已被篡改")
