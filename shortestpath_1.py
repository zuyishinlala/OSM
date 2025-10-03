import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString
from geopy.distance import geodesic

# 1. 下載自行車網路
G = ox.graph_from_place("Arlington County, Virginia, USA", network_type="bike")

# 2. 起點和終點 (故意不在節點上)
origin_point = (38.8890, -77.0850)
destination_point = (38.8860, -77.0920)

# 3. 找最近邊
u1, v1, key1 = ox.distance.nearest_edges(G, X=origin_point[1], Y=origin_point[0])
u2, v2, key2 = ox.distance.nearest_edges(G, X=destination_point[1], Y=destination_point[0])

# 4. 把點投影到邊上 (snap)
def snap_point_to_edge(G, u, v, key, x, y):
    edge_data = G[u][v][key]
    if "geometry" in edge_data:
        line = edge_data["geometry"]
    else:
        line = LineString([(G.nodes[u]["x"], G.nodes[u]["y"]),
                           (G.nodes[v]["x"], G.nodes[v]["y"])])
    point = Point(x, y)
    return line.interpolate(line.project(point))

snap_start = snap_point_to_edge(G, u1, v1, key1, origin_point[1], origin_point[0])
snap_end   = snap_point_to_edge(G, u2, v2, key2, destination_point[1], destination_point[0])

# 5. 臨時在圖上加入 snap node
temp_start_node = max(G.nodes) + 1
temp_end_node   = max(G.nodes) + 2
G.add_node(temp_start_node, x=snap_start.x, y=snap_start.y)
G.add_node(temp_end_node, x=snap_end.x, y=snap_end.y)

# 6. 分割原邊，插入 snap node
def split_edge_with_snap(G, u, v, key, snap_node):
    edge = G[u][v][key]
    total_len = edge.get("length", geodesic(
        (G.nodes[u]["y"], G.nodes[u]["x"]), (G.nodes[v]["y"], G.nodes[v]["x"])
    ).meters)
    
    u_point = Point(G.nodes[u]["x"], G.nodes[u]["y"])
    v_point = Point(G.nodes[v]["x"], G.nodes[v]["y"])
    snap_point = Point(G.nodes[snap_node]["x"], G.nodes[snap_node]["y"])
    
    d_total = u_point.distance(v_point)
    d_u = u_point.distance(snap_point)
    d_v = v_point.distance(snap_point)
    
    G.remove_edge(u, v, key)
    G.add_edge(u, snap_node, length=total_len*d_u/d_total)
    G.add_edge(snap_node, v, length=total_len*d_v/d_total)

split_edge_with_snap(G, u1, v1, key1, temp_start_node)
split_edge_with_snap(G, u2, v2, key2, temp_end_node)

# 7. 計算最短路徑
route = nx.astar_path(G, temp_start_node, temp_end_node, weight="length")
route_length = sum(G[u][v][0]["length"] for u, v in zip(route[:-1], route[1:]))
print(f"總路徑距離: {route_length:.2f} m")

# 8. 畫圖
fig, ax = plt.subplots(figsize=(12,12))

# 畫所有邊
edges = ox.graph_to_gdfs(G, nodes=False, edges=True)
edges.plot(ax=ax, linewidth=1, edgecolor="lightgray")

# 畫路徑
route_nodes = [(G.nodes[n]['x'], G.nodes[n]['y']) for n in route]
route_x, route_y = zip(*route_nodes)
ax.plot(route_x, route_y, color='red', linewidth=4, zorder=3, label="Shortest Path")

# 畫 snap 節點
ax.scatter(snap_start.x, snap_start.y, c='green', s=100, marker='*', label="Snap Start")
ax.scatter(snap_end.x, snap_end.y, c='purple', s=100, marker='*', label="Snap End")

# 畫原始起點/終點
ax.scatter(origin_point[1], origin_point[0], c='blue', s=60, marker='o', label="Origin (GPS)")
ax.scatter(destination_point[1], destination_point[0], c='orange', s=60, marker='o', label="Destination (GPS)")

# 標註路徑節點編號
for i, (x, y) in enumerate(route_nodes):
    ax.scatter(x, y, c='black', s=20)
    ax.text(x, y, str(i+1), fontsize=8, color='black')

# 自動縮放
margin = 0.002
ax.set_xlim(min(route_x)-margin, max(route_x)+margin)
ax.set_ylim(min(route_y)-margin, max(route_y)+margin)
plt.axis('off')
plt.legend()
plt.title("Shortest Path with Snap Nodes")
plt.show()