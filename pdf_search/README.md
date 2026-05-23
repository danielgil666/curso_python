  Sistema de Búsqueda de Textos en Documentos PDF

Este proyecto consiste en un sistema web completo (Frontend y Backend) desarrollado en **Python con Flask** y estilizado con el Framework **Bootstrap 5**. El objetivo principal de la aplicación es indexar documentos PDF desde diversas fuentes web, extraer su contenido de texto (con soporte avanzado de OCR para imágenes) y permitir realizar búsquedas difusas utilizando el algoritmo de **Distancia de Levenshtein** con precisión de hasta 3 dígitos decimales.

Proyecto desarrollado para la materia de Desarrollo de Sistemas, Universidad de Sonora (2026-1).

---

## 👥 Integrantes del Equipo
* **José Emmanuel Gallegos Mazariego**
* **Daniel Gil**

---

## 🚀 Características del Sistema

El sistema está estructurado bajo una arquitectura limpia y modular que divide las responsabilidades del Backend (Base de Datos, Scrapper y Motor Algorítmico) y el Frontend (Vistas e Interfaces dinámicas con Jinja2).

### 1. Panel de Inicio (Home Dashboard)
* **Métricas Globales:** Muestra en tiempo real el total de documentos actualmente indexados en el sistema y la suma acumulada de todas las palabras procesadas.
* **Agrupación Cronológica:** Presenta un desglose dinámico del número total de documentos clasificados por año de publicación (ej. `Año 2026: 6 documentos`), construido mediante consultas agregadas en la base de datos (`COUNT` y `GROUP BY`).

### 2. Extractor de Documentos (Scrapper Panel)
* **Monitoreo de Fuentes:** Muestra un listado interactivo de todas las direcciones web configuradas en el sistema junto con su estatus de procesamiento (`no escrapeada` / `scrappeada`).
* **Procesamiento Asíncrono:** Cada fuente cuenta con un botón dedicado para iniciar la extracción. Para garantizar una experiencia de usuario óptima y evitar bloqueos en la interfaz web, el proceso de raspado, descarga y análisis de PDFs se ejecuta en hilos secundarios en segundo plano (`threading`).
* **Jerarquía de Archivos:** Inmediatamente debajo de cada dirección web, la interfaz renderiza la lista con los nombres de todos los archivos PDF que han sido descargados y procesados de forma exclusiva desde esa fuente.

### 3. Panel de Configuración (Configuration)
* **Gestión Dinámica de URLs:** Incluye un formulario de entrada validado para registrar de forma persistente nuevas direcciones web (`URLs`) en el sistema.
* **Persistencia Inmediata:** Al añadir una nueva fuente, esta se inserta automáticamente en la base de datos local y pasa a estar disponible de forma inmediata en el panel de control del Scrapper.

### 4. Motor de Búsqueda Avanzado con Levenshtein
* **Algoritmo de Ventana Móvil (Sliding Window):** Para resolver las limitaciones tradicionales de Levenshtein al comparar cadenas de longitudes dispares, el backend divide los bloques de texto indexados y desplaza una "ventana" del tamaño exacto de la consulta palabra por palabra, garantizando coincidencias exactas y parciales de alta precisión.
* **Filtro Interactiva (Similitud Slider):** La página de resultados (`/search`) incorpora un control deslizante (*Slider HTML5*) que permite ajustar en tiempo real el umbral mínimo de coincidencia matemática deseada (donde `0` representa similitud nula y `1` indica identidad absoluta).
* **Formato de Resultados Estricto:** Cada resultado detectado se despliega en una tarjeta dinámica de Bootstrap que incluye de forma explícita:
    * La URL de procedencia del documento original como un enlace directo e hipervínculo funcional.
    * El bloque o fragmento de contexto textual exacto donde ocurrió el hallazgo.
    * El porcentaje matemático exacto de similitud con un formato riguroso de **hasta 3 dígitos decimales**.
    * Codificación por colores visuales (*badges* verde, amarillo y rojo) según la confianza y proximidad de la coincidencia.

### 5. Característica Extra: Soporte Óptico de Caracteres (OCR)
* **Procesamiento de Renders de Imagen:** El extractor integra un flujo híbrido utilizando **PyMuPDF (`fitz`)** para la lectura nativa de texto digital. En caso de detectar páginas vacías o compuestas por renders de imagen escaneados, el sistema activa automáticamente un fallback hacia **Tesseract OCR (`pytesseract`)** con el paquete de idioma en español (`spa`), garantizando la extracción e indexación del 100% de los documentos.

---

## 🛠️ Arquitectura de la Base de Datos (SQLite)

La persistencia de datos está centralizada en un archivo local relacional (`database/searcher.db`) con tres entidades principales optimizadas con llaves foráneas:

1.  **`urls`**: Almacena las direcciones base del scraping, identificadores únicos y el estado del procesamiento del sitio.
2.  **`documents`**: Guarda la relación de los archivos PDF descargados, vinculados a su URL de origen, registrando metadatos analizados como el nombre del archivo, año de publicación detectado por expresiones regulares (`regex`) y el conteo total de palabras.
3.  **`document_blocks`**: Almacena el texto completo de los documentos segmentado en bloques estructurados para agilizar el rendimiento de las operaciones matemáticas de comparación en el motor de búsqueda.

---

## 💻 Requisitos e Instalación

### Requisitos del Sistema
* Python 3.10 o superior
* **Tesseract OCR** instalado en el sistema operativo básico.
    * *En macOS (vía Homebrew):* `brew install tesseract tesseract-lang`
    * *En Ubuntu/Linux:* `sudo apt install tesseract-ocr tesseract-ocr-spa`

### Instalación del Proyecto

1. **Clonar el repositorio:**
