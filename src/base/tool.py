from typing import Protocol, List, Sequence, TypeVar, Union, runtime_checkable
from functools import reduce
import operator
import math



T = TypeVar("T", bound=Union["SupportsLerp", float])

LERP = TypeVar("LERP", bound="ClassLerp")

@runtime_checkable
class SupportsLerp(Protocol):
    def __add__(self : T, other : T) -> T : ...
    def __mul__(self : T, weight : float) -> T : ...

@runtime_checkable
class ClassLerp(SupportsLerp, Protocol):

    @staticmethod
    def lerp(val0 : LERP, val1 : LERP, coef : float) -> LERP : ...
    @staticmethod
    def weightedMean(values : Sequence[LERP], weights : List[float]) -> LERP : ...


@runtime_checkable
class PropertyModifier(ClassLerp, Protocol):
    def transformValue(self, baseValue : float) -> float : ...
    def quickPrint(self) -> None : ...



class Iter:
    def __init__(self, seq : List):
        self.data = seq
        self.index = len(seq)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0: 
            raise StopIteration
        
        self.index = self.index - 1
        return self.data[self.index]




def clamp(minimum : float, x : float, maximum : float) -> float :
    return max(minimum, min(x, maximum))



def weightedMean(values : Sequence[T], weights : List[float]) -> T :
    assert len(values) == len(weights), f"Invalid Lists on weightedMean. length: {len(values)} != {len(weights)}."
    assert len(values) != 0, "Invalid Lists on weightedMean. Lists are empty."
    if len(values) == 1 : return values[0]

    assert all([weight >= 0 for weight in weights]), "Invalid weight on weightedMean. All eights should be >= 0."
    total = sum(weights)
    weights = [weight / total for weight in weights]
    weighted = [value * weight for value, weight in zip(values, weights)]

    return reduce(operator.add, weighted)

def lerpToWeightedMean(val0 : T, val1 : T, coef : float, function) -> T :
    assert coef >= 0 and coef <= 1, f"Invalid coef on lerpToWeightedMean. {coef} is not in [0, 1]. It should be like 0 <= {coef} <= 1"
    if coef == 0 : return val0
    if coef == 1 : return val1
    return function([val0, val1], [1 - coef, coef])

def lerp(val0 : T, val1 : T, coef : float) -> T :
    # return val0 * (1 - coef) + val1 * coef
    return lerpToWeightedMean(val0, val1, coef, weightedMean)



def Dist(coord : List[float]) -> float :
    assert len(coord) > 0, "Invalid Lists on Dist. The List is empty."

    if len(coord) > 1 :
        return math.sqrt(sum([val*val for val in coord]))
    
    if len(coord) == 1 :
        return abs(coord[0])

    return 0


def easyLerp(val0 : LERP, val1 : LERP, coefs : List[float]) -> List[LERP] :
    assert val0.__class__ == val1.__class__, f"Error in easyLerp. Not the same Type: {val0.__class__} != {val1.__class__}."
    return [val0.lerp(val0, val1, coef) for coef in coefs]


def transformValue(propertymodifier : PropertyModifier, values : List[float]) -> List[float] :
    return [propertymodifier.transformValue(value) for value in values]
