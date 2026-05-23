# Módulo de Frontend - Buscador de PDFs (Daniel Gil)

Este directorio contiene toda la estructura de enrutamiento base y el diseño de las interfaces de usuario para el sistema de extracción y búsqueda de documentos PDF. El diseño fue construido utilizando **Python (Flask)** para el servidor web y **Bootstrap** para la maquetación responsiva.

---

## Componentes e Interfaces Diseñadas

Actualmente, la rama `feature-frontend-vistas` tiene las siguientes vistas completamente funcionales y enlazadas a través del menú de navegación superior:

1. *** Dashboard General (`home.html`):**
   - Panel principal de control estático.
   - Muestra tarjetas de indicadores visuales para el total de documentos y palabras indexadas.
   - Desglose ordenado de documentos capturados por año (2025 y 2026).

2. *** Extractor de Documentos (`scrapper.html`):**
   - Panel de control de fuentes web.
   - Muestra el estatus dinámico visual de indexación (`scrappeada` / `no escrapeada`) mediante badges de Bootstrap.
   - Relación visual del árbol de archivos PDF descargados asociados a cada URL origen.

3. *** Configuración del Sistema (`configuration.html`):**
   - Formulario limpio para la captura de nuevas direcciones URL de origen.
   - Botón de acción rápido ("ADD").
   - Tabla base en la parte inferior para visualizar las fuentes que ya están dadas de alta.

4. *** Resultados de la Búsqueda (`search.html`):**
   - Despliegue estático de fragmentos de texto coincidentes según la palabra buscada.
   - Mapeo de URL origen de los PDFs con fuente monoespaciada para facilitar la lectura de las rutas.
   - **Punto Extra Implementado:** Slider interactivo de escala 0.00 a 1.00 para pre-configurar el rango mínimo de similitud por Levenshtein.

---

## Cómo Ejecutar y Probar el Frontend Localmente

Para levantar el servidor y navegar de forma interactiva por las pantallas, sigue estos pasos en tu terminal:

1. **Asegúrate de tener instalada la librería de Flask:**
   ```bash
   pip install flask
