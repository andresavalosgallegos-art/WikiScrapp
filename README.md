# WikiScrapp 🧠🔍

WikiScrapp es una aplicación de escritorio hecha en **Python + Tkinter** que permite buscar información en **Wikipedia** de manera rápida, sencilla y visual. Solo escribes lo que quieres (por ejemplo: *Pingüinos*, *Python*, *Historia de Chile*) y la app muestra:

* 📝 Un resumen corto
* 🖼️ Imágenes relacionadas
* 🔗 Enlace directo al artículo
* 💾 Opción para guardar el texto

Además, es **liviano**, **modular** y con una interfaz mejorada.

---

## 🚀 Características

* ✔️ Interfaz gráfica con Tkinter
* ✔️ Búsqueda rápida en Wikipedia
* ✔️ Muestra imágenes del artículo
* ✔️ Modo modular (archivos separados por lógica)
* ✔️ Exportar resumen a .txt
* ✔️ Ejecutable para Windows (.exe)

---

## 🧩 Estructura del proyecto

```
WikiScrapp/
│
├─ main.py              # Inicio de la app
├─ gui/                 # Interfaz
│   ├─ gui.py
│   └─ assets/          # Imágenes locales
├─ core/                # Lógica interna
│   ├─ wiki_api.py
│   └─ utils.py
└─ README.md
```

---

## 📦 Instalación (Código Fuente)

Clona el repositorio:

```
git clone https://github.com/andresavalosgallegos-art/WikiScrapp.git
cd WikiScrapp
```

Instala las dependencias:

```
pip install -r requirements.txt
```

Ejecuta la aplicación:

```
python main.py
```

---

## 🖥️ Ejecutable (.EXE)

Puedes descargar la versión compilada para Windows desde la sección **Releases**:

👉 [https://github.com/andresavalosgallegos-art/WikiScrapp/releases](https://github.com/andresavalosgallegos-art/WikiScrapp/releases)

Solo descarga el archivo `.exe` y ejecútalo. ¡No necesitas instalar Python!

---

## 🛠️ Cómo compilar tu propio .EXE

Instala PyInstaller:

```
pip install pyinstaller
```

Compila:

```
pyinstaller --onefile --windowed main.py
```

El ejecutable aparecerá dentro de:

```
dist/main.exe
```

---

## 🌐 Página Web del Proyecto

Puedes ver la página del repositorio aquí:

👉 [https://github.com/andresavalosgallegos-art/WikiScrapp/tree/main](https://github.com/andresavalosgallegos-art/WikiScrapp/tree/main)

Ideal para documentación, descargas y futuras actualizaciones.

---

## 👨‍💻 Autor

Desarrollado por **Andrés Santiago Ávalos Gallegos**.

---

## 📜 Licencia

MIT — libre para usar, modificar y compartir.
