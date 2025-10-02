import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString

# 1. 下載自行車網路
G = ox.graph_from_place("Arlington County, Virginia, USA", network_type="bike")

# 2. 定義起點和終點
origin_point = (38.8906, -77.0860)
destination_point = (38.8847, -77.0947)

# 3. 找最近節點
# orig_node = ox.distance.nearest_nodes(G, origin_point[1], origin_point[0])
# dest_node = ox.distance.nearest_nodes(G, destination_point[1], destination_point[0])

u1, v1, key1 = ox.distance.nearest_edges(G, X=origin_point[1], Y=origin_point[0])
u2, v2, key2 = ox.distance.nearest_edges(G, X=destination_point[1], Y=destination_point[0])

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

def closest_endpoint(G, u, v, point):
    pu = Point(G.nodes[u]["x"], G.nodes[u]["y"])
    pv = Point(G.nodes[v]["x"], G.nodes[v]["y"])
    return u if point.distance(pu) < point.distance(pv) else v

orig_node = closest_endpoint(G, u1, v1, snap_start)
dest_node = closest_endpoint(G, u2, v2, snap_end)

# 4. 計算最短路徑
route = nx.astar_path(G, orig_node, dest_node, weight='length')


# 5. 印出節點經緯度
print("路徑節點經緯度：")
for i, node in enumerate(route):
    node_data = G.nodes[node]
    print(f"{i+1}. 節點ID {node}: (lat, lon) = ({node_data['y']}, {node_data['x']})")


# -----------------------------
# 6. 自己畫路網 + 路徑 + 節點
# -----------------------------
fig, ax = plt.subplots(figsize=(12,12))

# 畫所有邊
edges = ox.graph_to_gdfs(G, nodes=False, edges=True)
edges.plot(ax=ax, linewidth=1, edgecolor="lightgray")

# 畫最短路徑
route_nodes = [(G.nodes[n]['x'], G.nodes[n]['y']) for n in route]
route_x, route_y = zip(*route_nodes)
ax.plot(route_x, route_y, color='red', linewidth=4, zorder=2, label='Shortest Path')

# 標示每個節點
for i, (x, y) in enumerate(route_nodes):
    ax.scatter(x, y, c='blue', s=40, zorder=3)
    ax.text(x, y, str(i+1), fontsize=8, color='black', zorder=4)  # 顯示順序號碼

# ===========================
# 顯示起點（綠色）與終點（紫色）
# ===========================
ax.scatter(origin_point[1], origin_point[0], c='green', s=80, marker='*', zorder=5, label="Origin")
ax.text(origin_point[1], origin_point[0], "Start", fontsize=10, color='green', zorder=6)

ax.scatter(destination_point[1], destination_point[0], c='purple', s=80, marker='*', zorder=5, label="Destination")
ax.text(destination_point[1], destination_point[0], "End", fontsize=10, color='purple', zorder=6)


# 自動縮放到路徑附近
margin = 0.002  # 經緯度 margin
ax.set_xlim(min(route_x)-margin, max(route_x)+margin)
ax.set_ylim(min(route_y)-margin, max(route_y)+margin)


ax.set_title("Arlington Bike Network - Shortest Path with Nodes")
plt.axis('off')
plt.legend()
plt.show()

# 7. 計算總距離
route_length = sum(G[u][v][0]['length'] for u, v in zip(route[:-1], route[1:]))
print(f"\n最短路徑距離: {route_length:.2f} 公尺")