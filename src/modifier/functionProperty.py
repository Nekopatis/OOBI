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
    
    


class FunctionProperty():
    def transformPositiveValue(self, baseValue : float) -> float :
        ...

    def transformValue(self, baseValue : float) -> float :
        sign = math.copysign(1, baseValue)
        result = self.transformPositiveValue(abs(baseValue))
        return result * sign

    def quickPrint(self) :
        ...

    def __call__(self, value : float) -> float :
        return self.transformValue(value)

class FunctionPropertyPow(FunctionProperty):
    def __init__(self, power : float, x_1 : float, y_1 : float) :
        assert x_1 > 0, "Error in FunctionPropertyPow. x_1 must be over 0."
        assert y_1 > 0, "Error in FunctionPropertyPow. y_1 must be over 0."
        assert power > 0, "Error in FunctionPropertyPow. power must be over 0."

        self.power : float = power
        self.x_1 : float = x_1
        self.y_1 : float = y_1

    def transformPositiveValue(self, baseValue : float) -> float :
        value = baseValue / self.x_1
        value = pow(value, self.power)
        value = value * self.y_1
        return value
    
    def quickPrint(self) :
        print(f"power: {self.power}\tx_1: {self.x_1}\ty_1: {self.y_1}")

    @staticmethod
    def rndCenter1(scale : float) -> float :
        tmp = random.uniform(-scale, scale)
        if tmp >= 0 : return tmp + 1 
        else : return 1 / (1 - tmp)

    @staticmethod
    def rnd(scale : float) -> "FunctionPropertyPow" :
        return FunctionPropertyPow(
            math.sqrt(math.sqrt(FunctionPropertyPow.rndCenter1(scale))),
            math.sqrt(FunctionPropertyPow.rndCenter1(scale)),
            math.sqrt(FunctionPropertyPow.rndCenter1(scale)),
        ) 


class FunctionPropertyFunc(FunctionProperty):
    def __init__(self, function : Callable[[float], float]) :
        self.func : Callable[[float], float] = function

    def transformPositiveValue(self, baseValue : float) -> float :
        return self.func(baseValue)
    
    def quickPrint(self) :
        print()