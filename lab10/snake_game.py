import pygame, random, sys
from db import get_user, save_score

pygame.init()

WIDTH, HEIGHT, CELL_SIZE = 800, 600, 25
CELL_WIDTH = WIDTH // CELL_SIZE
CELL_HEIGHT = HEIGHT // CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Жылан")
clock = pygame.time.Clock()

BASE_SPEED = 7
FOOD_PER_LEVEL = 4

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY  = (100, 100, 100)
GOLD = (255, 215, 0)

def random_food_position(snake):
    while True:
        pos = (random.randint(0, CELL_WIDTH - 1), random.randint(0, CELL_HEIGHT - 1))
        if pos not in snake:
            return pos

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def main():
    username = input("Введите имя игрока: ")
    state = get_user(username)
    score, level = 0, 1
    if state:
        level, score = state
        print(f"Добро пожаловать, {username}! Ваш уровень: {level}, счёт: {score}")

    snake = [(CELL_WIDTH // 2, CELL_HEIGHT // 2),
             (CELL_WIDTH // 2 - 1, CELL_HEIGHT // 2),
             (CELL_WIDTH // 2 - 2, CELL_HEIGHT // 2)]
    dx, dy = 1, 0
    food = random_food_position(snake)
    speed = BASE_SPEED + (level - 1) * 2

    while True:
        clock.tick(speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_score(username, score, level)
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dy == 0: dx, dy = 0, -1
                elif event.key == pygame.K_DOWN and dy == 0: dx, dy = 0, 1
                elif event.key == pygame.K_LEFT and dx == 0: dx, dy = -1, 0
                elif event.key == pygame.K_RIGHT and dx == 0: dx, dy = 1, 0
                elif event.key == pygame.K_p:
                    save_score(username, score, level)
                    print("Пауза. Прогресс сохранён.")

        new_head = (snake[0][0] + dx, snake[0][1] + dy)
        if (new_head[0] < 0 or new_head[0] >= CELL_WIDTH or 
            new_head[1] < 0 or new_head[1] >= CELL_HEIGHT or 
            new_head in snake):
            save_score(username, score, level)
            print("Игра окончена. Прогресс сохранён.")
            pygame.quit(); sys.exit()

        snake.insert(0, new_head)

        if new_head == food:
            score += 1
            if score % FOOD_PER_LEVEL == 0:
                level += 1
                speed = BASE_SPEED + (level - 1) * 2
            food = random_food_position(snake)
        else:
            snake.pop()

        screen.fill(WHITE)
        draw_grid()
        for segment in snake:
            pygame.draw.rect(screen, BLUE, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, GOLD, (food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        font = pygame.font.SysFont(None, 30)
        text = font.render(f"Score: {score}  Level: {level}", True, BLACK)
        screen.blit(text, (5, 5))
        pygame.display.flip()

if __name__ == "__main__":
    main()
