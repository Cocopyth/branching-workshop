**Example repository to load data from dataset**

- Example data can be found [here](https://www.dropbox.com/t/GVeUQHWycTeNOeIg)
- `load_draw.ipynb` provides a notebook that load the graph and plots it
- `read.py` contains the loading function, the loaded graph should have node position
attributes consistent with the plotting. Nodes have a `"position"` attribute which is a `shapely` point
and edges have a `"pixel_list"` attribute that is the list of points of the curve linking the nodes. 