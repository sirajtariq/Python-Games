import tkinter
import random

# Game constants
ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS

class Tile:
    """Represents a single tile on the game board."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Create the game window
window = tkinter.Tk()
window.title("Snake_io")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg="#000000", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
canvas.pack()
window.update()

# Center the window on the screen
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# Initialize game variables
snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)  # Snake head
food = Tile(10 * TILE_SIZE, 10 * TILE_SIZE)
velocityX = 0
velocityY = 0
snake_body = []  # Multiple tile size
game_over = False
score = 0

def change_direction(e):
    """Handles keyboard events to change the snake's direction."""
    global velocityX, velocityY

    if not game_over:
        if (e.keysym == "Up" and velocityY != 1):
            velocityX = 0
            velocityY = -1
        elif (e.keysym == "Down" and velocityY != -1):
            velocityX = 0
            velocityY = 1
        elif (e.keysym == "Left" and velocityX != 1):
            velocityX = -1
            velocityY = 0
        elif (e.keysym == "Right" and velocityX != -1):
            velocityX = 1
            velocityY = 0

def move():
    """Updates the snake's position and checks for collisions."""
    global snake, game_over, food, snake_body, score

    if not game_over:
        if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
            game_over = True
            return

        for tile in snake_body:
            if (snake.x == tile.x and snake.y == tile.y):
                game_over = True
                return

        # Check for food collision
        if (snake.x == food.x and snake.y == food.y):
            snake_body.append(Tile(food.x, food.y))
            food.x = random.randint(0, COLS - 1) * TILE_SIZE
            food.y = random.randint(0, ROWS - 1) * TILE_SIZE
            score += 1

        # Update the snake body
        for i in range(len(snake_body) - 1, -1, -1):
            tile = snake_body[i]
            if i == 0:
                tile.x = snake.x
                tile.y = snake.y
            else:
                prev_tile = snake_body[i - 1]
                tile.x = prev_tile.x
                tile.y = prev_tile.y

        snake.x += velocityX * TILE_SIZE
        snake.y += velocityY * TILE_SIZE

def draw():
    """Draws the game elements on the canvas."""
    global snake, food, snake_body, game_over, score

    move()

    canvas.delete("all")

    # Draw food
    canvas.create_oval(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill="#ffe873")

    # Draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill="#4b8bbe")

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill="#4b8bbe")

    if game_over:
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, font="Poppins 20", text=f"Game Over: {score}", fill="#ffffff")
    else:
        canvas.create_text(30, 20, font="Poppins 10", text=f"Score: {score}", fill="#ffffff")

    window.after(100, draw)  # 100ms = 10FPS

draw()

window.bind("<KeyRelease>", change_direction)
window.mainloop()