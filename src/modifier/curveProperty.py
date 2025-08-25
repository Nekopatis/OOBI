import math
from typing import List, Sequence
from base.tool import ClassLerp, PropertyModifier, lerpToWeightedMean, weightedMean
import random

class CurveProperty(PropertyModifier):
    def __init__(self, 
            logOffset : float, 
            offset : float, 
            period : float, 
            sinStrength : float, 
            coef : float, 
            power : float
        ) :
        self.logOffset : float = logOffset

        self.offset : float = offset
        self.period : float = period
        self.sinStrength : float = sinStrength

        self.coef : float = coef
        self.power : float = power

        self.__makeFunc()

    def __makeFunc(self) -> None:
        def modifier(offset : float, coef : float) :
            def ret(x : float):
                ret =  math.log(self.logOffset + x)
                ret = self.sinStrength * math.sin(offset + self.period * ret)
                ret = 1+abs(ret)
                return coef * (1/ret)**self.power
            return ret
        
        pos = modifier(self.offset + math.pi / 2, self.coef)
        neg = modifier(self.offset, - self.coef)

        self.func = lambda x : x * (1 + pos(x) + neg(x))



    def __add__(self, other) :
        return CurveProperty(
            self.logOffset + other.logOffset,
            self.offset + other.offset,
            self.period + other.period,
            self.sinStrength + other.sinStrength,
            self.coef + other.coef,
            self.power + other.power
        )
    
    def __mul__(self, weight : float) :
        return CurveProperty(
            self.logOffset * weight,
            self.offset * weight,
            self.period * weight,
            self.sinStrength * weight,
            self.coef * weight,
            self.power * weight
        )

        

    def transformValue(self, baseValue : float) -> float :
        return self.func(baseValue)
    

    def quickPrint(self) :
        print(f"logStrength= {self.logOffset}")
        print(f"offset= {self.offset}")
        print(f"period= {self.period}")
        print(f"sinStrength= {self.sinStrength}")
        print(f"coef= {self.coef}")
        print(f"power= {self.power}")



    @staticmethod
    def lerp(val0 : ClassLerp, val1 : ClassLerp, coef : float) -> ClassLerp :
        return lerpToWeightedMean(val0, val1, coef, CurveProperty.weightedMean)
    
    @staticmethod
    def weightedMean(values : Sequence[ClassLerp], weights : List[float]) -> ClassLerp :
        return weightedMean(values, weights)
    
    @staticmethod
    def rnd() :
        return CurveProperty(
            math.sqrt(random.uniform(0, 100)),
            random.uniform(0, 2*math.pi),
            math.sqrt(random.uniform(0.1, 2.9)),
            math.sqrt(random.uniform(0, 50)),
            math.sqrt(random.uniform(0, 5)),
            math.sqrt(random.uniform(0.5, 5)),
        )
    
    