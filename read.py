from pathlib import Path

from matplotlib import cm, pyplot as plt
from shapely.geometry.point import Point
import networkx as nx
import geojson
import pandas as pd

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


def read_graph_from_excel(filename: str | Path) -> nx.Graph:
    """
    Read an Excel file with 'Edges' and 'Nodes' sheets into a NetworkX graph.

    Parameters:
    - filename: Path to the Excel file.

    Returns:
    - G: NetworkX graph with spatial data.
    """
    xls = pd.ExcelFile(filename)
    edges_df = pd.read_excel(xls, sheet_name="Edges")
    nodes_df = pd.read_excel(xls, sheet_name="Nodes")

    G = nx.Graph()

    # Add nodes
    for _, row in nodes_df.iterrows():
        node_id = row["node_Idx"]
        x = row["node_X_pix"]
        y = row["node_Y_pix"]
        attrs = row.drop(labels=["node_Idx", "node_X_pix", "node_Y_pix"]).to_dict()
        G.add_node(node_id, position=Point(x, y), **attrs)

    # Add edges
    for _, row in edges_df.iterrows():
        source = row["node_Idx_1"]
        target = row["node_Idx_2"]
        attrs = row.drop(labels=["node_Idx_1", "node_Idx_2"]).to_dict()
        G.add_edge(source, target, **attrs)

    # Attach metadata
    G.metadata = {"source_file": str(filename)}

    return G


