import tkinter as tk
from tkinter import filedialog
from docx2pdf import convert
from tkinter import messagebox
def browse_files():
    file_paths = filedialog.askopenfilenames(
        filetypes=[("Word files", "*.docx")],
        title="Select DOCX files to convert to PDF",
    )
    for input_file in file_paths:
        convert(input_file)
    messagebox.showinfo("Done", f"Đã convert {len(file_paths)}/{len(file_paths)}!")

# Create the main window
root = tk.Tk()
root.title("DOCX to PDF Converter")

# Create and configure a label
label = tk.Label(root, text="Vui lòng chọn file DOCX to PDF:")
label.pack()

# Create a button to trigger file selection
browse_button = tk.Button(root, text="Browse Files", command=browse_files)
browse_button.pack()

# Run the main loop
root.mainloop()
