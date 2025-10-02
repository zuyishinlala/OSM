import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

# Load Arlington bike graph
G = ox.graph_from_place("Arlington County, Virginia, USA", network_type="bike")

# Pick two random nodes
orig, dest = list(G.nodes())[0], list(G.nodes())[3899]

# Dijkstra shortest path by edge length
path = nx.shortest_path(G, source=orig, target=dest, weight="length")

# Path length (in meters)
length = nx.shortest_path_length(G, source=orig, target=dest, weight="length")

fig, ax = ox.plot_graph_route(
    G, path,
    route_color="blue",
    route_linewidth=4,
    node_size=0,
    show=False, close=False   # keep figure open
)

# Get coordinates of origin/destination
orig, dest = path[0], path[-1]
x_orig, y_orig = G.nodes[orig]['x'], G.nodes[orig]['y']
x_dest, y_dest = G.nodes[dest]['x'], G.nodes[dest]['y']

# Plot markers
ax.scatter(x_orig, y_orig, c="red", s=100, zorder=5, label="Origin")
ax.scatter(x_dest, y_dest, c="green", s=100, zorder=5, label="Destination")

plt.legend()
plt.show()

# fig.show()