import os
import shutil
import unicodedata

import os
import shutil
import unicodedata

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    without_accents = ''.join([c for c in nfkd_form if not unicodedata.combining(c)])
    
    # Replace specific characters like 'đ' with their non-accented counterparts
    without_accents = without_accents.replace('đ', 'd')
    without_accents = without_accents.replace('Đ', 'D')
    return without_accents

def copy_and_delete_file(source_path):
    # Kiểm tra xem đường dẫn nguồn có tồn tại không
    if not os.path.exists(source_path):
        print(f"Đường dẫn '{source_path}' không tồn tại.")
        return

    # Lấy tên file từ đường dẫn nguồn
    file_name = os.path.basename(source_path)

    # Lấy đường dẫn của thư mục chứa file Python đang chạy
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Tạo đường dẫn không dấu cho file mới
    dest_name = remove_accents(file_name)
    dest_path = os.path.join(script_directory, dest_name)

    # Kiểm tra xem file mới có tồn tại chưa, nếu có thì thêm số đằng sau
    count = 1
    while os.path.exists(dest_path):
        dest_name = f"{remove_accents(os.path.splitext(file_name)[0])}_{count}{os.path.splitext(file_name)[1]}"
        dest_path = os.path.join(script_directory, dest_name)
        count += 1

    try:
        # Copy file
        shutil.copy2(source_path, dest_path)
        print(f"Đã tạo bản sao không dấu tại '{dest_path}'.")

        # Xóa file nguồn
        # os.remove(source_path)
        print(f"Đã xóa file nguồn '{source_path}'.")
    except Exception as e:
        print(f"Lỗi khi thực hiện tác vụ: {e}")

# Gọi hàm với đường dẫn nguồn cụ thể
# copy_and_delete_file("duong/dan/file.txt")


# Sử dụng hàm với một đường dẫn cụ thể
source_path = r"C:\Users\ngoct\Downloads\[Môn Hóa] Bài 7 - Liên kết ion - Thầy LMC (tự luận và trắc nghiệm).pdf"
copy_and_delete_file(source_path)
