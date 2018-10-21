from tkinter import *
from tkinter import messagebox
from random import randint
import time, _thread, sys, math
import Abstract_Classes


class Hexsweeper_Board(Abstract_Classes.Board):
    def __init__(self, tiles_x, tiles_y, tile_size, num_mines):
        super().__init__(tiles_x, tiles_y, tile_size, num_mines)

    def display_tile(self, tile, neighbours):
        global start_time, finish_time
        tile.uncovered = True
        if tile.surrounding_mines == 0 and tile.contains_mine == False:
            # instead of recursively calling we should instead iterate through a list
            for neighbour in neighbours:
                surrounding_neighbours = self.find_neighbours(neighbour)
                self.get_neighbour_mines(neighbour, surrounding_neighbours)
                self.display_tile(neighbour, surrounding_neighbours)

        elif tile.contains_mine == True:
            game_view.update_view()
            finish_time = time.time()
            minutes, seconds = divmod(int(finish_time - start_time), 60)
            game_controller.have_lost(minutes, seconds)

        if self.have_won():
            game_view.update_view()
            finish_time = time.time()
            minutes, seconds = divmod(int(finish_time - start_time), 60)
            game_controller.have_won(minutes, seconds)


    def find_neighbours(self, clicked_tile):
        neighbours = []
        offset_directions = [
            [[+1, 0], [+1, -1], [0, -1],
             [-1, -1], [-1, 0], [0, +1]],
            [[+1, +1], [+1, 0], [0, -1],
             [-1, 0], [-1, +1], [0, +1]],
        ]

        parity = clicked_tile.x & 1
        for i in range(6):
            dir = offset_directions[parity][i]
            if clicked_tile.x + dir[0] >= 0 and clicked_tile.x + dir[0] < self.tiles_x:
                if clicked_tile.y + dir[1] >= 0 and clicked_tile.y + dir[1] < self.tiles_y:
                    if self.tiles[clicked_tile.x + dir[0]][clicked_tile.y + dir[1]].uncovered == False:
                        neighbours.append(self.tiles[clicked_tile.x + dir[0]][clicked_tile.y + dir[1]])



        return neighbours

    def find_tile(self, find_id):
        for column in self.tiles:
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
        self.tiles = [[0] * self.tiles_y for i in range(self.tiles_x)]
        for i in range(self.tiles_y):
            for f in range(self.tiles_x):
                width = 2 * self.side_length
                height = math.sqrt(3) * self.side_length
                if f % 2 == 0:
                    centre_x = (width * 3/4) * f + (width)
                    centre_y = i * height + (height/2) + 5
                elif f % 2 == 1:
                    centre_x = (width * 3/4) * f + (width)
                    centre_y = i * height + height + 5
                points = []
                for j in range(6):
                    angle_deg = 60 * j
                    angle_rad = math.pi / 180 * angle_deg
                    points.append(centre_x + self.side_length * math.cos(angle_rad))
                    points.append(centre_y + self.side_length * math.sin(angle_rad))
                centre = {"x": centre_x, "y": centre_y}
                new_tile = Tile(f, i, game_view.create_canvas_tile(points), centre)
                self.tiles[f][i] = new_tile

        while placed_mines < self.num_mines:
            rand_x = randint(0, self.tiles_x - 1)
            rand_y = randint(0, self.tiles_y - 1)
            if self.tiles[rand_x][rand_y].contains_mine == False:
                self.tiles[rand_x][rand_y].contains_mine = True
                placed_mines += 1

    def have_won(self):
        for column in self.tiles:
            for tile in column:
                if tile.uncovered == False and tile.contains_mine == False:
                    return False
        return True

    def reveal_tile(self, clicked):
        global start_time
        global timer_thread
        clicked_tile = self.find_tile(clicked[0])
        if clicked_tile:
            if start_time == 0:
                start_time = time.time()
                timer_thread = _thread.start_new_thread(game_view.timer, ())
            if clicked_tile.uncovered == False:
                neighbours = self.find_neighbours(clicked_tile)
                self.get_neighbour_mines(clicked_tile, neighbours)
                self.display_tile(clicked_tile, neighbours)

    def flag_tile(self, clicked):
        clicked_tile = self.find_tile(clicked[0])
        if clicked_tile:
            if clicked_tile.uncovered == False and clicked_tile.is_flagged == False:
                clicked_tile.is_flagged = True
            elif clicked_tile.uncovered == False and clicked_tile.is_flagged == True:
                clicked_tile.is_flagged = False


class Tile(Abstract_Classes.Tile):
    def __init__(self, x, y, canvas_id, centre):
        super().__init__(x, y, canvas_id, centre)


class Hexsweeper_Controller(Abstract_Classes.Controller):

    def reveal_event(self, event):
        if game_view.canvas.find_withtag(CURRENT):
            clicked = game_view.canvas.find_withtag(CURRENT)
            game_board.reveal_tile(clicked)
            game_view.update_view()

    def flag_event(self, event):
        if game_view.canvas.find_withtag(CURRENT):
            clicked = game_view.canvas.find_withtag(CURRENT)
            game_board.flag_tile(clicked)
            game_view.update_view()

    def have_won(self, minutes, seconds):
        if messagebox.askyesno('Winner!',
                               'You Won in {} minutes and {} seconds! Try Again?'.format(minutes, seconds)):
            game_board.setup_board()
            game_view.reset_view()
        else:
            sys.exit(0)

    def have_lost(self, minutes, seconds):
        if messagebox.askyesno('Game Over',
                               'You lost in {} minutes and {} seconds, Try Again?'.format(minutes, seconds)):
            game_board.setup_board()
            game_view.reset_view()
        else:
            sys.exit(0)


class Hexsweeper_View(Abstract_Classes.View):
    def __init__(self):
        self.root = Tk()
        Grid.rowconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 0, weight=1)

        self.frame = Frame(self.root)
        self.frame.grid(row=0, sticky=W + E)
        Grid.rowconfigure(self.frame, 0, weight=1)
        Grid.columnconfigure(self.frame, 0, weight=1)
        Grid.columnconfigure(self.frame, 1, weight=1)
        Grid.columnconfigure(self.frame, 2, weight=1)

        self.time_label = Label(self.frame, text="Time: ", width=10)
        self.time_label.grid(row=0, column=0, sticky=W)
        self.reset_button = Button(self.frame, text="Reset", width=15, command=game_board.setup_board).grid(row=0, column=1)
        self.score_label = Label(self.frame, text="Score: ", width=10)
        self.score_label.grid(row=0, column=2, sticky=W)

        self.canvas = Canvas(self.root, width=game_board.tiles_x * (1.75 * game_board.side_length),
                             height=(game_board.tiles_y * (math.sqrt(3) * game_board.side_length))
                                        + (math.sqrt(3) * game_board.side_length))
        self.canvas.grid(row=1)

        self.canvas.bind("<Button-1>", game_controller.reveal_event)
        self.canvas.bind("<Button-3>", game_controller.flag_event)

    def update_view(self):
        for column in game_board.tiles:
            for tile in column:
                if tile.is_flagged == True and tile.uncovered == False:
                    self.canvas.itemconfig(tile.canvas_id, fill="red")
                elif tile.is_flagged == False and tile.uncovered == False:
                    self.canvas.itemconfig(tile.canvas_id, fill=game_board.default_colour)
                elif tile.uncovered == True:
                    self.canvas.itemconfig(tile.canvas_id, fill="white")

                if tile.uncovered == True and tile.contains_mine == True:
                    self.canvas.create_text(tile.centre["x"], tile.centre["y"],
                                                 font=("", int((game_board.side_length * 2) / 3)), text="*")
                elif tile.uncovered == True and tile.surrounding_mines > 0:
                    self.canvas.create_text(tile.centre["x"], tile.centre["y"],
                                                 font=("", int((game_board.side_length * 2) / 3)),
                                                 text=tile.surrounding_mines)

        self.canvas.update_idletasks()


    def reset_view(self):
        self.time_label.config(text="Time: ")
        self.score_label.config(text="Score: ")

    def create_canvas_tile(self, points):
        return self.canvas.create_polygon(points, outline = "black",fill=game_board.default_colour)

    def timer(self):
        global finish_time
        global start_time
        while start_time != 0 and finish_time == 0:
            game_time = int(time.time() - start_time)
            self.time_label.config(text="Time: {}".format(game_time))
            self.score_label.config(text="Score: {}".format(10000 - (game_time * 5)))
            time.sleep(1)


game_board = Hexsweeper_Board(10, 10, 30, 20)
game_controller = Hexsweeper_Controller()
game_view = Hexsweeper_View()
game_board.setup_board()
game_view.root.mainloop()