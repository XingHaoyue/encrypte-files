import sys

from PyQt5.QtWidgets import QApplication

from pycheck import *
from pydeciphering import *
from pyencryption import *


class Main(QTabWidget):
    def __init__(self):
        super().__init__()

        self.en = EncryptionBar()
        self.de = DecipheringBar()
        self.check = CheckBar()

        self.addTab(self.en, "加密")
        self.addTab(self.de, "解密")
        self.addTab(self.check, "检查")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = Main()
    window.show()
    sys.exit(app.exec_())
