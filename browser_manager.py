from playwright.sync_api import sync_playwright
import time
from playwright.sync_api import Error

class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.pages = {}
        self.initialize_browser()

    def initialize_browser(self):
        try:
            # Playwright 초기화
            self.playwright = sync_playwright().start()
            
            # 브라우저 설정
            self.browser = self.playwright.chromium.launch(
                headless=False,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-infobars",
                    "--disable-dev-shm-usage",
                    "--disable-extensions",
                    "--disable-gpu",
                    "--disable-software-rasterizer",
                    "--disable-notifications",
                    "--disable-popup-blocking",
                    "--disable-features=IsolateOrigins,site-per-process"
                ]
            )
            
            # 브라우저 컨텍스트 설정
            self.context = self.browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                ignore_https_errors=True
            )
            
            # AI 플랫폼 URL 설정
            ai_platforms = {
                'ChatGPT': 'https://chat.openai.com',
                'Grok': 'https://grok.com/chat',
                'Claude': 'https://claude.ai'
            }
            
            # 각 AI 플랫폼에 대해 새 페이지 열기
            for name, url in ai_platforms.items():
                try:
                    page = self.context.new_page()
                    page.goto(url, wait_until="networkidle", timeout=30000)
                    self.pages[name] = page
                    print(f"{name} 페이지 열기 완료")
                    
                    # Claude의 경우 인증 페이지 처리
                    if name == 'Claude':
                        self.handle_claude_auth(page)
                except Error as e:
                    print(f"{name} 페이지 열기 실패: {str(e)}")
                    continue
            
        except Exception as e:
            print(f"브라우저 초기화 실패: {str(e)}")
            self.close_all()

    def handle_claude_auth(self, page):
        """Claude의 보안 인증 페이지를 자동으로 처리합니다."""
        try:
            # 인증 페이지가 로드될 때까지 대기
            page.wait_for_selector(".challenge-box", timeout=20000)
            
            # 인증을 자동으로 진행
            # 1. 쿠키 수락하기
            try:
                accept_button = page.query_selector("#accept-cookies")
                if accept_button:
                    accept_button.click()
                    time.sleep(1)  # 클릭 후 대기
            except:
                pass
            
            # 2. 보안 인증을 자동으로 진행
            # 클로드의 보안 인증 메커니즘 분석
            try:
                # 보안 인증 요소 찾기
                auth_elements = page.query_selector_all("input[type='text'], input[type='password']")
                if auth_elements:
                    # 임시로 텍스트 입력 시도
                    for element in auth_elements:
                        try:
                            element.fill("test")
                            time.sleep(0.5)
                        except:
                            continue
                
                # 제출 버튼 클릭 시도
                submit_buttons = page.query_selector_all("button[type='submit'], input[type='submit']")
                if submit_buttons:
                    for button in submit_buttons:
                        try:
                            button.click()
                            time.sleep(1)
                        except:
                            continue
            except:
                pass
            
            # 추가 대기
            time.sleep(5)  # 보안 인증 페이지가 로드될 시간을 기다림
            
        except Exception as e:
            print(f"Claude 인증 처리 실패: {str(e)}")
            return False
        return True

    def send_prompt_to_all(self, prompt):
        """모든 AI 플랫폼에 프롬프트를 전송합니다."""
        try:
            # 각 페이지에 프롬프트 전송
            for name, page in self.pages.items():
                print(f"{name} 페이지에 프롬프트 전송 중...")
                
                # 페이지가 로드될 때까지 대기
                page.wait_for_load_state("networkidle")
                
                # 각 AI 플랫폼에 맞는 프롬프트 입력 방법 구현
                if name == 'ChatGPT':
                    try:
                        # ChatGPT의 입력 필드 찾기
                        input_field = page.query_selector("textarea")
                        if input_field:
                            input_field.fill(prompt)
                            time.sleep(1)
                            # 전송 버튼 클릭
                            send_button = page.query_selector("button[type='submit']")
                            if send_button:
                                send_button.click()
                    except:
                        print(f"{name} 프롬프트 전송 실패")
                        continue
                
                elif name == 'Grok':
                    try:
                        # Grok의 입력 필드 찾기
                        input_field = page.query_selector("textarea")
                        if input_field:
                            input_field.fill(prompt)
                            time.sleep(1)
                            # 전송 버튼 클릭
                            send_button = page.query_selector("button[type='submit']")
                            if send_button:
                                send_button.click()
                    except:
                        print(f"{name} 프롬프트 전송 실패")
                        continue
                
                elif name == 'Claude':
                    try:
                        # Claude의 입력 필드 찾기
                        input_field = page.query_selector("textarea")
                        if input_field:
                            input_field.fill(prompt)
                            time.sleep(1)
                            # 전송 버튼 클릭
                            send_button = page.query_selector("button[type='submit']")
                            if send_button:
                                send_button.click()
                    except:
                        print(f"{name} 프롬프트 전송 실패")
                        continue
                
                # 응답 대기
                time.sleep(5)
                
        except Exception as e:
            print(f"프롬프트 전송 실패: {str(e)}")
            return False
        return True

    def close_all(self):
        """브라우저를 종료합니다."""
        if self.browser:
            try:
                # 모든 페이지 닫기
                for page in self.pages.values():
                    page.close()
                
                # 브라우저 종료
                self.browser.close()
                self.playwright.stop()
                print("브라우저 종료 완료")
            except Exception as e:
                print(f"브라우저 종료 실패: {str(e)}")
