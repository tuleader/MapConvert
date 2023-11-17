import os
from unidecode import unidecode
import shutil

def copy_file_without_accents(source_path):
    # Kiểm tra xem đường dẫn nguồn có tồn tại không
    if not os.path.exists(source_path):
        print(f"Đường dẫn '{source_path}' không tồn tại.")
        return

    # Lấy tên file từ đường dẫn nguồn
    file_name = os.path.basename(source_path)

    # Tạo đường dẫn không dấu cho file mới
    dest_path = os.path.join(os.path.dirname(source_path), unidecode(file_name))

    # Kiểm tra xem file mới có tồn tại chưa, nếu có thì thêm số đằng sau
    count = 1
    while os.path.exists(dest_path):
        dest_path = os.path.join(
            os.path.dirname(source_path),
            unidecode(os.path.splitext(file_name)[0]) + f"_{count}" + os.path.splitext(file_name)[1]
        )
        count += 1

    try:
        # Copy file
        shutil.copy2(source_path, dest_path)
        print(f"Đã tạo bản sao không dấu tại '{dest_path}'.")
    except Exception as e:
        print(f"Lỗi khi tạo bản sao: {e}")

# Sử dụng hàm với một đường dẫn cụ thể
source_path = r"C:\Users\ngoct\Downloads\[Môn Hóa] Bài 7 - Liên kết ion - Thầy LMC (tự luận và trắc nghiệm).pdf"
copy_file_without_accents(source_path)
