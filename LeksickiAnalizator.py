import sys

class Automat:

    def __init__(self, lista):
        self.rijeci = lista[:]

    def rastavi(self, rijec):
        G = []
        for z in self.rijeci:
            for i in range(len(rijec)):
                broji = 0
                for j in range(len(z)):
                    if i + j < len(rijec) and rijec[i + j] == z[j]:
                        broji += 1
                if broji == len(z):
                    G.append((i, len(z)))
        nova = []
        G.sort(key=lambda x: x[0])
        for i in range(len(G)):
            if i == 0:
                nova.append((0, G[i][0]))
            else:
                nova.append((G[i - 1][0] + G[i - 1][1], G[i][0] - G[i - 1][0] - G[i - 1][1]))
            if i == len(G) - 1:
                nova.append((G[i][0] + G[i][1], len(rijec) - G[i][0] - G[i][1]))
        for i in range(len(nova)):
            G.append(nova[i])
        G.sort(key=lambda x: x[0])
        if len(G) == 0:
            G.append((0, len(rijec)))
        vrati = [rijec[G[i][0]:G[i][0] + G[i][1]] for i in range(len(G))]
        for i in range(len(vrati)):
            vrati[i] = vrati[i].strip()
        return vrati


def main():

    def makniRazmakeIzListe(lista):
        vrati = []
        for i in range(len(lista)):
            lista[i] = lista[i].strip()
        for i in range(len(lista)):
            if lista[i] != '':
                vrati.append(lista[i])
        return vrati

    mapa = {"za": "KR_ZA",
            "od": "KR_OD",
            "do": "KR_DO",
            "az": "KR_AZ",
            "+": "OP_PLUS",
            "-": "OP_MINUS",
            "*": "OP_PUTA",
            "/": "OP_DIJELI",
            "(": "L_ZAGRADA",
            ")": "D_ZAGRADA",
            "=": "OP_PRIDRUZI",}

    def checkNumerical(rijec):
        flag = True
        for i in range(len(rijec)):
            if not rijec[i].isdigit():
                flag = False
        return flag

    def dajNaziv(rijec):
        if rijec in mapa:
            return mapa[rijec]
        else:
            return "BROJ" if checkNumerical(rijec) else "IDN"

    for br, redak in enumerate(sys.stdin):
        bez_komentara = redak.split("//")[0]
        bez_komentara = " " + bez_komentara + " "

        bez_komentara = bez_komentara.split("\t")
        bez_komentara = " ".join(bez_komentara)

        KR = Automat([" za ", " az ", " od ", " do "])
        rijeci = makniRazmakeIzListe(KR.rastavi(bez_komentara))
        OS = Automat(["*", "/", "+", "-", "=", "(", ")", " "])
        lista = []
        for i in range(len(rijeci)):
            lista.append(makniRazmakeIzListe(OS.rastavi(rijeci[i])))

        listaPopravljena = []
        for i in range(len(lista)):
            for j in range(len(lista[i])):
                listaPopravljena.append(lista[i][j])
        listaNova = []
        for i in range(len(listaPopravljena)):
            prvoNeBroj = -1
            for j in range(len(listaPopravljena[i])):
                if not listaPopravljena[i][j].isdigit():
                    prvoNeBroj = j
                    break
            if prvoNeBroj != -1:
                listaNova.append(listaPopravljena[i][:prvoNeBroj])
                listaNova.append(listaPopravljena[i][prvoNeBroj:])
            else:
                listaNova.append(listaPopravljena[i])
        listaNova2 = [ x.split(" ") for x in listaNova ]
        listaPopravljena2 = []
        for i in range(len(listaNova2)):
            for j in range(len(listaNova2[i])):
                if listaNova2[i][j] != "":
                    listaPopravljena2.append(listaNova2[i][j].strip())
        for i in range(len(listaPopravljena2)):
            listaPopravljena2[i] = listaPopravljena2[i].strip()
            if listaPopravljena2[i] != '':
                print(f"{dajNaziv(listaPopravljena2[i])} {br + 1} {listaPopravljena2[i]}")
    return


main()
