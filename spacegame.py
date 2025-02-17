import pygame
import random


pygame.init()


WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))


player_ship = pygame.image.load("assets/PNG/playerShip1_blue.png")


laser_img = pygame.image.load("assets/PNG/Lasers/laserRed01.png")
laser_img = pygame.transform.scale(laser_img, (10, 30))  


enemy_img = pygame.image.load("assets/PNG/Enemies/enemyRed1.png")
enemy_img = pygame.transform.scale(enemy_img, (50, 50))  


clock = pygame.time.Clock()


font = pygame.font.SysFont(None, 36)


def game_loop():
    
    x = WIDTH / 2 - 25
    y = HEIGHT - 100
    speed = 3

    lasers = []
    laser_speed = 5

    enemies = []
    enemy_speed = 2
    spawn_delay = 85
    frame_count = 0

    max_enemy_reach = 5
    enemies_reached_bottom = 0

    score = 0

    running = True
    while running:
        screen.fill((0, 0, 0))  

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  

            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    lasers.append([x + 20, y])  

        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            x -= speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            x += speed

        
        x = max(0, min(WIDTH - 50, x))

        
        for laser in lasers:
            laser[1] -= laser_speed

        
        lasers = [laser for laser in lasers if laser[1] > 0]

        
        frame_count += 1
        if frame_count >= spawn_delay:
            enemy_x = random.randint(0, WIDTH - 50)  
            enemies.append([enemy_x, -50])  
            frame_count = 0  

        
        for enemy in enemies:
            enemy[1] += enemy_speed  

        
        for enemy in enemies[:]:
            if enemy[1] >= HEIGHT:
                enemies_reached_bottom += 1  
                enemies.remove(enemy)  
                if enemies_reached_bottom >= max_enemy_reach:
                    return game_over_screen(score)  

       
        for laser in lasers[:]:
            laser_rect = pygame.Rect(laser[0], laser[1], 10, 30)  
            for enemy in enemies[:]:
                enemy_rect = pygame.Rect(enemy[0], enemy[1], 50, 50)  
                if laser_rect.colliderect(enemy_rect):  
                    lasers.remove(laser)  
                    enemies.remove(enemy)  
                    score += 1  

       
        screen.blit(player_ship, (x, y))

        
        for laser in lasers:
            screen.blit(laser_img, (laser[0], laser[1]))

        
        for enemy in enemies:
            screen.blit(enemy_img, (enemy[0], enemy[1]))

       
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        
        pygame.display.flip()

        
        clock.tick(60)  

    return False  


def game_over_screen(final_score):
    
    screen.fill((0, 0, 0))

    
    game_over_text = font.render("Game Over!", True, (255, 0, 0))
    restart_text = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
    score_text = font.render(f"Final Score: {final_score}", True, (255, 255, 255))

   
    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - 180, HEIGHT // 2 + 50))

    pygame.display.flip()

    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  
                if event.key == pygame.K_q:
                    return False  



while True:
    if not game_loop():
        break  

pygame.quit()
