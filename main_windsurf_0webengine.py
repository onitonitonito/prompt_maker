import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QTextEdit, QTabWidget)
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
import webbrowser

class MultiAIAssistant(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Multi-AI Assistant')
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create input area
        input_layout = QHBoxLayout()
        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText('프롬프트를 입력하세요...')
        self.send_button = QPushButton('모든 AI에 전송')
        self.send_button.clicked.connect(self.send_prompt_to_all)
        
        input_layout.addWidget(self.prompt_input)
        input_layout.addWidget(self.send_button)
        main_layout.addLayout(input_layout)
        
        # Create tab widget for AI platforms
        self.tab_widget = QTabWidget()
        self.ai_tabs = []
        
        # Add AI platforms in order
        ai_platforms = [
            ('ChatGPT', 'https://chat.openai.com'),
            ('Grok', 'https://grok.ai'),
            ('Copilot', 'https://copilot.github.com'),
            ('Claude', 'https://claude.ai'),
            ('Gemini', 'https://gemini.google.com')
        ]
        
        for name, url in ai_platforms:
            # Create a new profile for each tab
            profile = QWebEngineProfile.defaultProfile()
            profile.setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)
            
            tab = QWebEngineView()
            tab.page().profile().setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)
            tab.load(QUrl(url))
            self.tab_widget.addTab(tab, name)
            self.ai_tabs.append(tab)
        
        main_layout.addWidget(self.tab_widget)
        
    def send_prompt_to_all(self):
        prompt = self.prompt_input.toPlainText()
        if not prompt.strip():
            return
            
        # Send prompt to all AI platforms
        for tab in self.ai_tabs:
            # This is a placeholder - actual implementation will depend on each AI platform's API
            # For now, we'll just focus on the UI structure
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MultiAIAssistant()
    window.show()
    sys.exit(app.exec_())
