import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random
import heapq as h
def create_graph():
    graph = nx.Graph()

    # Locations
    locations = {
        "Gate": (8, 14),        
        "Pharmacy": (10, 13),    
        "Basketball": (12, 8),   
        "BoysHostel": (12, 10),  
        "Sports": (14, 8),       
        "Canteen": (14, 6),     
        "Administration": (10, 8),  
        "ECE1": (6, 10),
        "ECE2": (8, 8),
        "Polytechnic": (8, 6),
        "Placements": (10, 4),   
        "BSH": (8, 2),
        "CSE1": (2, 8),          
        "CSE2": (0, 8),          
        "MECH": (0, 6),         
        "EEE": (2, 6),           
        "AIML": (2, 4),
        "Civil": (0, 4),         
        "GirlsHostel": (0, 2),
        "CAI": (4, 4),           
        "SaraswatiHimataStatue": (4, 7),  
        "ECE1_Saraswati": (5, 8), 
        "BusArea": (8, 0)
}


    for loc, pos in locations.items():
        graph.add_node(loc, pos=pos)

    edges = [
        ("Gate", "Pharmacy"), ("Gate", "ECE2"),
        ("Gate", "Administration"), ("Gate", "Basketball"),
        ("Pharmacy", "BoysHostel"), ("BoysHostel", "Basketball"),
        ("BoysHostel", "Sports"), ("Sports", "Canteen"),
        ("Administration", "Basketball"), ("Basketball", "Sports"),
        ("ECE1", "Administration"), ("ECE1", "ECE2"),
        ("ECE2", "Polytechnic"), ("Polytechnic", "Placements"),
        ("Placements", "BSH"), ("BSH", "BusArea"),
        ("ECE2", "SaraswatiHimataStatue"), ("Polytechnic", "SaraswatiHimataStatue"),
        ("SaraswatiHimataStatue", "CAI"), ("CAI", "BSH"), ("CAI", "BusArea"),
        ("ECE1", "CSE1"), ("CSE1", "EEE"), ("EEE", "AIML"), ("AIML", "CAI"),
        ("CSE1", "SaraswatiHimataStatue"), ("EEE", "SaraswatiHimataStatue"),
        ("GirlsHostel", "CAI"), ("Civil", "AIML"), ("MECH", "EEE"), ("CSE2", "CSE1"),
        ("CSE2", "MECH"), ("MECH", "Civil"), ("Civil", "GirlsHostel"),
        ("CSE1", "EEE"), ("Polytechnic", "Canteen"), ("Placements", "Canteen"), ("BSH", "Canteen"),
        ("ECE1", "ECE1_Saraswati"),("Gate","CSE2"),("Gate","CSE1"),
        ("Gate","ECE1"),("ECE1_Saraswati", "SaraswatiHimataStatue") 
    ]



    for edge in edges:
        graph.add_edge(*edge, weight=random.randint(1, 20))  # Random weight between 1 and 20

    return graph, locations

def visualize_graph(graph, path):
    pos = nx.get_node_attributes(graph, 'pos')
    plt.figure(figsize=(12, 8))

    # Customizing node colors
    node_colors = ['lightblue' if node not in path else 'red' for node in graph.nodes]

    nx.draw_networkx_nodes(graph, pos, node_size=1000, node_color=node_colors)
    nx.draw_networkx_edges(graph, pos, width=1.5)
    nx.draw_networkx_labels(graph, pos, font_size=8, font_weight='bold')

    # Draw edge weights with increased font size
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=10, font_color='blue')  # Increased font size to 10 and added color

    if path:
        path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='red', width=3)

    plt.title("Campus Navigation System", fontsize=14)
    st.pyplot(plt)


def find_shortest_path(graph, start, end):
    try:
        path = nx.astar_path(graph, start, end, heuristic=lambda u, v: heuristic(graph, u, v), weight='weight')
        return path
    except nx.NetworkXNoPath:
        return []

def heuristic(graph, u, v):
    x1, y1 = graph.nodes[u]['pos']
    x2, y2 = graph.nodes[v]['pos']
    return ((x1 - x2)*2 + (y1 - y2)*2)*0.5

def main():
    st.title("Sri Vasavi Engineering College Route Map")
    st.sidebar.header("Navigation System")

    graph, locations = create_graph()

    start = st.sidebar.selectbox("Select Your Current Location", list(locations.keys()))
    end = st.sidebar.selectbox("Select Your Destination", list(locations.keys()))

    if st.sidebar.button("Find Shortest Path"):
        if start == end:
            st.warning("Source and destination cannot be the same.")
        else:
            path = find_shortest_path(graph, start, end)
            if path:
                st.success(f"Shortest Path: {' -> '.join(path)}")
                visualize_graph(graph, path)
            else:
                st.error("No path found between the selected locations.")

if __name__ == "__main__":
    main()
