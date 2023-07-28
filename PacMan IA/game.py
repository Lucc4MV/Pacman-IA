import pygame
from player import Player
from enemies import *
import tkinter
from tkinter import messagebox
from AIAgent import *
import time


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576

# Define ome colors
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)

class Game(object):
    def __init__(self):
        self.font = pygame.font.Font(None,40)
        self.about = False
        self.game_over = True
        # Crie a variável para a pontuação
        self.score = 0
        # Crie a variavel das Vidas do Pacman
        # Crie a fonte para exibir a partitura na tela
        self.font = pygame.font.Font(None,35)
        # Crie o menu do jogo
        self.menu = Menu(("Iniciar","Sair"),font_color = WHITE,font_size=60)
        # Cire o jogador
        self.player = Player(32,128,"player.png")
        # Crie os blocos que definirão os caminhos por onde o jogador pode ir
        self.horizontal_blocks = pygame.sprite.Group()
        self.vertical_blocks = pygame.sprite.Group()
        # Crie um grupo para os pontos na tela
        self.dots_group = pygame.sprite.Group()
        # Defina o ambiente:
        for i,row in enumerate(enviroment()):
            for j,item in enumerate(row):
                if item == 1:
                    self.horizontal_blocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
                elif item == 2:
                    self.vertical_blocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
        # Crie os inimigos
        self.enemies = pygame.sprite.Group()
        self.enemies.add(Slime(288,96,0,2))
        self.enemies.add(Slime(288,320,0,-2))
        self.enemies.add(Slime(544,128,0,2))
        self.enemies.add(Slime(32,224,0,2))
        self.enemies.add(Slime(160,64,2,0))
        self.enemies.add(Slime(448,64,-2,0))
        self.enemies.add(Slime(640,448,2,0))
        self.enemies.add(Slime(448,320,2,0))
        # Adicione os pontos dentro do jogo
        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item != 0:
                    self.dots_group.add(Ellipse(j*32+12,i*32+12,WHITE,8,8))

        # Carregar os efeitos sonoros
        self.pacman_sound = pygame.mixer.Sound("pacman_sound.ogg")
        self.game_over_sound = pygame.mixer.Sound("game_over_sound.ogg")


    def process_events(self):
        for event in pygame.event.get(): # O usuário fez algo
            if event.type == pygame.QUIT: # Se o usuário clicou em fechar
                return True
            self.menu.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.game_over and not self.about:
                        if self.menu.state == 0:
                            # ---- Inicio ------
                            self.__init__()
                            self.game_over = False
                        elif self.menu.state == 2:
                            # --- SAIR -------
                            return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.player.explosion = True
        return False

    def run_logic(self):
        if not self.game_over:
            self.player.update(self.horizontal_blocks,self.vertical_blocks)
            block_hit_list = pygame.sprite.spritecollide(self.player,self.dots_group,True)
            # Quando a block_hit_list contém um sprite, isso significa que o jogador atingiu um ponto
            if len(block_hit_list) > 0:
                # Aqui será o efeito sonoro
                self.pacman_sound.play()
                self.score += 1
            block_hit_list = pygame.sprite.spritecollide(self.player,self.enemies,True)
            if len(block_hit_list) > 0:
                self.player.explosion = True
                self.game_over_sound.play()
            self.game_over = self.player.game_over
            self.enemies.update(self.horizontal_blocks,self.vertical_blocks)
            #messagebox.showinfo("GAME OVER!","Final Score = "+(str)(self.score))    

    def display_frame(self,screen):
        screen.fill(BLACK)
        # O código do desenho deve ir aqui
        if self.game_over:
            if self.about:
                self.display_message(screen,"É um jogo de arcade")
            else:
                self.menu.display_frame(screen)
        else:
            self.horizontal_blocks.draw(screen)
            self.vertical_blocks.draw(screen)
            draw_enviroment(screen)
            self.dots_group.draw(screen)
            self.enemies.draw(screen)
            screen.blit(self.player.image,self.player.rect)
            # Renderizar o texto para aba
            text = self.font.render("Score: " + str(self.score),True,GREEN)
            # Coloque o texto na tela
            screen.blit(text,[120,20])
            
        # --- Vá em frente e atualize a tela com o que desenhamos.
        pygame.display.flip()

    def display_message(self,screen,message,color=(255,0,0)):
        label = self.font.render(message,True,color)
        # Obtenha a largura e a altura do rótulo
        width = label.get_width()
        height = label.get_height()
        # Determinar a posição da etiqueta
        posX = (SCREEN_WIDTH /2) - (width /2)
        posY = (SCREEN_HEIGHT /2) - (height /2)
        # Desenhe o rótulo na tela
        screen.blit(label,(posX,posY))

class Menu(object):
    state = 0
    def __init__(self,items,font_color=(0,0,0),select_color=(255,0,0),ttf_font=None,font_size=25):
        self.font_color = font_color
        self.select_color = select_color
        self.items = items
        self.font = pygame.font.Font(ttf_font,font_size)
        
    def display_frame(self,screen):
        for index, item in enumerate(self.items):
            if self.state == index:
                label = self.font.render(item,True,self.select_color)
            else:
                label = self.font.render(item,True,self.font_color)
            
            width = label.get_width()
            height = label.get_height()
            
            posX = (SCREEN_WIDTH /2) - (width /2)
            # t_h: altura total do bloco de texto
            t_h = len(self.items) * height
            posY = (SCREEN_HEIGHT /2) - (t_h /2) + (index * height)
            
            screen.blit(label,(posX,posY))
        
    def event_handler(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.state > 0:
                    self.state -= 1
            elif event.key == pygame.K_DOWN:
                if self.state < len(self.items) -1:
                    self.state += 1