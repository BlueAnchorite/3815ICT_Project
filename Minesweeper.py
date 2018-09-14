from tkinter import *

root = Tk()
tiles_x, tiles_y = 10, 10
side_length = 15
canvas = Canvas(root, width=tiles_x * side_length, height=tiles_y * side_length)
canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
canvas.pack()


class Tile(object):
    def __init__(self, x, y, canvas_id):
        self.x = x
        self.y = y
        self.canvas_id = canvas_id


def click(event):
    if canvas.find_withtag(CURRENT):
        canvas.itemconfig(CURRENT, fill="blue")
        clicked = canvas.find_withtag(CURRENT)
        print(clicked[0])
        clicked_tile = find_tile(clicked[0])
        print(clicked_tile.x, clicked_tile.y)
        find_neighbours(clicked_tile)
        canvas.update_idletasks()
        canvas.after(200)
        canvas.itemconfig(CURRENT, fill="red")


def find_neighbours(clicked_tile):
    neighbours = []
    if clicked_tile.y == 0:
        y_start = 0
    elif clicked_tile.y == tiles_y - 1:
        y_end = tiles_y - 1
    else:
        y_start = clicked_tile.y - 1
        y_end = clicked_tile.y + 2

    if clicked_tile.x == 0:
        x_start = 0
    elif clicked_tile.x == tiles_x - 1:
        x_end = tiles_x - 1
    else:
        x_start = clicked_tile.x - 1
        x_end = clicked_tile.x + 2

    for y in range(y_start, y_end):
        for x in range(x_start, x_end):
            neighbours.append(tiles[x][y])
    for i in neighbours:
        print(i.x, i.y)


def find_tile(find_id):
    for column in tiles:
        for item in column:
            if item.canvas_id == find_id:
                return item


items = []
tiles = [[] for i in range(tiles_x)]
for i in range(tiles_y):
    y = i * side_length
    for f in range(tiles_x):
        x = side_length * f
        canvas_id = canvas.create_rectangle(x, y, x + side_length, y + side_length, fill="red")
        new_tile = Tile(f, i, canvas_id)
        tiles[i].append(new_tile)

canvas.bind("<Button-1>", click)
items = canvas.find_all()
print(items)
root.mainloop()