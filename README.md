# PathGuard: Búsqueda de Caminos Óptimos y Seguros en Redes de Nodos

## Descripción
**PathGuard** es una aplicación interactiva que permite encontrar caminos en una red de nodos según tres criterios principales:
1. **Camino más corto**: Minimiza la distancia total entre dos puntos.
2. **Camino más seguro**: Prioriza las rutas con menor índice de inseguridad.
3. **Camino óptimo**: Encuentra un balance entre distancia y seguridad usando un modelo ponderado.

La aplicación combina una interfaz gráfica intuitiva con visualización de mapas interactivos generados en HTML. Está diseñada para ser utilizada en aplicaciones urbanas, análisis de rutas, y sistemas de navegación personalizados.

## Características
- **Interfaz gráfica**: Basada en `tkinter`, permite seleccionar nodos de inicio y destino de forma sencilla.
- **Algoritmos avanzados**: Utiliza algoritmos basados en Dijkstra adaptados a diferentes criterios de optimización.
- **Visualización en mapas**: Genera mapas interactivos usando `folium` para mostrar rutas y detalles como distancia y seguridad.
- **Personalización**:
  - Ponderación configurable entre distancia y seguridad en el cálculo de rutas óptimas.
  - Datos cargados dinámicamente desde un archivo CSV.

## Requisitos
- Python 3.8 o superior.
- Bibliotecas requeridas:
  - `tkinter`
  - `networkx`
  - `pandas`
  - `folium`
  - `heapq`
