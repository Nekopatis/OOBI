from typing import List, cast
import plotly.express as px
import plotly.graph_objects as go
import plotly.colors as pc
from .helper import DisplayLineWithSimpleLerp
from modifier.pointProperty import Point2D, PointProperty

def mergePointsAndMakeColors(
    centers : List[Point2D], 
    directions : List[Point2D], 
    finals : List[Point2D]
) -> tuple[List[Point2D], List[str], List[str]] :
    assert len(centers) == len(directions) == len(finals), "Error in MergePointsAndMakeColors. Not all list are the same size."

    points, colorsIndex = Point2D.mergePoints(centers, directions, finals)
    colors : List[str] = [px.colors.qualitative.Plotly[1], px.colors.qualitative.Plotly[2], px.colors.qualitative.Plotly[3]]

    return points, colorsIndex, colors



def displayPoint2D(points : List[Point2D], colorsIndex : List[str], colors : List[str]) -> None :
    x, y = Point2D.splitSimplePoints(points)
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
    centers, directions, finals, coefs = PointProperty.scatter(pointProperties)

    points, colorsIndex, colors = mergePointsAndMakeColors(centers, directions, finals)
    displayPoint2D(points, colorsIndex, colors)

    #displayPointsPropertyProjection(x, centers, f"centers of {name}")
    displayPointsPropertyProjection(x, directions, f"directions of {name}")
    displayPointsPropertyProjection(x, finals, f"finals of {name}")
    DisplayLineWithSimpleLerp(x, coefs, f"coefs of {name}", name)


def displayPointsPropertyProjection(x : List[float], points : List[Point2D], name : str) -> None :
    x_, y_ = Point2D.splitSimplePoints(points)
    
    DisplayLineWithSimpleLerp(x, x_, f"x value of {name}", name)
    DisplayLineWithSimpleLerp(x, y_, f"y value of {name}", name)

def displayPointsPropertyProjectionWithName(x : List[float], properties : List[PointProperty], memberName : str, name : str) -> None :
    points : List[Point2D] = PointProperty.getPointMember(properties, memberName)
    displayPointsPropertyProjection(x, points, name)