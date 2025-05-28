from pathlib import Path

from matplotlib import cm, pyplot as plt
from shapely.geometry.point import Point
import networkx as nx
import geojson

def read_graph_file(filename: str | Path = "graph_data.geojson") -> nx.Graph:
    """
    Read a GeoJSON file into a NetworkX graph, preserving node and edge attributes.

    Parameters:
    - filename: Name of the GeoJSON file to read.

    Returns:
    - G: NetworkX graph with spatial data.
    """
    G = nx.Graph()

    with open(filename, "r") as f:
        data = geojson.load(f)

    # Process each feature in the GeoJSON
    for feature in data["features"]:
        if feature["geometry"]["type"] == "Point":
            # Node feature
            node_id = feature["properties"].pop("id")
            x, y = feature["geometry"]["coordinates"]
            # Ensure no duplicate 'x' and 'y' in properties
            feature["properties"].pop("x", None)
            feature["properties"].pop("y", None)
            feature["properties"].pop("position", None)

            # Add node with position and other properties
            G.add_node(node_id, position = Point(x,y), **feature["properties"])
        elif feature["geometry"]["type"] == "LineString":
            # Edge feature
            source = feature["properties"].pop("source")
            target = feature["properties"].pop("target")
            pixel_list = feature["geometry"]["coordinates"]
            G.add_edge(source, target, pixel_list=pixel_list, **feature["properties"])
    G.metadata = data.get("metadata")
    return G

