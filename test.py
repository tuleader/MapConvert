import tkinter as tk
from tkinter import filedialog, messagebox
from docx2pdf import convert
from pdf2image import convert_from_path
import PyPDF2
import os
def convert_pdf_to_images(pdf_path):
    print(pdf_path)
    # Đọc tệp PDF
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Tạo thư mục mới dựa trên tên tệp PDF
        pdf_folder = os.path.splitext(pdf_path)[0]  # Lấy tên tệp PDF (không kể phần mở rộng)
        os.makedirs(pdf_folder, exist_ok=True)  # Tạo thư mục, tự động bỏ qua nếu thư mục đã tồn tại

        # Lặp qua từng trang và chuyển đổi thành hình ảnh
        for page_number in range(len(pdf_reader.pages)):
            # Đọc trang PDF
            # pdf_page = pdf_reader.pages[page_number]

            # Chuyển đổi trang PDF thành hình ảnh
            images = convert_from_path(pdf_path, first_page=page_number + 1, last_page=page_number + 1)

            # Lưu hình ảnh
            image_path = os.path.join(pdf_folder, f"page_{page_number + 1}.png")
            images[0].save(image_path, "PNG")