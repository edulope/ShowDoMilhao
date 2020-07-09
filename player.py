class Player:
    def __init__(self, name = "Nome não informado", color = 0):
        #name: nome a ser exibido
        self._name = name
        #color: cor para o nome a ser exibido
        self._color = color
        #points: pontuacao atual do player
        self._points = 0

    def GetColor(self):
        return self._color

    def GetName(self):
        return self._name

    def GetPoints(self):
        return self._points

    def SetColor(self, Color):
        self._color = Color
        return

    def SetName(self, Name):
        self._Name = Name
        return

    def SetPoints(self, Points):
        self._points = Points
        return