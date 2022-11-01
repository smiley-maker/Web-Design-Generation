import math
import random

class Gene:
    def __init__(self, possibleValues, value=None):
        self.possibleValues = possibleValues
        if value:
            self.value = value
        else:
            idx = math.floor(random.random()*len(self.possibleValues))
            self.value = possibleValues[idx]
    def getValue(self):
        return self.value
    def filtering(self):
        return lambda val: val if (val != self.value) else None
    def mutate(self, p = 0.02):
        if random.random() < p:
            newPossibilities = filter(self.filtering(), self.possibleValues)
            self.value = newPossibilities[math.floor(random.random()*len(newPossibilities))]