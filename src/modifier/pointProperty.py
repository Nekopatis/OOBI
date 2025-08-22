import copy
from typing import List, Sequence, cast
from base.tool import ClassLerp, Dist, PropertyModifier, SupportsLerp, lerpToWeightedMean, weightedMean, Iter
import random
import math

def rnd_circle() -> tuple[float, float]:
    theta = random.uniform(0, 2*math.pi)
    r = math.sqrt(random.uniform(0, 1))
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return x, y

class Point2D(SupportsLerp):  
    def __init__(self, x, y) :
        self.x = x
        self.y = y

    def __neg__(self) -> "Point2D" :
        return Point2D(-self.x, -self.y)

    def __add__(self, other) -> "Point2D" :
        return Point2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other) -> "Point2D" :
        return Point2D(self.x - other.x, self.y - other.y)

    def __mul__(self, weight) -> "Point2D" :
        if isinstance(weight, self.__class__):
            return Point2D(self.x * weight.x, self.y * weight.y)
        elif isinstance(weight, float):
            return Point2D(self.x * weight, self.y * weight)
        else:
            raise TypeError("unsupported operand type(s)")
        

    def __truediv__(self, weight) -> "Point2D" :
        if isinstance(weight, self.__class__):
            return Point2D(self.x / weight.x, self.y / weight.y)
        elif isinstance(weight, float):
            return Point2D(self.x / weight, self.y / weight)
        else:
            raise TypeError("unsupported operand type(s)")  

    def __iter__(self) -> Iter :
        return Iter([self.x, self.y])


    def length(self) -> float :
        return Dist([self.x, self.y])
    
    def normalize(self) -> None :
        length = self.length()
        if len == 0 : return
        tmp = self / length
        self.x = tmp.x
        self.y = tmp.y

    def quickString(self) -> str :
        return f"x= {self.x}, y= {self.y}"
    
    @staticmethod
    def rnd_AutoCircle() -> "Point2D" :
        x, y = rnd_circle()
        return Point2D(x, y)
    
    @staticmethod
    def splitSimplePoints(points : List["Point2D"]) -> tuple[List[float], List[float]]:
        x = [coord for coord, _ in points]
        y = [coord for  _, coord in points]
        return x, y
    
    @staticmethod
    def mergePoints(
        centers : List["Point2D"], 
        directions : List["Point2D"], 
        finals : List["Point2D"]
    ) -> tuple[List["Point2D"], List[str]] :
        points : List[Point2D] = centers + directions + finals
        colorsIndex : List[str] = []

        [colorsIndex.append("centers") for _ in centers]
        [colorsIndex.append("directions") for _ in directions]
        [colorsIndex.append("finals") for _ in finals]

        return points, colorsIndex




class PointProperty(PropertyModifier):
    def __init__(self, coef : float, center : Point2D, direction : Point2D) :
        self.coef : float = coef
        self.center : Point2D = center
        self.direction : Point2D = direction

    def __add__(self, other) -> "PointProperty" :
        return PointProperty(self.coef + other.coef, 
                             self.center + other.center, 
                             self.direction + other.direction)
    
    def __mul__(self, weight : float) -> "PointProperty" :
        return PointProperty(self.coef * weight, 
                             self.center * weight, 
                             self.direction * weight)

    def transformValue(self, baseValue : float) -> float :
        return baseValue * self.coef

        
    def getFinalPosition(self) -> Point2D:
        return self.center + self.direction
    
    def length(self) -> float :
        return self.direction.length()

    def quickPrint(self) -> None :
        print(f"coef= {self.coef}")
        print(f"center= {self.center.quickString()}")
        print(f"direction= {self.direction.quickString()}")
        print(f"final= {self.getFinalPosition().quickString()}\n")

    @staticmethod
    def lerp(val0 : ClassLerp, val1 : ClassLerp, coef : float) -> ClassLerp :
        return lerpToWeightedMean(val0, val1, coef, PointProperty.weightedMean)
    
    @staticmethod
    def weightedMean(values : Sequence[ClassLerp], weights : List[float]) -> ClassLerp :
        assert all([value.__class__ == PointProperty for value in values]), "Error in PointProperty weightedMean. Not all value are PointProperty."
        valuesProperties : List[PointProperty] = [cast(PointProperty, value) for value in values]

        raw : PointProperty = weightedMean(valuesProperties, weights)
        ret : PointProperty = copy.deepcopy(raw)

        lengths : List[float] = [value.length() for value in valuesProperties]
        dist : float = weightedMean(lengths, weights)
 
        ret.direction.normalize()
        ret.direction = ret.direction * dist
        
        ret.coef *= 1 + (ret.getFinalPosition().y - raw.getFinalPosition().y)
        
        return ret
    
    @staticmethod
    def rnd_AutoCircle() -> "PointProperty":
        return PointProperty(
            random.uniform(1, 100), 
            Point2D.rnd_AutoCircle(), 
            Point2D.rnd_AutoCircle()
        )

    @staticmethod
    def scatter(properties : List["PointProperty"]) -> tuple[List[Point2D], List[Point2D], List[Point2D], List[float]]:
        centers : List[Point2D] = []
        directions : List[Point2D] = []
        finals : List[Point2D] = []
        coefs : List[float] = []

        for property in properties :
            centers.append(property.center)
            directions.append(property.direction)
            finals.append(property.getFinalPosition())
            coefs.append(property.coef)

        return centers, directions, finals, coefs 
    

    @staticmethod
    def getPointMember(properties : List["PointProperty"], memberName : str) -> List[Point2D] : 
        points = [getattr(pointProperty, memberName) for pointProperty in properties]
        return [cast(Point2D, point) for point in points]