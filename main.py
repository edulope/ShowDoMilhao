import os
from termcolor import colored
from player import Player
import time
from question import Question

# Gamestate
# 0 - cadastro inicial
# 1 - decide se vai continuar ou parar
# 2 - pausa
# 3 - remover usuario
# 4 - acertou a resposta, tela congela por 2 segundos
# 5 - errou a resposta, tela congela por 2 segundos
# 6 - recebe pergunta
# 7 - Um jogador venceu

#definindo o escopo de cores e premios
Colors = [["1 - vermelho","red",False],["2 - azul","blue",False],["3 - amarelo", "yellow",False],["4 - verde", "green",False],["5 - cinza", "grey",False],["6 - branco", "white",False],["7 - ciano", "cyan",False],["8 - magenta", "magenta",False]]
Awards = [[1000, 0, 0],[2000, 1000, 500],[3000, 2000, 1000],[4000, 3000, 1500],[5000, 4000, 2000],[10000, 5000, 2500],[20000, 10000, 5000],[30000, 20000, 10000],[40000, 30000, 15000],[50000, 40000, 20000],[100000, 50000, 25000],[200000, 100000, 50000],[300000, 200000, 100000],[400000, 300000, 150000],[500000, 400000, 200000],[1000000, 500000, 0]]

#a funcao clear é a responsavel pela limpeza do terminal
clear = lambda: os.system('cls')

#array com players
Players = []
#variavel de controle do jogo
Exit = False
#variavel de estado do jogo
GameState = 0
#variavel de questões em sequencia daquele jogador(vai ser utilizada no awards)
QuestionCount = 0
#variavel que define a vez dos jogadores
turn = 0
#questão atual e alternativas
Q = None
Alts = None




def ShowNames():
    if(GameState == 3):
        for i in range(len(Players)):
            print(i+1, " -> ", end='')
            print(colored(Players[i].GetName(), Colors[Players[i].GetColor()][1]))
    else:
        for i in range(len(Players)):
            if (i == turn): print(">>>", end='')
            print(colored(Players[i].GetName(), Colors[Players[i].GetColor()][1]), "RS$" + str(Players[i].GetPoints()) + ",00")

#Essa função é chamada a cada loop do jogo, ela é a responsavel por trazer a interface adequada para o estado atual
def GameText(Player = Player()):
    print("bem vindo ao Show do milhão")
    print("Utilize um teclado numérico para selecionar as alternativas, use P para entrar no menu de opções e Q para sair, e bom jogo :)")
    global Q
    global Alts
    global QuestionCount

    if(GameState == 0):
        print("Selecione o numero de jogadores(Max 8)")

    if(GameState == 1):
        ShowNames()
        print("Premio por acertar: R$" + str(Awards[QuestionCount][0]) + ",00")
        print("Premio por sair: R$" + str(Awards[QuestionCount][1]) + ",00")
        print("Premio por errar: R$" + str(Awards[QuestionCount][2]) + ",00")
        print((colored(Players[turn].GetName(), Colors[Players[turn].GetColor()][1])), ", o que você escolhe? (C)continuar ou (S)sair?")

    if(GameState == 2):
        print("deseja (A)adicionar/(R)remover jogador?")

    if(GameState == 3):
        print("Por favor insira o jogador que você deseja excluir")
        ShowNames()

    if(GameState == 4 or GameState == 5):
        ShowNames()
        print("\n")
        print(Q.GetPergunta())
        for i in range(len(Alts)):
            if(Alts[i] == Q.GetResposta()): print(str(i + 1) + "- " + colored(Alts[i], "green"))
            else: print(str(i + 1) + "- " + colored(Alts[i], "red"))
        if(GameState == 4):
            print("você acertou")
        else: print("você errou")

    if(GameState == 6):
        ShowNames()
        if (Q == None):
            Q = Question()
            Alts = Q.GetAlternativas()
        print("\n")
        print(Q.GetPergunta())
        print("1- " + Alts[0] + "\n" + "2- " + Alts[1] + "\n" + "3- " + Alts[2] + "\n" + "4- " + Alts[3])

    if(GameState == 7):
        ShowNames()
        print("Temos um novo milionário, parabéns ", Players[turn].GetName())
        print("deseja uma nova partida? (S) para continuar e (Q) para sair")

def RegisterPlayer():
    clear()
    print("Por favor insira seu nome.")
    name = input()
    print("Escolha uma cor")
    for i in Colors:
        if(not i[2]):
            print(colored(i[0], i[1]))
    color = input()
    while(not(color.isnumeric() and int(color) > 0 and int(color) < 9 and not Colors[int(color) -1][2])):
        print("por favor, insira uma cor válida")
        color = input()
    Players.append(Player(name=name, color = int(color)-1))
    Colors[int(color)-1][2] = True

def RemovePlayer(id):
    global turn
    global QuestionCount
    Colors[Players[id].GetColor()][2] = False
    if(id == turn): QuestionCount = 0
    Players.pop(id)
    if(len(Players) <= turn):
        turn = 0


#loop do jogo
while (not Exit):
    clear()
    GameText()
    #estados 4 e 5 não usam input, ficam com a tela congelada e depois voltam para 1 ou 7
    if(GameState != 4 and GameState != 5):
        Input = input()
        if(Input.isnumeric() and int(Input) > 0 and int(Input) < 9):
            if(GameState == 0):
                for i in range(int(Input)):
                    RegisterPlayer()
                GameState = 1
            if(GameState == 6 and int(Input) <= 4 and Q is not None):
                if(Alts[int(Input) - 1] == Q.GetResposta()):
                    GameState = 4
                else: GameState = 5
            if(GameState == 3 and int(Input)<= len(Players)):

                print("Tem certeza que deseja remover ", Players[int(Input)-1].GetName(),  "?(S/N)")
                answer = input()
                if(answer == "S"):
                    RemovePlayer(int(Input)-1)
                GameState = 2

        #tecla de pause
        elif(Input == "P"):
            if(GameState == 1):
                GameState = 2
            elif(GameState == 2):
                if (len(Players) == 0):
                    print("é necessário ter pelo menos um jogador")
                    time.sleep(1)
                else: GameState = 1

        #tecla para adicionar player durante pause
        elif(Input == "A"):
            if(GameState == 2):
                if(len(Players) < 8):
                    RegisterPlayer()
                else:
                    print("Numero Máximo de jogadores atingido")

        #tecla para remover players durante o pause
        elif (Input == "R"):
            if (GameState == 2 and len(Players)>0):
                GameState = 3

        #tecla para sair do jogo
        elif(Input == "Q"):
            Exit = True

        #tecla para desistir da aposta, também pode é utilizada para confirmar novo jogo e remoção de um player(a remoção está em outro trecho)
        elif(Input == "S"):
            if(GameState == 1):
                Players[turn].SetPoints(Players[turn].GetPoints() + Awards[QuestionCount][1])
                QuestionCount = 0
                turn = turn + 1
                if (turn >= len(Players)): turn = 0
            if(GameState == 7):
                for i in Players:
                    i.SetPoints(0)
                Q = Question()
                Alts = Q.GetAlternativas()
                GameState = 1

        #tecla para continuar aposta
        elif(Input == "C"):
            if(GameState == 1):
                GameState = 6

    else:
        time.sleep(2)
        if(GameState == 5):
            Players[turn].SetPoints(Players[turn].GetPoints() + Awards[QuestionCount][2])
            turn = turn + 1
            if(turn>=len(Players)): turn = 0
            QuestionCount = 0
            GameState = 1
        else:
            if(Players[turn].GetPoints() + Awards[QuestionCount][0]>= 1000000):
                Players[turn].SetPoints(Players[turn].GetPoints() + Awards[QuestionCount][0])
                GameState = 7
            else:
                QuestionCount += 1
                GameState = 1
        Q = Question()
        Alts = Q.GetAlternativas()