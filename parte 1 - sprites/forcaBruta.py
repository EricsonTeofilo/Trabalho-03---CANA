import math

class GerenciadorDistancia2:
    def _init_(self):
        pass

    def encontrar_par_mais_proximo(self, objetos):
        if len(objetos) < 2:
            return [], 0

        min_dist = float('inf')
        par_mais_proximo = []
        cont_verificacoes = 0

        for i in range(len(objetos)):
            for j in range(i + 1, len(objetos)):
                cont_verificacoes += 1
                obj1 = objetos[i]
                obj2 = objetos[j]
                dx = obj1.a - obj2.a
                dy = obj1.b - obj2.b
                dist = math.sqrt(dx * dx + dy * dy)

                if dist < min_dist:
                    min_dist = dist
                    par_mais_proximo = [obj1, obj2]

        return par_mais_proximo, cont_verificacoes