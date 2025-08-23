import numpy as np
import plotly.express as px
from analyzer.analyzer import mappingToPercent, mergeAnalyse, T

def displayMapping(mapping : dict[tuple[int, int], T], name : str) -> None :
    coords : list[int] = [-1, 0, 1]

    grid = np.full((3, 3), -100, dtype=float)
    for (i, j), value in zip(mapping.keys(), mapping.values()):
        grid[j+1, i + 1] = value

    fig = px.imshow(
        grid,
        x=coords,
        y=list(reversed(coords)),
        color_continuous_scale="RdBu",
        labels={'x': 'PropertyX', 'y': 'PropertyY', 'color': 'Appearance'},
        title=f"mapping of the appearance of out of bound value of {name} in %.",
        color_continuous_midpoint=0,
        zmin=-100,
        zmax=100
    )

    fig.update_xaxes(tickmode="array", tickvals=coords, ticktext=[str(c) for c in coords])
    fig.update_yaxes(tickmode="array", tickvals=list(reversed(coords)), ticktext=[str(c) for c in coords], scaleanchor="x")
    fig.show()

def displayAppearanceMapping(mapping : dict[tuple[int, int], int], name : str) -> None :
    mappingpercent = mappingToPercent(mapping)
    displayMapping(mappingpercent, name)

    mappingpercent = mergeAnalyse(mappingpercent)
    displayMapping(mappingpercent, f"merged {name}")