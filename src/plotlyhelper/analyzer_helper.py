import numpy as np
import plotly.express as px
from analyzer.analyzer import MergeAnalyse


def displayMapping(mapping : dict[tuple[int, int], int], name : str) -> None :
    coords : list[int] = [-1, 0, 1]

    total : float = float(sum(mapping.values()))
    z : list[float] = [100.0 * float(val) / total for val in mapping.values()]

    grid = np.full((3, 3), -max(z), dtype=float)
    for (i, j), z_ in zip(mapping.keys(), z):
        grid[j+1, i + 1] = z_

    fig = px.imshow(
        grid,
        x=coords,
        y=list(reversed(coords)),
        color_continuous_scale="RdBu",
        labels={'x': 'PropertyX', 'y': 'PropertyY', 'color': 'Appearance'},
        title=f"mapping of the appearance of out of bound value of {name} in %."
    )

    fig.update_xaxes(tickmode="array", tickvals=coords, ticktext=[str(c) for c in coords])
    fig.update_yaxes(tickmode="array", tickvals=list(reversed(coords)), ticktext=[str(c) for c in coords])
    fig.update_yaxes(scaleanchor="x")
    fig.show()

def displayAppearanceMapping(mapping : dict[tuple[int, int], int], name : str) -> None :
    displayMapping(mapping, name)

    mapping = MergeAnalyse(mapping)
    displayMapping(mapping, f"merged {name}")

