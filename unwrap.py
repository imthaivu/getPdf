import re

def unwrap_with_titles(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    output_lines = []
    buffer = ""
    title_pattern = re.compile(r'^\d+\.\s+[A-Z]')  # Ví dụ: "1. AMERICA: LAND OF OPPORTUNITY"

    for line in lines:
        stripped_line = line.rstrip('\n').rstrip()

        if stripped_line == '':
            # Dòng trống -> kết thúc đoạn
            if buffer:
                output_lines.append(buffer + '\n')
                buffer = ""
            output_lines.append('\n')  # giữ dòng trống
            continue

        if title_pattern.match(stripped_line):
            # Nếu gặp dòng tiêu đề:
            # Ghi buffer hiện tại (nếu có) rồi ghi tiêu đề nguyên trạng
            if buffer:
                output_lines.append(buffer + '\n')
                buffer = ""
            output_lines.append(stripped_line + '\n')
        else:
            # Đây là dòng nội dung, xử lý nối wrap
            if buffer:
                # nối dòng buffer với dòng hiện tại
                buffer += " " + stripped_line
            else:
                buffer = stripped_line

            # Kiểm tra dấu hiệu kết thúc câu để quyết định xuống dòng
            if buffer.endswith(('.', '!', '?')):
                output_lines.append(buffer + '\n')
                buffer = ""

    # Nếu còn buffer chưa ghi thì ghi ra
    if buffer:
        output_lines.append(buffer + '\n')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)


# Sử dụng:
input_file = 'input.txt'
output_file = 'output_processed.txt'
unwrap_with_titles(input_file, output_file)
