from typing import List
import plotly.express as px
import plotly.graph_objects as go
import plotly.colors as pc
from base.propertyClass import FullProperty, ValueProperty
from base.tool import PropertyModifier, easyLerp, transformValue

def DisplayLineWithSimpleLerp(x : List[float], y : List[float], fullName : str, lineName : str) -> None :
    assert len(x) == len(y), f"Error in DisplayLineWithSimpleLerp. Not all list are the same length: {len(x)} != {len(y)}."
    x = x.copy()
    y = y.copy()
    
    color : List[str] = []
    [color.append(lineName) for _ in x]

    
    color.append("linear")
    x.append(x[0])
    y.append(y[0])

    color.append("linear")
    x.append(x[-2])
    y.append(y[-2])
    

    fig = px.line(x=x, y=y, title=fullName, color=color)
    fig.show()


def DisplayPropertyModifier(x : List[float], propertymodifier : PropertyModifier, name : str, doPrint : bool = False) -> None :
    if doPrint :
        propertymodifier.quickPrint()

    y = transformValue(propertymodifier, x)
    DisplayLineWithSimpleLerp(x, y, f"property modifier: {name}", name)


def DisplayValuePropertyLerp(x : List[float], property0 : ValueProperty, property1 : ValueProperty, name : str) -> None :
    lerped : List[ValueProperty] = easyLerp(property0, property1, x)
    realValues = [lerpVal.transformValue() for lerpVal in lerped]
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