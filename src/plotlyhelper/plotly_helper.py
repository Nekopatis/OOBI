from typing import List
import plotly.express as px
import plotly.graph_objects as go
import plotly.colors as pc
from base.propertyClass import FullProperty, ValueProperty
from base.tool import LERP, PropertyModifier

def DisplayLineWithSimpleLerp(x : List[float], y : List[float], name : str) -> None :
    assert len(x) == len(y), f"Error in DisplayLineWithSimpleLerp. Not all list are the same length: {len(x)} != {len(y)}."
    x = x.copy()
    y = y.copy()
    
    color : List[str] = []
    [color.append(pc.qualitative.Plotly[0]) for _ in x]

    #"""
    color.append(pc.qualitative.Plotly[1])
    x.append(x[0])
    y.append(y[0])

    color.append(pc.qualitative.Plotly[1])
    x.append(x[-2])
    y.append(y[-2])
    #"""

    fig = px.line(x=x, y=y, title=name, color=color)
    fig.show()


def DisplayPropertyModifier(x : List[float], propertymodifier : PropertyModifier, name : str, doPrint : bool = False) -> None :
    if doPrint :
        propertymodifier.quickPrint()

    y = [propertymodifier.transformValue(x_) for x_ in x]
    DisplayLineWithSimpleLerp(x, y, f"property modifier: {name}")


def easyLerp(val0 : LERP, val1 : LERP, coefs : List[float]) -> List[LERP] :
    assert val0.__class__ == val1.__class__, "Error in easyLerp. Not the same Type."
    return [val0.lerp(val0, val1, coef) for coef in coefs]


def DisplayValuePropertyLerp(x : List[float], property0 : ValueProperty, property1 : ValueProperty, name : str) -> None :
    lerped : List[ValueProperty] = easyLerp(property0, property1, x)
    realValues = [lerpVal.transformValue() for lerpVal in lerped]
    DisplayLineWithSimpleLerp(x, realValues, f"graph of lerp of transfomed value from value property:  {name}")


def displayFullProperty(values : List[float], properties : List[FullProperty], name : str) -> None : 
    x = [val.propertyX.transformValue() for val in properties]
    y = [val.propertyY.transformValue() for val in properties]    

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