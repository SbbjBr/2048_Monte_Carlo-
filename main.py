import random 
import numpy as np
import os 
import pyfiglet
from alive_progress import alive_bar
from colorama import Fore, Back, Style
import time

bot_jogando = True

velocidade = 0
quantidade_vezes = 100

class Tabuleiro():
    def pegar_valores_vazios(self, tabuleiro):
        """Retorna uma lista com listas com as coordenadas (linha, indice) onde possuem valores vazios"""
        valores_vazios = []
        
        for index_linha, linha in enumerate(tabuleiro):
            for index, valor in enumerate(linha):
                if valor == 0:
                    valores_vazios.append([index_linha, index])
                    
        return valores_vazios
    
    
    def colocar_numero_nos_vazios(self, tabuleiro):
        """Pego a lista de valores vazios, seleciona uma coordenada aleatória e coloca um valor nela"""

        coordenadas = random.choice(self.pegar_valores_vazios(tabuleiro))
        
        valor_aleatorio = np.random.random()
        
        if valor_aleatorio <= 0.85:
            tabuleiro[coordenadas[0]][coordenadas[1]] = 2
        else:
            tabuleiro[coordenadas[0]][coordenadas[1]] = 4
            
        return tabuleiro
            
    def empurrar(self, tabuleiro, movimento):
        """Empurra o tabuleiro pra direção escolhida"""

        if movimento == "w":
            tabuleiro = np.rot90(tabuleiro)
        
        elif movimento == "d":
            tabuleiro = np.rot90(tabuleiro, 2)
        
        elif movimento == "s":
            tabuleiro = np.rot90(tabuleiro, 3)
    
    
        for indice_linha, linha in enumerate(tabuleiro): #sempre empurra pra direita
            for vezes_repeticao in range(3):
                for indice, valor in enumerate(linha):
                    if indice != 3:
                        if valor == 0 and linha[indice + 1] != 0:
                            tabuleiro[indice_linha][indice] = linha[indice + 1]
                            tabuleiro[indice_linha][indice + 1] = 0

        if movimento == "w":
            tabuleiro = np.rot90(tabuleiro, 3)
            
        elif movimento == "d":  
            tabuleiro = np.rot90(tabuleiro, 2)
        
        elif movimento == "s":
            tabuleiro = np.rot90(tabuleiro, 1)        
        
        return tabuleiro

    def empurrar_somar(self, tabuleiro, movimento):
        """Dado o tabuleiro, soma e empurra os valores dada a direção"""

        
        ultimo_tabuleiro = self.copiar_tabuleiro(tabuleiro)

        tabuleiro = self.empurrar(tabuleiro, movimento)
        
        pontos = 0

        
        if movimento == "w":
            tabuleiro = np.rot90(tabuleiro)
        
        elif movimento == "d":
            tabuleiro = np.rot90(tabuleiro, 2)
        
        elif movimento == "s":
            tabuleiro = np.rot90(tabuleiro, 3)
        
        for indice_linha, linha in enumerate(tabuleiro): #sempre empurra pra direita
            soma = 0
            for indice, valor in enumerate(linha):
                if indice != 3:
                    if soma != 0: #Esse if evita que some os valores duplicadamente, então caso some, ele pula um pra frente
                        soma = 0
                        continue
                        
                    if valor == linha[indice + 1]:
                        tabuleiro[indice_linha][indice + 1] = valor * 2
                        tabuleiro[indice_linha][indice] = 0
                        soma += 1
                        pontos += valor * 2

        if movimento == "w":
            tabuleiro = np.rot90(tabuleiro, 3)
            
        elif movimento == "d":  
            tabuleiro = np.rot90(tabuleiro, 2)
        
        elif movimento == "s":
            tabuleiro = np.rot90(tabuleiro, 1)   
            
        tabuleiro = self.empurrar(tabuleiro, movimento)
        
        if not np.array_equal(ultimo_tabuleiro, tabuleiro):
            tabuleiro = self.colocar_numero_nos_vazios(tabuleiro)
            
        return tabuleiro, pontos

        
    def copiar_tabuleiro(self, tabuleiro):
        """Copia o tabuleiro"""
        
        tabuleiro_copiado = np.copy(tabuleiro)

        tabuleiro_copiado = np.rot90(tabuleiro_copiado, 4)
        
        return tabuleiro_copiado
        
    def checar_se_ganhou(self, tabuleiro):
        """Checa se ganhou"""
        
        tabuleiro = self.copiar_tabuleiro(tabuleiro)
    
        for linha in tabuleiro:
            for valor in linha:
                if valor >= 2048:
                    return True
        return False

    def pegar_futuros(self, tabuleiro):
        """Pega os pontos futuros de um tabuleiro"""
    
        tabuleiro = self.copiar_tabuleiro(tabuleiro)
    
        possibilidades = ["w", "a", "s", "d"]
        lista_pontos_futuros = []
        lista_vazios_futuros = []

        for movimento in possibilidades:
            _, pontos = self.empurrar_somar(tabuleiro, movimento)
            lista_pontos_futuros.append(pontos)
            lista_vazios_futuros.append(len(self.pegar_valores_vazios(_)))

        return lista_pontos_futuros, lista_vazios_futuros
    
    
    def checar_se_perdeu(self, tabuleiro):
        vazio = [0,0,0,0]
        
        tabuleiro = self.copiar_tabuleiro(tabuleiro)

        vazios = self.pegar_valores_vazios(tabuleiro)

        pontos_futuros = self.pegar_futuros(tabuleiro)
        pontos_futuros = pontos_futuros[0]
    

        if np.array_equal(pontos_futuros, vazio) and len(vazios) == 0:
            return True
        else:
            return False    
    
    def pegar_valor_aleatorio(self, array):
        return np.random.choice(array)
    
    def pegar_maior_valor(self, array):
        return np.sort(array, axis=None)[-1]   

    
class Jogo():
    def __init__(self):
        """ variavel das funções dos tabuleiros será 'self.funcoes_t' """
        self.funcoes_t = Tabuleiro()
        
        self.quantidade_jogos = 0
        
        self.pontuacao_maxima = 0
        
        self.ultima_pontuacao = 0
    
    def iniciar_novo_tabuleiro(self):
        """Inicia um novo tabuleiro"""
    
        self.tabuleiro = [[0,0,0,0], 
                          [0,0,0,0],
                          [0,0,0,0],
                          [0,0,0,0]]
        
        self.tabuleiro = np.rot90(self.tabuleiro, 4)
        
        self.pontos = 0
        
        self.movimentos_totais = 0
        
        self.pontos_ganhos = 0
        
        self.ultimo_movimento = ""
        
        self.espacos_vazios = len(self.funcoes_t.pegar_valores_vazios(self.tabuleiro))

        for _ in range(2):
            self.funcoes_t.colocar_numero_nos_vazios(self.tabuleiro)    
    
    def imprimir(self):
        
        """Imprime o tabuleiro"""
        
        
        os.system("CLS")
        
        
        print(Fore.RED, pyfiglet.figlet_format("Lucas Rocha - 2048", font = "digital" ), Fore.RESET)
        print()
        
        for linha in self.tabuleiro:
            for index, valor in enumerate(linha):
                #==================================DEFINE AS CORES DOS NUMEROS =========================================================
                if valor == 0:
                    globals()[f"valor_{index}"] = Fore.RESET + Style.NORMAL + f"{valor}" + Fore.RESET + Style.NORMAL + Back.RESET
                elif valor == 2:
                    globals()[f"valor_{index}"] = Fore.YELLOW + Style.BRIGHT + f"{valor}" + Fore.RESET + Style.NORMAL + Back.RESET
                
                elif valor == 4:
                    globals()[f"valor_{index}"] = Fore.YELLOW + Style.NORMAL + f"{valor}" + Fore.RESET + Style.NORMAL + Back.RESET
                
                elif valor == 8:
                    globals()[f"valor_{index}"] = Fore.YELLOW + Style.DIM + f"{valor}" + Fore.RESET + Style.NORMAL + Back.RESET
                    
                elif valor == 16:
                    globals()[f"valor_{index}"] = Fore.RED +  Style.BRIGHT + f"{valor}" + Fore.RESET + Style.NORMAL + Back.RESET
                
                elif valor == 32:
                    globals()[f"valor_{index}"] = Fore.RED +  Style.NORMAL + f"{valor}" + Fore.RESET + Style.NORMAL + Back.RESET
                    
                elif valor == 64:
                    globals()[f"valor_{index}"] = Fore.RED +  Style.DIM + f"{valor}" + Fore.RESET + Style.NORMAL + Back.RESET
                
                elif valor == 128:
                    globals()[f"valor_{index}"] = Fore.CYAN +  Style.NORMAL + f"{valor}" + Fore.RESET + Style.NORMAL + Back.RESET
                
                elif valor == 256:
                    globals()[f"valor_{index}"] = Fore.CYAN +  Style.DIM + f"{valor}" + Fore.RESET + Style.NORMAL + Back.RESET
                
                elif valor == 512:
                    globals()[f"valor_{index}"] = Fore.BLUE +  Style.BRIGHT + f"{valor}" + Fore.RESET + Style.NORMAL + Back.RESET
                
                elif valor == 1024:
                    globals()[f"valor_{index}"] = Fore.BLUE +  Style.NORMAL + f"{valor}" + Fore.RESET + Style.NORMAL + Back.RESET
                
                else:
                    globals()[f"valor_{index}"] = Back.YELLOW + Fore.BLUE +  Style.DIM + f"{valor}" + Fore.RESET + Style.NORMAL + Back.RESET
                
                #=====================================================================================================================
                
            #Imprime a linha do tabuleiro        
            print("    ", valor_0, " " * (4 - len(str(linha[0]))), valor_1," " * (4 - len(str(linha[1]))), valor_2," " * (4 - len(str(linha[2]))), valor_3, Style.RESET_ALL)
        
        #imprime a pontuacao    
        print(f"                                    Pontos: {self.pontos}", " " * (8 - len(str(self.pontos))), f"Última pontuação: {self.ultima_pontuacao}", " " * (6 - len(str(self.ultima_pontuacao))), f"Pontuação máxima: {self.pontuacao_maxima}")
        
        #Imprime informações movimento e jogo
        print(f"                                    Movimento: {self.ultimo_movimento}", " " * (5 - len(str(self.ultimo_movimento))), f"Movimentos Totais: {self.movimentos_totais}", " " * (10 - len(str(self.movimentos_totais))),f"Jogo: {self.quantidade_jogos}")
        
        #Informações espacos vazios e pontos ganhos
        print(f"                                    Espaços vazios: {self.espacos_vazios}", " " * (5 - len(str(self.espacos_vazios))), f"Pontos ganhos:{self.pontos_ganhos}")

        #Imprime jogadas possíveis passadas
        print()
        print("                                                             Jogadas passadas:")
        print("                                                                           Pontos - Espaço")
        
        if self.movimentos_totais > 1:
            for i, possibilidades in enumerate(["w","a","s","d"]):
                if possibilidades == self.ultimo_movimento:
                     print(Fore.RED + f"                                                                 '{possibilidades.upper()[0]}'         {self.pontos_passados[i]}", " " * (8 - len(str(self.pontos_passados[i]))),f"{self.vazios_passados[i]}" + Fore.RESET)
                else:
                    print(f"                                                                 '{possibilidades.upper()[0]}'         {self.pontos_passados[i]}", " " * (8 - len(str(self.pontos_passados[i]))),f"{self.vazios_passados[i]}")
    
    def bot(self, tabuleiro, vezes = 1000):
        tabuleiro_original = self.funcoes_t.copiar_tabuleiro(tabuleiro)
        
        possibilidades = ["w","a","s","d"]
        
                 #   w  a  s  d
        pontuacao = [[],[],[],[]]   
        pontuacao_f = []
        
  
        for monte_c in range(vezes):
            tabuleiro = self.funcoes_t.copiar_tabuleiro(tabuleiro_original)
            primeira_jogada = self.funcoes_t.pegar_valor_aleatorio(possibilidades)
            trigger_perdeu = False
            
            tabuleiro, pontos_totais = self.funcoes_t.empurrar_somar(tabuleiro, primeira_jogada) 
            
            
            while trigger_perdeu == False:
                movimento = self.funcoes_t.pegar_valor_aleatorio(possibilidades)
                tabuleiro, ponto = self.funcoes_t.empurrar_somar(tabuleiro, movimento)
                pontos_totais += ponto

                
                trigger_perdeu = self.funcoes_t.checar_se_perdeu(tabuleiro)
            
            pontuacao[possibilidades.index(primeira_jogada)].append(pontos_totais)
                

        
        for i, arrays in enumerate(pontuacao):
            pontuacao_f.append(np.mean(arrays))

        pontuacao = 0
        movimento = None
        for i, valor in enumerate(pontuacao_f):
            if valor > pontuacao:
                pontuacao = valor
                movimento = possibilidades[i]
                
        return movimento
            
    
    def jogar(self, movimento = 0):
    
        self.iniciar_novo_tabuleiro()
        tabuleiro = 0
        
        while True:
        
            self.imprimir()
            
            self.futuros = self.funcoes_t.pegar_futuros(self.tabuleiro)
            self.pontos_passados = self.futuros[0]
            self.vazios_passados = self.futuros[1]
        
            possibilidades = ["w", "a", "s", "d"]
        
            if not bot_jogando: 
                if movimento == 0:
                    while movimento not in possibilidades:
                        movimento = input()
            
            else:
                movimento = self.bot(self.tabuleiro, quantidade_vezes)
                time.sleep(velocidade)
            
            tabuleiro, pontos = self.funcoes_t.empurrar_somar(self.tabuleiro, movimento)
            
            self.tabuleiro = tabuleiro
            
            self.pontos += pontos
            
            self.pontos_ganhos = pontos
            
            self.espacos_vazios = len(self.funcoes_t.pegar_valores_vazios(self.tabuleiro))
            
            self.ultimo_movimento = movimento
            
            self.movimentos_totais += 1
            
            movimento = 0
            
            
            self.trigger_ganhou = self.funcoes_t.checar_se_ganhou(self.tabuleiro)
            self.trigger_perdeu = self.funcoes_t.checar_se_perdeu(self.tabuleiro)
            
            
            if self.trigger_perdeu == True:
                pontos_futuros = self.funcoes_t.pegar_futuros(tabuleiro)
                print(pontos_futuro)
    
                print(Fore.RED + "VOCÊ PERDEU!" + Fore.RESET)
                a = input()
                self.imprimir()
                print(Fore.RED + "VOCÊ PERDEU!" + Fore.RESET)
                time.sleep(10)
                

                a = input()
            
                self.trigger_perdeu = False
                self.quantidade_jogos += 1
                self.movimentos_totais = 0
                
                if self.pontos > self.pontuacao_maxima:
                    self.pontuacao_maxima = self.pontos
                    self.ultima_pontuacao = self.pontos
                    self.pontos = 0
                
                self.iniciar_novo_tabuleiro()
                
        
        
if __name__ == "__main__":
    
    app = Jogo()
    app.jogar()
        