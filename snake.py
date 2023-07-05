import pygame
import random
import os

# 初始化pygame
pygame.init()

# 设置游戏窗口的宽度和高度
window_width = 800
window_height = 600

# 创建游戏窗口
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("贪吃蛇")

# 加载图标图片
icon_image = pygame.image.load("icon.png")

# 获取桌面图标列表
desktop_path = os.path.expanduser("~") + "/Desktop"
icon_files = [f for f in os.listdir(desktop_path) if f.endswith(".lnk")]

# 存储蛇身体坐标的列表
snake_body = []

# 初始化蛇的初始位置和长度
snake_x = window_width // 2
snake_y = window_height // 2
snake_length = 1

# 设置蛇移动的初始方向（右方向）
snake_direction = "RIGHT"

# 设置蛇的移动速度
snake_speed = 20

# 随机生成食物的位置
food_x = random.randint(0, window_width - 20)
food_y = random.randint(0, window_height - 20)

# 设置游戏结束的标志
game_over = False

# 游戏主循环
while not game_over:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        # 处理按键事件
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != "DOWN":
                snake_direction = "UP"
            elif event.key == pygame.K_DOWN and snake_direction != "UP":
                snake_direction = "DOWN"
            elif event.key == pygame.K_LEFT and snake_direction != "RIGHT":
                snake_direction = "LEFT"
            elif event.key == pygame.K_RIGHT and snake_direction != "LEFT":
                snake_direction = "RIGHT"

    # 根据蛇的移动方向更新蛇头的坐标
    if snake_direction == "UP":
        snake_y -= snake_speed
    elif snake_direction == "DOWN":
        snake_y += snake_speed
    elif snake_direction == "LEFT":
        snake_x -= snake_speed
    elif snake_direction == "RIGHT":
        snake_x += snake_speed

    # 判断蛇是否吃到了食物
    if snake_x == food_x and snake_y == food_y:
        # 随机生成新的食物位置
        food_x = random.randint(0, window_width - 20)
        food_y = random.randint(0, window_height - 20)

        # 增加蛇的长度
        snake_length += 1

        # 将食物图标加入蛇的身体列表
        snake_body.append((food_x, food_y))

    # 更新窗口
    window.fill((0, 0, 0))  # 清空窗口

    # 绘制食物
    pygame.draw.rect(window, (255, 0, 0), (food_x, food_y, 20, 20))

    # 绘制蛇身体
    for body_part in snake_body:
        pygame.draw.rect(window, (0, 255, 0), (body_part[0], body_part[1], 20, 20))

    # 绘制蛇头
    pygame.draw.rect(window, (0, 0, 255), (snake_x, snake_y, 20, 20))

    # 更新显示
    pygame.display.update()

    # 控制蛇的长度
    if len(snake_body) >= snake_length:
        del snake_body[0]

    # 判断蛇是否撞到了自己
    for body_part in snake_body:
        if body_part[0] == snake_x and body_part[1] == snake_y:
            game_over = True

    # 判断是否吃掉了所有的图标
    if len(snake_body) >= len(icon_files):
        game_over = True

# 游戏结束，退出pygame
pygame.quit()
