from flask import Flask
import requests
from bs4 import BeautifulSoup
import schedule
import threading
import time
import os

app = Flask(__name__)

# IFTTT Webhook URL 가져오기 (환경변수에서)
IFTTT_WEBHOOK_URL = os.getenv('IFTTT_WEBHOOK_URL')

# 포켓몬고 뉴스 크롤링 함수
def crawl_pokemon_events():
    print("[INFO] 포켓몬고 뉴스 크롤링 시작")
    url = "https://pokemongo.com/news?hl=ko"

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        articles = soup.find_all('div', class_='article-card')[:5]
        if not articles:
            print("[WARN] 크롤링 결과 없음")
            return

        message = "[포켓몬고 이벤트]\n\n"
        for article in articles:
            title = article.find('h2').text.strip()
            link = article.find('a')['href']
            full_link = f"https://pokemongo.com{link}"
            message += f"✅ {title}\n🔗 {full_link}\n\n"

        send_to_ifttt(message)

    except Exception as e:
        print(f"[ERROR] 크롤링 실패: {str(e)}")

# IFTTT Webhook 호출 함수 (디버깅 추가)
def send_to_ifttt(text):
    if not IFTTT_WEBHOOK_URL:
        print("[ERROR] IFTTT_WEBHOOK_URL 환경변수가 설정되지 않았습니다.")
        return

    payload = {
        "value1": text
    }
    print(f"[DEBUG] IFTTT로 전송할 Payload: {payload}")

    try:
        response = requests.post(IFTTT_WEBHOOK_URL, json=payload)
        print(f"[DEBUG] IFTTT 응답 코드: {response.status_code}")
        print(f"[DEBUG] IFTTT 응답 내용: {response.text}")
    except Exception as e:
        print(f"[ERROR] IFTTT 호출 실패: {str(e)}")

# 홈페이지 라우트
@app.route("/")
def home():
    return "포켓몬고 이벤트 서버 정상 작동 중!"

# 테스트용 수동 호출 라우트
@app.route("/test")
def manual_test():
    crawl_pokemon_events()
    return "포켓몬고 이벤트 수동 호출 완료!"

# 스케줄러 루프
def run_schedule():
    schedule.every().day.at("10:00").do(crawl_pokemon_events)
    while True:
        schedule.run_pending()
        time.sleep(1)

# 메인 서버 실행
if __name__ == "__main__":
    t = threading.Thread(target=run_schedule)
    t.start()
    app.run(host="0.0.0.0", port=8000)
