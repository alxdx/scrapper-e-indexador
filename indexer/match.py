class Match:
    def __init__(self,numeroLinea : int, ocurrencias: list):
        self.linea=numeroLinea
        self.ocurrencias=ocurrencias
    def addOcurrencias(self, new:list):
        for elem in new:
            if elem not in self.ocurrencias:
                self.ocurrencias.append(elem)
    def getOcurrencias(self):
        return self.ocurrencias
    def getLinea(self):
        return self.linea
    def getNumOcurrencias(self):
        return len(self.ocurrencias)