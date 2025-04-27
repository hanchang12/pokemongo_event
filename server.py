from flask import Flask
import requests
from bs4 import BeautifulSoup
import schedule
import threading
import time

app = Flask(__name__)

# IFTTT Webhook URL 입력 (IFTTT 설정할 때 받을 것)
IFTTT_WEBHOOK_URL = "https://maker.ifttt.com/trigger/pokemon_event_alert/with/key/dNtG45LvB4JL5nkREYOaXy"

# 포켓몬고 이벤트 크롤링
def crawl_pokemon_events():
    print("[INFO] 포켓몬고 뉴스 크롤링 시작")
    
    url = "https://pokemongo.com/news?hl=ko"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.find_all('div', class_='article-card')[:5]
    if not articles:
        print("[WARN] 뉴스 기사 없음")
        return

    message = "[포켓몬고 이벤트]\n\n"
    for article in articles:
        title = article.find('h2').text.strip()
        link = article.find('a')['href']
        full_link = f"https://pokemongo.com{link}"
        message += f"✅ {title}\n🔗 {full_link}\n\n"

    send_to_ifttt(message)

# IFTTT로 메시지 보내기
def send_to_ifttt(text):
    payload = {
        "value1": text
    }
    response = requests.post(IFTTT_WEBHOOK_URL, json=payload)
    print(f"[INFO] IFTTT 호출 결과: {response.status_code}")

# 매일 크롤링 스케줄
def run_schedule():
    schedule.every().day.at("10:00").do(crawl_pokemon_events)
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route("/")
def home():
    return "포켓몬고 이벤트 서버 정상 작동 중!"

@app.route("/test")
def manual_test():
    crawl_pokemon_events()
    return "포켓몬고 이벤트 수동 호출 완료!"

if __name__ == "__main__":
    t = threading.Thread(target=run_schedule)
    t.start()
    app.run(host="0.0.0.0", port=8000)
