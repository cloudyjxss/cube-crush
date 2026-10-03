
'''
Cube Crush
Jessica Collier
Version 1.1.5
11/03/2026
'''

#load pygame - no longer needed as using pyinstaller to package the game
import pygame
import sys
pygame.init()
#pygame.mixer.init() - removed music as need audio forwarding to work

#for random colour/size of the blocks
import random
#for timed mode countdown
import time

#image files in different folders - pathlib lets you use relative paths to access files in different folders
from pathlib import Path
project_dir = Path(__file__).parent
parts_dir = project_dir / "parts"
blocks_dir = parts_dir / "images" / "blocks"
buttons_dir = parts_dir / "images" / "buttons"

# finds the path for the file name parametre 
def find_asset(file_name):
    for folder in (blocks_dir, buttons_dir, parts_dir): # goes through each file in each folder
        current_file = folder / file_name # tries to make the path of the file
        if current_file.is_file() == True: # checks if the file exists, else tries the next file in for loop
            return current_file
    raise FileNotFoundError(file_name) # prints a specific file not found error for the file instead of none - removes confusing error message



global active_blocks, grid_array, single_blocks, score, timer
grid_array = [[0 for _ in range(8)] for _ in range(8)] # 2D array to represent the grid, 0 for empty, 1 for occupied
active_blocks = [] # list to hold the currently active block pieces that can be moved by the player
single_blocks = [] # list to hold individual block pieces for checking filled rows/columns
score = 0
timer = 30

# dictionary of all piece types with their position, shape, and colour
PIECE_TYPES = {
    "b2x1_line": [(0, 0), (1, 0)],
    "b3x1_line": [(0, 0), (1, 0), (2, 0)],
    "b4x1_line": [(0, 0), (1, 0), (2, 0), (3, 0)],
    "b5x1_line": [(0, 0), (1, 0), (2, 0), (3, 0), (4,0)],
    "b2x2_square": [(0, 0), (1, 0), (0, 1), (1, 1)],
    "b3x3_square": [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)],
    "b3x2_rectangle": [(0, 0), (1, 0), (2,0), (0, 1), (1, 1), (2,1)],
    "b2x2_L": [(0, 0), (0, 1), (1, 1)],
    "b3x2_L": [(0, 0), (0, 1), (1, 1), (2,1)],
    "b3x3_L": [(0, 0), (0, 1), (0, 2), (1,2), (2,2)],
    "b3x3_cross": [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
    "b3x2_cross": [(1, 0), (0, 1), (1, 1), (2, 1)],
    "p2x1_line": [(0, 0), (1, 0)],
    "p3x1_line": [(0, 0), (1, 0), (2, 0)],
    "p4x1_line": [(0, 0), (1, 0), (2, 0), (3, 0)],
    "p5x1_line": [(0, 0), (1, 0), (2, 0), (3, 0), (4,0)],
    "p2x2_square": [(0, 0), (1, 0), (0, 1), (1, 1)],
    "p3x3_square": [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)],
    "p3x2_rectangle": [(0, 0), (1, 0), (2,0), (0, 1), (1, 1), (2,1)],
    "p2x2_L": [(0, 0), (0, 1), (1, 1)],
    "p3x2_L": [(0, 0), (0, 1), (1, 1), (2,1)],
    "p3x3_L": [(0, 0), (0, 1), (0, 2), (1,2), (2,2)],
    "p3x3_cross": [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
    "p3x2_cross": [(1, 0), (0, 1), (1, 1), (2, 1)],
    "g2x1_line": [(0, 0), (1, 0)],
    "g3x1_line": [(0, 0), (1, 0), (2, 0)],
    "g4x1_line": [(0, 0), (1, 0), (2, 0), (3, 0)],
    "g5x1_line": [(0, 0), (1, 0), (2, 0), (3, 0), (4,0)],
    "g2x2_square": [(0, 0), (1, 0), (0, 1), (1, 1)],
    "g3x3_square": [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)],
    "g3x2_rectangle": [(0, 0), (1, 0), (2,0), (0, 1), (1, 1), (2,1)],
    "g2x2_L": [(0, 0), (0, 1), (1, 1)],
    "g3x2_L": [(0, 0), (0, 1), (1, 1), (2,1)],
    "g3x3_L": [(0, 0), (0, 1), (0, 2), (1,2), (2,2)],
    "g3x3_cross": [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
    "g3x2_cross": [(1, 0), (0, 1), (1, 1), (2, 1)],
    "y2x1_line": [(0, 0), (1, 0)],
    "y3x1_line": [(0, 0), (1, 0), (2, 0)],
    "y4x1_line": [(0, 0), (1, 0), (2, 0), (3, 0)],
    "y5x1_line": [(0, 0), (1, 0), (2, 0), (3, 0), (4,0)],
    "y2x2_square": [(0, 0), (1, 0), (0, 1), (1, 1)],
    "y3x3_square": [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)],
    "y3x2_rectangle": [(0, 0), (1, 0), (2,0), (0, 1), (1, 1), (2,1)],
    "y2x2_L": [(0, 0), (0, 1), (1, 1)],
    "y3x2_L": [(0, 0), (0, 1), (1, 1), (2,1)],
    "y3x3_L": [(0, 0), (0, 1), (0, 2), (1,2), (2,2)],
    "y3x3_cross": [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
    "y3x2_cross": [(1, 0), (0, 1), (1, 1), (2, 1)],
    "b1x1_block": [(0, 0)],
    "g1x1_block": [(0, 0)],
    "p1x1_block": [(0, 0)],
    "y1x1_block": [(0, 0)],
}

# for images
class object_on_screen:
    def __init__(self, x, y, height, width, object_image):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.image = pygame.image.load(find_asset(object_image))

    def x_setter(self, new_x):
        self.x = new_x

    def y_setter(self, new_y):
        self.y = new_y

    def image_setter(self, new_image):
        self.image = pygame.image.load(find_asset(new_image))

    def height_setter(self, new_height):
        self.height = new_height

    def width_setter(self, new_width):
        self.width = new_width

    def height_getter(self):
        return self.height
    
    def width_getter(self):
        return self.width
    
    def x_getter(self):
        return self.x
    
    def y_getter(self):
        return self.y
    
    def display(self, screen):
        scaled_image = pygame.transform.scale(self.image, (int(self.width), int(self.height)))
        screen.blit(scaled_image, (self.x, self.y))

# for images which can be clicked + have a function
class button(object_on_screen):
    def __init__(self, x, y, height, width, object_image, on_click=None):
        super().__init__(x, y, height, width, object_image)
        self.on_click = on_click

    def is_clicked(self,mouse_x, mouse_y):
        #checks if the mouse is within the button boundaries
        if (self.x <= mouse_x <= self.x + self.width) and (self.y <= mouse_y <= self.y + self.height):
            if self.on_click:
                self.on_click() #calls the buttons on_click function

# for the pictures of blocks used in active blocks     
class block(object_on_screen):
    def __init__(self, x, y, height, width, object_image, piece_type=None, is_dragged=False, rotation=0):
        super().__init__(x, y, height, width, object_image)
        self.piece_type = piece_type
        self.is_dragged = False
        self.original_x = x
        self.original_y = y
        self.rotation = rotation
        self.blocks = []
        if piece_type is not None:
            self.setup_blocks()
        if rotation == 90 or rotation == 270:
            # swap width and height for 90 or 270 degree rotation
            temp = self.width
            self.width = self.height
            self.height = temp
        if rotation != 0:
            self.image = pygame.transform.rotate(self.image, rotation)
    
    def on_mouse_down(self, mouse_x, mouse_y):
        #checks if the mouse is within the block boundaries
        if (self.x <= mouse_x <= self.x + self.width) and (self.y <= mouse_y <= self.y + self.height):
            self.is_dragged = True #sets the block to be dragged when clicked
            self.original_x = self.x #store original position for snapping
            self.original_y = self.y
    
    def on_mouse_up(self):
        self.is_dragged = False #sets the block to not be dragged when mouse button is released
    
    def on_mouse_motion(self, mouse_x, mouse_y):
        if self.is_dragged:
            self.x_setter(mouse_x - self.width/2)
            self.y_setter(mouse_y - self.height/2)
    
    def setup_blocks(self):
        if self.piece_type in PIECE_TYPES:
            self.blocks = PIECE_TYPES[self.piece_type]
        return

# the 1x1 blocks which replace active blocks on the grid
class single_block(object_on_screen):
    def __init__(self, x, y, piece_type="b1x1_block", cell_size=50, rotation=0):
        colour_letter = piece_type[0] # get the first letter of the piece type to determine colour
        if colour_letter == "p":
            image_file = "p1x1_block.png"
        elif colour_letter == "g":
            image_file = "g1x1_block.png"
        elif colour_letter == "y":
            image_file = "y1x1_block.png"
        else:
            image_file = "b1x1_block.png" # default to blue if it fails
        super().__init__(x, y, cell_size, cell_size, image_file)
        self.cell_size = cell_size


# rotate the blocks by swapping their x and y positions then appending to a list of their new (rotated) positions
def rotate_block(positions, rotation):
    rotated = []
    if rotation == 0 or rotation == 360:
        for x, y in positions:
            rotated.append((x, y))
    elif rotation == 90:
        for x, y in positions:
            rotated.append((y, -x))
    elif rotation == 180:
        for x, y in positions:
            rotated.append((-x, -y))
    elif rotation == 270:
        for x, y in positions:
            rotated.append((-y, x))
    else:
        # no rotation if error
        for x, y in positions:
            rotated.append((x, y))

    # normalise offset to (0,0)
    min_x = rotated[0][0]
    min_y = rotated[0][1]
    for pos in rotated:
        if pos[0] < min_x:
            min_x = pos[0]
        if pos[1] < min_y:
            min_y = pos[1]

    updated_coords = []
    for x, y in rotated:
        updated_coords.append((x - min_x, y - min_y))
    return updated_coords

# snapping blocks to the top left corner of the cell and swapping with single blocks
def check_and_snap_block(block, grid_bounds):
    global active_blocks, single_blocks, grid_array
    cell_size = 50
    block_center_x = block.x + block.width / 2
    block_center_y = block.y + block.height / 2
    
    grid_x = grid_bounds['x']
    grid_y = grid_bounds['y']
    grid_width = grid_bounds['width']
    grid_height = grid_bounds['height']

    
    # check if block center is within grid bounds
    if (grid_x <= block_center_x <= grid_x + grid_width and 
        grid_y <= block_center_y <= grid_y + grid_height):
        # calculate which grid cell the block center is in
        cell_col = int((block_center_x - grid_x)/cell_size)
        cell_row = int((block_center_y - grid_y)/cell_size)
        
        cell_col = max(0, min(cell_col, 7))
        cell_row = max(0, min(cell_row, 7))

        piece_positions = rotate_block(PIECE_TYPES[block.piece_type], block.rotation) # get positions of the blocks
        can_place = True
        for pos in piece_positions:
            grid_col = cell_col + pos[0]
            grid_row = cell_row + pos[1]
            if grid_col < 0 or grid_col >= 8 or grid_row < 0 or grid_row >= 8:
                can_place = False
                break
            if grid_array[grid_row][grid_col] == 1: # check if cell is already occupied
                can_place = False
                break
        
    
        if can_place == True:
            for pos in piece_positions:
                grid_col = cell_col + pos[0]
                grid_row = cell_row + pos[1]
                piece_type = block.piece_type
                single_blocks.append(single_block(grid_col * cell_size + grid_x, grid_row * cell_size + grid_y, piece_type))
                grid_array[grid_row][grid_col] = 1 # mark cell as occupied

            active_blocks.remove(block) # remove the block from active blocks list since it's now placed on the grid
        else:
            # can't place block, return to original position
            block.x_setter(block.original_x)
            block.y_setter(block.original_y)
    else:
        # can't place block, return to original position as its outside of the grid
        block.x_setter(block.original_x)
        block.y_setter(block.original_y)

#drawing the white/black preview of where the block will snap on the grid
def draw_block_preview(screen, block, grid_bounds):
    global grid_array
    cell_size = 50
    block_center_x = block.x + block.width / 2
    block_center_y = block.y + block.height / 2

    grid_x = grid_bounds['x']
    grid_y = grid_bounds['y']
    grid_width = grid_bounds['width']
    grid_height = grid_bounds['height']

#check if block center is within grid bounds
    if (grid_x <= block_center_x <= grid_x + grid_width and 
        grid_y <= block_center_y <= grid_y + grid_height):

        cell_col = int((block_center_x - grid_x)/cell_size)
        cell_row = int((block_center_y - grid_y)/cell_size)

        cell_col = max(0, min(cell_col, 7))
        cell_row = max(0, min(cell_row, 7))

        piece_positions = rotate_block(PIECE_TYPES[block.piece_type], block.rotation) # get positions of the blocks
        can_place = True
        for pos in piece_positions:
            grid_col = cell_col + pos[0]
            grid_row = cell_row + pos[1]
            if grid_col < 0 or grid_col >= 8 or grid_row < 0 or grid_row >= 8:
                can_place = False
                break
            if grid_array[grid_row][grid_col] == 1: # check if cell is already occupied
                can_place = False
                break
        
        if can_place == True:
            preview_colour = (255, 255, 255, 100) # semi-transparent white
        else:
            preview_colour = (66, 32, 29, 50) # semi-transparent black

        for pos in piece_positions:
            grid_col = cell_col + pos[0]
            grid_row = cell_row + pos[1]
            preview_x = grid_x + grid_col * cell_size
            preview_y = grid_y + grid_row * cell_size

            preview_surface = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
            preview_surface.fill(preview_colour)
            screen.blit(preview_surface, (preview_x, preview_y))

# spawn 4 randomised pieces of a random colour, shape, and rotation
def spawn_pieces():
    global active_blocks, state
    active_blocks = []
    piece_types = list(PIECE_TYPES.keys())
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    x_coords = [screen_width * 0.1, screen_width * 0.1, screen_width * 0.8, screen_width * 0.8]
    y_coords = [screen_height * 0.25, screen_height * 0.63, screen_height * 0.25, screen_height * 0.63]
    block_width = 0
    block_height = 0
    rotation = 0
    rotation_choices = [90,180,270,360]

    if state == "gameover": # if the state is gameover (runs when user clicks continue playing) the pieces that spawn are 4 single blocks (all 4 colours)
        block_height = 50
        block_width = 50
        active_blocks.append(block(x_coords[0], y_coords[0], block_height, block_width, "b1x1_block.png", piece_type="b1x1_block"))
        active_blocks.append(block(x_coords[1], y_coords[1], block_height, block_width, "p1x1_block.png", piece_type="p1x1_block"))
        active_blocks.append(block(x_coords[2], y_coords[2], block_height, block_width, "g1x1_block.png", piece_type="g1x1_block"))
        active_blocks.append(block(x_coords[3], y_coords[3], block_height, block_width, "y1x1_block.png", piece_type="y1x1_block"))
    else: # spawn 4 blocks with random shapes, colours, and rotations
        for i in range(4):
            random_piece_type = random.choice(piece_types)  
            rotation = random.choice(rotation_choices)     
            x = x_coords[i]
            y = y_coords[i]
            image_path = f"{random_piece_type}.png"
            if random_piece_type == "b2x1_line" or random_piece_type == "p2x1_line" or random_piece_type == "g2x1_line" or random_piece_type == "y2x1_line":
                block_height = 50
                block_width = 100
            elif random_piece_type == "b3x1_line" or random_piece_type == "p3x1_line" or random_piece_type == "g3x1_line" or random_piece_type == "y3x1_line":
                block_height = 50
                block_width = 150
            elif random_piece_type == "b4x1_line" or random_piece_type == "p4x1_line" or random_piece_type == "g4x1_line" or random_piece_type == "y4x1_line":
                block_height = 50
                block_width = 200
            elif random_piece_type == "b5x1_line" or random_piece_type == "p5x1_line" or random_piece_type == "g5x1_line" or random_piece_type == "y5x1_line":
                block_height = 50
                block_width = 250
            elif random_piece_type == "b2x2_L" or random_piece_type == "b2x2_square" or random_piece_type == "p2x2_L" or random_piece_type == "p2x2_square" or random_piece_type == "g2x2_L" or random_piece_type == "g2x2_square" or random_piece_type == "y2x2_L" or random_piece_type == "y2x2_square":
                block_height = 100
                block_width = 100
            elif random_piece_type == "b3x3_L" or random_piece_type == "b3x3_cross" or random_piece_type == "b3x3_square" or random_piece_type == "p3x3_L" or random_piece_type == "p3x3_cross" or random_piece_type == "p3x3_square" or random_piece_type == "g3x3_L" or random_piece_type == "g3x3_cross" or random_piece_type == "g3x3_square" or random_piece_type == "y3x3_L" or random_piece_type == "y3x3_cross" or random_piece_type == "y3x3_square":
                block_height = 150
                block_width = 150
            elif random_piece_type == "b3x2_rectangle" or random_piece_type == "b3x2_L" or random_piece_type == "b3x2_cross" or random_piece_type == "p3x2_rectangle" or random_piece_type == "p3x2_L" or random_piece_type == "p3x2_cross" or random_piece_type == "g3x2_rectangle" or random_piece_type == "g3x2_L" or random_piece_type == "g3x2_cross" or random_piece_type == "y3x2_rectangle" or random_piece_type == "y3x2_L" or random_piece_type == "y3x2_cross":
                block_height = 100
                block_width = 150
            elif random_piece_type == "b1x1_block" or random_piece_type == "p1x1_block" or random_piece_type == "g1x1_block" or random_piece_type == "y1x1_block":
                block_height = 50
                block_width = 50

            piece = block(x, y, block_height, block_width, image_path, piece_type=random_piece_type, rotation=rotation)
            active_blocks.append(piece)
    return active_blocks

# draws the 8x8 grid
def drawgrid(screen):
    white = (255,255,255)
    cols = 8
    rows = 8
    cell_size = 50
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    grid_width = cols * cell_size
    grid_height = rows * cell_size
    
    grid_x = (screen_width - grid_width) / 2
    grid_y = (screen_height - grid_height) / 2
    
    for col in range(cols + 1):
        x = grid_x + col * cell_size
        pygame.draw.line(screen, white, (x, grid_y), (x, grid_y + grid_height), 2)
    
    for row in range(rows + 1):
        y = grid_y + row * cell_size
        pygame.draw.line(screen, white, (grid_x, y), (grid_x + grid_width, y), 2)
    
    # Return grid bounds for snapping
    return {'x': grid_x, 'y': grid_y, 'width': grid_width, 'height': grid_height}

# checks all of the rows and columns to see if the grid_array has all 1s (means it's full) to then increase score and clear the row/column of all single blocks and swap to 0s in the grid array
def check_rows_and_columns():
    global grid_array, single_blocks, timer, state
    for row in range(8):
        if all(cell == 1 for cell in grid_array[row]):
            if state == "infinite_gamemode":
                increase_score()
            elif state == "timed_gamemode":
                timer += 5
            # clear the row 
            for col in range(8):
                grid_array[row][col] = 0 # set the grid array to 0s on the column which represent the cell is empty
                for block in single_blocks:
                    # work out which row this block is in
                    block_row = int((block.y_getter() - grid_bounds['y']) / 50)
                    if block_row == row:
                        single_blocks.remove(block) # remove blocks in the cleared row



    for col in range(8):
        if all(grid_array[row][col] == 1 for row in range(8)):
            if state == "infinite_gamemode": # increase score if infinite game mode
                increase_score()
            elif state == "timed_gamemode": # increase timer if timed game mode
                timer += 5
            # clear the column
            for row in range(8):
                grid_array[row][col] = 0  # set the grid array to 0s on the column which represent the cell is empty
                for block in single_blocks:
                    # work out which column this block is in
                    block_col = int((block.x_getter() - grid_bounds['x']) / 50)
                    if block_col == col:
                        single_blocks.remove(block) # remove blocks in the cleared column

# checks if the game is over by checking all of the active blocks in all positions of the grid, if all possible positions are 1s for all blocks, game is over
def check_game_over():
    global active_blocks, grid_array, state
    for block in active_blocks:
        piece_positions = rotate_block(PIECE_TYPES[block.piece_type], block.rotation) # gets rotated block positions for the pieces
        can_place = False
        for row in range(8):
            for col in range(8):
                can_place = True
                for pos in piece_positions:
                    grid_col = col + pos[0]
                    grid_row = row + pos[1]
                    if grid_col < 0 or grid_col >= 8 or grid_row < 0 or grid_row >= 8:
                        can_place = False
                        break
                    if grid_array[grid_row][grid_col] == 1: # check if cell is already occupied
                        can_place = False
                        break
                if can_place:
                    return False # found a valid placement, not game over
    return True # no valid placements found, game over

# increase the score by looking at the current score, calculating the appropriate tier, and then applying the multiplyer to the base value
def increase_score():
    colourwhite = (255,255,255)
    global score, score_text, scoreRecttext
    score = int(score)
    if score > 500: # low tier
        score_multiplyer = 2
    elif score > 1500: # medium tier
        score_multiplyer = 4
    else: # high tier
        score_multiplyer = 1
    score += 50 * score_multiplyer # calculate score
    # display the new score
    score = str(score)
    score_font = pygame.font.Font(find_asset("score_font.otf"), 75)
    score_text = score_font.render(score, True, colourwhite)
    scoreRecttext = score_text.get_rect(center=(screen.get_width()/2, screen.get_height()/6))
    screen.blit(score_text, scoreRecttext)
    return
    
# assigned so it doesn't error if called      
background_copy = None
grid_bounds = None

# click functions
def continueplaying_button_gameover_clicked():
    global state, lives, previous_state, active_blocks, timer
    if lives <= 0: # if user has no lives, function does nothing
        return
    else: # removes one life, spawns the 1x1 pieces, and then draws the previous game state
        lives = lives - 1
        spawn_pieces()
        if previous_state != "gameover":
            state = previous_state
        if state == "timed_gamemode" and timer < 31: # if previous state is timed game mode and the timer is less than 31 (game over most likely due to timer running out) set the timer to 31, else presume the game over was a result of full grid, so keep the higher timer that the user had
            timer = 31
        draw()
    return

def home_button_gameover_clicked():
    global state, previous_state
    state = "startup_screen"
    previous_state = "startup_screen"
    draw()
    return

def home_button_settings_clicked():
    global state, previous_state
    state = "startup_screen"
    previous_state = "startup_screen"
    draw()
    return

def infinite_button_clicked():
    global state, lives, score, active_blocks, single_blocks, grid_array
    state = "infinite_gamemode"
    lives = 2
    score = 0
    active_blocks = []
    single_blocks = []
    grid_array = [[0 for _ in range(8)] for _ in range(8)]
    draw()
    return

def restart_button_gameover_clicked():
    global state, score, grid_array, active_blocks, single_blocks, previous_state, score_text, scoreRecttext, lives, timer
    active_blocks = []
    lives = 2
    grid_array = [[0 for _ in range(8)] for _ in range(8)]
    single_blocks = []
    state = previous_state
    if state == "infinite_gamemode":
        score = 0
        score_text = score_font.render(str(score), True, colourwhite)
        scoreRecttext = score_text.get_rect(center=(screen.get_width()/2, screen.get_height()/6))
        screen.blit(score_text, scoreRecttext)
    elif state == "timed_gamemode":
        timer = 30
    draw()
    return

def settings_button_clicked():
        global state, previous_state, background_copy, settings_timer, timer
        if state == "settings_screen":
            return
        background_copy = pygame.transform.scale(screen.copy(), screen.get_size())
        previous_state = state
        state = "settings_screen"
        if previous_state == "timed_gamemode":
            settings_timer = timer # store the current timer value when entering settings from timed mode
        draw()
        return

def timed_button_clicked():
    global state, timer, lives, score, active_blocks, single_blocks, grid_array, timer_update
    state = "timed_gamemode"
    timer = 30
    lives = 2
    score = 0
    active_blocks = []
    single_blocks = []
    grid_array = [[0 for _ in range(8)] for _ in range(8)]
    timer_update = pygame.time.get_ticks()  # set timer_update only once when entering timed mode
    draw()
    return

def togglesound_button_settings_clicked():
    global music_paused
    if music_paused == True:
        #pygame.mixer.music.unpause()  - removed music as need audio forwarding to work
        music_paused = False
    else:
        #pygame.mixer.music.pause()  - removed music as need audio forwarding to work
        music_paused = True
    return

def restart_button_settings_clicked():
    global state, score, grid_array, active_blocks, single_blocks, previous_state, score_text, scoreRecttext, lives, timer
    active_blocks = []
    grid_array = [[0 for _ in range(8)] for _ in range(8)]
    single_blocks = []
    state = previous_state
    lives = 2
    if state == "infinite_gamemode":
        score = 0
        score_text = score_font.render(str(score), True, colourwhite)
        scoreRecttext = score_text.get_rect(center=(screen.get_width()/2, screen.get_height()/6))
        screen.blit(score_text, scoreRecttext)
    elif state == "timed_gamemode":
        timer = 30
    draw()
    return

def exit_settings_button_clicked():
    global state, previous_state, settings_timer, timer
    state = previous_state
    if state == "timed_gamemode":
        timer = settings_timer # restore the timer value when exiting settings to timed mode
    draw()
    return

def exit_game_button_settings_clicked():
    pygame.quit()
    sys.exit()

#main display and background
screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
bg_image = pygame.image.load(find_asset("background_image.jpg"))
pygame.display.set_caption("Cube Crush")
colourwhite = (255, 255, 255)

#scale the background image to window size
def scale_bg_image():
    return pygame.transform.scale(bg_image,screen.get_size())

#font and text
pygame.font.init()
pygame.font.get_init()
global logo_font
logo_font = pygame.font.Font(find_asset("logo_font.ttf"), 75)
logo_text = logo_font.render("CUBE CRUSH", True, colourwhite)
logoRecttext = logo_text.get_rect(center=(screen.get_width()/2, screen.get_height()/5))

global score_text, scoreRecttext
score_font = pygame.font.Font(find_asset("score_font.otf"), 75)
score_text = score_font.render(str(score), True, colourwhite)
scoreRecttext = score_text.get_rect(center=(screen.get_width()/2, screen.get_height()/6))

global timer_text, timerRecttext
timer_text = score_font.render(str(timer), True, colourwhite)
timerRecttext = timer_text.get_rect(center=(screen.get_width()/2, screen.get_height()/6))

#startup screen - creating instances
play_image = object_on_screen(screen.get_width()/2, screen.get_height()/5,50,25,"play_image.png")
infinite_button = button(100, 150, 200, 200, "infinite_button.png",on_click=infinite_button_clicked)
settings_button = button(100, 150, 200, 200, "settings_button.png",on_click=settings_button_clicked)
timed_button = button(100, 150, 200, 200, "timed_button.png",on_click=timed_button_clicked)
#gameover screen - creating instances
restart_button_gameover = button(100, 150, 200, 200, "restart_button_gameover.png",on_click=restart_button_gameover_clicked)
continueplaying_button_gameover = button(100, 150, 200, 200, "continueplaying_button_gameover.png",on_click=continueplaying_button_gameover_clicked)
home_button_gameover = button(100, 150, 200, 200, "home_button_gameover.png",on_click=home_button_gameover_clicked)
#settings screen - creating instances
restart_button_settings = button(100, 150, 200, 200, "restart_button_settings.png",on_click=restart_button_settings_clicked)
togglesound_button_settings = button(100, 150, 200, 200, "togglesound_button_settings.png",on_click=togglesound_button_settings_clicked)
home_button_settings = button(100, 150, 200, 200, "home_button_settings.png",on_click=home_button_settings_clicked)
settings_image = object_on_screen(100, 150, 200, 200, "settings_image.png")
exit_game_button_settings = button(100, 150, 200, 200, "exit_game_button_settings.png", on_click=exit_game_button_settings_clicked)
exit_settings_button = button(100, 150, 200, 200, "exit_settings_button.png", on_click=exit_settings_button_clicked)
#hearts - creating instances
full_heart_left = object_on_screen(100, 150, 200, 200, "full_heart.png")
full_heart_right = object_on_screen(100, 150, 200, 200, "full_heart.png")
empty_heart_left = object_on_screen(100, 150, 200, 200, "empty_heart.png")
empty_heart_right = object_on_screen(100, 150, 200, 200, "empty_heart.png")

#loading each state
def draw():
    global grid_bounds, state, previous_state, background_copy, timer
    if state == "startup_screen":
        # set the width, height, and coordinates of all the buttons and images
        screen.blit(bg_image, (0, 0))
        screen.blit(logo_text, logoRecttext)
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        play_image.height_setter(screen.get_height()/3)
        play_image.width_setter(screen.get_width() /4)
        play_image.x_setter(screen.get_width()/2 - play_image.width_getter()/2)
        play_image.y_setter(screen.get_height()/2 - play_image.height_getter()/2)
        play_image.display(screen)

        infinite_button.height_setter(screen.get_height()/10)
        infinite_button.width_setter(screen.get_width()/6)
        infinite_button.x_setter(screen.get_width()/2 - infinite_button.width_getter()/2)
        infinite_button.y_setter(screen.get_height()/2 - infinite_button.height_getter()/1.5 - infinite_button.height_getter()/20)
        infinite_button.display(screen)

        timed_button.height_setter(screen.get_height()/10)
        timed_button.width_setter(screen.get_width()/6)
        timed_button.x_setter(screen.get_width()/2 - timed_button.width_getter()/2)
        timed_button.y_setter(screen.get_height()/2 - timed_button.height_getter()/1.5  + timed_button.height_getter()/2 + timed_button.height_getter()/2)
        timed_button.display(screen)

        settings_button_size = min(screen.get_width(), screen.get_height()) / 15
        settings_button.height_setter(settings_button_size)
        settings_button.width_setter(settings_button_size)
        settings_button.x_setter(screen.get_width() - settings_button_size - 20)
        settings_button.y_setter(20)
        settings_button.display(screen)

        return
    if state == "infinite_gamemode":
        global score_text, scoreRecttext
        # set the width, height, and coordinates of all the buttons and images
        screen.blit(bg_image, (0, 0))
        screen.blit(score_text, scoreRecttext)
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        settings_button_size = min(screen_width, screen_height) / 15
        settings_button.height_setter(settings_button_size)
        settings_button.width_setter(settings_button_size)
        settings_button.x_setter(screen_width - settings_button_size - 20)
        settings_button.y_setter(20)
        settings_button.display(screen)
        grid_bounds = drawgrid(screen)

        if not active_blocks: # spawn pieces if active blocks is empty
            spawn_pieces()
        for block in single_blocks: # if a block in single blocks is placed, check the rows and columns to see if full & check if game is over
            block.display(screen)
            check_rows_and_columns()
            is_gameover = check_game_over()
            if is_gameover == True:
                background_copy = pygame.transform.scale(screen.copy(), screen.get_size())
                previous_state = "infinite_gamemode"
                state = "gameover"
                draw()
                return
        for piece in active_blocks: # if the piece is being dragged, draw the preview
            if piece.is_dragged:
                draw_block_preview(screen, piece, grid_bounds)
        for piece in active_blocks: # display the active blocks
            piece.display(screen)
        return
    if state == "timed_gamemode":
        is_timer_gameover = False
        is_gameover = False
        global timer_text, timerRecttext, timer_update
        # set the width, height, and coordinates of all the buttons and images
        screen.blit(bg_image, (0, 0))
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        settings_button_size = min(screen_width, screen_height) / 15
        settings_button.height_setter(settings_button_size)
        settings_button.width_setter(settings_button_size)
        settings_button.x_setter(screen_width - settings_button_size - 20)
        settings_button.y_setter(20)
        settings_button.display(screen)
        grid_bounds = drawgrid(screen)

        current_time = pygame.time.get_ticks() # get the current time
        if current_time - timer_update >= 1000 and timer > 0: # update the timer with the current time
            timer -= 1
            timer_update = current_time
        mins, secs = divmod(timer, 60) # put the timer into a minutes and seconds format
        timer_str = '{:02d}:{:02d}'.format(mins, secs)
        timer_text = score_font.render(timer_str, True, colourwhite) # timer text
        timerRecttext = timer_text.get_rect(center=(screen.get_width()/2, screen.get_height()/6))
        screen.blit(timer_text, timerRecttext)

        if not active_blocks: # spawn pieces if active blocks is empty
            spawn_pieces()
        for block in single_blocks: # if a block in single blocks is placed, check the rows and columns to see if full & check if game is over
            block.display(screen)
            check_rows_and_columns()
            is_gameover = check_game_over()
        for piece in active_blocks: # if the piece is being dragged, draw the preview
            if piece.is_dragged:
                draw_block_preview(screen, piece, grid_bounds)
        for piece in active_blocks: # display the active blocks
            piece.display(screen)
        if timer <= 0:
            timer = 0
            is_timer_gameover = True
        if is_gameover == True or is_timer_gameover == True:
            background_copy = pygame.transform.scale(screen.copy(), screen.get_size())
            previous_state = "timed_gamemode"
            state = "gameover"
            draw()
            return
        return
    if state == "settings_screen":
        # screen copy
        screen.blit(background_copy, (0, 0))
        # semi-transparent white overlay
        bg_setting_image = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        bg_setting_image.fill((0, 0, 0, 120))
        screen.blit(bg_setting_image, (0, 0))

        # set the width, height, and coordinates of all the buttons and images
        screen_w = screen.get_width()
        screen_h = screen.get_height()
        menu_width = screen_w * 0.2
        menu_height = screen_h * 0.59
        settings_image.width_setter(menu_width)
        settings_image.height_setter(menu_height)
        settings_image.x_setter((screen_w - menu_width) / 2)
        settings_image.y_setter((screen_h - menu_height) / 2)
        settings_image.display(screen)

        settings_button_width = menu_width * 0.8
        settings_button_height = menu_height / 7
        settings_button_x = (screen_w- settings_button_width) / 2
        settings_button_y_start = (screen_h - menu_height) / 2.6 + menu_height * 0.35
        settings_button_spacing = settings_button_height + screen_h * 0.013

        restart_button_settings.height_setter(settings_button_height)
        restart_button_settings.width_setter(settings_button_width)
        restart_button_settings.x_setter(settings_button_x)
        restart_button_settings.y_setter(settings_button_y_start)
        restart_button_settings.display(screen)

        togglesound_button_settings.height_setter(settings_button_height)
        togglesound_button_settings.width_setter(settings_button_width)
        togglesound_button_settings.x_setter(settings_button_x)
        togglesound_button_settings.y_setter(settings_button_y_start + settings_button_spacing)
        togglesound_button_settings.display(screen)

        home_button_settings.height_setter(settings_button_height)
        home_button_settings.width_setter(settings_button_width)
        home_button_settings.x_setter(settings_button_x)
        home_button_settings.y_setter(settings_button_y_start + settings_button_spacing * 2)
        home_button_settings.display(screen)

        exit_game_button_settings.height_setter(settings_button_height)
        exit_game_button_settings.width_setter(settings_button_width)
        exit_game_button_settings.x_setter(settings_button_x)
        exit_game_button_settings.y_setter(settings_button_y_start + settings_button_spacing * 3)
        exit_game_button_settings.display(screen)

        exit_settings_button.height_setter(settings_button_height*0.7)
        exit_settings_button.width_setter(settings_button_height*0.7)
        exit_settings_button.x_setter(((screen_h - menu_height) / 2) + settings_button_spacing*4.25)
        exit_settings_button.y_setter(settings_button_y_start - settings_button_spacing*2)
        exit_settings_button.display(screen)
        return
    if state == "gameover":
        global logo_font, lives

        # screen copy
        screen.blit(background_copy, (0, 0))
        # semi-transparent white overlay
        bg_gameover_image = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        bg_gameover_image.fill((0, 0, 0, 120))
        screen.blit(bg_gameover_image, (0, 0))
        gameover_text = logo_font.render("GAMEOVER", True, colourwhite)
        gameoverRecttext = gameover_text.get_rect(center=(screen.get_width()/2, screen.get_height()/6))
        screen.blit(gameover_text, gameoverRecttext)

        # set the width, height, and coordinates of all the buttons and images
        screen_w = screen.get_width()
        screen_h = screen.get_height()
        button_width = screen_w * 0.2
        button_height = screen_h * 0.1
        button_x = (screen_w - button_width) / 2
        button_y_start = screen_h / 2 - button_height / 2
        button_spacing = button_height + screen_h * 0.02
        continueplaying_button_gameover.height_setter(button_height + 10)
        continueplaying_button_gameover.width_setter(button_width)
        continueplaying_button_gameover.x_setter(button_x)
        continueplaying_button_gameover.y_setter(button_y_start)
        continueplaying_button_gameover.display(screen)
        restart_button_gameover.height_setter(button_height)
        restart_button_gameover.width_setter(button_width)
        restart_button_gameover.x_setter(button_x)
        restart_button_gameover.y_setter(button_y_start + button_spacing)
        restart_button_gameover.display(screen)
        home_button_gameover.height_setter(button_height)
        home_button_gameover.width_setter(button_width)
        home_button_gameover.x_setter(button_x)
        home_button_gameover.y_setter(button_y_start + button_spacing * 2)
        home_button_gameover.display(screen)

        if lives == 2: # two full hearts
            full_heart_left.y_setter(button_y_start - 90)
            full_heart_left.x_setter(screen_w/2 - 100)
            full_heart_left.height_setter(80)
            full_heart_left.width_setter(80)
            full_heart_left.display(screen)

            full_heart_right.y_setter(button_y_start - 90)
            full_heart_right.x_setter(screen_w/2 + 30)
            full_heart_right.height_setter(80)
            full_heart_right.width_setter(80)
            full_heart_right.display(screen)
        elif lives == 1: # one full heart, one empty heart
            full_heart_left.y_setter(button_y_start - 90)
            full_heart_left.x_setter(screen_w/2 - 100)
            full_heart_left.height_setter(80)
            full_heart_left.width_setter(80)
            full_heart_left.display(screen)

            empty_heart_right.y_setter(button_y_start - 90)
            empty_heart_right.x_setter(screen_w/2 + 100)
            empty_heart_right.height_setter(80)
            empty_heart_right.width_setter(80)
            empty_heart_right.display(screen)
        elif lives <= 0: # two empty hearts
            empty_heart_left.y_setter(button_y_start - 90)
            empty_heart_left.x_setter(screen_w/2 - 100)
            empty_heart_left.height_setter(80)
            empty_heart_left.width_setter(80)
            empty_heart_left.display(screen)

            empty_heart_right.y_setter(button_y_start - 90)
            empty_heart_right.x_setter(screen_w/2 + 30)
            empty_heart_right.height_setter(80)
            empty_heart_right.width_setter(80)
            empty_heart_right.display(screen) 
        return

#background music
# - removed music as need audio forwarding to work
#pygame.mixer.music.load(find_asset("background_music.mp3"))  # use your music file path
#pygame.mixer.music.set_volume(0.5)  # set volume (0.0 to 1.0)
#pygame.mixer.music.play(-1)  # play the music in a loop
music_paused = False

state = "startup_screen"
previous_state = state
#game loop
while True:
    bg_image = scale_bg_image()
    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            bg_image = scale_bg_image()
            screen_width = screen.get_width()
            screen_height = screen.get_height()
            logoRecttext.center = (screen_width/2, screen_height/5)
            if state == "settings_screen" and background_copy is not None:
                background_copy = pygame.transform.scale(background_copy, screen.get_size())
            draw()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            settings_button.is_clicked(mouse_pos[0], mouse_pos[1])
            if state == "settings_screen":
                restart_button_settings.is_clicked(mouse_pos[0], mouse_pos[1])
                togglesound_button_settings.is_clicked(mouse_pos[0], mouse_pos[1])
                home_button_settings.is_clicked(mouse_pos[0], mouse_pos[1])
                exit_game_button_settings.is_clicked(mouse_pos[0], mouse_pos[1])
                exit_settings_button.is_clicked(mouse_pos[0], mouse_pos[1])
            elif state == "startup_screen":
                infinite_button.is_clicked(mouse_pos[0], mouse_pos[1])
                timed_button.is_clicked(mouse_pos[0], mouse_pos[1])
            elif state == "gameover":
                restart_button_gameover.is_clicked(mouse_pos[0], mouse_pos[1])
                continueplaying_button_gameover.is_clicked(mouse_pos[0], mouse_pos[1])
                home_button_gameover.is_clicked(mouse_pos[0], mouse_pos[1])
            if state == "infinite_gamemode" or state == "timed_gamemode":
                for piece in active_blocks:
                    piece.on_mouse_down(mouse_pos[0], mouse_pos[1])
        elif event.type == pygame.MOUSEBUTTONUP:
            if state == "infinite_gamemode" or state == "timed_gamemode":
                for piece in active_blocks:
                    piece.on_mouse_up()
                    if grid_bounds and piece.is_dragged == False:
                        check_and_snap_block(piece, grid_bounds)
        elif event.type == pygame.MOUSEMOTION:
            if state == "infinite_gamemode" or state == "timed_gamemode":
                mouse_pos = pygame.mouse.get_pos()
                for piece in active_blocks:
                    piece.on_mouse_motion(mouse_pos[0], mouse_pos[1])


    pygame.display.update()

