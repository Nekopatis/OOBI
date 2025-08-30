import math
from collections import defaultdict
from typing import List, Sequence, Callable
from base.tool import ClassLerp, PropertyModifier, lerpToWeightedMean, weightedMean
import random


class FunctionPropertyMix(PropertyModifier):
    def __init__(self, values : List[tuple["FunctionProperty", float]]) :
        self.values : List[tuple["FunctionProperty", float]] = []
        self.__updateValue(values, 1)

    def __updateValue(self, values : List[tuple["FunctionProperty", float]], coef : float) -> None :
        assert 0 <= coef and coef <= 1, "Error in FunctionPropertyMix. coef should be in [0, 1]." 

        total : float = sum([value for _, value in values])
        values = FunctionPropertyMix.__cleanValue(values, coef / total)
        self.values = FunctionPropertyMix.__cleanValue(self.values, 1 - coef)
        self.values += values
        self.__merge()

    def __merge(self) -> None :
        merged: dict[FunctionProperty, float] = defaultdict(float)

        for propertyFunction, value in self.values:
            merged[propertyFunction] += value

        self.values = list(merged.items())

    def __add__(self, other) :
        return FunctionPropertyMix(self.values + FunctionPropertyMix.valueToFunctionPropertyMix(other).values)
    
    def __mul__(self, weight : float) :
        ret = FunctionPropertyMix(self.values)
        ret.values = FunctionPropertyMix.__cleanValue(ret.values, weight)
        return ret



    def transformValue(self, baseValue : float) -> float :
        return sum([FunctionProperty.transformValue(baseValue * value) for FunctionProperty, value in self.values])
    
    def quickPrint(self) :
        [(print(f"\tvalue: {value}"), FunctionProperty.quickPrint()) for FunctionProperty, value in self.values]


    def __call__(self, value : float) -> float :
        return self.transformValue(value)


    @staticmethod
    def __cleanValue(values : List[tuple["FunctionProperty", float]], weight : float) -> List[tuple["FunctionProperty", float]] :
        ret : List[tuple["FunctionProperty", float]] = []
        ret = [(propertyFunction, value * weight) for propertyFunction, value in values]
        return ret

    @staticmethod
    def lerp(val0 : ClassLerp, val1 : ClassLerp, coef : float) -> ClassLerp :
        return lerpToWeightedMean(val0, val1, coef, FunctionPropertyMix.weightedMean)
    
    @staticmethod
    def valueToFunctionPropertyMix(value) -> "FunctionPropertyMix" :
        if isinstance(value, FunctionPropertyMix) :
            return value

        if isinstance(value, FunctionProperty) :
            return FunctionPropertyMix([(value, 1)])
        
        assert False, "Error in FunctionPropertyMix valueToFunctionPropertyMix. value class is invalid. "

    @staticmethod
    def valuesToFunctionPropertyMix(values : Sequence) -> Sequence["FunctionPropertyMix"] :
        return [FunctionPropertyMix.valueToFunctionPropertyMix(value) for value in values]
    
    @staticmethod
    def weightedMean(values : Sequence[ClassLerp], weights : List[float]) -> ClassLerp :
        return weightedMean(FunctionPropertyMix.valuesToFunctionPropertyMix(values), weights)
    
    

class FunctionProperty(PropertyModifier):
    def __init__(self, function : Callable[[float], float]) :
        self.func : Callable[[float], float] = function

    def transformValue(self, baseValue : float) -> float :
        return self.func(baseValue)
    
    def quickPrint(self) :
        print()


    def __add__(self, other) :
        return FunctionPropertyMix.valueToFunctionPropertyMix(self) + FunctionPropertyMix.valueToFunctionPropertyMix(other)
    
    def __mul__(self, weight : float) :
        return FunctionPropertyMix.valueToFunctionPropertyMix(self) * weight
    
    def __call__(self, value : float) -> float :
        return self.transformValue(value)


    @staticmethod
    def lerp(val0 : ClassLerp, val1 : ClassLerp, coef : float) -> ClassLerp :
        return lerpToWeightedMean(val0, val1, coef, FunctionProperty.weightedMean)
    
    @staticmethod
    def weightedMean(values : Sequence[ClassLerp], weights : List[float]) -> ClassLerp :
        return FunctionPropertyMix.weightedMean(values, weights)
