import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Initialize the Graph with Custom Layout
def create_graph():
    graph = nx.Graph()

    # Node positions manually set to match the route map
    locations = {
        "Gate": (8, 8),
        "Pharmacy": (10, 8),
        "Basketball": (8, 6),
        "BoysHostel": (10, 6),
        "Sports": (10, 4),
        "Canteen": (10, 2),
        "Administration": (6, 8),
        "ECE1": (4, 6),
        "ECE2": (6, 4),
        "Polytechnic": (6, 2),
        "Placements": (6, 0),
        "BSH": (6, -2),
        "CSE1": (2, 6),
        "CSE2": (0, 8),
        "MECH": (0, 6),
        "EEE": (0, 4),
        "AIML": (0, 2),
        "Civil": (-2, 4),
        "GirlsHostel": (-2, 0),
        "CAI": (2, 0),
        "SaraswatiHimataStatue": (6, 6),
        "BusArea": (6, -4)
    }

    # Add nodes with positions
    for loc, pos in locations.items():
        graph.add_node(loc, pos=pos)

    # Add edges to match the route map
    edges = [
        ("Gate", "Pharmacy"), ("Gate", "Basketball"), ("Gate", "Administration"),
        ("Pharmacy", "BoysHostel"), ("Basketball", "BoysHostel"), ("Basketball", "Sports"),
        ("Sports", "Canteen"), ("ECE1", "ECE2"), ("ECE2", "SaraswatiHimataStatue"),
        ("ECE1", "CSE1"), ("CSE1", "CSE2"), ("CSE1", "MECH"),
        ("MECH", "EEE"), ("EEE", "AIML"), ("AIML", "Civil"), ("Civil", "GirlsHostel"),
        ("GirlsHostel", "CAI"), ("CAI", "BusArea"), ("Polytechnic", "Placements"),
        ("Placements", "BSH"), ("SaraswatiHimataStatue", "Polytechnic")
    ]

    # Adding edges to the graph
    graph.add_edges_from(edges)

    return graph, locations

# Visualization of the Graph with Custom Node Shapes
def visualize_graph(graph, path):
    pos = nx.get_node_attributes(graph, 'pos')
    plt.figure(figsize=(12, 8))

    # Draw nodes
    nx.draw_networkx_nodes(graph, pos, node_size=500, node_color='lightblue')

    # Draw edges
    nx.draw_networkx_edges(graph, pos, width=1.5)

    # Draw labels
    nx.draw_networkx_labels(graph, pos, font_size=10, font_weight='bold')

    # Highlight the path if one exists
    if path:
        path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='red', width=3)

    plt.title("Campus Navigation System")
    st.pyplot(plt)

# Finding Shortest Path Using A*
def find_shortest_path(graph, start, end):
    try:
        path = nx.astar_path(graph, start, end, heuristic=lambda u, v: heuristic(graph, u, v), weight='weight')
        return path
    except nx.NetworkXNoPath:
        return []

# Heuristic Function for A* (Euclidean Distance)
def heuristic(graph, u, v):
    x1, y1 = graph.nodes[u]['pos']
    x2, y2 = graph.nodes[v]['pos']
    return ((x1 - x2)*2 + (y1 - y2)*2)*0.5

# Streamlit Application
def main():
    st.title("Sri Vasavi Engineering College Route Map")
    st.sidebar.header("Navigation System")

    # Create the graph
    graph, locations = create_graph()

    # User input for start and destination
    start = st.sidebar.selectbox("Select Your Current Location", list(locations.keys()))
    end = st.sidebar.selectbox("Select Your Destination", list(locations.keys()))

    # Find and display the shortest path
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

if __name__ == "_main_":
    main()