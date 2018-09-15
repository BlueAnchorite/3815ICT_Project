from tkinter import *
from random import randint

root = Tk()
tiles_x, tiles_y = 10, 10
side_length = 30
num_mines = 10
placed_mines = 0

canvas = Canvas(root, width=tiles_x * side_length, height=tiles_y * side_length)
canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
canvas.pack()


class Tile(object):
    def __init__(self, x, y, canvas_id, centre):
        self.x = x
        self.y = y
        self.canvas_id = canvas_id
        self.contains_mine = False
        self.surrounding_mines = 0
        self.uncovered = False
        self.centre = centre


def click(event):
    if canvas.find_withtag(CURRENT):
        clicked = canvas.find_withtag(CURRENT)
        clicked_tile = find_tile(clicked[0])
        if clicked_tile:
            print("clicked tile is: ", clicked_tile.x, clicked_tile.y, clicked_tile.contains_mine)
            if clicked_tile.uncovered == False:
                neighbours = find_neighbours(clicked_tile)
                get_neighbour_mines(clicked_tile, neighbours)
                display_tile(clicked_tile, neighbours)
                canvas.update_idletasks()
                canvas.after(200)


def display_tile(tile, neighbours):
    tile.uncovered = True
    if tile.surrounding_mines == 0:
        for neighbour in neighbours:
            surrounding_neighbours = find_neighbours(neighbour)
            get_neighbour_mines(neighbour,surrounding_neighbours)
            display_tile(neighbour,surrounding_neighbours)
    else:
        canvas.create_text(tile.centre["x"], tile.centre["y"], font=("", int((side_length * 2 ) / 3)), text=tile.surrounding_mines)
    canvas.itemconfig(tile.canvas_id, fill="white")


def find_neighbours(clicked_tile):
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


def find_tile(find_id):
    for column in tiles:
        for item in column:
            if item.canvas_id == find_id:
                return item


def get_neighbour_mines(tile, neighbours):
    surrounding_mines = 0
    for neighbour in neighbours:
        if neighbour.contains_mine:
            surrounding_mines += 1
    tile.surrounding_mines = surrounding_mines


items = []
tiles = [[0] * tiles_y for i in range(tiles_x)]
for i in range(tiles_y):
    y = i * side_length
    for f in range(tiles_x):
        x = side_length * f
        canvas_id = canvas.create_rectangle(x, y, x + side_length, y + side_length, fill="red")
        centre_x = (x + (side_length/2))
        centre_y = (y + (side_length/2))
        centre = {"x": centre_x, "y": centre_y}
        new_tile = Tile(f, i, canvas_id, centre)
        tiles[f][i] = new_tile

while placed_mines < num_mines:
    rand_x = randint(0, tiles_x - 1)
    rand_y = randint(0, tiles_y - 1)
    if tiles[rand_x][rand_y].contains_mine == False:
        tiles[rand_x][rand_y].contains_mine = True
        placed_mines += 1

canvas.bind("<Button-1>", click)
root.mainloop()