import tkinter as tk
from tkinter import filedialog, messagebox
from docx2pdf import convert
from pdf2image import convert_from_path
import PyPDF2
import os

def convert_files(file_paths, conversion_type):
    if conversion_type == "docx_to_pdf":
        for input_file in file_paths:
            convert(input_file)
        messagebox.showinfo("Done", f"Đã convert {len(file_paths)} file(s) từ DOCX to PDF!")
    elif conversion_type == "pdf_to_png":
        for file_path in file_paths:
            convert_pdf_to_images(file_path)
        messagebox.showinfo("Done", f"Đã convert {len(file_paths)} file(s) từ PDF to PNG!")

def browse_files():
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
    convert_files(file_paths, selected_conversion_type)

def convert_pdf_to_images(pdf_path):
    # Đọc tệp PDF
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Tạo thư mục mới dựa trên tên tệp PDF
        pdf_folder = os.path.splitext(pdf_path)[0]  # Lấy tên tệp PDF (không kể phần mở rộng)
        os.makedirs(pdf_folder, exist_ok=True)  # Tạo thư mục, tự động bỏ qua nếu thư mục đã tồn tại

        # Lặp qua từng trang và chuyển đổi thành hình ảnh
        for page_number in range(len(pdf_reader.pages)):
            # Đọc trang PDF
            pdf_page = pdf_reader.pages[page_number]

            # Chuyển đổi trang PDF thành hình ảnh
            images = convert_from_path(pdf_path, first_page=page_number + 1, last_page=page_number + 1)

            # Lưu hình ảnh
            image_path = os.path.join(pdf_folder, f"page_{page_number + 1}.png")
            images[0].save(image_path, "PNG")

# Create the main window
root = tk.Tk()
root.title("File Converter")

# Create and configure a label
label = tk.Label(root, text="Vui lòng chọn file để chuyển đổi:")
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
