import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QWaitCondition
from PyQt5.QtCore import QMutex
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
import encrypt

class Thread(QThread):
    change_value = pyqtSignal(int)

    def __init__(self):
        QThread.__init__(self)
        self.cond = QWaitCondition()
        self.mutex = QMutex()
        self.cnt = 0
        self._status = True
    
    def __del__(self):
        self.wait()

    def run(self):
        while True:
            self.mutex.lock()

            if not self._status:
                self.cond.wait(self.mutex)

            if 100 == self.cnt:
                self.cnt = 0
            self.cnt += 1
            self.change_value.emit(self.cnt)
            self.msleep(100)  # ※주의 QThread에서 제공하는 sleep을 사용

            self.mutex.unlock()
    
    def toggle_status(self):
        self._status = not self._status
        if self._status:
            self.cond.wakeAll()

    @property
    def status(self):
        return self._status

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.filepath = ''
        self.th = Thread()
        self.initUI()
        self.th.start()

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

        # 프로그레스 바
        self.pbar = QProgressBar(self)
        self.pbar.setValue(0)
        self.th.change_value.connect(self.pbar.setValue)

        # 암호화 일시 중지 버튼
        self.pauseBtn = QPushButton("Pause")
        self.pauseBtn.clicked.connect(self.pause_button)

        layout = QVBoxLayout()
        layout.addWidget(self.loadBtn)
        layout.addWidget(self.label)
        layout.addWidget(self.passwordInput)
        layout.addWidget(self.encryptBtn)
        layout.addWidget(self.pbar)
        layout.addWidget(self.pauseBtn)

        self.setWindowTitle('PDF Encrypter')
        self.move(300, 300)
        self.resize(400, 200)
        self.setLayout(layout)
        self.show()
    
    def loadFile(self):
        try:
            fname = QFileDialog.getOpenFileName(self)
            self.filepath = fname[0]

            size = os.path.getsize(fname[0])
            filename = os.path.basename(fname[0])

            print('name:' + filename)
            print('size:' + str(size))

            self.label.setText(self.filepath)
        except os.error:
            print("Load File Error")
    
    def encryptFile(self):
        password = self.passwordInput.text()

        if self.filepath.strip() == '':
            QMessageBox.critical(self, 'Message', '파일을 불러오세요', QMessageBox.Yes, QMessageBox.Yes)
            return
        elif password.strip() == '':
            QMessageBox.critical(self, 'Message', '패스워드를 입력해주세요', QMessageBox.Yes, QMessageBox.Yes)
            return 

        encrypt.Encrypt.do(self.filepath, password)

    @pyqtSlot()
    def pause_button(self):
        """
        사용자정의 슬롯
        쓰레드의 status 상태 변경
        버튼 문자 변경
        쓰레드 재시작
        """
        self.th.toggle_status()
        self.pauseBtn.setText({True: "Pause", False: "Resume"}[self.th.status])

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())

