import tkinter as tk
from tkinter import ttk, messagebox
import threading 

from wiki.wiki_api import buscar_wikipedia, descargar_imagen, cambiar_idioma
from utils.utils import guardar_txt, abrir_url

# Definición de la paleta de colores y fuentes
COLOR_FONDO_VENTANA = "#EFEFEF"   # Gris muy claro
COLOR_CARD = "white"              # Blanco para el contenedor principal
COLOR_PRIMARIO = "#2C3E50"        # Azul oscuro para texto/títulos
COLOR_ACCENTO = "#3498DB"         # Azul claro para acción principal
COLOR_BOTON_SEC = "#95A5A6"       # Gris para botones secundarios
FUENTE_PRINCIPAL = "Segoe UI"     # Fuente moderna

def crear_gui():
    ventana = tk.Tk()
    ventana.title("WikiScrapp Modular PRO 🚀 | V3.1")
    ventana.geometry("1000x750")
    ventana.minsize(800, 600)
    ventana.configure(bg=COLOR_FONDO_VENTANA)

    # --- Variables de Estado ---
    global ultima_url, ultimo_titulo, idioma_actual
    ultima_url = ""
    ultimo_titulo = ""
    idioma_actual = tk.StringVar(value="es") 
    
    # --- Estilo y Contenedor Principal ---
    main_container = tk.Frame(ventana, bg=COLOR_FONDO_VENTANA)
    main_container.pack(expand=True, fill='both')
    
    main_card = tk.Frame(main_container, bg=COLOR_CARD, bd=2, relief=tk.RAISED, padx=20, pady=20)
    main_card.pack(fill='both', padx=30, pady=30, expand=True)
    
    style = ttk.Style()
    style.configure("TButton", font=(FUENTE_PRINCIPAL, 10, "bold"), padding=6)
    style.map("TButton", foreground=[('active', COLOR_ACCENTO)])
    style.configure("TProgressbar", thickness=15)

    # --- Funciones de Utilidad ---

    def guardar_func():
        contenido = texto_box.get(1.0, tk.END).strip()
        titulo = ultimo_titulo
        guardar_txt(titulo, contenido)

    def abrir_func():
        if ultima_url:
            abrir_url(ultima_url)
        else:
            messagebox.showwarning("Advertencia", "Primero realiza una búsqueda.")
            
    def limpiar_imagenes_func():
        """Limpia solo las imágenes mostradas."""
        for widget in imagen_frame.winfo_children():
            widget.destroy()
        imagen_counter.config(text="Imágenes limpiadas.", fg="red")

    def limpiar_func():
        """Limpia toda la interfaz."""
        global ultima_url, ultimo_titulo
        entrada.delete(0, tk.END)
        titulo_label.config(text="Esperando término...", fg=COLOR_BOTON_SEC)
        texto_box.delete(1.0, tk.END)
        avanzado_box.delete(1.0, tk.END) 
        html_box.delete(1.0, tk.END)     
        url_label.config(text="")
        
        limpiar_imagenes_func()
        
        progreso_bar.stop()
        progreso_bar.config(value=0)
        ultima_url = ""
        ultimo_titulo = ""


    # --- Función que ejecuta la búsqueda (Hilo de trabajo) ---
    def buscar_func():
        """Contiene la lógica pesada de red y procesamiento."""
        global ultima_url, ultimo_titulo
        termino = entrada.get().strip()
        
        try:
            # La línea que recibe los 6 valores de la API
            titulo, resumen, imagenes, url, tablas_listas, html_raw = buscar_wikipedia(termino)
            
            # 1. Guardar el estado
            ultimo_titulo = titulo
            ultima_url = url
            
            # 2. ACTUALIZAR LA GUI (Llamada al final del hilo)
            
            texto_box.delete(1.0, tk.END)
            avanzado_box.delete(1.0, tk.END)
            html_box.delete(1.0, tk.END)
            
            titulo_label.config(text=titulo, fg=COLOR_PRIMARIO)
            texto_box.insert(tk.END, resumen)
            avanzado_box.insert(tk.END, tablas_listas)
            html_box.insert(tk.END, html_raw)
            url_label.config(text=f"Artículo en: {url}", fg=COLOR_ACCENTO)
            
            # Mostrar imágenes
            img_cargadas = 0
            for widget in imagen_frame.winfo_children():
                widget.destroy()

            for img_url in imagenes:
                img = descargar_imagen(img_url)
                if img:
                    lbl = tk.Label(imagen_frame, image=img, bg=COLOR_CARD)
                    lbl.image = img
                    lbl.pack(side=tk.LEFT, padx=10, pady=5)
                    img_cargadas += 1
            
            imagen_counter.config(text=f"Imágenes cargadas: {img_cargadas}/{len(imagenes)}", fg=COLOR_BOTON_SEC)
            
        except Exception as e:
            ultimo_titulo = ""
            ultima_url = ""
            titulo_label.config(text="⚠️ Error: No se encontró o falló la conexión", fg="red")
            texto_box.insert(tk.END, f"Verifica el término. Detalle del error: {e}")
            url_label.config(text="")
            imagen_counter.config(text="")
        finally:
            progreso_bar.stop()
            progreso_bar.config(value=0)
            boton_buscar.config(state=tk.NORMAL) 


    # --- NUEVA FUNCIÓN: Lanza el hilo de búsqueda (Hilo principal) ---
    def iniciar_busqueda():
        termino = entrada.get().strip()
        if not termino:
            messagebox.showerror("Error", "Introduce un término de búsqueda.")
            return
        
        # Deshabilitar botón y activar barra de progreso
        boton_buscar.config(state=tk.DISABLED)
        progreso_bar.start(10)
        
        titulo_label.config(text="Buscando...", fg=COLOR_ACCENTO)

        # Crear y arrancar el hilo
        busqueda_thread = threading.Thread(target=buscar_func)
        busqueda_thread.start()


    # --- Header Frame (Idioma, Entrada y Búsqueda) USANDO GRID ---
    header_frame = tk.Frame(main_card, bg=COLOR_CARD, pady=10)
    header_frame.pack(fill='x')
    
    # 1. Selector de Idioma (Columna 0)
    idioma_menu = ttk.OptionMenu(header_frame, idioma_actual, 'es', 'es', 'en', 
                                 command=lambda lang: cambiar_idioma(lang))
    idioma_menu.grid(row=0, column=0, padx=(0, 10), sticky="w")
    
    # 2. Entrada de texto (Columna 1 - Se expande)
    entrada = tk.Entry(header_frame, font=(FUENTE_PRINCIPAL, 14), 
                       fg=COLOR_PRIMARIO, bd=1, relief=tk.SOLID) 
    entrada.grid(row=0, column=1, sticky="ew", padx=10)
    entrada.bind("<Return>", lambda event: iniciar_busqueda())

    # 3. Botón de Búsqueda (Columna 2)
    boton_buscar = tk.Button(header_frame, text="Buscar 🔎", font=(FUENTE_PRINCIPAL, 12, "bold"),
                             bg=COLOR_ACCENTO, fg="white", activebackground="#0056b3", 
                             activeforeground="white", relief=tk.FLAT, padx=15, command=iniciar_busqueda)
    boton_buscar.grid(row=0, column=2, padx=(10, 0), sticky="e")
    
    header_frame.grid_columnconfigure(1, weight=1) 
    
    # Barra de Progreso
    progreso_bar = ttk.Progressbar(main_card, mode='indeterminate')
    progreso_bar.pack(fill='x', padx=10, pady=10)

    # --- Contenido del Resultado ---
    
    titulo_label = tk.Label(main_card, text="Esperando término...", 
                            font=(FUENTE_PRINCIPAL, 18, "bold"), bg=COLOR_CARD, fg=COLOR_BOTON_SEC)
    titulo_label.pack(pady=(0, 10))
    
    url_label = tk.Label(main_card, text="", font=(FUENTE_PRINCIPAL, 9, "italic"), bg=COLOR_CARD, fg=COLOR_ACCENTO)
    url_label.pack(pady=(0, 10))
    
    # --- Pestañas (Notebook) ---
    notebook = ttk.Notebook(main_card)
    notebook.pack(fill='both', expand=True, padx=10, pady=10)

    # Pestaña 1: Resumen
    resumen_tab = ttk.Frame(notebook)
    notebook.add(resumen_tab, text='📄 Resumen')
    scrollbar_resumen = ttk.Scrollbar(resumen_tab)
    scrollbar_resumen.pack(side=tk.RIGHT, fill=tk.Y)
    texto_box = tk.Text(resumen_tab, wrap="word", font=(FUENTE_PRINCIPAL, 12),
                        bg="#F9F9F9", fg=COLOR_PRIMARIO, bd=0, relief=tk.FLAT, 
                        yscrollcommand=scrollbar_resumen.set, padx=10, pady=10)
    texto_box.pack(side=tk.LEFT, fill='both', expand=True)
    scrollbar_resumen.config(command=texto_box.yview)


    # Pestaña 2: Contenido Avanzado (Tablas, Listas)
    avanzado_tab = ttk.Frame(notebook)
    notebook.add(avanzado_tab, text='📊 Tablas & Listas')
    scrollbar_avanzado = ttk.Scrollbar(avanzado_tab)
    scrollbar_avanzado.pack(side=tk.RIGHT, fill=tk.Y)
    avanzado_box = tk.Text(avanzado_tab, wrap="word", font=(FUENTE_PRINCIPAL, 12),
                           bg="#F9F9F9", fg=COLOR_PRIMARIO, bd=0, relief=tk.FLAT, 
                           yscrollcommand=scrollbar_avanzado.set, padx=10, pady=10)
    avanzado_box.pack(side=tk.LEFT, fill='both', expand=True)
    scrollbar_avanzado.config(command=avanzado_box.yview)
    
    # Pestaña 3: HTML Original (Debug)
    html_tab = ttk.Frame(notebook)
    notebook.add(html_tab, text='⚙️ HTML Crudo')
    scrollbar_html = ttk.Scrollbar(html_tab)
    scrollbar_html.pack(side=tk.RIGHT, fill=tk.Y)
    html_box = tk.Text(html_tab, wrap="word", font=("Courier New", 10),
                       bg="#333333", fg="white", bd=0, relief=tk.FLAT, 
                       yscrollcommand=scrollbar_html.set, padx=10, pady=10)
    html_box.pack(side=tk.LEFT, fill='both', expand=True)
    scrollbar_html.config(command=html_box.yview)
    
    # --- Imágenes y Acciones ---
    
    imagen_frame = tk.Frame(main_card, bg=COLOR_CARD, pady=10)
    imagen_frame.pack(pady=10)
    
    imagen_counter = tk.Label(main_card, text="", font=(FUENTE_PRINCIPAL, 9), bg=COLOR_CARD, fg=COLOR_BOTON_SEC)
    imagen_counter.pack(pady=(5, 0))

    acciones_frame = tk.Frame(main_card, bg=COLOR_CARD, pady=10)
    acciones_frame.pack(pady=(10, 0))
    
    # Botones
    boton_guardar = ttk.Button(acciones_frame, text="Guardar TXT 💾", command=guardar_func)
    boton_guardar.pack(side=tk.LEFT, padx=15)
    
    boton_abrir = ttk.Button(acciones_frame, text="Abrir en Wiki 🌐", command=abrir_func)
    boton_abrir.pack(side=tk.LEFT, padx=15)
    
    boton_limpiar_imagenes = ttk.Button(acciones_frame, text="Limpiar Imágenes 🖼️", command=limpiar_imagenes_func)
    boton_limpiar_imagenes.pack(side=tk.LEFT, padx=15)
    
    boton_limpiar = ttk.Button(acciones_frame, text="Limpiar Todo 🧹", command=limpiar_func)
    boton_limpiar.pack(side=tk.LEFT, padx=15)


    ventana.mainloop()
