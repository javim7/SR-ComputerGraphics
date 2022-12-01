from vector import *


class matriz(object):
    def __init__(self, matriz):
        self.matriz = matriz

    def __mul__(self, other):
        try:

            if(type(other) == V4):
                other = matriz([[other.x], [other.y], [other.z], [other.w]])

            prodcuto = []
            for x in range(len(self.matriz)):
                prodcuto.append([])
                for y in range(len(other.matriz[0])):
                    prodcuto[x].append([])
                    temp = 0
                    for k in range(len(other.matriz)):
                        temp += self.matriz[x][k] * other.matriz[k][y]
                    prodcuto[x][y] = temp
            return matriz(prodcuto)

        except:
            print('Error en la multiplicación!')

    def show(self, matrix):
        for i in matrix:
            print(i)
