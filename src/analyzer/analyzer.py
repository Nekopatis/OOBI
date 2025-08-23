from typing import List, TypeVar, cast
from collections import Counter

from base.propertyClass import FullProperty, ValueProperty

T = TypeVar("T", int, float)

class Bound :
    def __init__(self, bound1 : float, bound2 : float) -> None:
        self.lower : float = min(bound1, bound2)
        self.upper : float = max(bound1, bound2)

    def classify(self, value : float) -> int :
        if value < self.lower : return -1
        if value > self.upper : return  1
        return 0

    def locationBound(self, values : List[float]) -> List[int]:
        return [self.classify(value) for value in values]
    
    @staticmethod
    def fromValueProperty(
        values : List[float], 
        property0 : ValueProperty, 
        property1 : ValueProperty
    ) -> List[int] :
        return Bound(property0.transformValue(), property1.transformValue()).locationBound(values)


def analyseOutOfBoundFullProperty(properties : List[FullProperty], property0 : FullProperty, property1 : FullProperty) -> dict[tuple[int, int], int] :
    valuesX, valuesY = FullProperty.getMultipleValues(properties)
    BoundX : List[int] = Bound.fromValueProperty(valuesX, property0.propertyX, property1.propertyX)
    BoundY : List[int] = Bound.fromValueProperty(valuesY, property0.propertyY, property1.propertyY)
    return Counter(zip(BoundX, BoundY))

def mergeAnalyse(mapping : dict[tuple[int, int], T]) -> dict[tuple[int, int], T] :
    merged : dict[tuple[int, int], T] = {}
    for (i, j), count in mapping.items():
        key = (i, j) if i >= j else (j, i) # order: i >> j
        merged[key] = merged.get(key, 0) + count
    return merged

def mappingToPercent(mapping : dict[tuple[int, int], int]) -> dict[tuple[int, int], float] :
    total : float = float(sum(mapping.values()))
    values : list[float] = [100.0 * float(val) / total for val in mapping.values()]
    return {key: value for key, value in zip(mapping.keys(), values)}

def mergeDict(dict1 : dict, dict2 : dict) -> dict :
    return {k: dict1.get(k, 0) + dict2.get(k, 0) for k in set(dict1) | set(dict2)}

def analyseOneFullProperty(property : FullProperty, lerpProperties : List[FullProperty], count : int) -> dict[tuple[int, int], int] :
    iter : List[float] = [float(i) / float(count) for i in range(count+1)] 
    ret : dict[tuple[int, int], int] = {}

    for lerpProperty in lerpProperties :
        lerped : List[FullProperty] = [cast(FullProperty, FullProperty.lerp(property, lerpProperty, i)) for i in iter]
        tmp = analyseOutOfBoundFullProperty(lerped, property, lerpProperty)
        ret = mergeDict(ret, tmp)
    
    return ret