from typing import List, Sequence
from tool import ClassLerp, LERP, PropertyModifier, lerpToWeightedMean, weightedMean
from typing import cast

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
        self.propertyX.quickPrint()
        self.propertyY.quickPrint()
        print()

    @staticmethod
    def lerp(val0 : ClassLerp, val1 : ClassLerp, coef : float) -> ClassLerp :
        return lerpToWeightedMean(val0, val1, coef, FullProperty.weightedMean)


    @staticmethod
    def weightedMean(values : Sequence[ClassLerp], weights : List[float]) -> ClassLerp :
        return weightedMean(values, weights)
