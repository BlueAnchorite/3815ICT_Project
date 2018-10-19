from abc import *


class Tile(ABC):
    @abstractmethod
    def __init__(self, x, y, canvas_id, centre):
        self.x = x
        self.y = y
        self.canvas_id = canvas_id
        self.contains_mine = False
        self.is_flagged = False
        self.surrounding_mines = 0
        self.uncovered = False
        self.centre = centre


class Board(ABC):
    @abstractmethod
    def __init__(self, tiles_x, tiles_y, tile_size, num_mines):
        self.tiles_x, self.tiles_y = tiles_x, tiles_y
        self.side_length = tile_size
        self.num_mines = num_mines
        self.tiles = []
        self.default_colour = "#b7f4f0"
        self.start_time = 0
        self.finish_time = 0

    @abstractmethod
    def display_tile(self, tile, neighbours):
        pass

    @abstractmethod
    def find_neighbours(self, clicked_tile):
        pass

    @abstractmethod
    def find_tile(self, find_id):
        pass

    @abstractmethod
    def get_neighbour_mines(self, tile, neighbours):
        pass

    @abstractmethod
    def setup_board(self):
        pass

    @abstractmethod
    def have_won(self):
        pass

    @abstractmethod
    def reveal_tile(self, clicked):
        pass

    @abstractmethod
    def flag_tile(self, clicked):
        pass


class Controller(ABC):

    @abstractmethod
    def reveal_event(self, event):
        pass

    @abstractmethod
    def flag_event(self, event):
        pass

    @abstractmethod
    def have_won(self, minutes, seconds):
        pass

    @abstractmethod
    def have_lost(self, minutes, seconds):
        pass


class View(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def update_view(self):
        pass

    @abstractmethod
    def reset_view(self):
        self.time_label.config(text="Time: ")
        self.score_label.config(text="Score: ")

    @abstractmethod
    def create_canvas_tile(self, points):
        pass

    @abstractmethod
    def timer(self):
        pass
