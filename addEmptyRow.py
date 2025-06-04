import re

def add_blank_line_before_numbered_lines(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    output_lines = []
    pattern = re.compile(r'^\d+\.')  # dòng bắt đầu bằng số + dấu chấm

    for line in lines:
        if pattern.match(line.strip()):
            output_lines.append('\n')  # thêm dòng trống trước dòng bắt đầu bằng số
        output_lines.append(line)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)

# Sử dụng:
input_file = 'output_processed.txt'
output_file = 'output.txt'
add_blank_line_before_numbered_lines(input_file, output_file)
