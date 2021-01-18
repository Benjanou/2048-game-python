import pygame
from Board import Board

#initialize
pygame.init()

HEIGHT = 600
WIDTH = 600

screen = pygame.display.set_mode((WIDTH,HEIGHT))
font = pygame.font.SysFont("Calibri", 40, bold=True)
screen.fill((0,0,0))
pygame.display.update()

def draw_game(board):
    margin = 10
    square_height = (HEIGHT-2*margin)/(board.get_height())
    square_width = (WIDTH-2*margin)/(board.get_width())
    for i in range(board.get_height()):
        for j in range(board.get_width()):
            color = (180,180,180)
            item = board.get_item(j,i)
            text = ""
            if item is not None:
                color = item.get_color()
                text = str(item)
            x = (square_width)*j +margin
            y = (square_height)*i +margin
            pygame.draw.rect(screen, color, (x, y, square_width, square_height))
            text_surf = font.render(text, True, (0, 0, 0))
            text_x = x + 0.5*square_width - 2*margin
            text_y = y + 0.5*square_height - 2*margin
            screen.blit(text_surf, (text_x, text_y))


game_board = Board()
draw_game(game_board)
print(game_board)

is_running = True
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                game_board.move_verticly(is_down=True)
                print(game_board)

            if event.key == pygame.K_UP:
                game_board.move_verticly(is_down=False)
                print(game_board)

            if event.key == pygame.K_RIGHT:
                game_board.move_horizontally(is_right=True)
                print(game_board)

            if event.key == pygame.K_LEFT:
                game_board.move_horizontally(is_right=False)
                print(game_board)


    draw_game(game_board)
    pygame.display.update()


