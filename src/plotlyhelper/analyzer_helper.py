from typing import List
import numpy as np
import plotly.express as px
from analyzer.analyzer import mappingToPercent, mergeAnalyse, T
from analyzer.listanalyzer import FullAnalyzerResult, ListAnalyzerResult, Centile

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


def displayFullAnalyzerResultProperty(propertyResult : List[Centile]) -> None :
    x = list(range(101)) * len(propertyResult)
    y : list[float] = [val for centile in propertyResult for val in centile.centiles]
    color : list[int] = [(id + 1) for id, centile in enumerate(propertyResult) for val in centile.centiles]

    fig = px.line(x=x, y=y, color=color)
    fig.show()

def displayFullAnalyzerResult(result : FullAnalyzerResult) -> None :
    values : List[List[Centile]] = [comb.valuePropertyCentiles for comb in result.combinaison]
    values = [list(val) for val in zip(*values)]
    [displayFullAnalyzerResultProperty(val) for val in values]


def displayFullAnalyzerResultMap(result : List[tuple[float, float, int]]) -> None :
    x, y, id = map(list, zip(*result))
    id_str = [str(v) for v in id]

    def make1Value(y) :
        fig = px.violin(
            x=id_str,
            y=y,
            color=id_str,
            box=True,
        )
        fig.update_traces(spanmode="hard")
        fig.show()

    make1Value(x)
    make1Value(y)
