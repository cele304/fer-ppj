import sys


class Automat:

    def __init__(self, gramatika, ulaz):
        self.gramatika = gramatika.split("\n")
        self.indeks = 0
        self.ulaz = ulaz
        self.parsirano = []
        self.nista = "$"
        for i in range(len(self.gramatika)):
            self.gramatika[i] = self.gramatika[i].split(" ::= ")

        for i in range(len(self.gramatika)):
            self.gramatika[i][1] = self.gramatika[i][1].split(" = ")

        for i in range(len(self.gramatika)):
            for j in range(len(self.gramatika[i][1])):
                self.gramatika[i][1][j] = self.gramatika[i][1][j].split(" ")
                for k in range(len(self.gramatika[i][1][j])):
                    self.gramatika[i][1][j][k] = self.gramatika[i][1][j][k].replace("{", "")
                    self.gramatika[i][1][j][k] = self.gramatika[i][1][j][k].replace("}", "")
            self.gramatika[i][0] = self.gramatika[i][0].strip()

    def pronadi(self, gornji_znak, znak):
        for i in range(len(self.gramatika)):
            if self.gramatika[i][0] == gornji_znak and znak in self.gramatika[i][1][1]:
                return self.gramatika[i][1][0]
        return

    def dajUlazniZnak(self, indeks):
        if self.indeks > len(self.ulaz):
            return None
        elif self.indeks == len(self.ulaz):
            return "⏊"
        return self.ulaz[self.indeks].split(" ")[0]

    def traziPoRedu(self, znak, broj):
        brojac = 0
        for i in range(len(self.ulaz)):
            if self.ulaz[i].split(" ")[0] == znak:
                brojac += 1
                if brojac == broj:
                    return self.ulaz[i].split(" ")
        return self.ulaz[i].split(" ")


    def ispisi(self):
        brojac = {}
        for i in range(len(self.parsirano)):
            if "<" in self.parsirano[i][0] or "$" in self.parsirano[i][0]:
                print(" " * self.parsirano[i][1] + self.parsirano[i][0])
                continue
            elif self.parsirano[i][0] not in brojac:
                brojac[self.parsirano[i][0]] = 1
            else:
                brojac[self.parsirano[i][0]] += 1
            print(" " * self.parsirano[i][1] + self.parsirano[i][0] + " " + self.traziPoRedu(self.parsirano[i][0], brojac[self.parsirano[i][0]])[1] + " " + self.traziPoRedu(self.parsirano[i][0], brojac[self.parsirano[i][0]])[2])

    def parsiraj(self, gornji, dubina):
        self.parsirano.append((gornji, dubina))
        znak = self.dajUlazniZnak(self.indeks)
        dobro = "DOBRO"
        #print(" " * dubina + gornji, znak, sep=" ")
        if gornji == self.nista:
            return "DOBRO"
        if "<" in gornji:
            if self.pronadi(gornji, znak) is None:
                return "NEMA_ZNAKA"
            else:
                for i in range(len(self.pronadi(gornji, znak))):
                    vrati = self.parsiraj(self.pronadi(gornji, znak)[i], dubina + 1)
                    if vrati != "DOBRO":
                        dobro = vrati
                        return dobro
            return dobro
        else:
            if znak == gornji:
                self.indeks += 1
                return "DOBRO"
            else:
                return "NISU_ISTI"

    def rijesi(self):
        reza = self.parsiraj("<program>", 0)
        i = len([x for x in self.parsirano if "<" not in x[0] and x[0] != "$"])
        if reza == "DOBRO":
            self.ispisi()
        elif reza == "NEMA_ZNAKA" and self.parsirano[i][0] != "⏊" and i < len(self.ulaz):
            a, b, c = self.ulaz[i].split(" ")
            print("err" + " " + a + " " + str(b) + " " + c)
        elif reza == "NISU_ISTI" and i < len(self.ulaz):
            a, b, c = self.ulaz[i-1].split(" ")
            print("err" + " " + a + " " + str(b) + " " + c)
        else:
            print("err kraj")





def main():
    gramatika = """<program> ::= <lista_naredbi> = {IDN KR_ZA ⏊}
    <lista_naredbi> ::= <naredba> <lista_naredbi> = {IDN KR_ZA}
    <lista_naredbi> ::= $ = {KR_AZ ⏊}
    <naredba> ::= <naredba_pridruzivanja> = {IDN}
    <naredba> ::= <za_petlja> = {KR_ZA}
    <naredba_pridruzivanja> ::= IDN OP_PRIDRUZI <E> = {IDN}
    <za_petlja> ::= KR_ZA IDN KR_OD <E> KR_DO <E> <lista_naredbi> KR_AZ = {KR_ZA}
    <E> ::= <T> <E_lista> = {IDN BROJ OP_PLUS OP_MINUS L_ZAGRADA}
    <E_lista> ::= OP_PLUS <E> = {OP_PLUS}
    <E_lista> ::= OP_MINUS <E> = {OP_MINUS}
    <E_lista> ::= $ = {IDN KR_ZA KR_DO KR_AZ D_ZAGRADA ⏊}
    <T> ::= <P> <T_lista> = {IDN BROJ OP_PLUS OP_MINUS L_ZAGRADA}
    <T_lista> ::= OP_PUTA <T> = {OP_PUTA}
    <T_lista> ::= OP_DIJELI <T> = {OP_DIJELI}
    <T_lista> ::= $ = {IDN KR_ZA KR_DO KR_AZ OP_PLUS OP_MINUS D_ZAGRADA ⏊}
    <P> ::= OP_PLUS <P> = {OP_PLUS}
    <P> ::= OP_MINUS <P> = {OP_MINUS}
    <P> ::= L_ZAGRADA <E> D_ZAGRADA = {L_ZAGRADA}
    <P> ::= IDN = {IDN}
    <P> ::= BROJ = {BROJ}"""

    ulaz = []
    for x in sys.stdin:
        if "br" in x:
            break
        ulaz.append(x.strip())

    A = Automat(gramatika, ulaz)

    A.rijesi()

    return

main()
