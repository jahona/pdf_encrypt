import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QVBoxLayout, QLineEdit, QMessageBox
import encrypt

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 불러오기 버튼
        self.loadBtn = QPushButton('load', self)
        self.loadBtn.setCheckable(True)
        self.loadBtn.clicked.connect(self.loadFile)

        # 선택 파일 이름 출력
        self.label = QLabel()

        # 패스워드 입력 인풋
        self.passwordInput = QLineEdit(self)

        # 암호화 버튼
        self.encryptBtn = QPushButton('encrypt', self)
        self.encryptBtn.setCheckable(True)
        self.encryptBtn.clicked.connect(self.encryptFile)

        layout = QVBoxLayout()
        layout.addWidget(self.loadBtn)
        layout.addWidget(self.label)
        layout.addWidget(self.passwordInput)
        layout.addWidget(self.encryptBtn)

        self.setWindowTitle('PDF Encrypter')
        self.move(300, 300)
        self.resize(400, 200)
        self.setLayout(layout)
        self.show()
    
    def loadFile(self):
        fname = QFileDialog.getOpenFileName(self)
        print(fname[0])
        self.label.setText(fname[0])
    
    def encryptFile(self):
        password = self.passwordInput.text()
        filePath = self.label.text();

        if filePath.strip() == '':
            QMessageBox.critical(self, 'Message', '파일을 불러오세요', QMessageBox.Yes, QMessageBox.Yes)
        elif password.strip() == '':
            QMessageBox.critical(self, 'Message', '패스워드를 입력해주세요', QMessageBox.Yes, QMessageBox.Yes)

        print('encrypt')
        encrypt.Encrypt.do(filePath, password)

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())

