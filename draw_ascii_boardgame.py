# draw game board
dashes = " ---"
bars = "|   "


def dashes_line(width):
    line = ""
    for i in range(width):
        line += dashes
    return line


def bar_line(width):
    line = ""
    for i in range(width):
        line += bars
    line += "|"
    return line


def draw_board(width, height):
    for r in range(height):
        print(dashes_line(width))
        print(bar_line(width))
    print(dashes_line(width))


while True:
    board_width = int(input("Board width? "))
    board_height = int(input("Board height? "))
    draw_board(board_width, board_height)
