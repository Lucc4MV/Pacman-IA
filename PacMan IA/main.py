from tkinter import messagebox
import pygame
from AIAgent import AIAgent
from game import Game

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576

def main():
    # Inicializar todos os módulos pygame importados
    pygame.init()
    # Defina a largura e a altura da tela [width, height]
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    # Definir a legenda da janela atual
    pygame.display.set_caption("PACMAN")
    # Faça um loop até que o usuário clique no botão Fechar.
    done = False
    # Usado para gerenciar a rapidez com que a tela é atualizada
    clock = pygame.time.Clock()
    # Criar um objeto de jogo
    game = Game()
    # -------- Loop do programa principal ---------
    while not done:
        # --- processar eventos (keystrokes, mouse clicks, etc)
        done = game.process_events()
        # --- A lógica do jogo deve ir aqui
        game.run_logic()
        # --- Desenhe o quadro atual
        game.display_frame(screen)
        # --- Limit to 30 frames per second
        clock.tick(30)
        #----Looping da IA
        AIAgent(game.player, game.enemies)
        #messagebox.showinfo("GAME OVER!","Final Score = "+(str)(game.score))
    # Feche a janela e saia.
    # Se você esquecer esta linha, o programa irá 'travar'
    # na saída, se estiver executando em IDLE.
    pygame.quit()

if __name__ == '__main__':
    main()