import math
import gene
import random
from functools import reduce

class chromosone:
    def __init__(self, vals={}):
        self.genes = {
            "elementwidth": gene(["1/4", "1/2", "1"], vals.elementwidth),   
        }
    def getObjectRepresentation(self):
        obj = {}
        for name in self.genes.keys:
            obj[name] = name.getValue()
        return obj
    @staticmethod
    def uniformCrossover(self, cr1, cr2, p=0.5):
        newProps = {}
        for name in cr1.genes.keys:
            if random.random() < p:
                newProps[name] = cr1.genes[name].getValue()
            else:
                newProps[name] = cr2.genes[name].getValue()
        return chromosone(newProps)
    def mutate(self, p = 0.02) :
        newChromosome = chromosone(self.getObjectRepresentation())
        for name in newChromosome.genes.keys:
            newChromosome.genes[name].mutate(p)
        return newChromosome
    def selection(self, pop, num):
        fitnesses = list(map(pop, lambda obj: obj.fitness))
        totalFitness = list(reduce((lambda tot, current: tot + current), fitnesses))
        indices = []
        while num:
            num -= 1;
            randVal = math.floor(random.random()*totalFitness)
            for idx in range(len(fitnesses)):
                randVal -= fitnesses[idx]
                if randVal <= 0:
                    indices.push(idx)
                    break
        return indices