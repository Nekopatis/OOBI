from typing import List
from collections import Counter
from base.propertyClass import FullProperty, ValueProperty

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


def AnalyseOutOfBoundFullProperty(properties : List[FullProperty], property0 : FullProperty, property1 : FullProperty) -> dict[tuple[int, int], int] :
        valuesX, valuesY = FullProperty.getMultipleValues(properties)
        BoundX : List[int] = Bound.fromValueProperty(valuesX, property0.propertyX, property1.propertyX)
        BoundY : List[int] = Bound.fromValueProperty(valuesY, property0.propertyY, property1.propertyY)
        return Counter(zip(BoundX, BoundY))

def MergeAnalyse(mapping : dict[tuple[int, int], int]) -> dict[tuple[int, int], int] :
    merged : dict[tuple[int, int], int] = {}
    for (i, j), count in mapping.items():
        key = (i, j) if i >= j else (j, i) # order: i >> j
        merged[key] = merged.get(key, 0) + count
    return merged
