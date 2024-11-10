import pygame

# pygame 초기화
pygame.init()

# 창 크기
WINDOW_WIDTH = 1850
WINDOW_HEIGHT = 900


# 창 설정
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Bomb Game")

clock = pygame.time.Clock()

# 이미지
# 캐릭터 이미지
user_image = pygame.image.load("C:/mypackage/pygame/image_file/user.png")
user_rect = user_image.get_rect()
user_rect.topleft = (850, 700)

# 폭탄 이미지
bomb_image = pygame.image.load("C:/mypackage/pygame/image_file/bomb.png")
bomb_rect = bomb_image.get_rect()
bomb_rect.topleft = (10, 10)


# 게임이 동작하는 동안 이벤트
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 키보드 기능
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and user_rect.left > 0:
        user_rect.x -= 6
    if keys[pygame.K_RIGHT] and user_rect.right < WINDOW_WIDTH:
        user_rect.x += 6
    if keys[pygame.K_UP] or keys[pygame.K_w] and user_rect.top > 0:
        user_rect.y -= 6
    if keys[pygame.K_DOWN] or keys[pygame.K_s] and user_rect.bottom < WINDOW_HEIGHT:
        user_rect.y += 6


    # 캐릭터 충돌 이벤트 구현
    if user_rect.colliderect(bomb_rect):
        print("충돌")

    # 바탕화면, 그림을 나타냄
    display_surface.fill(('gray'))

    display_surface.blit(user_image, user_rect)
    display_surface.blit(bomb_image, bomb_rect)

    # 디스플레이 업데이트
    pygame.display.update()

    clock.tick(60)

pygame.quit()
