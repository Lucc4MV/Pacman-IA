import pygame
import random
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576

# Definir algumas cores
BLACK = (0,0,0)
WHITE = (255,255,255)

class Player(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    explosion = False
    game_over = False
    def __init__(self,x,y,filename):
        # Chame o construtor da classe pai (sprite)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        # Carrega a imagem que será para a animação
        img = pygame.image.load("walk.png").convert()
        # Crie os objetos de animação
        self.move_right_animation = Animation(img,32,32)
        self.move_left_animation = Animation(pygame.transform.flip(img,True,False),32,32)
        self.move_up_animation = Animation(pygame.transform.rotate(img,90),32,32)
        self.move_down_animation = Animation(pygame.transform.rotate(img,270),32,32)
        # Carregar imagem da explosão
        img = pygame.image.load("explosion.png").convert()
        self.explosion_animation = Animation(img,30,30)
        # Salve a imagem do jogador
        self.player_image = pygame.image.load(filename).convert()
        self.player_image.set_colorkey(BLACK)

    def update(self,horizontal_blocks,vertical_blocks):
        if not self.explosion:
            if self.rect.right < 0:
                self.rect.left = SCREEN_WIDTH
            elif self.rect.left > SCREEN_WIDTH:
                self.rect.right = 0
            if self.rect.bottom < 0:
                self.rect.top = SCREEN_HEIGHT
            elif self.rect.top > SCREEN_HEIGHT:
                self.rect.bottom = 0
            self.rect.x += self.change_x
            self.rect.y += self.change_y

            # Isso fará com que o usuário pare de subir ou descer quando estiver dentro da caixa

            for block in pygame.sprite.spritecollide(self,horizontal_blocks,False):
                self.rect.centery = block.rect.centery
                self.change_y = 0
            for block in pygame.sprite.spritecollide(self,vertical_blocks,False):
                self.rect.centerx = block.rect.centerx
                self.change_x = 0

            # Isso fará com que a animação comece
            
            if self.change_x > 0:
                self.move_right_animation.update(10)
                self.image = self.move_right_animation.get_current_image()
            elif self.change_x < 0:
                self.move_left_animation.update(10)
                self.image = self.move_left_animation.get_current_image()

            if self.change_y > 0:
                self.move_down_animation.update(10)
                self.image = self.move_down_animation.get_current_image()
            elif self.change_y < 0:
                self.move_up_animation.update(10)
                self.image = self.move_up_animation.get_current_image()
        else:
            if self.explosion_animation.index == self.explosion_animation.get_length() -1:
                pygame.time.wait(500)
                self.game_over = True
            self.explosion_animation.update(12)
            self.image = self.explosion_animation.get_current_image()
            

    def move_right(self):
        self.change_x = 3

    def move_left(self):
        self.change_x = -3

    def move_up(self):
        self.change_y = -3

    def move_down(self):
        self.change_y = 3

    def stop_move_right(self):
        if self.change_x != 0:
            self.image = self.player_image
        self.change_x = 0

    def stop_move_left(self):
        if self.change_x != 0:
            self.image = pygame.transform.flip(self.player_image,True,False)
        self.change_x = 0

    def stop_move_up(self):
        if self.change_y != 0:
            self.image = pygame.transform.rotate(self.player_image,90)
        self.change_y = 0

    def stop_move_down(self):
        if self.change_y != 0:
            self.image = pygame.transform.rotate(self.player_image,270)
        self.change_y = 0

	#Faz que o pacman procure os inimidos por perto
    def search_direction_enemies_close(self, enemies):
        closest_enemy = None
        closest_distance = float('inf')

        for enemy in enemies:
            dx = enemy.rect.centerx - self.rect.centerx
            dy = enemy.rect.centery - self.rect.centery
            distance = math.sqrt(dx**2 + dy**2)

            if distance < closest_distance:
                closest_enemy = enemy
                closest_distance = distance

        if closest_enemy is not None:
            dx = closest_enemy.rect.centerx - self.rect.centerx
            dy = closest_enemy.rect.centery - self.rect.centery

            if abs(dx) > abs(dy):
                if dx > 0:
                    return 'right'
                else:
                    return 'left'
            else:
                if dy > 0:
                    return 'down'
                else:
                    return 'up'

        return None
    # Vidas do jogador
    def reset(self):
        self.rect.x = 32  # Posição inicial x do jogador
        self.rect.y = 128  # Posição inicial y do jogador
        self.explosion
False  # Redefinir o estado de explosão
    
class Animation(object):
    def __init__(self,img,width,height):
        # Carregar a folha de sprite
        self.sprite_sheet = img
        # Crie uma lista para armazenar as imagens
        self.image_list = []
        self.load_images(width,height)
        # Crie uma variável que irá conter a imagem atual da lista
        self.index = 0
        # Crie uma variável que retenha o tempo
        self.clock = 1
        
    def load_images(self,width,height):
        #Passe por cada imagem na folha de sprite
        for y in range(0,self.sprite_sheet.get_height(),height):
            for x in range(0,self.sprite_sheet.get_width(),width): 
                # carregar imagens em uma lista
                img = self.get_image(x,y,width,height)
                self.image_list.append(img)

    def get_image(self,x,y,width,height):
        # Crie uma nova imagem em branco
        image = pygame.Surface([width,height]).convert()
        # Copie o sprite da folha grande para a menor
        image.blit(self.sprite_sheet,(0,0),(x,y,width,height))
        # Assumindo que o preto funciona como a cor transparente
        image.set_colorkey((0,0,0))
        # Devolva a imagem
        return image

    def get_current_image(self):
        return self.image_list[self.index]

    def get_length(self):
        return len(self.image_list)

    def update(self,fps=30):
        step = 30 // fps
        l = range(1,30,step)
        if self.clock == 30:
            self.clock = 1
        else:
            self.clock += 1

        if self.clock in l:
            # Aumentar índice
            self.index += 1
            if self.index == len(self.image_list):
                self.index = 0