import wikipedia
import requests
from io import BytesIO
from PIL import Image, ImageTk
from bs4 import BeautifulSoup 

# Configuración inicial
wikipedia.set_lang("es")

def cambiar_idioma(lang):
    """Cambia el idioma de búsqueda global de Wikipedia."""
    wikipedia.set_lang(lang)
    print(f"Idioma de Wikipedia cambiado a: {lang}")

def descargar_imagen(url, tamaño=(150,150)):
    """Descarga una imagen de una URL y la prepara para Tkinter, con manejo de errores."""
    try:
        data = requests.get(url, timeout=5).content
        img = Image.open(BytesIO(data))
        img = img.resize(tamaño)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error al descargar imagen desde {url}: {e}")
        return None

def extraer_contenido_avanzado(url):
    """
    Realiza un scraping avanzado para extraer tablas y listas,
    usando un User-Agent para evitar el error 403 Forbidden.
    """
    tablas_texto = "--- Tablas Extraídas ---\n"
    listas_texto = "--- Listas Desordenadas (UL) Extraídas --\n"
    html_raw = ""

    # CABECERAS NECESARIAS para evitar el error 403 Forbidden
    headers = {
        'User-Agent': 'WikiScrapp/1.0 (Python Application; Contact: user@example.com)'
    }

    try:
        # Petición con el User-Agent
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() 
        html_raw = response.text
        soup = BeautifulSoup(html_raw, 'html.parser')

        content_div = soup.find('div', id='mw-content-text')
        
        if content_div:
            # 1. Extracción de Tablas (limitamos a las primeras 3)
            tables = content_div.find_all('table', limit=3)
            if tables:
                for i, table in enumerate(tables):
                    tablas_texto += f"\n[ TABLA {i+1} ]\n"
                    
                    caption = table.find('caption')
                    if caption:
                        tablas_texto += f"Título: {caption.get_text().strip()}\n"
                        
                    for row in table.find_all(['tr']):
                        row_data = [cell.get_text(separator=' ', strip=True) for cell in row.find_all(['td', 'th'])]
                        if row_data:
                            tablas_texto += "| " + " | ".join(row_data) + " |\n"
                    tablas_texto += "\n"
            else:
                tablas_texto += "No se encontraron tablas.\n"
                
            # 2. Extracción de Listas (limitamos a las primeras 3 listas desordenadas)
            lists = content_div.find_all('ul', limit=3)
            if lists:
                for i, ul in enumerate(lists):
                    listas_texto += f"\n[ LISTA {i+1} ]\n"
                    for li in ul.find_all('li', recursive=False):
                        listas_texto += f"- {li.get_text(strip=True)}\n"
            else:
                listas_texto += "No se encontraron listas desordenadas (UL).\n"
        
        contenido_avanzado = tablas_texto + "\n" + listas_texto
        return contenido_avanzado, html_raw

    except requests.exceptions.RequestException as e:
        error_msg = f"Error de conexión al intentar obtener contenido avanzado: {e}"
        return error_msg, error_msg
    except Exception as e:
        error_msg = f"Error al procesar el contenido avanzado con BeautifulSoup: {e}"
        return error_msg, html_raw if html_raw else error_msg

def buscar_wikipedia(termino):
    """
    Realiza la búsqueda principal, manejando errores de ambigüedad/página no encontrada.
    
    Retorna 6 valores: Título, Resumen, Imágenes, URL, Contenido Avanzado, HTML Crudo.
    """
    
    try:
        # 1. Intentar obtener la página directamente
        page = wikipedia.page(termino, auto_suggest=False)
        
    except wikipedia.exceptions.DisambiguationError as e:
        # 2. Manejar términos ambiguos (e.g., "Jupiter")
        sugerencia = e.options[0]
        page = wikipedia.page(sugerencia, auto_suggest=False)
        print(f"Búsqueda ambigua, usando sugerencia: {sugerencia}")
        
    except wikipedia.exceptions.PageError:
        # 3. Manejar error de página no encontrada (e.g., error tipográfico)
        sugerencias = wikipedia.search(termino)
        if sugerencias:
            sugerencia = sugerencias[0]
            page = wikipedia.page(sugerencia, auto_suggest=False)
            print(f"Página no encontrada, usando sugerencia: {sugerencia}")
        else:
            # 4. Si no hay sugerencias, lanzar un error claro que la GUI capturará
            raise Exception(f"No se encontró ningún artículo que coincida con la búsqueda '{termino}'.")
            
    # El resto de la lógica de extracción (Parte 1)
    resumen = wikipedia.summary(page.title, sentences=3)
    imagenes = [img for img in page.images if img.lower().endswith((".jpg",".png",".jpeg"))]
    url = page.url
    
    # Parte 2: Uso del scraping avanzado
    contenido_avanzado, html_raw = extraer_contenido_avanzado(url)
    
    # Retorna los 6 valores
    return page.title, resumen, imagenes[:3], url, contenido_avanzado, html_raw
