from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# 크롬 옵션 설정
chrome_options = Options()
chrome_options.add_argument('--headless')  # 브라우저 안 띄우고 실행
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# 크롬 드라이버 경로 설정
driver = webdriver.Chrome(options=chrome_options)

# 포켓몬고 뉴스 페이지 접속
driver.get("https://pokemongo.com/news?hl=ko")

# 이벤트 항목 찾기
events = driver.find_elements(By.CSS_SELECTOR, "div.NewsList-content-block a")

for event in events:
    title = event.text
    link = event.get_attribute('href')
    print(f"제목: {title}")
    print(f"링크: {link}")
    print("="*50)

# 브라우저 종료
driver.quit()
