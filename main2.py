import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import networkx as nx
import heapq
from math import radians, sin, cos, sqrt, atan2
import folium

# funcion para la formula del haversine
def haversine(coord1, coord2):
    R = 6371.0  # Radio de la Tierra en kilómetros

    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance
def calculate_score(distance, security):
    # Ajusta estos pesos según la importancia relativa que quieras darle a la distancia y la seguridad
    distance_weight = 0.4
    security_weight = 0.6

    # Calcula el puntaje combinado
    score = distance_weight * distance + security_weight * security
    return score
def dijkstra_optimal_path(G, start, goal):
    queue = [(0, start, [])]
    seen = set()
    
    while queue:
        (score, node, path) = heapq.heappop(queue)
        
        if node in seen:
            continue
        
        path = path + [node]
        seen.add(node)
        
        if node == goal:
            return score, path
        
        for next_node, data in G[node].items():
            if next_node not in seen:
                distance = data['distance']
                security = data['seguridad']
                edge_score = calculate_score(distance, security)
                heapq.heappush(queue, (score + edge_score, next_node, path))
    
    return float("inf"), []
def find_optimal_path(G, start, goal):
    score, path = dijkstra_optimal_path(G, start, goal)
    
    if path:
        path_str = ' -> '.join(map(str, path))
        print(f"Camino óptimo (Puntaje combinado): {path_str}. Puntaje total: {score:.2f}")
    else:
        print("No se encontró un camino válido entre los nodos seleccionados.")

# funcion para calcular el camino mas corto usando Dijkstra
def dijkstra_shortest_path(G, start, goal):
    queue = [(0, start, [])]
    seen = set()
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node in seen:
            continue
        path = path + [node]
        seen.add(node)
        if node == goal:
            return cost, path
        for next_node, data in G[node].items():
            if next_node not in seen:
                heapq.heappush(queue, (cost + data['distance'], next_node, path))
    return float("inf"), []
def dijkstra_safest_path(G, start, goal):
    queue = [(0, start, [])]
    seen = set()
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node in seen:
            continue
        path = path + [node]
        seen.add(node)
        if node == goal:
            return cost, path
        for next_node, data in G[node].items():
            if next_node not in seen:
                heapq.heappush(queue, (max(cost, data['seguridad']), next_node, path))
    return float("inf"), []
def find_safest_path(G, start, goal):
    cost, path = dijkstra_safest_path(G, start, goal)
    return cost, path
# Función que maneja la busqueda del camino mas corto 
def find_shortest_path(G, start, goal):
    cost, path = dijkstra_shortest_path(G, start, goal)
    return cost, path
# Función para manejar el botón de búsqueda de camino más seguro
def find_safest_path_button():
    start = node_start_var.get()
    goal = node_goal_var.get()

    try:
        start = int(start)
        goal = int(goal)
        cost, path = find_safest_path(G, start, goal)
        if path:
            path_str = ' -> '.join(map(str, path))
            result_label.config(text=f"Camino más seguro: {path_str}. Seguridad máxima: {cost:.2f}")

            # Generar y guardar el mapa HTML del camino más seguro
            generate_map(path)

            # Abrir el archivo HTML generado
            import webbrowser
            webbrowser.open_new_tab('caminoresult.html')

            # Mostrar mensaje en la consola
            print("Resultado generado (camino más seguro)")

        else:
            result_label.config(text="No se encontró un camino válido entre los nodos seleccionados.")
    except ValueError:
        messagebox.showerror("Error", "Por favor selecciona nodos válidos.")
# Función para manejar el botón de búsqueda de camino óptimo
def find_optimal_path_button():
    start = node_start_var.get()
    goal = node_goal_var.get()

    try:
        start = int(start)
        goal = int(goal)
        score, path = dijkstra_optimal_path(G, start, goal)
        
        if path:
            path_str = ' -> '.join(map(str, path))
            print(f"Camino óptimo (Puntaje combinado): {path_str}. Puntaje total: {score:.2f}")
            
            # Generar y guardar el mapa HTML del camino óptimo
            generate_map(path)

            # Abrir el archivo HTML generado
            import webbrowser
            webbrowser.open_new_tab('caminoresult.html')

        else:
            print("No se encontró un camino válido entre los nodos seleccionados.")
            messagebox.showerror("Error", "No se encontró un camino válido entre los nodos seleccionados.")
    
    except ValueError:
        messagebox.showerror("Error", "Por favor selecciona nodos válidos.")

# al presionar el boton de buscar camino corto
def find_path():
    start = node_start_var.get()
    goal = node_goal_var.get()

    try:
        start = int(start)
        goal = int(goal)
        cost, path = find_shortest_path(G, start, goal)
        if path:
            path_str = ' -> '.join(map(str, path))
            result_label.config(text=f"Camino más corto: {path_str}. Costo total: {cost:.2f} km.")

            # Generar y guardar el mapa HTML del camino más corto
            generate_map(path)

            # Abrir el archivo HTML generado
            import webbrowser
            webbrowser.open_new_tab('caminoresult.html')

            # Mostrar mensaje en la consola
            print("Resultado generado")

        else:
            result_label.config(text="No se encontró un camino válido entre los nodos seleccionados.")
    except ValueError:
        messagebox.showerror("Error", "Por favor selecciona nodos válidos.")

# crear el grafo apartir del csv
def create_graph_from_csv(filename):
    df = pd.read_csv(filename)
    G = nx.Graph()

    for index, row in df.iterrows():
        coord1 = (row['coord1lat1'], row['coord1lat2'])
        coord2 = (row['coord2lat1'], row['coord2lat2'])
        distance = row['Distancia']
        seguridad = row['Seguridad']
        calle = row['Calle']
        
        # Agregar nodos al grafo con sus atributos
        G.add_node(row['Nodo1'], coord1lat1=coord1[0], coord1lat2=coord1[1])
        G.add_node(row['Nodo2'], coord1lat1=coord2[0], coord1lat2=coord2[1])
        
        # Agregar arista entre los nodos con atributos adicionales
        G.add_edge(row['Nodo1'], row['Nodo2'], distance=float(distance), seguridad=seguridad, calle=calle)

    return G

# genera el mapa en html
def generate_map(path):
    m = folium.Map(location=lima_coords, zoom_start=14)

    for i in range(len(path) - 1):
        node1 = path[i]
        node2 = path[i + 1]

        # Obtener coordenadas de los nodos
        coord1 = (G.nodes[node1]['coord1lat1'], G.nodes[node1]['coord1lat2'])
        coord2 = (G.nodes[node2]['coord1lat1'], G.nodes[node2]['coord1lat2'])

        # Calcular la distancia entre los nodos
        distance = haversine(coord1, coord2)
        distance_text = f"{distance:.2f} km"

        # Añadir línea que conecta los dos nodos con el nombre de la calle como popup
        folium.PolyLine(
            locations=[coord1, coord2],
            color='blue',
            weight=5,
            popup=f"Calle: {G[node1][node2]['calle']}, Seguridad: {G[node1][node2]['seguridad']}, Distancia: {distance_text}"
        ).add_to(m)

        # Añadir marcadores para cada nodo del camino
        folium.Marker(coord1, popup=f"Nodo {node1}").add_to(m)
        folium.Marker(coord2, popup=f"Nodo {node2}").add_to(m)

    # Guardar el mapa en un archivo HTML
    m.save('caminoresult.html')

    # Imprimir mensaje en consola
    print("Resultado generado")


# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Buscar Camino Más Corto")

# Variables para almacenar los nodos de inicio y destino seleccionados
node_start_var = tk.StringVar(root)
node_goal_var = tk.StringVar(root)

# Frame principal
main_frame = ttk.Frame(root, padding="20")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Etiquetas y desplegables para seleccionar nodos de inicio y destino
ttk.Label(main_frame, text="Nodo de inicio:").grid(row=0, column=0, padx=5, pady=5)
node_start_combo = ttk.Combobox(main_frame, textvariable=node_start_var, width=5)
node_start_combo.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(main_frame, text="Nodo de destino:").grid(row=1, column=0, padx=5, pady=5)
node_goal_combo = ttk.Combobox(main_frame, textvariable=node_goal_var, width=5)
node_goal_combo.grid(row=1, column=1, padx=5, pady=5)

# Botón para buscar el camino más corto
find_button = ttk.Button(main_frame, text="Buscar Camino Más Corto", command=find_path)
find_button.grid(row=2, column=0, columnspan=2, pady=10)

find_safest_button = ttk.Button(main_frame, text="Buscar Camino Más Seguro", command=find_safest_path_button)
find_safest_button.grid(row=4, column=0, columnspan=2, pady=10)

find_optimal_button = ttk.Button(main_frame, text="Buscar Camino Óptimo (Puntaje combinado)", command=find_optimal_path_button)
find_optimal_button.grid(row=5, column=0, columnspan=2, pady=10)

# Etiqueta para mostrar el resultado del camino más corto
result_label = ttk.Label(main_frame, text="")
result_label.grid(row=3, column=0, columnspan=2, pady=10)

# Crear el grafo desde el archivo CSV
filename = 'conexiones.csv'
G = create_graph_from_csv(filename)

# Obtener la lista de nodos únicos para los desplegables
nodes = sorted(G.nodes())
node_start_combo['values'] = nodes
node_goal_combo['values'] = nodes

# Coordenadas del centro de Lima
lima_coords = [-12.046374, -77.042793]

# Ejecutar la aplicación
root.mainloop()
  