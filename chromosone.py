import gene

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