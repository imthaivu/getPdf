import os
import time
import base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# === CẤU HÌNH ===
output_folder = "DATA"
links_file = "links.txt"
delay_after_load = 2  # Thời gian chờ sau khi load trang (giây)

# === TẠO THƯ MỤC ĐÍCH ===
os.makedirs(output_folder, exist_ok=True)

# === ĐỌC LINK TỪ FILE ===
if not os.path.exists(links_file):
    print(f"❌ Không tìm thấy file {links_file}. Vui lòng chạy collect_links.py trước.")
    exit()

with open(links_file, "r") as f:
    links = [line.strip() for line in f if line.strip().startswith("http")]

if not links:
    print("❌ Không có link hợp lệ trong links.txt.")
    exit()

print(f"📄 Tổng cộng {len(links)} link sẽ được in ra PDF...\n")

# === CẤU HÌNH CHROME HEADLESS ===
options = Options()
options.add_argument('--headless=new')  # dùng chế độ headless mới
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)

# === IN TỪNG TRANG RA PDF ===
for idx, url in enumerate(links):
    print(f"➡️  [{idx + 1}/{len(links)}] Đang xử lý: {url}")
    try:
        driver.get(url)
        time.sleep(delay_after_load)

        result = driver.execute_cdp_cmd("Page.printToPDF", {
            "printBackground": True
        })

        pdf_data = base64.b64decode(result['data'])
        output_path = os.path.join(output_folder, f"page_{idx + 1}.pdf")

        with open(output_path, "wb") as f:
            f.write(pdf_data)

        print(f"✅ Đã lưu PDF vào: {output_path}\n")
    except Exception as e:
        print(f"❌ Lỗi khi xử lý {url}: {e}\n")

driver.quit()

# === GỢI Ý KIỂM TRA ===
print("\n🎉 Đã hoàn tất in PDF cho tất cả link! rồi đó")
