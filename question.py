import random


class Question:
    def __init__(self):
        f = open("questions.txt", "r", encoding="utf-8")
        lines = f.readlines()
        #a cada 5 linhas temos 1 pergunta e 4 alternativas, a ultima sendo a resposta
        selected = random.randint(0, (len(lines)//5)-1)
        self._pergunta = lines[(5*selected)]
        self._alternativa1 = lines[(5*selected)+1][3:]
        self._alternativa2 = lines[(5*selected)+2][3:]
        self._alternativa3 = lines[(5*selected)+3][3:]
        self._alternativa4 = lines[(5*selected)+4][3:]
        f.close()


    def GetPergunta(self):
        return self._pergunta


    def GetResposta(self):
        return self._alternativa4

    #embaralha alternativas a fim de que a ultima não necessáriamente seja a resposta
    def GetAlternativas(self):
        AltArr = [self._alternativa1, self._alternativa2, self._alternativa3, self._alternativa4]
        randomAltArr = []
        forSize = len(AltArr)
        for i in range(forSize):
            selected = random.randint(0, len(AltArr)-1)
            randomAltArr.append(AltArr[selected])
            AltArr.pop(selected)
        return randomAltArr