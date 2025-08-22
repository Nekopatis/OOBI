from typing import List, cast
import plotly.express as px
import plotly.graph_objects as go
import plotly.colors as pc
from helper import DisplayLineWithSimpleLerp
from modifier.pointProperty import Point2D, PointProperty

def SplitSimplePoints(points : List[Point2D]) -> tuple[List[float], List[float]]:
    x = [coord for coord, _ in points]
    y = [coord for  _, coord in points]
    return x, y

def getPointMember(properties : List[PointProperty], memberName : str) -> List[Point2D] : 
    points = [getattr(pointProperty, memberName) for pointProperty in properties]
    return [cast(Point2D, point) for point in points]


def MergePointsAndMakeColors(
    centers : List[Point2D], 
    directions : List[Point2D], 
    finals : List[Point2D]
) -> tuple[List[Point2D], List[str], List[str]] :
    assert len(centers) == len(directions) == len(finals), "Error in MergePointsAndMakeColors. Not all list are the same size."

    points : List[Point2D] = centers + directions + finals
    colorsIndex : List[str] = []
    colors : List[str] = [px.colors.qualitative.Plotly[1], px.colors.qualitative.Plotly[2], px.colors.qualitative.Plotly[3]]

    [colorsIndex.append("centers") for _ in centers]
    [colorsIndex.append("directions") for _ in directions]
    [colorsIndex.append("finals") for _ in finals]

    return points, colorsIndex, colors



def displayPoint2D(points : List[Point2D], colorsIndex : List[str], colors : List[str]) -> None :
    x, y = SplitSimplePoints(points)
    useUnitCircle : bool = all([point.length() <= 1.2 for point in points])

    if len(colors) != 0 :
        if len(colorsIndex) == 0 :
            fig = px.scatter(x=x, y=y, color=[str(i) for i in range(len(colors))], color_discrete_sequence=colors)
        else :
            fig = px.scatter(x=x, y=y, color=colorsIndex, color_discrete_sequence=colors)
    else :
        fig = px.scatter(x=x, y=y)

    if useUnitCircle :
        fig.update_xaxes(range=[-2.2, 2.1])
        fig.update_yaxes(range=[-2.2, 2.2])
        fig.update_layout(
            yaxis=dict(scaleanchor="x", scaleratio=1),
            xaxis=dict(constrain="domain")
        )

        fig.add_shape(
            type="circle", layer="below",
            xref="x", yref="y",
            x0=-1, y0=-1, x1=1, y1=1,
            line=dict(color=pc.sequential.Greys[5], width=2)
        )
    
    fig.show()

def displayPointsProperty(property0 : PointProperty, property1 : PointProperty, x : List[float], name : str) -> None :
    pointProperties : list[PointProperty] = [cast(PointProperty, PointProperty.lerp(property0, property1, x_)) for x_ in x]
    centers, directions, finals, coefs = PointProperty.Scatter(pointProperties)

    points, colorsIndex, colors = MergePointsAndMakeColors(centers, directions, finals)
    displayPoint2D(points, colorsIndex, colors)

    #displayPointsPropertyProjection(x, centers, f"centers of {name}")
    displayPointsPropertyProjection(x, directions, f"directions of {name}")
    displayPointsPropertyProjection(x, finals, f"finals of {name}")
    DisplayLineWithSimpleLerp(x, coefs, f"coefs of {name}")


def displayPointsPropertyProjection(x : List[float], points : List[Point2D], name : str) -> None :
    x_, y_ = SplitSimplePoints(points)
    
    DisplayLineWithSimpleLerp(x, x_, f"x value of {name}")
    DisplayLineWithSimpleLerp(x, y_, f"y value of {name}")

def displayPointsPropertyProjectionWithName(x : List[float], properties : List[PointProperty], memberName : str, name : str) -> None :
    points : List[Point2D] = getPointMember(properties, memberName)
    displayPointsPropertyProjection(x, points, name)