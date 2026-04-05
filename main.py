import pygame
import random

pygame.init()
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("لعبة الثعبان - اتجاهات صحيحة")
clock = pygame.time.Clock()

snake_block = 20
snake_speed = 8

black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
red = (255,0,0)

def game_loop():
    x = width//2
    y = height//2
    dx = 0
    dy = 0
    snake = []
    length = 1
    food_x = random.randrange(0, width, snake_block)
    food_y = random.randrange(0, height, snake_block)
    score = 0
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dy == 0:        # شمال
                    dx = 0
                    dy = -snake_block
                elif event.key == pygame.K_DOWN and dy == 0:    # جنوب
                    dx = 0
                    dy = snake_block
                elif event.key == pygame.K_RIGHT and dx == 0:   # شرق
                    dx = snake_block
                    dy = 0
                elif event.key == pygame.K_LEFT and dx == 0:    # غرب
                    dx = -snake_block
                    dy = 0
        
        x += dx
        y += dy
        
        # حدود
        if x < 0 or x >= width or y < 0 or y >= height:
            running = False
        
        screen.fill(black)
        pygame.draw.rect(screen, red, (food_x, food_y, snake_block, snake_block))
        
        snake.append([x, y])
        if len(snake) > length:
            del snake[0]
        
        for segment in snake[:-1]:
            if segment == [x, y]:
                running = False
        
        for seg in snake:
            pygame.draw.rect(screen, green, (seg[0], seg[1], snake_block, snake_block))
        
        # عرض النقاط
        font = pygame.font.Font(None, 35)
        text = font.render(f"النقاط: {score}", True, white)
        screen.blit(text, (10, 10))
        
        pygame.display.update()
        
        if x == food_x and y == food_y:
            food_x = random.randrange(0, width, snake_block)
            food_y = random.randrange(0, height, snake_block)
            length += 1
            score += 1
        
        clock.tick(snake_speed)
    
    pygame.quit()

game_loop()
