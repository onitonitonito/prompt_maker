import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QTextEdit, QTextBrowser, QTabWidget)
from PyQt5.QtCore import Qt
from browser_manager import BrowserManager

class AIAssistant(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AI Assistant Manager')
        self.setGeometry(300, 555, 900, 1200)
        
        # 브라우저 관리자 초기화
        self.browser_manager = BrowserManager()
        
        # 중앙 위젯과 메인 레이아웃 생성
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # 프롬프트 입력 영역
        input_layout = QHBoxLayout()
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText('프롬프트를 입력하세요...')
        self.send_button = QPushButton('모든 AI에 전송')
        self.send_button.clicked.connect(self.send_prompt)
        
        input_layout.addWidget(self.prompt_input)
        input_layout.addWidget(self.send_button)
        main_layout.addLayout(input_layout)
        
        # 응답 표시 영역
        self.response_browser = QTextBrowser()
        self.response_browser.setReadOnly(True)
        main_layout.addWidget(self.response_browser)
        
        # 상태 표시줄
        self.statusBar().showMessage('대기 중...')
        
    def send_prompt(self):
        prompt = self.prompt_input.toPlainText().strip()
        if not prompt:
            self.statusBar().showMessage('프롬프트를 입력하세요')
            return
            
        self.statusBar().showMessage('프롬프트 전송 중...')
        try:
            self.browser_manager.send_prompt_to_all(prompt)
            self.statusBar().showMessage('프롬프트 전송 완료')
            self.response_browser.append(f'입력한 프롬프트: {prompt}\n')
        except Exception as e:
            self.statusBar().showMessage(f'오류 발생: {str(e)}')

    def closeEvent(self, event):
        self.browser_manager.close_all()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AIAssistant()
    window.show()
    sys.exit(app.exec_())
