import rasterio
import rioxarray
import matplotlib.pyplot as plt
import osmnx as ox


slope = rioxarray.open_rasterio("Arlington.tif")
slope_data = slope[0]

G = ox.graph_from_place("Arlington County, Virginia, USA", network_type="bike")
nodes, edges = ox.graph_to_gdfs(G)

edges = edges.to_crs(slope.rio.crs)

# 4. Plot slope with bike edges overlay
fig, ax = plt.subplots(figsize=(12, 12))
slope_data.plot(ax=ax, cmap="terrain", alpha=0.6)
edges.plot(ax=ax, color="blue", linewidth=0.5)

plt.title("Arlington Slope Map with Bike Network Overlay", fontsize=14)
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()