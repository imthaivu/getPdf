import time
import os
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
options.add_argument('--disable-software-rasterizer')  # Tắt cảnh báo WebGL

# Khởi tạo trình duyệt
driver = webdriver.Chrome(options=options)

# Tải các link bài viết từ nhiều trang
base_url = "https://www.dogonews.com"
visited_links = set()  # Tạo một tập hợp để lưu các link đã truy cập

# Kiểm tra nếu file links.txt đã tồn tại
file_path = 'links.txt'

# Nếu file đã tồn tại, đọc nội dung vào visited_links
if os.path.exists(file_path):
    with open(file_path, 'r') as file:
        visited_links = set(file.read().splitlines())

for page_num in range(2, 581):  # Bạn có thể điều chỉnh số trang ở đây
    print(f"Đang xử lý trang {page_num}...")
    url = f"{base_url}/page/{page_num}"
    driver.get(url)

    # Tìm các thẻ a có dạng /YYYY/MM/DD/...
    article_links = driver.find_elements(By.XPATH, "//a[starts-with(@href, '/20')]")
    for link in article_links:
        href = link.get_attribute("href")
        if href and href not in visited_links:  # Kiểm tra link đã có chưa
            visited_links.add(href)  # Thêm link vào tập hợp
            print(f"Link bài viết: {href}")

# Lưu các link đã thu thập vào file links.txt
with open(file_path, 'a') as file:
    for link in visited_links:
        file.write(link + '\n')

driver.quit()
print("🎉 Hoàn tất!")
