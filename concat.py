import os
from pypdf import PdfReader, PdfWriter

folder_path = "DATA6"

def extract_page_number(filename):
    return int(filename.replace("page_", "").replace(".pdf", ""))

pdf_files = sorted(
    [f for f in os.listdir(folder_path) if f.endswith(".pdf")],
    key=extract_page_number
)

writer = PdfWriter()

total_files = len(pdf_files)
for idx, filename in enumerate(pdf_files, start=1):
    file_path = os.path.join(folder_path, filename)
    print(f"📄 [{idx}/{total_files}] ")
    
    reader = PdfReader(file_path)
    for page in reader.pages:
        writer.add_page(page)

output_file_path = "merged_result6.pdf"
with open(output_file_path, "wb") as output_file:
    writer.write(output_file)

print(f"\n✅ Đã nối {total_files} file PDF thành công vào '{output_file_path}'")
