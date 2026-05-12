import os
import time
import random
import datetime
import requests
import zipfile
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
TELEGRAM_TOKEN = "8610739586:AAEgbQNP3V3ZjQIJHdOSHJFTPwEXke5z-4M"
TELEGRAM_CHAT_ID = "8713970122"
TWOCAPTCHA_API_KEY = "4fc0b17ce6557ae55c9ceb513435fc45"
solver = TwoCaptcha(TWOCAPTCHA_API_KEY)

# ========================================================
# 🌐 브라이트데이터 프록시 설정 (새 인증서 적용 완료)
# ========================================================
PROXY_HOST = "brd.superproxy.io"
PROXY_PORT = 33335
PROXY_USER = "brd-customer-hl_ff00167d-zone-residential_proxy1"
PROXY_PASS = "w1a5968u1glk"

# 🚫 사이트별 누적 실패 횟수 저장 (6회 이상 차단용)
site_fail_counts = {}

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
# 🛡️ 프록시 IP 자동 변경 확장프로그램 생성
# ========================================================
def create_proxy_extension(proxy_user):
    manifest_json = '{"version": "1.0.0", "manifest_version": 2, "name": "Chrome Proxy", "permissions": ["proxy", "tabs", "unlimitedStorage", "storage", "<all_urls>", "webRequest", "webRequestBlocking"], "background": {"scripts": ["background.js"]}, "minimum_chrome_version":"22.0.0"}'
    background_js = 'var config = { mode: "fixed_servers", rules: { singleProxy: { scheme: "http", host: "%s", port: parseInt(%s) }, bypassList: ["localhost"] } }; chrome.proxy.settings.set({value: config, scope: "regular"}, function() {}); function callbackFn(details) { return { authCredentials: { username: "%s", password: "%s" } }; } chrome.webRequest.onAuthRequired.addListener( callbackFn, {urls: ["<all_urls>"]}, ["blocking"] );' % (PROXY_HOST, PROXY_PORT, proxy_user, PROXY_PASS)
    pluginfile = 'proxy_auth_plugin.zip'
    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    return pluginfile

# ========================================================
# 🧠 2. 데이터셋 및 타겟 사이트 (여유분 아이디 추가)
# ========================================================
regions = ["서울", "강남", "서초", "송파", "여의도", "종로", "마포", "용산", "인천", "송도", "청라", "부천", "수원", "판교", "분당", "광교", "동탄", "일산", "성남", "안양", "남양주", "대전", "세종", "천안", "공주", "청주", "충주", "아산", "부산", "해운대", "서면", "대구", "수성구", "울산", "창원", "포항", "구미", "진주", "광주", "상무지구", "전주", "익산", "여수", "순천", "춘천", "원주", "강릉", "제주", "서귀포"]
tele_ids = ["@BTCKOREA"]
keywords = ["코인 대행"]
actions = ["빠른 1:1 대응", "24시간 무료 문의 환영", "즉각적인 피드백 보장", "철저한 비밀보장 상담", "안전한 익명 상담", "전문 상담사 직접 응대", "실시간 빠른 상담 연결", "무료 초기 상담 제공", "정확한 맞춤 상담 진행", "신속한 문제 해결 지원", "고객 중심 상담 서비스", "최적 해결책 제안 상담"]
author_names = ["김민준", "이서연", "박지훈", "최유진", "정하늘", "강다은", "조현우", "윤서진", "장예린", "임도윤"]

# 💡 여유분 계정 세팅 예시: accounts 배열 안에 {"id": "아이디", "pw": "비번"} 형태로 무한 추가 가능합니다.
target_sites = [
    {
        "site_name": "천우식품", 
        "login_url": "https://1000food.co.kr/member/login.html", 
        "write_url": "https://1000food.co.kr/board/product/write.html?board_no=6", 
        "accounts": [
            {"id": "sdfkoko3421d", "pw": "QkRnsh001@@"},
            {"id": "여유아이디1", "pw": "여유비번1"},
            {"id": "여유아이디2", "pw": "여유비번2"}
        ], 
        "platform": "cafe24"
    },
    {
        "site_name": "다향연", 
        "login_url": "https://dahyangyeon.com/member/login.html", 
        "write_url": "https://dahyangyeon.com/board/product/write.html?board_no=5", 
        "accounts": [{"id": "sdfkopikop3123", "pw": "QkRnsh001@@"}], 
        "platform": "cafe24"
    },
    {
        "site_name": "YSSAD", 
        "login_url": "", 
        "write_url": "http://yssad.co.kr/sub/sub04_01.php?boardid=free&mode=write", 
        "accounts": [{"id": "", "pw": "QkRnsh001"}], 
        "platform": "yssad_captcha", "cooldown": 3600
    },
    {
        "site_name": "Ssoul", 
        "login_url": "", 
        "write_url": "https://ssoul.org/program_a/?board=b20210512946ab67798ecc&bmode=write", 
        "accounts": [{"id": "", "pw": "QkRnsh001@@"}], 
        "platform": "ssoul_custom", "cooldown": 3600
    },
    {
        "site_name": "잡플랜컨설팅", 
        "login_url": "https://www.busanhrd.co.kr/bbs/login.php", 
        "write_url": "https://www.busanhrd.co.kr/bbs/write.php?bo_table=qa", 
        "accounts": [
            {"id": "YOUR_ID", "pw": "YOUR_PW"},
            {"id": "BACKUP_ID", "pw": "BACKUP_PW"}
        ], 
        "platform": "gnuboard_smarteditor", "cooldown": 3600
    }
]

# ========================================================
# 📝 3. 원고 생성기
# ========================================================
def generate_random_post():
    region = random.choice(regions)
    keyword = random.choice(keywords)
    tele = random.choice(tele_ids)
    action = random.choice(actions)
    author = random.choice(author_names)

    title_templates = [
        f"{tele} [{region}] {keyword} 확실하게 해결해 드립니다",
        f"{tele} / {region} 최고의 {keyword} 전문가와 상담하세요",
        f"[{region}] {tele} {keyword} 확실하게 해결해 드립니다"
    ]
    title = random.choice(title_templates)

    html_templates = [
        f"<div style='padding: 15px; border: 1px solid #ddd; background-color: #f9f9f9;'><h3 style='color: #333;'>[{region}] {keyword} 전문 센터</h3><p>안녕하세요. <strong>{region}</strong> 지역 <strong>{keyword}</strong> 관련하여 고민이 많으신가요?</p><p>저희는 고객님의 상황에 맞춘 <strong>{action}</strong>을 최우선으로 생각합니다.</p><p style='font-size: 16px; color: #d32f2f; margin-top: 20px;'><strong>💡 24시간 긴급 연락처: {tele}</strong></p></div>"
    ]
    html_content = random.choice(html_templates)

    plain_content = f"[{region}] {keyword} 전문 센터\n안녕하세요. 저희는 고객님께 {action}을 약속드립니다.\n💡 연락처: {tele}"

    return title, html_content, plain_content, author

# ========================================================
# ⚙️ 4. 메인 글쓰기 로직 (크롬 숨김 + 차단방지 + 아이디/IP 회전)
# ========================================================
def process_site(site):
    site_name = site['site_name']
    
    # 🚫 누적 실패 6회 이상이거나 차단당한 사이트는 영구 스킵
    if site_fail_counts.get(site_name, 0) >= 6:
        print(f"🚫 [{site_name}] 누적 실패 6회 이상 또는 차단 감지로 인해 실행을 건너뜁니다.")
        return

    print(f"\n🚀 [{site_name}] 작업 시작...")
    
    # 여유분 아이디 목록 가져오기
    accounts = site.get('accounts', [{"id": site.get('user_id', ''), "pw": site.get('user_pw', '')}])
    success = False
    
    for account in accounts:
        # 브라이트데이터 세션 ID를 랜덤 생성하여 매 로그인 시도마다 새로운 가정집 IP로 완벽하게 둔갑
        session_id = random.randint(100000, 999999)
        current_proxy_user = f"{PROXY_USER}-session-{session_id}"
        proxy_plugin_file = create_proxy_extension(current_proxy_user)

        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        
        # 👻 크롬 브라우저를 화면에 안 보이게 숨김 (헤드리스 모드)
        chrome_options.add_argument("--headless=new") 
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_extension(proxy_plugin_file)
        
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 10)
        
        try:
            title, html_content, plain_content, author = generate_random_post()
            print(f"👤 시도 계정: {account['id']} / 📝 제목: {title}")
            
            site['user_id'] = account['id']
            site['user_pw'] = account['pw']
            
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
                try:
                    img_path = os.path.join(os.getcwd(), "captcha.png")
                    driver.find_element(By.XPATH, "//img[contains(@src, 'captcha') or contains(@id, 'zsfImg')]").screenshot(img_path)
                    captcha_code = solver.normal(img_path)['code']
                    driver.find_element(By.XPATH, "//input[@type='text' and (contains(@name, 'code') or contains(@id, 'captcha'))]").send_keys(captcha_code)
                    driver.find_element(By.XPATH, "//button[contains(., '확인') or @type='submit']").click()
                    time.sleep(3)
                    if os.path.exists(img_path): os.remove(img_path)
                except: pass

            elif site.get('platform') == "ssoul_custom":
                driver.get(site['write_url'])
                time.sleep(3)
                try:
                    driver.find_element(By.NAME, "name").send_keys(author)
                    driver.find_element(By.NAME, "password").send_keys(site['user_pw'])
                    driver.find_element(By.NAME, "subject").send_keys(title)
                except: pass
                try: driver.execute_script(f"document.getElementsByName('content')[0].value = `{html_content}`;")
                except: pass
                try: driver.execute_script("$('#is_secret_input').val('no'); $('#is_secret_input').parent().find('a').removeClass('active');")
                except: pass
                try: driver.find_element(By.XPATH, "//button[contains(., '등록') or contains(., '확인')]").click()
                except: driver.execute_script("document.forms[0].submit();")
                time.sleep(3)

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
                driver.execute_script("var h=arguments[0]; if(typeof EC_FROALA_INSTANCE!=='undefined'){EC_FROALA_INSTANCE.applyContentToFroala(h);} var f=document.getElementById('content_IFRAME'); if(f){(f.contentDocument||f.contentWindow.document).body.innerHTML=h;} document.getElementById('content').value=h;", html_content)
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

            try: driver.switch_to.alert.accept()
            except: pass

            # 🚫 관리자 차단 문구 감지 로직
            page_text = driver.find_element(By.TAG_NAME, "body").text
            if any(word in page_text for word in ["차단되었습니다", "접근 금지", "권한이 없습니다", "작성 권한"]):
                print(f"🚫 [{site_name}] 페이지 내 차단 문구 감지. 영구 스킵 처리합니다.")
                site_fail_counts[site_name] = 6
                break # 차단당했으므로 여유분 계정 시도 중지

            published_url = driver.current_url
            if "write" not in published_url and "login" not in published_url:
                save_published_url(site['site_name'], published_url)
                print(f"🎉 [{site['site_name']}] 등록 성공: {published_url}")
                send_telegram_noti(f"✅ [{site['site_name']}] 포스팅 성공!\nURL: {published_url}")
                site_fail_counts[site_name] = 0 # 성공 시 에러 카운트 리셋
                success = True
                break # 👈 성공했으므로 다음 여유분 아이디 시도 없이 깔끔하게 종료
            else:
                print(f"⚠️ [{site['site_name']}] 계정({account['id']}) 등록 실패. 다음 아이피/계정으로 재시도합니다.")

        except Exception as e:
            print(f"❌ [{site['site_name']}] 작업 에러: {e}")
        finally:
            driver.quit()
            if os.path.exists(proxy_plugin_file): os.remove(proxy_plugin_file)

    # 준비된 모든 계정(메인+여유분)을 돌았는데도 실패한 경우 카운트 +1
    if not success:
        site_fail_counts[site_name] = site_fail_counts.get(site_name, 0) + 1
        print(f"❌ [{site_name}] 모든 계정/IP 시도 실패 (누적 실패: {site_fail_counts[site_name]}회)")

# ========================================================
# 🚀 5. 자동화 실행 루프 (무인 모드)
# ========================================================
if __name__ == "__main__":
    last_run_times = {}
    print("🤖 자동 포스팅 봇을 가동합니다. (백그라운드 모드)")
    send_telegram_noti("🤖 자동 포스팅 봇이 가동되었습니다. (무인 모드 시작)")
    
    while True:
        for site in target_sites:
            site_name = site['site_name']
            cooldown = site.get('cooldown', 0)
            last_run = last_run_times.get(site_name, 0)
            
            if time.time() - last_run >= cooldown:
                process_site(site)
                last_run_times[site_name] = time.time()
                time.sleep(random.randint(15, 30))
            else:
                remaining = int(cooldown - (time.time() - last_run))
                print(f"⏳ [{site_name}] 쿨타임 대기 중... ({remaining}초 남음)")
                
        print("\n💤 모든 사이트 1회전 완료. 5분 대기 후 반복합니다...")
        time.sleep(300)
