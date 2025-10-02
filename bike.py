import osmnx as ox
import matplotlib.pyplot as plt
import networkx as nx
from networkx.convert_matrix import to_scipy_sparse_array


G = ox.graph_from_place("Arlington County, Virginia, USA", network_type="bike")

A_sparse = to_scipy_sparse_array(G, weight="length")
print(A_sparse.shape)

# Pick two random nodes
orig, dest = list(G.nodes())[0], list(G.nodes())[100]

# Dijkstra shortest path by edge length
path = nx.shortest_path(G, source=orig, target=dest, weight="length")

# Path length (in meters)
length = nx.shortest_path_length(G, source=orig, target=dest, weight="length")

# nodes, edges = ox.graph_to_gdfs(G)

'''
Node columns: ['y', 'x', 'street_count', 'junction', 'highway', 'ref', 'geometry']
                  y          x  street_count junction highway  ref                    geometry
osmid                                                                                         
63327661  38.895989 -77.145820             3      NaN     NaN  NaN  POINT (-77.14582 38.89599)
63327666  38.874198 -77.127269             3      NaN     NaN  NaN   POINT (-77.12727 38.8742)
63327668  38.873346 -77.129697             4      NaN     NaN  NaN   POINT (-77.1297 38.87335)
63327674  38.880953 -77.093440             4      NaN     NaN  NaN  POINT (-77.09344 38.88095)
63327677  38.881061 -77.095503             3      NaN     NaN  NaN   POINT (-77.0955 38.88106)

Edge columns: ['osmid', 'highway', 'maxspeed', 'name', 'oneway', 'reversed', 'length', 'geometry', 'lanes', 'service', 'ref', 'width', 'bridge', 'access', 'junction', 'tunnel']
                             osmid      highway maxspeed                    name  oneway reversed  ...  ref width bridge access junction tunnel
u        v          key                                                                            ...                                         
63327661 5456374522 0      8795141  residential   25 mph   North McKinley Street   False     True  ...  NaN   NaN    NaN    NaN      NaN    NaN
         63351421   0      8797698  residential   25 mph         25th Road North   False    False  ...  NaN   NaN    NaN    NaN      NaN    NaN
         63362586   0      8797698  residential   25 mph         25th Road North   False     True  ...  NaN   NaN    NaN    NaN      NaN    NaN
63327666 63352404   0    740877054  residential      NaN  North Jefferson Street   False    False  ...  NaN   NaN    NaN    NaN      NaN    NaN
         63327668   0      8795142  residential      NaN        7th Street North   False    False  ...  NaN   NaN    NaN    NaN      NaN    NaN

[5 rows x 16 columns]

# '''
# # Show node attributes
# print("Node columns:", nodes.columns.tolist())
# print(nodes.head())

# # Show edge attributes
# print("Edge columns:", edges.columns.tolist())
# print(edges.head())


# fig, ax = ox.plot_graph(
#     G,
#     node_size=5,
#     node_color="red",
#     edge_color="gray",
#     edge_linewidth=0.5,
#     show=False,   # don’t auto-show
#     close=False   # don’t auto-close
# )

# plt.show()   # keep window open until you close it
