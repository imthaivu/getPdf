import os
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Cấu hình Chrome headless
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--log-level=3")
options.add_argument("--disable-extensions")
options.add_argument("--disable-infobars")
options.add_argument('--disable-software-rasterizer')

# Khởi tạo trình duyệt
driver = webdriver.Chrome(options=options)

# Cấu hình
base_url = "https://www.dogonews.com"
file_path = 'links.txt'
current_year = datetime.now().year
min_year = current_year - 5

# Hàm lấy ngày từ link
def extract_date_key(link):
    match = re.search(r"/(20\d{2})/(\d{1,2})/(\d{1,2})", link)
    if match:
        return tuple(map(int, match.groups()))
    return (0, 0, 0)

# Đọc link đã có nếu tồn tại
visited_links = set()
if os.path.exists(file_path):
    with open(file_path, 'r') as f:
        visited_links = set(f.read().splitlines())

# Bắt đầu từ trang 1 và lặp cho đến khi gặp bài cũ
page_num = 1
new_links = []
stop = False

while not stop:
    url = f"{base_url}/page/{page_num}" if page_num > 1 else base_url
    print(f"🔎 Đang xử lý {url}")
    driver.get(url)

    article_links = driver.find_elements(By.XPATH, "//a[starts-with(@href, '/20')]")
    for link in article_links:
        href = link.get_attribute("href")
        if not href or href in visited_links:
            continue

        match = re.search(r"/(20\d{2})/", href)
        if match:
            year = int(match.group(1))
            if year < min_year:
                stop = True
                print(f"🛑 Gặp bài viết cũ hơn {min_year}, dừng lại.")
                break
            else:
                visited_links.add(href)
                new_links.append(href)
                print(f"✅ Thêm: {href}")
    page_num += 1

# Sắp xếp kết quả mới
new_links.sort(key=extract_date_key)

# Ghi đè vào file
with open(file_path, 'w') as f:
    for link in new_links:
        f.write(link + '\n')

driver.quit()
print("🎉 Hoàn tất! Đã lưu các bài trong 5 năm gần nhất, đã sắp xếp rồi.") 
