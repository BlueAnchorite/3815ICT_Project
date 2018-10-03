from tkinter import *
from tkinter import messagebox
from random import randint
import time, _thread, sys


class Board(object):
    def __init__(self, tiles_x, tiles_y, tile_size, num_mines):
        self.tiles_x, self.tiles_y = tiles_x, tiles_y
        self.side_length = tile_size
        self.num_mines = num_mines
        self.tiles = []
        self.default_colour = "#b7f4f0"
        self.start_time = 0
        self.finish_time = 0

    def reveal_tile(self, event):
        global start_time
        global timer_thread
        if canvas.find_withtag(CURRENT):
            clicked = canvas.find_withtag(CURRENT)
            clicked_tile = self.find_tile(clicked[0])
            if clicked_tile:
                if start_time == 0:
                    start_time = time.time()
                    timer_thread = _thread.start_new_thread(timer, ())
                if clicked_tile.uncovered == False:
                    neighbours = self.find_neighbours(clicked_tile)
                    self.get_neighbour_mines(clicked_tile, neighbours)
                    self.display_tile(clicked_tile, neighbours)
                    canvas.update_idletasks()
                    canvas.after(200)

    def flag_tile(self, event):
        if canvas.find_withtag(CURRENT):
            clicked = canvas.find_withtag(CURRENT)
            clicked_tile = self.find_tile(clicked[0])
            if clicked_tile:
                if clicked_tile.uncovered == False and clicked_tile.is_flagged == False:
                    canvas.itemconfig(clicked_tile.canvas_id, fill="red")
                    clicked_tile.is_flagged = True
                    canvas.update_idletasks()
                    canvas.after(200)
                elif clicked_tile.uncovered == False and clicked_tile.is_flagged == True:
                    canvas.itemconfig(clicked_tile.canvas_id, fill=default_colour)
                    clicked_tile.is_flagged = False

    def display_tile(self, tile, neighbours):
        global start_time, finish_time
        tile.uncovered = True
        canvas.itemconfig(tile.canvas_id, fill="white")
        if tile.surrounding_mines == 0 and tile.contains_mine == False:
            for neighbour in neighbours:
                surrounding_neighbours = self.find_neighbours(neighbour)
                self.get_neighbour_mines(neighbour, surrounding_neighbours)
                self.display_tile(neighbour, surrounding_neighbours)
        elif tile.contains_mine == True:
            canvas.create_text(tile.centre["x"], tile.centre["y"], font=("", int((side_length * 2) / 3)), text="*")
            finish_time = time.time()
            minutes, seconds = divmod(int(finish_time - start_time), 60)
            # create custom popup with 3 buttons, one to reset, one to go to main menu and one to quit entirely
            if messagebox.askyesno('Game Over',
                                   'You lost in {} minutes and {} seconds, Try Again?'.format(minutes, seconds)):
                self.setup_board()
            else:
                sys.exit(0)

        else:
            canvas.create_text(tile.centre["x"], tile.centre["y"], font=("", int((side_length * 2) / 3)),
                               text=tile.surrounding_mines)

        if self.have_won():
            finish_time = time.time()
            minutes, seconds = divmod(int(finish_time - start_time), 60)
            # create custom popup with 3 buttons, one to reset, one to go to main menu and one to quit entirely
            if messagebox.askyesno('Winner!',
                                   'You Won in {} minutes and {} seconds! Try Again?'.format(minutes, seconds)):
                self.setup_board()
            else:
                sys.exit(0)

    def find_neighbours(self, clicked_tile):
        neighbours = []
        if clicked_tile.y == 0:
            y_start = 0
            y_end = clicked_tile.y + 2
        elif clicked_tile.y == (tiles_y - 1):
            y_start = clicked_tile.y - 1
            y_end = tiles_y
        else:
            y_start = clicked_tile.y - 1
            y_end = clicked_tile.y + 2

        if clicked_tile.x == 0:
            x_start = 0
            x_end = clicked_tile.x + 2
        elif clicked_tile.x == (tiles_x - 1):
            x_start = clicked_tile.x - 1
            x_end = tiles_x
        else:
            x_start = clicked_tile.x - 1
            x_end = clicked_tile.x + 2

        for y in range(y_start, y_end):
            for x in range(x_start, x_end):
                if clicked_tile.x != x or clicked_tile.y != y:
                    if tiles[x][y].uncovered == False:
                        neighbours.append(tiles[x][y])
        return neighbours

    def find_tile(self, find_id):
        for column in tiles:
            for item in column:
                if item.canvas_id == find_id:
                    return item

    def get_neighbour_mines(self, tile, neighbours):
        surrounding_mines = 0
        for neighbour in neighbours:
            if neighbour.contains_mine:
                surrounding_mines += 1
        tile.surrounding_mines = surrounding_mines

    def setup_board(self):
        placed_mines = 0
        global tiles, start_time, finish_time

        start_time = 0
        finish_time = 0
        tiles = [[0] * tiles_y for i in range(tiles_x)]
        time_label.config(text="Time: ")
        score_label.config(text="Score: ")
        for i in range(tiles_y):
            y = i * side_length
            for f in range(tiles_x):
                x = side_length * f
                centre_x = (x + (side_length / 2))
                centre_y = (y + (side_length / 2))
                canvas_id = canvas.create_rectangle(centre_x - (side_length / 2), centre_y - (side_length / 2),
                                                    centre_x + (side_length / 2), centre_y + (side_length / 2),
                                                    fill=default_colour)
                centre = {"x": centre_x, "y": centre_y}
                new_tile = Tile(f, i, canvas_id, centre)
                tiles[f][i] = new_tile

        while placed_mines < num_mines:
            rand_x = randint(0, tiles_x - 1)
            rand_y = randint(0, tiles_y - 1)
            if tiles[rand_x][rand_y].contains_mine == False:
                tiles[rand_x][rand_y].contains_mine = True
                placed_mines += 1

    def have_won(self):
        for column in tiles:
            for tile in column:
                if tile.uncovered == False and tile.contains_mine == False:
                    return False
        return True


root = Tk()
tiles_x, tiles_y = 15, 15
side_length = 30
num_mines = 20
tiles = []
default_colour = "#b7f4f0"
start_time = 0
finish_time = 0


class Tile(object):
    def __init__(self, x, y, canvas_id, centre):
        self.x = x
        self.y = y
        self.canvas_id = canvas_id
        self.contains_mine = False
        self.is_flagged = False
        self.surrounding_mines = 0
        self.uncovered = False
        self.centre = centre


def timer():
    global finish_time
    global start_time
    while start_time != 0 and finish_time == 0:
        game_time = int(time.time()- start_time)
        time_label.config(text="Time: {}".format(game_time))
        score_label.config(text="Score: {}".format(10000 - (game_time * 5)))
        time.sleep(1)


game_board = Board(10, 10, 30, 20)

Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)

frame = Frame(root)
frame.grid(row=0, sticky=W+E)
Grid.rowconfigure(frame, 0, weight=1)
Grid.columnconfigure(frame, 0, weight=1)
Grid.columnconfigure(frame, 1, weight=1)
Grid.columnconfigure(frame, 2, weight=1)

time_label = Label(frame, text="Time: ", width=10)
time_label.grid(row=0, column=0, sticky=W)
reset_button = Button(frame, text="Reset", width=15, command = game_board.setup_board).grid(row=0, column=1)
score_label = Label(frame, text="Score: ", width=10)
score_label.grid(row=0, column=2, sticky=W)

canvas = Canvas(root, width=tiles_x * side_length, height=tiles_y * side_length)
canvas.grid(row=1)

canvas.bind("<Button-1>", game_board.reveal_tile)
canvas.bind("<Button-3>", game_board.flag_tile)
game_board.setup_board()
root.mainloop()
