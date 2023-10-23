import pygame as pg
from sys import exit 
from random import randint, choice
import runner_player
import runner_obstacle

def display_score():
    current_time = int(pg.time.get_ticks() / 1000) - start_time
    score = test_font.render(f"Score:{current_time}", False, (64, 64, 64))
    score_rect = score.get_rect(center=(400, 50))
    screen.blit(score, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail, obstacle_rect)
            else:
                screen.blit(fly, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []


def collision(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


def collision_sprite():
    if pg.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]


pg.init()
screen = pg.display.set_mode((1200, 400))
pg.display.set_caption("runner")
clock = pg.time.Clock()
test_font = pg.font.Font("font/Pixeltype.ttf", 50)
game_active = False
start_time = 0
score = 0
bg_music = pg.mixer.Sound("audio/music.wav")
bg_music.play(loops=-1).set_volume(0.2)

player = pg.sprite.GroupSingle()
player.add(runner_player.Player())

obstacle_group = pg.sprite.Group()

sky = pg.image.load("graphics/Sky.png").convert()
ground = pg.image.load("graphics/Ground.png").convert()

# obstacle
snail_frame_1 = pg.image.load("graphics/snail/snail1.png").convert_alpha()
snail_frame_2 = pg.image.load("graphics/snail/snail2.png").convert_alpha()
snail_frame = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail = [snail_frame_index]

fly_frame_1 = pg.image.load("graphics/fly/fly1.png").convert_alpha()
fly_frame_2 = pg.image.load("graphics/fly/fly2.png").convert_alpha()
fly_frame = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly = [fly_frame_index]

obstacle_rect_list = []

player_walk_1 = pg.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_walk_2 = pg.image.load("graphics/player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pg.image.load("graphics/player/jump.png").convert_alpha()
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom=(80, 300))
player_gravity = 0
# intro screen
player_stand = pg.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand_scaled = pg.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand_scaled.get_rect(center=(400, 200))

game_name = test_font.render("Pixel runner", False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render("press space to run", False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 320))

obstacle_timer = pg.USEREVENT + 1
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
                obstacle_group.add(runner_obstacle.Obstacle(choice(["fly", "snail", "snail", "snail"])))
            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                sanil = snail_frame[snail_frame_index]
            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                sanil = fly_frame[fly_frame_index]

    if game_active:
        screen.blit(sky, (0, 0))
        screen.blit(ground, (0, 300))
        score = display_score()
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()
        game_active = collision_sprite()

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand_scaled, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0
        score_message = test_font.render(f"Your score: {score}", False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(game_name, game_name_rect)
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)
        
    pg.display.update()
    clock.tick(60)
