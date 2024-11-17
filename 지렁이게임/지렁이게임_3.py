import pygame
import random

pygame.init()

WHITE = (255, 255, 255)
PINK = (255, 105, 180)
BROWN = (139, 69, 19)

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600
CELL_SIZE = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("지렁이 게임")


clock = pygame.time.Clock()

#지렁이/먹이 설정
snake_pos = [[100, 50]]
snake_direction = "RIGHT"
snake_speed = 8
food_pos = [random.randrange(1, (SCREEN_WIDTH // CELL_SIZE)) * CELL_SIZE,
            random.randrange(1, (SCREEN_HEIGHT // CELL_SIZE)) * CELL_SIZE]
score = 0

#적 지렁이
another_snake_pos = []
another_snake_direction = "RIGHT"
another_spawned = False

game_over = False

def draw_snake(snake_pos, color):
    for pos in snake_pos:
        pygame.draw.rect(screen, color, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))

def move_snake(snake_pos, direction):
    if direction == 'UP':
        new_head = [snake_pos[0][0], snake_pos[0][1] - CELL_SIZE]
    elif direction == 'DOWN':
        new_head = [snake_pos[0][0], snake_pos[0][1] + CELL_SIZE]
    elif direction == 'LEFT':
        new_head = [snake_pos[0][0] - CELL_SIZE, snake_pos[0][1]]
    elif direction == 'RIGHT':
        new_head = [snake_pos[0][0] + CELL_SIZE, snake_pos[0][1]]
    
    snake_pos.insert(0, new_head)
    return snake_pos

#먹이 충돌
def check_food_collision(snake_pos, food_pos):
    snake_head = pygame.Rect(snake_pos[0][0], snake_pos[0][1], CELL_SIZE, CELL_SIZE)
    food_rect = pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE)
    return snake_head.colliderect(food_rect)

#벽 충돌
def check_wall_collision(snake_pos, area_width, area_height):
    if (snake_pos[0][0] >= area_width or snake_pos[0][0] < 0 or
        snake_pos[0][1] >= area_height or snake_pos[0][1] < 0):
        return True
    return False

#자기 충돌
def self_collision(snake_pos):
    if snake_pos[0] in snake_pos[1:]:
        return True
    return False

#적 지렁이 충돌 (스치기만 해도)
def another_snake_collision(snake_pos, another_snake_pos):
    snake_head_rect = pygame.Rect(snake_pos[0][0], snake_pos[0][1], CELL_SIZE, CELL_SIZE)
    for pos in another_snake_pos:
        another_snake_rect = pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE)
        if snake_head_rect.colliderect(another_snake_rect):  #충돌 감지
            return True
    return False

#적 지렁이 이동 및 영역 제한
def move_another_snake(another_snake_pos, direction):
    #머리 좌표 계산
    if direction == 'UP':
        new_head = [another_snake_pos[0][0], another_snake_pos[0][1] - CELL_SIZE]
    elif direction == 'DOWN':
        new_head = [another_snake_pos[0][0], another_snake_pos[0][1] + CELL_SIZE]
    elif direction == 'LEFT':
        new_head = [another_snake_pos[0][0] - CELL_SIZE, another_snake_pos[0][1]]
    elif direction == 'RIGHT':
        new_head = [another_snake_pos[0][0] + CELL_SIZE, another_snake_pos[0][1]]
    
    #벽에 닿았는지
    if new_head[0] < 0 or new_head[0] >= 450 or new_head[1] < 0 or new_head[1] >= 550:
        #가능한 새로운 방향 설정
        if new_head[0] < 0:  #왼쪽 벽
            new_head[0] = 0
            direction = random.choice(['UP', 'DOWN', 'RIGHT'])
        elif new_head[0] >= 450:  #오른쪽
            new_head[0] = 450 - CELL_SIZE
            direction = random.choice(['UP', 'DOWN', 'LEFT'])
        elif new_head[1] < 0:  #위
            new_head[1] = 0
            direction = random.choice(['DOWN', 'LEFT', 'RIGHT'])
        elif new_head[1] >= 550:  #아래
            new_head[1] = 550 - CELL_SIZE
            direction = random.choice(['UP', 'LEFT', 'RIGHT'])

    another_snake_pos.insert(0, new_head)
    another_snake_pos.pop()
    
    return another_snake_pos, direction



def random_direction():
    return random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != 'DOWN':
                snake_direction = 'UP'
            elif event.key == pygame.K_DOWN and snake_direction != 'UP':
                snake_direction = 'DOWN'
            elif event.key == pygame.K_LEFT and snake_direction != 'RIGHT':
                snake_direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and snake_direction != 'LEFT':
                snake_direction = 'RIGHT'

   
    snake_pos = move_snake(snake_pos, snake_direction)
    
    #먹이 충돌
    if check_food_collision(snake_pos, food_pos):
        food_pos = [random.randrange(1, (SCREEN_WIDTH // CELL_SIZE)) * CELL_SIZE,
                    random.randrange(1, (SCREEN_HEIGHT // CELL_SIZE)) * CELL_SIZE]
        score += 10
    else:
        snake_pos.pop()

    #벽 충돌
    if check_wall_collision(snake_pos, SCREEN_WIDTH, SCREEN_HEIGHT):
        game_over = True

    #자기 충돌
    if self_collision(snake_pos):
        game_over = True

    #적 지렁이 등장 조건 (100점 이상)
    if score >= 100 and not another_spawned:
        start_x = random.randrange(1, (450 // CELL_SIZE)) * CELL_SIZE
        start_y = random.randrange(1, (550 // CELL_SIZE)) * CELL_SIZE
    
        #랜덤으로 가로 or 세로
        if random.choice(["HORIZONTAL", "VERTICAL"]) == "HORIZONTAL":
            another_snake_pos = [[start_x - i * CELL_SIZE, start_y] for i in range(15)]
        else:
            another_snake_pos = [[start_x, start_y - i * CELL_SIZE] for i in range(15)]
    
        another_spawned = True


    #적 지렁이 이동 및 충돌 확인
    if another_spawned:
        another_snake_pos, another_snake_direction = move_another_snake(another_snake_pos, another_snake_direction)
        
        if check_wall_collision(another_snake_pos, 450, 550):
            another_snake_direction = random_direction()
        
        #적 지렁이와 사용자 지렁이 충돌
        if another_snake_collision(snake_pos, another_snake_pos):
            game_over = True

    
    background = pygame.image.load("ground.png")
    screen.blit(background, (0,0))
    draw_snake(snake_pos, PINK)

    if another_spawned:
        draw_snake(another_snake_pos, BROWN)
    pygame.draw.rect(screen, WHITE, pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))
    font = pygame.font.SysFont("Arial", 25)
    score_text = font.render(f"SCORE: {score}", True, WHITE)
    screen.blit(score_text, [10,10])

    pygame.display.flip()

    clock.tick(snake_speed)

pygame.quit()
