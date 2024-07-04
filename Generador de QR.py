import qrcode
import uuid
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os
import csv
from reportlab.pdfgen import canvas
import webbrowser

# Ruta para guardar los QR generados
qr_folder = r"C:\Users\forwa\OneDrive\Desktop\qr"
if not os.path.exists(qr_folder):
    os.makedirs(qr_folder)

# Variables globales para el seguimiento de los archivos QR generados
qr_files = []
current_index = -1

# Ruta de la imagen personalizada
custom_image_path = "logo.png"

# Función para validar la URL del formulario
def validate_url(url):
    if url.startswith("https://www.facebook.com/launicacihualteca?locale=es_LA"):
        return True
    return False

# Función para seleccionar la carpeta de destino
def select_folder():
    global qr_folder
    qr_folder = filedialog.askdirectory()
    if qr_folder:
        load_all_images()

# Función para generar un QR único y guardar la imagen
def generate_unique_qr():
    global current_index
    unique_id = str(uuid.uuid4())
    form_url = f"https://www.facebook.com/launicacihualteca?locale=es_LA={unique_id}"
    
    if not validate_url(form_url):
        messagebox.showerror("Invalid URL", "The form URL is invalid.")
        return
    
    filename = f"qr_{len(qr_files) + 1}.png"
    img_path = os.path.join(qr_folder, filename)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(form_url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white').convert('RGB')

    # Añadir imagen personalizada en el centro del QR
    if os.path.exists(custom_image_path):
        custom_img = Image.open(custom_image_path)
        custom_img = custom_img.resize((50, 50), Image.LANCZOS)
        pos = ((img.size[0] - custom_img.size[0]) // 2, (img.size[1] - custom_img.size[1]) // 2)
        img.paste(custom_img, pos, mask=custom_img)

    img.save(img_path)

    qr_files.append((img_path, unique_id))
    current_index = len(qr_files) - 1
    load_qr_image(img_path, filename)

    messagebox.showinfo("QR Code Generated", f"Generated QR Code with ID: {unique_id}")

# Función para cargar y mostrar la imagen del QR
def load_qr_image(img_path, filename):
    img = Image.open(img_path)
    img = img.resize((250, 250), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)

    qr_label.config(image=img_tk)
    qr_label.image = img_tk
    filename_label.config(text=filename)

# Función para mostrar el QR anterior
def show_previous_qr():
    global current_index
    if current_index > 0:
        current_index -= 1
        img_path, _ = qr_files[current_index]
        filename = os.path.basename(img_path)
        load_qr_image(img_path, filename)

# Función para mostrar el QR siguiente
def show_next_qr():
    global current_index
    if current_index < len(qr_files) - 1:
        current_index += 1
        img_path, _ = qr_files[current_index]
        filename = os.path.basename(img_path)
        load_qr_image(img_path, filename)

# Función para cargar todas las imágenes del directorio al iniciar
def load_all_images():
    global qr_files, current_index
    qr_files = []
    for filename in os.listdir(qr_folder):
        if filename.endswith(".png"):
            img_path = os.path.join(qr_folder, filename)
            qr_files.append((img_path, filename))
    if qr_files:
        current_index = 0
        load_qr_image(qr_files[0][0], qr_files[0][1])

# Función para generar un reporte en PDF
def generate_pdf_report():
    pdf_path = os.path.join(qr_folder, "qr_report.pdf")
    c = canvas.Canvas(pdf_path)
    c.drawString(100, 800, "QR Code Report")
    y = 750
    for img_path, filename in qr_files:
        c.drawString(100, y, filename)
        c.drawImage(img_path, 100, y - 100, width=100, height=100)
        y -= 150
    c.save()
    messagebox.showinfo("PDF Report Generated", f"Report saved at {pdf_path}")

# Función para exportar los datos a CSV
def export_to_csv():
    csv_path = os.path.join(qr_folder, "qr_data.csv")
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Filename", "UUID"])
        for img_path, filename in qr_files:
            writer.writerow([filename, img_path])
    messagebox.showinfo("CSV Exported", f"Data exported to {csv_path}")

# Función para generar un QR personalizado con un nombre especificado
def generate_custom_qr():
    global current_index
    custom_filename = filename_entry.get().strip()
    custom_url = url_entry.get().strip()
    
    if not custom_filename or not custom_url:
        messagebox.showerror("Invalid Input", "Please enter a valid filename and URL.")
        return
    
    if not custom_url.startswith("http://") and not custom_url.startswith("https://"):
        messagebox.showerror("Invalid URL", "Please enter a valid URL.")
        return

    custom_filename += ".png"
    img_path = os.path.join(qr_folder, custom_filename)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(custom_url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white').convert('RGB')

    # Añadir imagen personalizada en el centro del QR
    if os.path.exists(custom_image_path):
        custom_img = Image.open(custom_image_path)
        custom_img = custom_img.resize((50, 50), Image.LANCZOS)
        pos = ((img.size[0] - custom_img.size[0]) // 2, (img.size[1] - custom_img.size[1]) // 2)
        img.paste(custom_img, pos, mask=custom_img)

    img.save(img_path)

    qr_files.append((img_path, custom_filename))
    current_index = len(qr_files) - 1
    load_qr_image(img_path, custom_filename)

    messagebox.showinfo("QR Code Generated", f"Generated QR Code for URL: {custom_url}")

# Función para abrir el perfil de Instagram
def open_instagram():
    webbrowser.open("https://www.instagram.com/forwardtecno/")

# Función para manejar el clic en el Entry y limpiar el texto de ejemplo
def on_entry_click(event, entry, default_text):
    if entry.get() == default_text:
        entry.delete(0, tk.END)
        entry.config(fg='black')

# Función para manejar la pérdida de foco en el Entry y restaurar el texto de ejemplo si está vacío
def on_focus_out(event, entry, default_text):
    if entry.get() == '':
        entry.insert(0, default_text)
        entry.config(fg='grey')

# Crear la ventana principal
root = tk.Tk()
root.title("Generador de QR")
root.configure(bg="#87CEFA")  # Fondo de la ventana
root.iconbitmap("logo.png")  # Cambiar el icono de la aplicación

# Crear el botón para seleccionar la carpeta de destino
select_folder_button = tk.Button(root, text="Seleccionar Carpeta", command=select_folder, 
                                 font=("Helvetica", 12), bg="#4682B4", fg="white", borderwidth=2, relief="solid", padx=5, pady=5)
select_folder_button.pack(pady=10)

# Añadir imagen "descarga.png" junto al botón "Seleccionar Carpeta"
try:
    descarga_img = Image.open("descarga.png")
    descarga_img = descarga_img.resize((30, 30), Image.LANCZOS)
    descarga_img_tk = ImageTk.PhotoImage(descarga_img)
    descarga_label = tk.Label(root, image=descarga_img_tk, bg="#87CEFA")
    descarga_label.image = descarga_img_tk
    descarga_label.pack(pady=5)
except FileNotFoundError:
    print("Imagen descarga.png no encontrada")

# Texto de ejemplo para las entradas
filename_example_text = " Ingresa nombre opcional      "
url_example_text =      " URL Obligatoria                                 "

# Etiqueta y cuadro de entrada para el nombre del archivo personalizado
filename_label_entry = tk.Label(root, text="Nombre del archivo", font=("Helvetica", 14), bg="#87CEFA")
filename_label_entry.pack()
filename_entry = tk.Entry(root, font=("Helvetica", 14), fg='grey')
filename_entry.insert(0, filename_example_text)
filename_entry.bind('<FocusIn>', lambda event: on_entry_click(event, filename_entry, filename_example_text))
filename_entry.bind('<FocusOut>', lambda event: on_focus_out(event, filename_entry, filename_example_text))
filename_entry.pack(pady=5)

# Etiqueta y cuadro de entrada para la URL del formulario
url_label_entry = tk.Label(root, text="URL del formulario", font=("Helvetica", 14), bg="#87CEFA")
url_label_entry.pack()
url_entry = tk.Entry(root, font=("Helvetica", 14), fg='grey')
url_entry.insert(0, url_example_text)
url_entry.bind('<FocusIn>', lambda event: on_entry_click(event, url_entry, url_example_text))
url_entry.bind('<FocusOut>', lambda event: on_focus_out(event, url_entry, url_example_text))
url_entry.pack(pady=5)

# Botón para generar un QR personalizado
generate_custom_qr_button = tk.Button(root, text="Generar QR Personalizado", command=generate_custom_qr,
                                      font=("Helvetica", 14), bg="#4682B4", fg="white", borderwidth=2, relief="solid", padx=5, pady=5)
generate_custom_qr_button.pack(pady=10)

# Crear el botón para generar un QR único
generate_qr_button = tk.Button(root, text="Generar QR Único", command=generate_unique_qr,
                               font=("Helvetica", 14), bg="#4682B4", fg="white", borderwidth=2, relief="solid", padx=5, pady=5)
generate_qr_button.pack(pady=10)

# Etiqueta para mostrar la imagen del QR generado
qr_label = tk.Label(root, bg="#87CEFA")
qr_label.pack(pady=10)

# Etiqueta para mostrar el nombre del archivo del QR generado
filename_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#87CEFA")
filename_label.pack(pady=5)

# Crear los botones para navegar entre los QR generados
nav_frame = tk.Frame(root, bg="#87CEFA")
nav_frame.pack(pady=10)
prev_button = tk.Button(nav_frame, text="Anterior", command=show_previous_qr,
                        font=("Helvetica", 12), bg="#4682B4", fg="white", borderwidth=2, relief="solid", padx=5, pady=5)
prev_button.grid(row=0, column=0, padx=10)
next_button = tk.Button(nav_frame, text="Siguiente", command=show_next_qr,
                        font=("Helvetica", 12), bg="#4682B4", fg="white", borderwidth=2, relief="solid", padx=5, pady=5)
next_button.grid(row=0, column=1, padx=10)

# Crear el botón para generar un reporte en PDF
pdf_button = tk.Button(root, text="Generar Reporte PDF", command=generate_pdf_report,
                       font=("Helvetica", 12), bg="#4682B4", fg="white", borderwidth=2, relief="solid", padx=5, pady=5)
pdf_button.pack(pady=10)

# Crear el botón para exportar los datos a CSV
csv_button = tk.Button(root, text="Exportar a CSV", command=export_to_csv,
                       font=("Helvetica", 12), bg="#4682B4", fg="white", borderwidth=2, relief="solid", padx=5, pady=5)
csv_button.pack(pady=10)

# Crear el botón para abrir el perfil de Instagram
instagram_button = tk.Button(root, text="Abrir Instagram", command=open_instagram,
                             font=("Helvetica", 12), bg="#4682B4", fg="white", borderwidth=2, relief="solid", padx=5, pady=5)
instagram_button.pack(pady=10)

# Cargar todas las imágenes al iniciar
load_all_images()

# Iniciar el bucle principal de la aplicación
root.mainloop()
