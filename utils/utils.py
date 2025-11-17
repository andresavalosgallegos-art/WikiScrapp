from tkinter import filedialog, messagebox
import webbrowser

def guardar_txt(titulo, contenido):
    if not contenido:
        messagebox.showwarning("Advertencia", "No hay texto para guardar")
        return
    archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Texto","*.txt")])
    if archivo:
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(f"{titulo}\n\n{contenido}")
        messagebox.showinfo("Éxito", f"Resumen guardado en {archivo}")

def abrir_url(url):
    webbrowser.open(url)
