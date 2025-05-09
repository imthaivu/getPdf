import os
from PyPDF2 import PdfReader, PdfWriter

def remove_last_page_if_short(pdf_path, char_threshold=60):
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)

    if total_pages == 0:
        print(f"❌ {pdf_path}: PDF không có trang nào.")
        return

    last_page = reader.pages[-1]
    text = last_page.extract_text() or ""
    text = text.strip()

    if len(text) < char_threshold:
        print(f"🗑️ {os.path.basename(pdf_path)}: Trang cuối có {len(text)} ký tự, sẽ bị xoá.")
        writer = PdfWriter()
        for i in range(total_pages - 1):  # giữ lại tất cả trừ trang cuối
            writer.add_page(reader.pages[i])
        with open(pdf_path, "wb") as f:
            writer.write(f)
    else:
        print(f"✅ {os.path.basename(pdf_path)}: Trang cuối có {len(text)} ký tự, giữ lại.")

def main():
    folder = "DATA"
    if not os.path.exists(folder):
        print("❌ Không tìm thấy thư mục DATA.")
        return

    pdf_files = [f for f in os.listdir(folder) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print("❌ Không tìm thấy file PDF nào trong DATA.")
        return

    for pdf_file in pdf_files:
        full_path = os.path.join(folder, pdf_file)
        remove_last_page_if_short(full_path)

    print("\n🎉 Đã xử lý xong tất cả file PDF trong thư mục DATA!")

if __name__ == "__main__":
    main()
