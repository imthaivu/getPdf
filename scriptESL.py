import requests
from bs4 import BeautifulSoup

def get_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Tiêu đề bài học
        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else "No Title"

        # Nội dung chính
        contain_div = soup.find("div", class_="contain")
        if not contain_div:
            raise ValueError("Không tìm thấy <div class='contain'>")

        paragraphs = contain_div.find_all("p")
        content_lines = [
            p.get_text(separator=" ", strip=True)
            for p in paragraphs
            if p.get_text(strip=True)
        ]

        full_content = f"{title}\n" + "-" * len(title) + "\n" + "\n".join(content_lines)
        return full_content

    except Exception as e:
        print(f"[ERROR] Could not process {url}: {e}")
        return None

def main():
    all_texts = []

    with open("eslfast_links_1_to_104.txt", "r", encoding="utf-8") as file:
        urls = [line.strip() for line in file if line.strip()]

    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] Processing: {url}")
        text = get_text_from_url(url)
        if text:
            all_texts.append(text)

    # Gộp tất cả nội dung lại
    full_output = "\n\n" + ("=" * 40 + "\n\n").join(all_texts)

    with open("all_lessons1.txt", "w", encoding="utf-8") as out_file:
        out_file.write(full_output)

    print("✅ Saved all lessons to 'all_lessons.txt'")

if __name__ == "__main__":
    main()
