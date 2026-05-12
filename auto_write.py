import os
import time
import random
import datetime
import requests
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twocaptcha import TwoCaptcha

# ========================================================
# 🔑 개인 설정 정보 (API 키 입력 필수)
# ========================================================
# 1. 텔레그램 설정 (CHAT_ID는 적용 완료, TOKEN만 넣으세요)
TELEGRAM_TOKEN = "8610739586:AAEgbQNP3V3ZjQIJHdOSHJFTPwEXke5z-4M"
TELEGRAM_CHAT_ID = "8713970122"

# 2. 2Captcha 설정 (https://2captcha.com/setting 에서 확인)
TWOCAPTCHA_API_KEY = "4fc0b17ce6557ae55c9ceb513435fc45"
solver = TwoCaptcha(TWOCAPTCHA_API_KEY)

# ========================================================
# 📁 1. 유틸리티 함수 (알림 및 저장)
# ========================================================
def send_telegram_noti(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message})
    except: pass

def save_published_url(site_name, url):
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "published_urls.txt")
    with open(desktop_path, "a", encoding="utf-8") as f:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{now}] {site_name} : {url}\n")

# ========================================================
# 🧠 2. 데이터셋 및 타겟 사이트
# ========================================================
regions = [
    "서울", "강남", "서초", "송파", "여의도", "종로", "마포", "용산", 
    "인천", "송도", "청라", "부천", "수원", "판교", "분당", "광교", "동탄", "일산", "성남", "안양", "남양주",
    "대전", "세종", "천안", "공주", "청주", "충주", "아산", 
    "부산", "해운대", "서면", "대구", "수성구", "울산", "창원", "포항", "구미", "진주",
    "광주", "상무지구", "전주", "익산", "여수", "순천",
    "춘천", "원주", "강릉", "제주", "서귀포"
]
tele_ids = [
    "@BTCKOREA"
]
keywords = ["코인 대행"]
actions = [
    "빠른 1:1 대응", "24시간 무료 문의 환영", "즉각적인 피드백 보장", "철저한 비밀보장 상담",
    "안전한 익명 상담", "전문 상담사 직접 응대", "실시간 빠른 상담 연결", "무료 초기 상담 제공",
    "정확한 맞춤 상담 진행", "신속한 문제 해결 지원", "고객 중심 상담 서비스", "최적 해결책 제안 상담",
    "경험 기반 전문 상담", "즉시 문의 가능 서비스", "온라인 간편 상담 접수", "빠른 답변 보장 시스템",
    "24시간 실시간 대응", "비공개 안전 상담 시스템", "신뢰 기반 상담 진행", "전문팀 즉각 대응 지원",
    "간편 문의 빠른 처리", "최적화된 상담 프로세스", "고품질 상담 서비스 제공", "검증된 상담 노하우 적용",
    "상담부터 해결까지 원스톱"
]
author_names = ["김민준", "이서연", "박지훈", "최유진", "정하늘", "강다은", "조현우", "윤서진", "장예린", "임도윤", "한지민", "오승현", "서가은", "신재원", "권유나", "황지호", "안채원", "송민재", "고은서", "문태윤", "양소희", "배준서", "백예진", "남건우", "노지아", "차민성", "유하린", "전우진", "하은솔", "곽지훈"]

target_sites = [
    # 🛒 [Cafe24 플랫폼]
    {"site_name": "천우식품", "login_url": "https://1000food.co.kr/member/login.html", "write_url": "https://1000food.co.kr/board/product/write.html?board_no=6", "user_id": "sdfkoko3421d", "user_pw": "QkRnsh001@@", "platform": "cafe24"},
    {"site_name": "다향연", "login_url": "https://dahyangyeon.com/member/login.html", "write_url": "https://dahyangyeon.com/board/product/write.html?board_no=5", "user_id": "sdfkopikop3123", "user_pw": "QkRnsh001@@", "platform": "cafe24"},
    {"site_name": "오트리스", "login_url": "https://oatrice.co.kr/member/login.html", "write_url": "https://oatrice.co.kr/board/product/write.html?board_no=6&page=1", "user_id": "sdfkopikop3123", "user_pw": "QkRnsh001@@", "platform": "cafe24"},
    {"site_name": "락피쉬웨더웨어", "login_url": "https://en.rockfish-weatherwear.co.kr/member/login.html", "write_url": "https://en.rockfish-weatherwear.co.kr/board/product/write.html?board_no=5", "user_id": "sdfkopikop3123", "user_pw": "QkRnsh001@@", "platform": "cafe24"},
    {"site_name": "혜담", "login_url": "https://hyedamcc.co.kr/member/login.html", "write_url": "https://hyedamcc.co.kr/board/product/write.html?board_no=8", "user_id": "sdfkopikop3123", "user_pw": "QkRnsh001@@", "platform": "cafe24"},
    {"site_name": "갤러리스", "login_url": "https://gallerys.co.kr/member/login.html", "write_url": "https://gallerys.co.kr/board/product/write.html?board_no=6", "user_id": "sdfkopikop3123", "user_pw": "QkRnsh001@@", "platform": "cafe24"},
    {"site_name": "예움(상품QA)", "login_url": "https://yeaum.com/member/login.html", "write_url": "https://yeaum.com/board/product/write.html?board_no=6", "user_id": "sdfkopikop3123", "user_pw": "QkRnsh001@@", "platform": "cafe24"},
    {"site_name": "예움(자유)", "login_url": "https://yeaum.com/member/login.html", "write_url": "https://yeaum.com/board/free/write.html?board_no=7", "user_id": "sdfkopikop3123", "user_pw": "QkRnsh001@@", "platform": "cafe24"},
    {"site_name": "조아팩", "login_url": "https://joapack.co.kr/member/login.html", "write_url": "https://joapack.co.kr/board/product/write.html?board_no=6", "user_id": "sdfkopikop3123", "user_pw": "QkRnsh001@@", "platform": "cafe24"},
    {"site_name": "아이템코리아", "login_url": "https://itemkorea.kr/member/login.html", "write_url": "https://itemkorea.kr/board/product/write.html?board_no=6", "user_id": "sdfkopikop3123", "user_pw": "QkRnsh001@@", "platform": "cafe24"},
    
    # 🤖 [YSSAD 캡챠 자동해독 플랫폼]
    {"site_name": "YSSAD", "login_url": "", "write_url": "http://yssad.co.kr/sub/sub04_01.php?boardid=free&mode=write", "user_id": "", "user_pw": "QkRnsh001", "platform": "yssad_captcha", "cooldown": 3600},
    
    # 🔓 [Ssoul 비회원 비밀글해제 플랫폼]
    {"site_name": "Ssoul", "login_url": "", "write_url": "https://ssoul.org/program_a/?board=b20210512946ab67798ecc&bmode=write", "user_id": "", "user_pw": "QkRnsh001@@", "platform": "ssoul_custom", "cooldown": 3600},
    
    # 📝 [그누보드 스마트에디터 플랫폼]
    {"site_name": "잡플랜컨설팅", "login_url": "https://www.busanhrd.co.kr/bbs/login.php", "write_url": "https://www.busanhrd.co.kr/bbs/write.php?bo_table=qa", "user_id": "YOUR_ID", "user_pw": "YOUR_PW", "platform": "gnuboard_smarteditor", "cooldown": 3600}
]

# ========================================================
# 📝 3. 원고 생성기 (다양성 강화 버전 - ID 앞/중앙 배치)
# ========================================================
def generate_random_post():
    region = random.choice(regions)
    keyword = random.choice(keywords) if keywords and keywords[0] != "" else "상담"
    tele = random.choice(tele_ids)
    action = random.choice(actions)
    author = random.choice(author_names)

    # 🎯 1. 제목 템플릿 (tele_ids 필수 포함, 앞/중간 랜덤 배치)
    title_templates = [
        # 📌 텔레그램 ID 앞쪽 배치
        f"{tele} [{region}] {keyword} 확실하게 해결해 드립니다",
        f"{tele} / {region} 최고의 {keyword} 전문가와 상담하세요",
        f"{tele} - [{keyword}] {region} {action} 100% 보장",
        f"{tele} 답답한 {keyword} 문제, {region} 담당자가 해결합니다",
        f"{tele} {region} {keyword} {action} 전문, 24시간 대기중",
        
        # 📌 텔레그램 ID 중간 배치
        f"[{region}] {tele} {keyword} 확실하게 해결해 드립니다",
        f"최고의 {keyword} 전문가 {tele} 빠른 상담하세요",
        f"[{keyword}] {region} 담당자 {tele} 즉시 해결합니다",
        f"◆ {region} {keyword} ◆ {tele} {action} 24시 대기중",
        f"신속한 {action} 보장! {region} {keyword} 문의는 {tele}"
    ]
    title = random.choice(title_templates)

    # 🌐 2. HTML 본문 템플릿
    html_templates = [
        f"""
        <div style='padding: 15px; border: 1px solid #ddd; background-color: #f9f9f9;'>
            <h3 style='color: #333;'>[{region}] {keyword} 전문 센터</h3>
            <p>안녕하세요. <strong>{region}</strong> 지역 <strong>{keyword}</strong> 관련하여 고민이 많으신가요?</p>
            <p>저희는 고객님의 상황에 맞춘 <strong>{action}</strong>을 최우선으로 생각합니다.</p>
            <p style='font-size: 16px; color: #d32f2f; margin-top: 20px;'><strong>💡 24시간 긴급 연락처: {tele}</strong></p>
            <p>망설이지 말고 지금 바로 문의 남겨주시면 즉각적으로 피드백 드리겠습니다.</p>
        </div>
        """,
        f"""
        <h2>🔥 {region} {keyword} 압도적 1위 🔥</h2>
        <p>더 이상 혼자 고민하지 마세요. 확실한 <strong>{action}</strong>으로 결과로 증명합니다.</p>
        <ul style='line-height: 1.8;'>
            <li>✔ 지역: {region} 전 지역 커버</li>
            <li>✔ 핵심 서비스: {keyword} 완벽 처리</li>
            <li>✔ 우리의 약속: <strong>{action}</strong></li>
        </ul>
        <hr style='border: 0; border-top: 1px dashed #ccc;'>
        <p style='font-size: 18px;'><strong>📲 실시간 문의 및 상담: <span style='color: blue;'>{tele}</span></strong></p>
        """
    ]
    html_content = random.choice(html_templates)

    # 📝 3. 일반 텍스트 본문 템플릿
    plain_templates = [
        f"[{region}] {keyword} 전문 센터\n\n안녕하세요. {region} 지역 {keyword} 관련 고민이신가요?\n저희는 고객님께 {action}을 약속드립니다.\n\n💡 24시간 연락처: {tele}\n\n망설이지 말고 바로 문의주세요.",
        f"🔥 {region} {keyword} 압도적 1위 🔥\n\n더 이상 혼자 고민하지 마세요. 확실한 {action}으로 결과로 증명합니다.\n- 지역: {region}\n- 분야: {keyword}\n\n📲 실시간 문의: {tele}"
    ]
    plain_content = random.choice(plain_templates)

    return title, html_content, plain_content, author

# ========================================================
# ⚙️ 4. 메인 글쓰기 로직
# ========================================================
def process_site(site):
    print(f"\n🚀 [{site['site_name']}] 작업 시작...")
    
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # 화면 숨김 처리 필요 시 아래 줄 주석 해제
    # chrome_options.add_argument("--headless")
    
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)
    
    try:
        title, html_content, plain_content, author = generate_random_post()
        print(f"👤 닉네임: {author} / 📝 제목: {title}")
        
        # --------------------------------------------------------
        # 🤖 4-1. YSSAD (2Captcha 자동 해독)
        # --------------------------------------------------------
        if site.get('platform') == "yssad_captcha":
            driver.get(site['write_url'])
            time.sleep(2)
            try:
                driver.find_element(By.ID, "user_name").send_keys(author)
                driver.find_element(By.ID, "title").send_keys(title)
                driver.find_element(By.ID, "pass").send_keys(site['user_pw'])
            except: pass
            
            driver.execute_script("if(typeof oEditors_contents !== 'undefined'){ oEditors_contents.getById['contents'].exec('PASTE_HTML', [arguments[0]]); }", html_content)
            time.sleep(1)
            
            print("🔍 보안문자 이미지 분석 중...")
            try:
                img_element = driver.find_element(By.XPATH, "//img[contains(@src, 'captcha') or contains(@id, 'zsfImg')]")
                img_path = os.path.join(os.getcwd(), "captcha.png")
                img_element.screenshot(img_path)
                
                result = solver.normal(img_path)
                captcha_code = result['code']
                print(f"✅ 해독 완료: {captcha_code}")
                
                driver.find_element(By.XPATH, "//input[@type='text' and (contains(@name, 'code') or contains(@id, 'captcha'))]").send_keys(captcha_code)
                driver.find_element(By.XPATH, "//button[contains(., '확인') or @type='submit']").click()
                time.sleep(3)
                
                if os.path.exists(img_path): os.remove(img_path)
            except Exception as e:
                print(f"❌ 캡챠 해독/입력 실패: {e}")

        # --------------------------------------------------------
        # 🔓 4-2. Ssoul (비회원 비밀글 강제 해제)
        # --------------------------------------------------------
        elif site.get('platform') == "ssoul_custom":
            driver.get(site['write_url'])
            time.sleep(3)
            try:
                driver.find_element(By.NAME, "name").send_keys(author)
                driver.find_element(By.NAME, "password").send_keys(site['user_pw'])
                driver.find_element(By.NAME, "subject").send_keys(title)
            except: pass
            
            try:
                driver.execute_script(f"document.getElementsByName('content')[0].value = `{html_content}`;")
            except: pass
            
            # 비밀글 해제
            try:
                driver.execute_script("$('#is_secret_input').val('no'); $('#is_secret_input').parent().find('a').removeClass('active');")
            except: pass
            
            try:
                driver.find_element(By.XPATH, "//button[contains(., '등록') or contains(., '확인')]").click()
            except:
                driver.execute_script("document.forms[0].submit();")
            time.sleep(3)

        # --------------------------------------------------------
        # 🛒 4-3. Cafe24 (쇼핑몰 통합)
        # --------------------------------------------------------
        elif site.get('platform') == "cafe24":
            driver.get(site['login_url'])
            time.sleep(2)
            try:
                driver.find_element(By.ID, "member_id").send_keys(site['user_id'])
                driver.find_element(By.ID, "member_passwd").send_keys(site['user_pw'])
                driver.find_element(By.ID, "member_passwd").send_keys(Keys.RETURN)
                time.sleep(2)
            except: pass
            
            driver.get(site['write_url'])
            time.sleep(3)
            try: driver.find_element(By.ID, "subject").send_keys(title)
            except: pass
            
            js_inject = "var h=arguments[0]; if(typeof EC_FROALA_INSTANCE!=='undefined'){EC_FROALA_INSTANCE.applyContentToFroala(h);} var f=document.getElementById('content_IFRAME'); if(f){(f.contentDocument||f.contentWindow.document).body.innerHTML=h;} document.getElementById('content').value=h;"
            driver.execute_script(js_inject, html_content)
            time.sleep(1)
            
            try:
                driver.find_element(By.XPATH, "//input[@type='password']").send_keys(site['user_pw'])
                for cb in driver.find_elements(By.XPATH, "//input[@type='checkbox']"):
                    cb_id = cb.get_attribute('id') or ''
                    if 'agree' in cb_id and not cb.is_selected(): driver.execute_script("arguments[0].click();", cb)
                    elif 'secure' in cb_id and 'secret' not in cb_id and not cb.is_selected(): driver.execute_script("arguments[0].click();", cb)
            except: pass
            
            driver.execute_script("BOARD_WRITE.form_submit('boardWriteForm');")
            time.sleep(3)

        # --------------------------------------------------------
        # 📝 4-4. 그누보드 스마트에디터 (잡플랜컨설팅)
        # --------------------------------------------------------
        elif site.get('platform') == "gnuboard_smarteditor":
            driver.get(site['login_url'])
            time.sleep(2)
            try:
                driver.find_element(By.NAME, "mb_id").send_keys(site['user_id'])
                driver.find_element(By.NAME, "mb_password").send_keys(site['user_pw'])
                driver.find_element(By.CLASS_NAME, "btn_submit").click()
                time.sleep(2)
            except: pass
            
            driver.get(site['write_url'])
            time.sleep(3)
            try: driver.find_element(By.NAME, "wr_subject").send_keys(title)
            except: pass
            
            try:
                iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'SmartEditor2Skin.html')]")))
                driver.switch_to.frame(iframe)
                editor_body = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "se2_inputarea")))
                editor_body.click()
                editor_body.send_keys(plain_content) 
                driver.switch_to.default_content()
            except:
                driver.switch_to.default_content()
                try: driver.execute_script(f"document.getElementById('wr_content').value = `{html_content}`;")
                except: pass
                
            try: driver.find_element(By.ID, "btn_submit").click()
            except: driver.execute_script("document.getElementById('fwrite').submit();")
            time.sleep(3)

        # ========================================================
        # ✅ 성공 여부 확인 및 후처리
        # ========================================================
        try: driver.switch_to.alert.accept()
        except: pass
        
        published_url = driver.current_url
        if "write" not in published_url:
            save_published_url(site['site_name'], published_url)
            print(f"🎉 [{site['site_name']}] 등록 성공: {published_url}")
            # 성공 시 텔레그램으로도 알림 발송
            send_telegram_noti(f"✅ [{site['site_name']}] 포스팅 성공!\nURL: {published_url}")
        else:
            print(f"❌ [{site['site_name']}] 에러: 등록 페이지를 벗어나지 못했습니다.")

    except Exception as e:
        print(f"❌ [{site['site_name']}] 작업 중 치명적 에러: {e}")
    finally:
        driver.quit()

# ========================================================
# 🚀 5. 자동화 실행 루프 (무인 모드)
# ========================================================
if __name__ == "__main__":
    last_run_times = {}
    print("🤖 자동 포스팅 봇을 가동합니다.")
    send_telegram_noti("🤖 자동 포스팅 봇이 가동되었습니다. (무인 모드 시작)")
    
    while True:
        for site in target_sites:
            site_name = site['site_name']
            cooldown = site.get('cooldown', 0)
            last_run = last_run_times.get(site_name, 0)
            
            if time.time() - last_run >= cooldown:
                process_site(site)
                last_run_times[site_name] = time.time()
                time.sleep(random.randint(15, 30)) # 사이트 간 이동 간격 (15~30초)
            else:
                remaining = int(cooldown - (time.time() - last_run))
                print(f"⏳ [{site_name}] 쿨타임 대기 중... ({remaining}초 남음)")
                
        print("\n💤 모든 사이트 1회전 완료. 5분 대기 후 반복합니다...")
        time.sleep(300) # 한 바퀴 다 돌면 5분 대기