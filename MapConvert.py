import tkinter as tk
from tkinter import filedialog, messagebox
from docx2pdf import convert
from pdf2image import convert_from_path
import PyPDF2
import os
import shutil
import unicodedata

def convert_files(file_paths, conversion_type, destination_directory):
    if conversion_type == "docx_to_pdf":
        for input_file in file_paths:
            convert(input_file, os.path.join(destination_directory, os.path.basename(input_file) + ".pdf"))
        messagebox.showinfo("Done", f"Đã convert {len(file_paths)} file(s) từ DOCX to PDF!")
    elif conversion_type == "pdf_to_png":
        for file_path in file_paths:
            copy_file(file_path, destination_directory)
        messagebox.showinfo("Done", f"Đã convert {len(file_paths)} file(s) từ PDF to PNG!")

def browse_files():
    # Chọn đường dẫn lưu
    destination_directory = filedialog.askdirectory(title="Chọn thư mục lưu")

    # Chọn file dựa trên loại tệp được chọn
    if conversion_type.get() == "docx_to_pdf":
        file_types = [("Word files", "*.docx")]
    else:
        file_types = [("PDF files", "*.pdf")]

    file_paths = filedialog.askopenfilenames(
        filetypes=file_types,
        title="Chọn file để chuyển đổi",
    )

    # Get the selected conversion type
    selected_conversion_type = conversion_type.get()

    # Perform the conversion
    convert_files(file_paths, selected_conversion_type, destination_directory)

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    without_accents = ''.join([c for c in nfkd_form if not unicodedata.combining(c)])
    
    # Replace specific characters like 'đ' with their non-accented counterparts
    without_accents = without_accents.replace('đ', 'd')
    without_accents = without_accents.replace('Đ', 'D')
    return without_accents

def copy_file(source_path, destination_directory):
    # Kiểm tra xem đường dẫn nguồn có tồn tại không
    if not os.path.exists(source_path):
        print(f"Đường dẫn '{source_path}' không tồn tại.")
        return

    # Lấy tên file từ đường dẫn nguồn
    file_name = os.path.basename(source_path)

    # Tạo đường dẫn không dấu cho file mới
    dest_name = remove_accents(file_name)
    dest_path = os.path.join(destination_directory, dest_name)

    # Kiểm tra xem file mới có tồn tại chưa, nếu có thì thêm số đằng sau
    count = 1
    while os.path.exists(dest_path):
        dest_name = f"{remove_accents(os.path.splitext(file_name)[0])}_{count}{os.path.splitext(file_name)[1]}"
        dest_path = os.path.join(destination_directory, dest_name)
        count += 1

    try:
        print(dest_path)
        # Copy file
        shutil.copy2(source_path, dest_path)
        # thực hiện convert
        convert_pdf_to_images(dest_path)
        # Xóa file copy
        os.remove(dest_path)
    except Exception as e:
        messagebox.showerror("Error",f"Lỗi khi thực hiện tác vụ: {e}")

def convert_pdf_to_images(pdf_path):
    try:
        # Đọc tệp PDF
        with open(pdf_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Tạo thư mục mới dựa trên tên tệp PDF
            pdf_folder = os.path.splitext(pdf_path)[0]  # Lấy tên tệp PDF (không kể phần mở rộng)
            os.makedirs(pdf_folder, exist_ok=True)  # Tạo thư mục, tự động bỏ qua nếu thư mục đã tồn tại

            # Lặp qua từng trang và chuyển đổi thành hình ảnh
            for page_number in range(len(pdf_reader.pages)):
                # Chuyển đổi trang PDF thành hình ảnh
                images = convert_from_path(pdf_path, first_page=page_number + 1, last_page=page_number + 1)

                # Lưu hình ảnh
                image_path = os.path.join(pdf_folder, f"page_{page_number + 1}.png")
                images[0].save(image_path, "PNG")
    except Exception as e:
        messagebox.showerror("Error",f"Lỗi khi thực hiện tác vụ: {e}")

# Create the main window
root = tk.Tk()
root.title("File Converter")

# Create and configure a label
label = tk.Label(root, text="Vui lòng chọn định dạng file để chuyển đổi:")
label.pack()

# Create a variable to store the selected conversion type
conversion_type = tk.StringVar()
conversion_type.set("docx_to_pdf")  # Default conversion type

# Create Radiobuttons for conversion type selection
docx_to_pdf_button = tk.Radiobutton(root, text="DOCX to PDF", variable=conversion_type, value="docx_to_pdf")
docx_to_pdf_button.pack()

pdf_to_png_button = tk.Radiobutton(root, text="PDF to PNG", variable=conversion_type, value="pdf_to_png")
pdf_to_png_button.pack()

# Create a button to trigger file selection
browse_button = tk.Button(root, text="Chọn Files", command=browse_files)
browse_button.pack()

# Run the main loop
root.mainloop()
