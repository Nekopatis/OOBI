import math
from collections import defaultdict
from typing import List, Sequence, Callable
from base.tool import ClassLerp, PropertyModifier, lerpToWeightedMean, weightedMean
import random

"""
similar to functionProperty
but DoubleFunctionPropertyMix.transformValue change from FunctionPropertyMix.transformValue
because DoubleFunctionProperty.transformValue change from FunctionProperty.transformValue
DoubleFunctionProperty.transformValue take its proporiton / weight as a parameter
and pass its ProportionModifier variable.

ProportionModifier :
- functor float -> float
- [0; 1] -> Real
- continuous
- 0 -> 0
- 1 -> 1

ProportionModifier modulate the result of the usual FunctionProperty.transformValue
FunctionProperty.transformValue can be more fancy, with less restriction
"""



class DoubleFunctionPropertyMix(PropertyModifier):
    def __init__(self, values : List[tuple["DoubleFunctionProperty", float]]) :
        self.values : List[tuple["DoubleFunctionProperty", float]] = []
        self.__updateValue(values, 1)

    def __updateValue(self, values : List[tuple["DoubleFunctionProperty", float]], coef : float) -> None :
        assert 0 <= coef and coef <= 1, "Error in FunctionPropertyMix. coef should be in [0, 1]." 

        total : float = sum([value for _, value in values])
        values = DoubleFunctionPropertyMix.__cleanValue(values, coef / total)
        self.values = DoubleFunctionPropertyMix.__cleanValue(self.values, 1 - coef)
        self.values += values
        self.__merge()

    def __merge(self) -> None :
        merged: dict[DoubleFunctionProperty, float] = defaultdict(float)

        for propertyFunction, value in self.values:
            merged[propertyFunction] += value

        self.values = list(merged.items())

    def __add__(self, other) :
        return DoubleFunctionPropertyMix(self.values + DoubleFunctionPropertyMix.valueToFunctionPropertyMix(other).values)
    
    def __mul__(self, weight : float) :
        ret = DoubleFunctionPropertyMix(self.values)
        ret.values = DoubleFunctionPropertyMix.__cleanValue(ret.values, weight)
        return ret



    def transformValue(self, baseValue : float) -> float :
        return sum([FunctionProperty.transformValue(baseValue, value) for FunctionProperty, value in self.values])
    
    def quickPrint(self) :
        [(print(f"\tvalue: {value}"), FunctionProperty.quickPrint()) for FunctionProperty, value in self.values]


    def __call__(self, value : float) -> float :
        return self.transformValue(value)


    @staticmethod
    def __cleanValue(values : List[tuple["DoubleFunctionProperty", float]], weight : float) -> List[tuple["DoubleFunctionProperty", float]] :
        ret : List[tuple["DoubleFunctionProperty", float]] = []
        ret = [(propertyFunction, value * weight) for propertyFunction, value in values]
        return ret

    @staticmethod
    def lerp(val0 : ClassLerp, val1 : ClassLerp, coef : float) -> ClassLerp :
        return lerpToWeightedMean(val0, val1, coef, DoubleFunctionPropertyMix.weightedMean)
    
    @staticmethod
    def valueToFunctionPropertyMix(value) -> "DoubleFunctionPropertyMix" :
        if isinstance(value, DoubleFunctionPropertyMix) :
            return value

        if isinstance(value, DoubleFunctionProperty) :
            return DoubleFunctionPropertyMix([(value, 1)])
        
        assert False, "Error in FunctionPropertyMix valueToFunctionPropertyMix. value class is invalid. "

    @staticmethod
    def valuesToFunctionPropertyMix(values : Sequence) -> Sequence["DoubleFunctionPropertyMix"] :
        return [DoubleFunctionPropertyMix.valueToFunctionPropertyMix(value) for value in values]
    
    @staticmethod
    def weightedMean(values : Sequence[ClassLerp], weights : List[float]) -> ClassLerp :
        return weightedMean(DoubleFunctionPropertyMix.valuesToFunctionPropertyMix(values), weights)
    

# [0; 1] -> R
# continuous
# 0 -> 0
# 1 -> 1
class ProportionModifier() :
    def __init__(self, function : Callable[[float], float]) :
        self.func : Callable[[float], float] = function

    def transformPositiveValue(self, baseValue : float) -> float :
        return self.func(baseValue)
    
    def __call__(self, baseValue : float) -> float :
        return self.transformPositiveValue(baseValue)





class DoubleFunctionProperty():
    def __init__(self, proportionModifier : ProportionModifier) -> None:
        self.proportionModifier : ProportionModifier = proportionModifier

    def transformPositiveValue(self, baseValue : float) -> float :
        ...

    def transformValue(self, baseValue : float, proportion : float) -> float :
        sign = math.copysign(1, baseValue)
        result = self.transformPositiveValue(abs(baseValue))
        return result * sign * self.proportionModifier(proportion)

    def quickPrint(self) :
        ...

    def __call__(self, value : float, proportion : float) -> float :
        assert 0 <= proportion <= 1
        return self.transformValue(value, proportion)

class DoubleFunctionPropertyFunc(DoubleFunctionProperty):
    def __init__(self, function : Callable[[float], float]) :
        self.func : Callable[[float], float] = function

    def transformPositiveValue(self, baseValue : float) -> float :
        return self.func(baseValue)
    
    def quickPrint(self) :
        print()