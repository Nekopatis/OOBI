from typing import List, cast
import numpy as np
from itertools import combinations

from base.propertyClass import FullProperty


class Centile :
    LAST : int = 100
    def __init__(self, values : List[float]) -> None :
        self.centiles : List[float] = []
        self.__initCentiles(values)

    def __initCentiles(self, values : List[float]) -> None :
        self.centiles = np.percentile(values, range(101)).tolist()


class ListAnalyzerResult :
    def __init__(self, propertyValues : List[List[float]]) -> None :
        self.valuePropertyCentiles : List[Centile] = [Centile(value) for value in propertyValues]

    def getBound(self, index : int) -> tuple[float, float, float] :
        value = self.valuePropertyCentiles[index]
        return value.centiles[0], value.centiles[50], value.centiles[101]
    
    @staticmethod
    def makeAnalyse(properties : List[FullProperty]) -> "ListAnalyzerResult" :
        return ListAnalyzerResult(FullProperty.getAllValuesSplited(properties))


class FullAnalyzerResult :
    def __init__(self) -> None:
        self.combinaison : List[ListAnalyzerResult] = []

def makeCombinaison(properties : List[FullProperty], index : List[int], weights : List[int]) -> FullProperty :
    assert len(index) == len(weights), "Error in makeCombinaison. index and weights must be the same size."

    total : float = float(sum(weights))
    weightNormal : List[float] = [float(val) / total for val in weights]
    selectedProperties : List[FullProperty] = [properties[i] for i in index]

    return cast(FullProperty, FullProperty.weightedMean(selectedProperties, weightNormal))

"""
def generateWeightCompositions(maxValue : int, size : int) :
    maxUniqueValue : int = maxValue - size + 1
    for comb in product(range(1, maxUniqueValue + 1), repeat=size):
        if sum(comb) == maxValue:
            yield list(comb)
"""

# like generateWeightCompositions but way faster
def updateWeight(weights : List[int], maxValue : int) -> bool :
    assert len(weights) > 1, "Error in updateWeight. Cannot incremente a list of a single item."
    assert len(weights) <= maxValue, "Error in updateWeight. Step is too small."

    maxUniqueValue : int = maxValue - len(weights) + 1
    if weights[1] == maxUniqueValue : return False # Last iteration already happened
    weights[0] = 1

    subIndex = len(weights) - 1
    weights[subIndex] += 1 
    while subIndex > 1 and (weights[subIndex] > maxUniqueValue or maxValue < sum(weights)) :
        weights[subIndex] = 1
        subIndex -= 1
        weights[subIndex] += 1

    weights[0] += maxValue - sum(weights)
    return True


def analyseIter(properties : List[FullProperty], quantityLerp : int) -> ListAnalyzerResult :
    assert len(properties) >= quantityLerp, "Error in analyseIter. Not enough properties for a mean."
    assert quantityLerp > 0, "Error in analyseIter. quantityLerp must be over 0."
    if quantityLerp == 1 : return ListAnalyzerResult.makeAnalyse(properties)

    fullProperty : List[FullProperty] = []
    for index in combinations(range(len(properties)), quantityLerp) :
        weights : list[int] = [1] * quantityLerp
        weights[-1] = 0
        while updateWeight(weights, 20) :
            fullProperty.append(makeCombinaison(properties, list(index), weights))

    return ListAnalyzerResult.makeAnalyse(fullProperty)


def analyzeProperties(properties : List[FullProperty]) -> FullAnalyzerResult:
    assert len(properties) > 1, "Error in analyzeProperties. Need at least 2 properties."
    ret = FullAnalyzerResult()
    [(print(i), ret.combinaison.append(analyseIter(properties, i))) for i in range(1, len(properties) + 1)]
    return ret