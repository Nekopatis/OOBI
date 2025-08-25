from typing import List, Sequence, cast
from .tool import ClassLerp, LERP, PropertyModifier, lerpToWeightedMean, weightedMean

class ValueProperty(ClassLerp):
    def __init__(self, baseValue : float, modifier : PropertyModifier) :
        self.baseValue : float = baseValue
        self.modifier : PropertyModifier = modifier


    def __add__(self, other) :
        return ValueProperty(self.baseValue + other.baseValue, 
                             self.modifier + other.modifier)
    
    def __mul__(self, weight : float) :
        return ValueProperty(self.baseValue * weight, 
                             self.modifier * weight)
    


    def transformValue(self) -> float:
        return self.modifier.transformValue(self.baseValue)
    
    def quickPrint(self) :
        print(f"\trealValue = {self.transformValue()}")
        print(f"\tbaseValue = {self.baseValue}")
        self.modifier.quickPrint()
        print()

    @staticmethod
    def lerp(val0 : ClassLerp, val1 : ClassLerp, coef : float) -> ClassLerp : 
        return lerpToWeightedMean(val0, val1, coef, ValueProperty.weightedMean)

    @staticmethod
    def weightedMean(values : Sequence[ClassLerp], weights : List[float]) -> ClassLerp :
        assert all([value.__class__ == ValueProperty for value in values]), "Error in ValueProperty weightedMean. Not all value are a ValueProperty."
        valuesProperties : List[ValueProperty] = [cast(ValueProperty, value) for value in values]

        baseValue = weightedMean([value.baseValue for value in valuesProperties], weights)
        modifiers : List[PropertyModifier] = [value.modifier for value in valuesProperties]
        modifier = valuesProperties[0].modifier.weightedMean(modifiers, weights)
        
        return ValueProperty(baseValue, cast(PropertyModifier, modifier))
    
    @staticmethod 
    def transformValues(values : List["ValueProperty"]) -> List[float] :
        return [value.transformValue() for value in values]




class FullProperty(ClassLerp) :
    def __init__(self, propertyX : ValueProperty, propertyY : ValueProperty) :
        self.propertyX : ValueProperty = propertyX
        self.propertyY : ValueProperty = propertyY

    def __add__(self, other) :
        return FullProperty(self.propertyX + other.propertyX, 
                             self.propertyY + other.propertyY)
    
    def __mul__(self, weight : float) :
        return FullProperty(self.propertyX * weight, self.propertyY * weight)
    
    def print(self) :
        [(print(name), subProperty.quickPrint()) for subProperty, name in self.getNamedProperties()]
        print()

    def getValues(self) -> List[float] :
        return [valueProperty.transformValue() for valueProperty in self.getProperties()]
    
    def getProperties(self) -> List[ValueProperty] :
        return [subProperty for subProperty, _ in self.getNamedProperties()]
    
    def getNamedProperties(self) -> List[tuple[ValueProperty, str]] :
        return [
            (self.propertyX, "propertyX"),
            (self.propertyY, "propertyY"),
        ]



    @staticmethod
    def lerp(val0 : ClassLerp, val1 : ClassLerp, coef : float) -> ClassLerp :
        return lerpToWeightedMean(val0, val1, coef, FullProperty.weightedMean)

    @staticmethod
    def weightedMean(values : Sequence[ClassLerp], weights : List[float]) -> ClassLerp :
        assert all([value.__class__ == FullProperty for value in values]), "Error in FullProperty weightedMean. Not all value are a FullProperty."
        valuesProperties : List[FullProperty] = [cast(FullProperty, value) for value in values]

        tmp : list[List[ValueProperty]] = [value.getProperties() for value in valuesProperties]
        tmp = [list(val) for val in zip(*tmp)] # matrice transpose
        properties : List[ValueProperty] = [cast(ValueProperty, ValueProperty.weightedMean(val, weights)) for val in tmp]

        assert len(properties) >= 2, "Error in FullProperty weightedMean. FullProperty have less than 2 ValueProperty."
        return FullProperty(properties[0], properties[1])

    @staticmethod
    def getValuesXY(properties : List["FullProperty"]) -> tuple[List[float], List[float]] :
        values : List[List[float]] = FullProperty.getAllValuesSplited(properties)
        propertyX : List[float] = [] if len(values) < 1 else values[0]
        propertyY : List[float] = [] if len(values) < 2 else values[1]
        return propertyX, propertyY
    
    @staticmethod
    def getAllValuesSplited(properties : List["FullProperty"]) -> List[List[float]] :
        if len(properties) == 0 : 
            return []
        values : List[List[float]] = [val.getValues() for val in properties]
        return [list(val) for val in zip(*values)] # matrice transpose