import osmnx as ox

G_drive = ox.graph_from_place("Arlington County, Virginia, USA", network_type="drive")
nodes, edges = ox.graph_to_gdfs(G_drive)

# Each edge = one street/bike path segment
print(edges.columns)

# Show first rows (includes lat/lng geometry)
print(edges[['name', 'highway', 'length']].head())

# Save to GeoJSON (can open in QGIS or GIS tools)
edges.to_file("arlington_bike_lanes.geojson", driver="GeoJSON")