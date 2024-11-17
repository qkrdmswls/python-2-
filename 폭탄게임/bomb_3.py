import pygame
import random
import sys

# pygame 초기화
pygame.init()

# 창 크기
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 600

# 창 설정
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Bomb Game")

# 색상 설정
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 캐릭터 설정
player_width = 40
player_height = 40
player_x = WINDOW_WIDTH // 2 - player_width // 2
player_y = WINDOW_HEIGHT - player_height - 10
player_speed = 5

# 장애물 설정
obstacle_width = 50
obstacle_height = 50
min_obstacle_speed = 5  # 최소 속도
max_obstacle_speed = 10  # 최대 속도
obstacles = []
obstacle_spawn_delay = 30  # 장애물 생성 간격 (프레임 수)
min_distance_between_obstacles = 30  # 장애물 간 최소 거리

# 폭발 이미지 크기
bomb_width = WINDOW_WIDTH
bomb_height = WINDOW_HEIGHT

# 메인 화면 이미지 크기
main_width = WINDOW_WIDTH
main_height = WINDOW_HEIGHT

# 플레이 화면 이미지 크기
background_width = WINDOW_WIDTH
background_height = WINDOW_HEIGHT

# 플레이어 이미지 로드
player_image = pygame.image.load("C:/mypackage/pygame/image_file/user.png")
player_image = pygame.transform.scale(player_image, (player_width, player_height))

# 장애물 이미지 로드
obstacle_image = pygame.image.load("C:/mypackage/pygame/image_file/bomb.png")
obstacle_image = pygame.transform.scale(obstacle_image, (obstacle_width, obstacle_height))

# 폭발 이미지 로드
bomb_image = pygame.image.load("C:/mypackage/pygame/image_file/bomb_image.png")
bomb_image = pygame.transform.scale(bomb_image, (bomb_width, bomb_height))
bomb_rect = bomb_image.get_rect()

# 메인 화면 이미지 로드
main_image = pygame.image.load("C:/mypackage/pygame/image_file/sea.png")
main_image = pygame.transform.scale(main_image, (main_width, main_height))
main_rect = main_image.get_rect()

# 플레이 화면 이미지 로드
background_image = pygame.image.load("C:/mypackage/pygame/image_file/BombGame_BackGround.png")
background_image = pygame.transform.scale(background_image, (background_width, background_height))
background_rect = background_image.get_rect()

# 게임 설정
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# 점수 초기화
score = 0
frame_count = 0

# 버튼 설정
button_font = pygame.font.Font(None, 48)
button_text = button_font.render("Start Game", True, WHITE)
button_rect = button_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

# 게임 상태
game_active = False

# 함수
# 장애물 생성 함수
def create_obstacle():
    x_pos = random.randint(0, WINDOW_WIDTH - obstacle_width)
    y_pos = -obstacle_height
    speed = random.randint(min_obstacle_speed, max_obstacle_speed)  # 랜덤 속도 설정
    
    # 다른 장애물과의 최소 거리 확인
    for obstacle in obstacles:
        if abs(obstacle["rect"].x - x_pos) < min_distance_between_obstacles:
            return  # 너무 가까이 생성되면 생성하지 않음

    obstacles.append({"rect": pygame.Rect(x_pos, y_pos, obstacle_width, obstacle_height), "speed": speed})

# 게임 종료 함수
def game_over():
    global game_active, score, frame_count
    display_surface.blit(bomb_image, bomb_rect)
    game_over_text = font.render("Game Over", True, RED)
    display_surface.blit(game_over_text, (WINDOW_WIDTH // 2 - 70, WINDOW_HEIGHT // 2 - 30))
    pygame.display.flip()
    pygame.time.delay(2000)
    score = 0
    frame_count = 0
    obstacles.clear()
    game_active = False

# 메인 루프
while True:
    display_surface.fill(WHITE)
    display_surface.blit(background_image, background_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 버튼 클릭 검사
            if not game_active and button_rect.collidepoint(event.pos):
                game_active = True

    if game_active:
        # 키보드 기능
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WINDOW_WIDTH - player_width:
            player_x += player_speed

        # 장애물 생성
        frame_count += 1
        if frame_count % obstacle_spawn_delay == 0:  # 일정 간격으로 생성
            create_obstacle()

        # 장애물 이동 및 충돌 검사
        for obstacle in obstacles[:]:
            obstacle["rect"].y += obstacle["speed"]  # 각 장애물의 개별 속도로 이동
            if obstacle["rect"].y > WINDOW_HEIGHT:
                obstacles.remove(obstacle)
                score += 1
            if obstacle["rect"].colliderect(pygame.Rect(player_x, player_y, player_width, player_height)):
                game_over()

        # 플레이어 및 장애물 그리기
        display_surface.blit(player_image, (player_x, player_y))
        for obstacle in obstacles:
            display_surface.blit(obstacle_image, (obstacle["rect"].x, obstacle["rect"].y))

        # 점수 표시
        score_text = font.render("Score: " + str(score), True, BLACK)
        display_surface.blit(score_text, (10, 10))
    else:
        # 게임 시작 버튼 표시
        display_surface.blit(main_image, main_rect)
        display_surface.blit(button_text, button_rect)

    # 디스플레이 업데이트
    pygame.display.update()
    clock.tick(30)
