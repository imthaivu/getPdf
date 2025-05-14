import re

def extract_year(url):
    match = re.search(r"/(\d{4})/", url)
    if match:
        return int(match.group(1))
    return None

# Bước 1: Đọc file
with open("links.txt", "r") as file:
    lines = [line.strip() for line in file if line.strip()]

# Bước 2: Lọc các link có năm > 2019
valid_links = []
for link in lines:
    year = extract_year(link)
    if year and year > 2019:
        valid_links.append((year, link))

# Bước 3: Sắp xếp theo năm
valid_links.sort(key=lambda x: x[0])

# Bước 4: Ghi lại file
with open("links.txt", "w") as file:
    for _, link in valid_links:
        file.write(link + "\n")

print("✅ Đã lọc và sắp xếp xong các link từ năm 2020 trở đi.")
