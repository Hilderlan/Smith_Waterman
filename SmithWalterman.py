match = None
mismatch = None
gap = None
sequencia1 = ""
sequencia2 = ""
matriz = []


def alinhamento_global():
    linha = []

    for _ in range(len(sequencia2) + 1):
        for _ in range(len(sequencia1) + 1):
            linha.append(0)
        matriz.append(linha)
        linha = []


if __name__ == "__main__":
    sequencia1 = "ATAGACGACATACAGACAGCATACAGACAGCATACAGA"
    sequencia2 = "TTTAGCATGCGCATATCAGCAATACAGACAGATACG"

    alinhamento_global()
