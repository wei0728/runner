import random
import pygame as pg
from sys import exit
from random import randint, choice

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        player_walk_1 = pg.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pg.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pg.image.load('graphics/player/jump.png').convert_alpha() 
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (200,300))
        self.gravity = 0

        self.jump_sound = pg.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):self.player_index= 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pg.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pg.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pg.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pg.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pg.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    
    def update(self):
        self.animation_state()
        self.rect.x -= 6 
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pg.time.get_ticks()/1000) - start_time
    score = test_font.render(f'Score:{current_time}', False, (64,64,64))
    score_rect = score.get_rect(center = (400, 50))
    screen.blit(score, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -=5
            
            if obstacle_rect.bottom == 300:
                screen.blit(snail, obstacle_rect)
            else:
                screen.blit(fly, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []

def collision(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):return False
    return True

def collision_sprite():
    if pg.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True

def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):player_index = 0
        player_surf = player_walk[int(player_index)]

pg.init()
screen = pg.display.set_mode((800,400))
pg.display.set_caption('runner')
clock = pg.time.Clock()
test_font = pg.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pg.mixer.Sound('audio/music.wav')
bg_music.play(loops = -1).set_volume(0.2)

player = pg.sprite.GroupSingle()
player.add(Player())

obstacle_group = pg.sprite.Group()

sky  = pg.image.load('graphics/Sky.png').convert()
ground = pg.image.load('graphics/Ground.png').convert() 

#obstacle
snail_frame_1 = pg.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pg.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frame = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail = [snail_frame_index]

fly_frame_1 = pg.image.load('graphics/fly/fly1.png').convert_alpha()
fly_frame_2 = pg.image.load('graphics/fly/fly2.png').convert_alpha()
fly_frame = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly = [fly_frame_index]

obstacle_rect_list = []

player_walk_1 = pg.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pg.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pg.image.load('graphics/player/jump.png').convert_alpha()
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0;
#intro screen 
player_stand = pg.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand_scaled = pg.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand_scaled.get_rect(center = (400,200))

game_name = test_font.render('Pixel runner', False, (111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('press space to run', False, (111,196,169))
game_message_rect = game_message.get_rect(center = (400,320))
 
obstacle_timer = pg.USEREVENT +1
pg.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pg.USEREVENT + 2
pg.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pg.USEREVENT + 3
pg.time.set_timer(fly_animation_timer, 200)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if game_active:    
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
        else:
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                game_active = True
                start_time = int(pg.time.get_ticks() / 1000)
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
            if event.type == snail_animation_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                sanil = snail_frame[snail_frame_index]
            if event.type == fly_animation_timer:
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                sanil = fly_frame[fly_frame_index]

    if game_active: 
        screen.blit(sky, (0,0))
        screen.blit(ground, (0,300))
        score = display_score()
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()
        game_active = collision_sprite()

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand_scaled, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0
        score_message = test_font.render(f'Your score: {score}', False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (400,330))        
        screen.blit(game_name, game_name_rect)
        if score == 0:    
            screen.blit(game_message, game_message_rect)
        else:    
            screen.blit(score_message, score_message_rect)
    pg.display.update()
    clock.tick(60)