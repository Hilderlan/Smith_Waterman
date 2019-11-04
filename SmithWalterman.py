match = 0
mismatch = 0
gap = 0
sequencia1 = ""
sequencia2 = ""
caminho = []
matriz = []
lista_scores = []


class Score:
    def __init__(self, valor, path=(), pais=[]):
        self.valor = valor
        self.path = path
        self.pais = pais

    def addPais(self, pais):
        self.pais.append(pais)

    def limpar_lista(self):
        self.pais = []


def alinhamento_global():
    linha = []

    # Incializa a matriz com 0's, para depois efetuar o processamento.
    for _ in range(len(sequencia1) + 1):
        for _ in range(len(sequencia2) + 1):
            linha.append(0)
        matriz.append(linha)
        linha = []

    processaMatriz()

    pos_inicial = criarScoreMatriz()

    backtrace(pos_inicial)


def verificar(path):
    for s in lista_scores:
        if s.path == path:
            return s
    return None


def buscarPais(pais):
    for s in lista_scores:
        for pai in s.pais:
            if pai[0] == pais[0] and pai[1] == pais[1]:
                return s
    return None


def processaBacktrace():
    sequencia1_alinhada = ""
    sequencia2_alinhada = ""
    path_inicial = caminho[0]
    j, k = path_inicial
    score = verificar(path_inicial)

    for i in range(1, len(caminho)):
        # Movimento diagonal
        if path_inicial[0] == caminho[i][0] + 1 and path_inicial[1] == caminho[i][1] + 1:
            sequencia1_alinhada += sequencia1[j - 1]
            sequencia2_alinhada += sequencia2[k - 1]

        # Movimento a esquerda
        elif path_inicial[0] == caminho[i][0] and path_inicial[1] == caminho[i][1] + 1:
        #    print(f"Esq -> i: {i} | j: {j} | k: {k}")
            sequencia1_alinhada += "-"
            sequencia2_alinhada += sequencia2[k - 1]

        # Movimento para cima
        elif path_inicial[0] == caminho[i][0] + 1 and path_inicial[1] == caminho[i][1]:
        #    print(f"Cima -> i: {i} | j: {j} | k: {k}")
            sequencia1_alinhada += sequencia1[j - 1]
            sequencia2_alinhada += "-"

        path_inicial = caminho[i]
        j, k = path_inicial

    # Ajeitando a ultima entrada
    if j == 0 and k == 0:
        sequencia1_alinhada += ""
        sequencia2_alinhada += ""
    elif j - 1 < 0:
        sequencia1_alinhada += "-"
        sequencia2_alinhada += sequencia2[k - 1]
    elif k - 1 < 0:
        sequencia1_alinhada += sequencia1[j - 1]
        sequencia2_alinhada += "-"
    else:
        sequencia1_alinhada += ""
        sequencia2_alinhada += ""

    alinhamento_final = ''.join(
        reversed(sequencia1_alinhada)) + "\n" + ''.join(reversed(sequencia2_alinhada)) + "\n" + "SCORE = " + str(score.valor)

    print(alinhamento_final)

    arq_final = open("output.fasta", "w")
    arq_final.write(alinhamento_final)


def backtrace(pos_inicial):
    caminho.append(pos_inicial)

    s = verificar(pos_inicial)
    while len(s.pais) > 0:
        pos_inicial = s.pais[0]
        caminho.append(pos_inicial)

        s = verificar(pos_inicial)

    print(f"\n\nCaminho: {caminho}\n\n")

    processaBacktrace()


def criarScoreMatriz():
    for i in range(1, len(sequencia1) + 1):
        for j in range(1, len(sequencia2) + 1):
            comparacao = match if sequencia1[i -
                                             1] == sequencia2[j-1] else mismatch

            score_1 = matriz[i - 1][j - 1] + comparacao
            score_2 = matriz[i][j-1] + gap
            score_3 = matriz[i - 1][j] + gap

            if score_1 >= score_2 and score_1 >= score_3:
                s = Score(score_1, (i, j))
                s.limpar_lista()
                s.addPais((i - 1, j - 1))

                if score_1 == score_2:
                    s.addPais((i, j - 1))
                    new_s = s
                    lista_scores.append(new_s)

                elif score_1 == score_3:
                    s.addPais((i - 1, j))
                    new_s = s
                    lista_scores.append(new_s)
                else:
                    new_s = s
                    lista_scores.append(new_s)

                matriz[i][j] = score_1

            elif score_2 >= score_1 and score_2 >= score_3:
                s = Score(score_2, (i, j))
                s.limpar_lista()
                s.addPais((i, j - 1))

                if score_2 == score_1:
                    s.addPais((i - 1, j - 1))
                    new_s = s
                    lista_scores.append(new_s)

                elif score_2 == score_3:
                    s.addPais((i - 1, j))
                    new_s = s
                    lista_scores.append(new_s)
                else:
                    new_s = s
                    lista_scores.append(new_s)

                matriz[i][j] = score_2

            elif score_3 >= score_1 and score_3 >= score_2:
                s = Score(score_3, (i, j))
                s.limpar_lista()
                s.addPais((i - 1, j))

                if score_3 == score_1:
                    s.addPais((i - 1, j - 1))
                    new_s = s
                    lista_scores.append(new_s)

                elif score_3 == score_2:
                    s.addPais((i, j - 1))
                    new_s = s
                    lista_scores.append(new_s)
                else:
                    new_s = s
                    lista_scores.append(new_s)

                matriz[i][j] = score_3

            pos_inicial = (i, j)

    printMatriz()
    return pos_inicial


def processaMatriz():
    i = gap - gap
    j = 0

    for val in matriz[0]:
        val += i
        i += gap

        s = Score(val, (0, j))
        s.limpar_lista()
        new_s = s
        lista_scores.append(new_s)

        matriz[0][j] = val
        j += 1

    indice = 0
    i = gap - gap
    for val in matriz:
        j = 0
        j += i
        i += gap

        s = Score(j, (indice, 0))
        s.limpar_lista()
        new_s = s
        lista_scores.append(new_s)

        matriz[indice][0] = j
        indice += 1


def printMatriz():
    for linha in matriz:
        print(linha)


if __name__ == "__main__":
    arq = open("input.fasta", "r")
    lista_entrada = arq.readlines()

    sequencia1 = lista_entrada[1].split("\n")[0]
    sequencia2 = lista_entrada[3].split("\n")[0]

    match = int(input("Digite o valor do Math: "))
    mismatch = int(input("Digite o valor do Mismath: "))
    gap = int(input("Digite o valor do GAP: "))
    print("\n\n")

    alinhamento_global()

    arq.close()
