import pygame
import random
import sys

pygame.init()

WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(213,50,80)
GREEN=(0,255,0)

#화면크기
SCREEN_WIDTH=500
SCREEN_HEIGHT=600

screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Hangman Game')

#폰트
font=pygame.font.Font(None, 48)
small_font=pygame.font.Font(None,36)

try:
    # 이미지 파일 경로는 절대경로 또는 상대경로로 정확히 지정
    head_img = pygame.image.load("hangman_head.png").convert_alpha()
    head_img = pygame.transform.scale(head_img, (500, 500))  # 크기 조정

    left_arm_img = pygame.image.load("hangman_right_arm.png").convert_alpha()
    left_arm_img = pygame.transform.scale(left_arm_img, (500, 500))

    body_img = pygame.image.load("hangman_body.png").convert_alpha()
    body_img = pygame.transform.scale(body_img, (500, 500))

    right_arm_img = pygame.image.load("hangman_left_arm.png").convert_alpha()
    right_arm_img = pygame.transform.scale(right_arm_img, (500,500))

    left_leg_img = pygame.image.load("hangman_left_leg.png").convert_alpha()
    left_leg_img = pygame.transform.scale(left_leg_img, (500, 500))

    right_leg_img = pygame.image.load("hangman_right_leg.png").convert_alpha()
    right_leg_img = pygame.transform.scale(right_leg_img, (500, 500))

except pygame.error as e:
    print(f"Error loading image: {e}")
    pygame.quit()
    sys.exit()
    
# 단어 리스트
words = [
    "apple", "banana", "cat", "dog", "table", "chair", "book", "car", "house", "tree",
    "ball", "bag", "bird", "door", "window", "shoe", "hat", "pencil", "paper", "sun", "moon",
    "star", "flower", "fish", "cow", "horse", "mountain", "river", "ocean", "beach", "food",
    "water", "chocolate", "pizza", "school", "friend", "family", "toy", "music", "phone", "computer",
    "clock", "tree", "beach", "garden", "milk", "bread", "park", "shirt", "spoon"
]

def reset_game():
    global random_word, randomWord, lives, user_input, hint_used, endGame
    random_word = random.choice(words)  # 새로운 단어 선택
    randomWord = ["_"] * len(random_word)  # 단어를 숨김
    user_input = " "  # 사용자가 입력한 문자 초기화
    hint_used = False  # 힌트 사용 여부 초기화
    lives = 6  # 생명 초기화
    endGame = False  # 게임 종료 상태 초기화

# 게임 초기화
reset_game()

#게임 진행
while True:
    screen.fill(WHITE)  # 화면을 흰색으로 채워서 이전 그림을 지웁니다

    # 왼쪽 화면 영역 (행맨 그림 위치 고정)
    left_width = SCREEN_WIDTH // 2.5

    # 고정된 위치에 행맨 그림을 그리기
    hangman_x = -30 #left_width // 8  # 그림을 왼쪽 1/4 지점에 배치
    hangman_y = 100  # 그림의 y 좌표 고정
    
    if lives <= 5:
        screen.blit(head_img, (hangman_x, hangman_y))  # 머리
    if lives <= 4:
        screen.blit(right_arm_img, (hangman_x , hangman_y))  # 오른팔
    if lives <= 3:
        screen.blit(body_img, (hangman_x, hangman_y ))  # 몸통
    if lives <= 2:
        screen.blit(left_arm_img, (hangman_x , hangman_y ))  # 왼팔
    if lives <= 1:
        screen.blit(right_leg_img, (hangman_x , hangman_y ))  # 오른다리
    if lives == 0:
        screen.blit(left_leg_img, (hangman_x , hangman_y ))  # 왼다리
    

    # 오른쪽 화면 영역 (단어 상태, 생명, 힌트 등)
    right_width = SCREEN_WIDTH - left_width
    
    word_display = " ".join(randomWord)
    word_text = font.render(word_display, True, BLACK)
    screen.blit(word_text, (left_width + 50, 50))

    # 남은 기회(생명) 숫자 표시
    lives_text = font.render(f"Lives left: {lives}", True, RED)
    screen.blit(lives_text, (left_width + 50, 150))

    #사용자가 입력한 글자 화면 표
    user_input_text = small_font.render(f"Your Input: {user_input}", True, GREEN)
    screen.blit(user_input_text, (left_width + 50, 250))


    # 힌트 버튼 텍스트
    hint_text = small_font.render("Press H for Hint", True, GREEN)
    screen.blit(hint_text, (left_width + 50, 200))

     # 게임 종료 처리 (오른쪽 다리가 그려지면 게임 종료)
    if lives == 0:
        game_over_text = font.render("Game Over!", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 350))
        restart_text = font.render("Press R to Restart", True, GREEN)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 400))

    elif "_" not in randomWord:
        victory_text = font.render("You win!", True, GREEN)
        screen.blit(victory_text, (SCREEN_WIDTH // 2 - victory_text.get_width() // 2, 350))
        restart_text = font.render("Press R to Restart", True, GREEN)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 400))

    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

        if event.type==pygame.KEYDOWN:
            input_char=pygame.key.name(event.key).lower()

            #게임 종료 후 입력 그만 받기
            if endGame:
                if input_char == "r":  # "r"을 누르면 게임을 리셋
                    reset_game()
                continue

            if input_char=="h" and not hint_used:
                hint_used = True

                #힌트 제공
                hidden_indices = [i for i, c in enumerate(randomWord) if c == "_"]
                hint_index = random.choice(hidden_indices)  # 숨겨진 알파벳의 인덱스를 랜덤으로 선택
                randomWord[hint_index] = random_word[hint_index] 

                lives-=1

            #알파벳 맞추기
            elif input_char.isalpha() and len(input_char) == 1:
                if input_char in user_input:  # 이미 입력한 글자인지 확인
                    error_message = small_font.render("You've already entered that letter!", True, RED)
                    screen.blit(error_message, (SCREEN_WIDTH // 2 - error_message.get_width() // 2, 450))
                else:  
                    user_input += input_char # 새로 입력된 글자 저장
                    if input_char in random_word:
                        for index in range(len(random_word)):
                            if random_word[index] == input_char:
                                randomWord[index] = input_char
                    else:
                        lives -= 1

            if "_" not in randomWord:
                endGame = True
                victory_text = font.render("You win!", True, GREEN)
                screen.blit(victory_text, (SCREEN_WIDTH // 2 - victory_text.get_width() // 2, 350))

                            
            #게임 종료

            if lives == 0:
                endGame = True
                game_over_text = font.render("Game Over!", True, RED)
                screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 350))
                restart_text = font.render("Press R to Restart", True, GREEN)
                screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 400))

    pygame.display.update()
