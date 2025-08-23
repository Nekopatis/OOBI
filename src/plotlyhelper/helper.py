from typing import List
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.colors as pc

from analyzer.analyzer import analyseOutOfBoundFullProperty
from .analyzer_helper import displayAppearanceMapping
from base.propertyClass import FullProperty, ValueProperty
from base.tool import PropertyModifier, easyLerp, transformValue



def DisplayLineWithSimpleLerp(x : List[float], y : List[float], fullName : str, lineName : str) -> None :
    assert len(x) == len(y), f"Error in DisplayLineWithSimpleLerp. Not all list are the same length: {len(x)} != {len(y)}."
    x = x.copy()
    y = y.copy()

    colorMap : dict[str, str] = {
        lineName        : "blue",
        "linear"        : "red",
        "bound_begin"   : "green",
        "bound_end"     : "orange"
    }

    lineTypeMap : dict[str, str] = {
        lineName        : "solid",
        "linear"        : "dashdot",
        "bound_begin"   : "dot",
        "bound_end"     : "dot"
    }
    
    lineType : List[str] = []
    [lineType.append(lineName) for _ in x]

    minVal = x[0],  y[0]
    maxVal = x[-1], y[-1]

    def append(colorName : str, xValue : float, yValue : float) :
        lineType.append(colorName)
        x.append(xValue)
        y.append(yValue)

    append("linear",        minVal[0], minVal[1])
    append("linear",        maxVal[0], maxVal[1])

    append("bound_begin",   minVal[0], minVal[1])
    append("bound_begin",   maxVal[0], minVal[1])

    append("bound_end",     minVal[0], maxVal[1])
    append("bound_end",     maxVal[0], maxVal[1])


    df = pd.DataFrame({"x": x, "y": y, "lineType": lineType})

    fig = px.line(
        df, x="x", y="y", color="lineType", line_dash="lineType",
        color_discrete_map=colorMap,
        line_dash_map=lineTypeMap,
        title=fullName
    )

    fig.show()


def DisplayPropertyModifier(x : List[float], propertymodifier : PropertyModifier, name : str, doPrint : bool = False) -> None :
    if doPrint :
        propertymodifier.quickPrint()

    y = transformValue(propertymodifier, x)
    DisplayLineWithSimpleLerp(x, y, f"property modifier: {name}", name)


def DisplayValuePropertyLerp(x : List[float], property0 : ValueProperty, property1 : ValueProperty, name : str) -> None :
    lerped : List[ValueProperty] = easyLerp(property0, property1, x)
    realValues : List[float] =  ValueProperty.transformValues(lerped)
    DisplayLineWithSimpleLerp(x, realValues, f"graph of lerp of transfomed value from value property:  {name}", name)


def displayFullProperty(values : List[float], properties : List[FullProperty], name : str) -> None : 
    x, y = FullProperty.getMultipleValues(properties)

    fig = px.scatter(x=x, y=y, title=name, color=values, color_continuous_scale="Viridis")
    fig.add_trace(go.Scatter(
        x=[0],
        y=[0],
        mode="markers",
        marker=dict(size=12, color="red"),
        name="Origine",
        showlegend=False
    ))
    fig.show()


def MakeFullPropertyExample(iterator : List[float], property0 : FullProperty, property1 : FullProperty) -> None :
    lerped = easyLerp(property0, property1, iterator)
    displayFullProperty(iterator, lerped, "lerped")

    DisplayValuePropertyLerp(iterator, property0.propertyX, property1.propertyX, "propertyX")
    DisplayValuePropertyLerp(iterator, property0.propertyY, property1.propertyY, "propertyY")

    mapping : dict[tuple[int, int], int] = analyseOutOfBoundFullProperty(lerped, property0, property1)
    displayAppearanceMapping(mapping, "example")