import osmnx as ox
# from osmnx.distance import euclidean_dist_vec
import networkx as nx
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString

place = "Arlington County, Virginia, USA"
G = ox.graph_from_place(place, network_type="bike")

start_x, start_y = -77.095, 38.88
end_x, end_y   = -77.07, 38.87

# key: (u, v, key):
# u start OSMID node
# v end OSMID node
# key == 0 is drive, key == 1 means bike
u1, v1, key1 = ox.distance.nearest_edges(G, X=start_x, Y=start_y)
u2, v2, key2 = ox.distance.nearest_edges(G, X=end_x, Y=end_y)

# print("Start edge:", u1, v1, key1)
# print("End edge:", u2, v2, key2)
# geometry: a curve, else a straight line
def snap_point_to_edge(G, u, v, key, x, y):
    edge_data = G[u][v][key]
    if "geometry" in edge_data:
        line = edge_data["geometry"]
    else:
        line = LineString([(G.nodes[u]["x"], G.nodes[u]["y"]),
                           (G.nodes[v]["x"], G.nodes[v]["y"])])
    point = Point(x, y)
    return line.interpolate(line.project(point))

snap_start = snap_point_to_edge(G, u1, v1, key1, start_x, start_y)
snap_end   = snap_point_to_edge(G, u2, v2, key2, end_x, end_y)

print("Snapped start:", snap_start.x, snap_start.y)
print("Snapped end:", snap_end.x, snap_end.y)

# # ------------------------
# # 5. Pick closest node in the line
# # ------------------------
def closest_endpoint(G, u, v, point):
    pu = Point(G.nodes[u]["x"], G.nodes[u]["y"])
    pv = Point(G.nodes[v]["x"], G.nodes[v]["y"])
    return u if point.distance(pu) < point.distance(pv) else v

orig = closest_endpoint(G, u1, v1, snap_start)
dest = closest_endpoint(G, u2, v2, snap_end)

# ------------------------
# 6. Run A* shortest path
# ------------------------
def euclidean_heuristic(u, v):
    dx = G.nodes[u]["x"] - G.nodes[v]["x"]
    dy = G.nodes[u]["y"] - G.nodes[v]["y"]
    return (dx**2 + dy**2) ** 0.5

route = nx.astar_path(G, source=orig, target=dest,
                      heuristic=euclidean_heuristic, weight="length")

# ------------------------
# 7. Visualize the route
# ------------------------
fig, ax = ox.plot_graph_route(
    G, route,
    route_color="blue",
    route_linewidth=3,
    node_size=0,
    show=False, close=False
)

# Add snapped points
ax.scatter(snap_start.x, snap_start.y, c="red", s=100, zorder=5, label="Start")
ax.scatter(snap_end.x, snap_end.y, c="green", s=100, zorder=5, label="End")

plt.legend()
plt.show()
