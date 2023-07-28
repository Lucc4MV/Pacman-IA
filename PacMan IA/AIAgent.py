import math
import random


class AIAgent:
    def __init__(self, player, enemies):
        self.player = player
        self.enemies = enemies
        self.q_table = {}
        
        for state in range(200):
            rand = random.randint(0,3)
            direction = player.search_direction_enemies_close(enemies)
            if(direction == None):
                direction = random.randint(0,3)
                lados = ['up', 'right', 'down', 'left']
                direction = lados[direction]               
            if(direction == 'down'):
                player.move_up()
            if(direction == 'up'):
                player.move_down()
            if(direction == 'left'):
                player.move_right()
            if(direction == 'right'):
                player.move_left()

    def get_next_move(self):
        state = self.get_current_state()
        action = ""
        best_value = -math.inf

        for action in ["up", "down", "left", "right"]:
            current_value = self.q_table[(state, action)]

            if current_value > best_value:
                action = action
                best_value = current_value
            return action
        
    def search_scores(self):
            closest_score = None
            closest_distance = float('inf')

            for score in self.scores:
                dx = score.x - self.player.rect.centerx
                dy = score.y - self.player.rect.centery
                distance = math.sqrt(dx**2 + dy**2)

                if distance < closest_distance:
                    closest_score = score
                    closest_distance = distance

            if closest_score is not None:
                dx = closest_score.x - self.player.rect.centerx
                dy = closest_score.y - self.player.rect.centery

                if abs(dx) > abs(dy):
                    if dx > 0:
                        self.player.move_right()
                    else:
                        self.player.move_left()
                else:
                    if dy > 0:
                        self.player.move_down()
                    else:
                        self.player.move_up()
                        
    def run_away_from_enemies(self):
        for enemy in self.enemies:
            dx = self.player.rect.centerx - enemy.rect.centerx
            dy = self.player.rect.centery - enemy.rect.centery

            if abs(dx) > abs(dy):
                if dx > 0:
                    self.player.move_left()
                else:
                    self.player.move_right()
            else:
                if dy > 0:
                    self.player.move_up()
                else:
                    self.player.move_down()
    def update(self):
        self.run_away_from_enemie
        self.search_scores()
        next_move = self.get_next_move()