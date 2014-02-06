"""
PixelPics - Nonogram game
Copyright (c) 2014 Stompy Blondie Games http://stompyblondie.com
"""

# Python imports
import os, sys, string, glob, uuid
import cPickle as pickle

# Game engine imports
from core import *

# Game imports
from consts import *



class Pack(object):
    name = "Test Pack"
    """
    Dictionary with keys as filenames. Values are tuples containing puzzle info.
    (puzzle name, width, height)
    """
    puzzles = {"001.puz" : ["Puzzle", 10, 10]}
    """
    This is used to tie authors to their puzzles. It's really cheesy and cheap.
    There's a text file in the packs directory that simply contains a uuid. Only packs
    that match this id will be editable.
    Used in sharing to attempt to stop users uploading a pack multiple times. Again, really shitty.
    """
    author_id = ""
    """
    Small bit of text says who the author is, defined by pack creator.
    """
    author_name = ""
    """
    Cheap way to tell if a pack has been shared. A quick check is done server-side in addition.
    """
    shared = False
    """
    Random ID also to determine if packs have been saved server-size. Like author ID, it's pretty shitty too.
    """
    uuid = ""
    """
    Order of puzzle filenames as they should appear to the player.
    """
    order = ["001.puz"]
    """
    If the puzzles in this pack should be played in freemode or not.
    """
    freemode = False



class Puzzle(object):
    name = "Puzzle"
    width = 10
    height = 10
    cells = [
        [(True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1))],
        [(True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1))],
        [(True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1))],
        [(True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1))],
        [(True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1))],
        [(True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1))],
        [(True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1))],
        [(True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1))],
        [(True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1))],
        [(True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1)), (True, (0,0,1))],
        ]
    row_numbers = [(10), (10), (10), (10), (10), (10), (10), (10), (10), (10)]
    column_numbers = [(10), (10), (10), (10), (10), (10), (10), (10), (10), (10)]
    background = 'blue'



class Puzzle_save(object):
    pack_dir = ""
    puzzle_filename = ""
    puzzle_state = []
    timer = 0
    lives = 0
    


class Puzzle_manager(object):

    current_puzzle_file = "001"
    current_puzzle_pack = "001"

    current_puzzle = None
    current_pack = None

    current_puzzle_state = []
    current_puzzle_row_completion = []
    current_puzzle_column_completion = []

    packs = []
    pack_directory_list = []
    pack_uuids = []

    game_packs = {}
    game_pack_directory_list = []

    load_puzzle_state_from = ""

    user_created_puzzles = False

    starred_packs = []
    all_main_packs_starred = False
    last_pack_unlocked = False
    

    def __init__(self, game):
        self.game = game
        self.load_packs()
        self.load_packs(user_created = False)
        self.check_which_packs_starred()
        self.check_if_last_pack_unlocked()


    def load_packs(self, user_created = True):
        if user_created:
            self.packs = []
            self.pack_directory_list = []
            self.pack_uuids = []            
            packs = self.packs
            pack_directory_list = self.pack_directory_list
            pack_dir = self.game.core.path_user_pack_directory
        else:
            self.game_packs = {}
            self.game_pack_directory_list = []
            packs = self.game_packs
            pack_directory_list = self.game_pack_directory_list
            pack_dir = self.game.core.path_game_pack_directory
            
        # Get all valid pack directories
        cur_dir = os.getcwd()
        os.chdir(pack_dir)
        directories = glob.glob("*")
        os.chdir(cur_dir)
        
        for dir in directories:
            if os.path.isdir(os.path.join(pack_dir, dir)) and os.path.exists(os.path.join(pack_dir, dir, FILE_PACK_INFO_FILE)):
                pack_directory_list.append(dir)

        # Load all packs
        for pack_dir_name in pack_directory_list:
            f = open(os.path.join(pack_dir, pack_dir_name, FILE_PACK_INFO_FILE), "r")
            pack = pickle.load(f)
            f.close()
            if user_created:
                packs.append(pack)
                self.pack_uuids.append(pack.uuid)
            else:
                packs[pack_dir_name] = pack
                

    def check_which_packs_starred(self):
        self.starred_packs = []

        game_packs = []
        for p in self.game_packs:
            game_packs.append(self.game_packs[p])
            
        for pack in game_packs + self.packs:
            starred = True
            if pack.uuid in self.game.player.puzzle_scores:
                for puzzle_filename in pack.puzzles:
                    if puzzle_filename in self.game.player.puzzle_scores[pack.uuid]:
                        if pack.freemode:
                            seconds = int(self.game.player.puzzle_scores[pack.uuid][puzzle_filename][0] / 60)
                            if int(seconds / 60) > 60:
                                starred = False
                                break
                        else:
                            if self.game.player.puzzle_scores[pack.uuid][puzzle_filename][1] < 4:
                                starred = False
                                break
                    else:
                        starred = False
                        break
            else:
                starred = False

            if starred:
                self.starred_packs.append(pack.uuid)

        self.all_main_packs_starred = True
        for pack in game_packs:
            if not pack.uuid in self.starred_packs:
                self.all_main_packs_starred = False
                break
                

    def check_if_last_pack_unlocked(self):
        self.last_pack_unlocked = True
        for p in self.game_packs:
            # skip last pack and tutorial because they are not required for
            # unlocking the final pack.
            if p in ['last', '0001']:
                continue
            if not self.game_packs[p].uuid in self.game.player.cleared_categories:
                self.last_pack_unlocked = False
                break


    def load_pack(self, pack_dir, user_created = True):
        try:
            main_dir = self.game.core.path_user_pack_directory if user_created else self.game.core.path_game_pack_directory
            f = open(os.path.join(main_dir, pack_dir, FILE_PACK_INFO_FILE), "r")
            self.current_pack = pickle.load(f)
            self.game.freemode = self.current_pack.freemode
            self.current_puzzle_pack = pack_dir
            f.close()
        except IOError as e:
            raise e


    def load_puzzle(self, pack_dir, puzzle_filename, set_state = False, user_created = True):
        try:
            self.load_pack(pack_dir, user_created = user_created)

            main_dir = self.game.core.path_user_pack_directory if user_created else self.game.core.path_game_pack_directory
            
            f = open(os.path.join(main_dir, pack_dir, puzzle_filename), "r")
            puzzle = pickle.load(f)
            self.current_puzzle = puzzle
            self.current_puzzle_file = puzzle_filename

            self.current_puzzle_state = []
            for y in range(self.current_puzzle.height):
                self.current_puzzle_state.append([])
                for x in range(self.current_puzzle.width):
                    if set_state and self.current_puzzle.cells[y][x][0]:
                        self.current_puzzle_state[y].append(True)
                    else:
                        self.current_puzzle_state[y].append(None)

            self.current_puzzle_row_completion = [False] * self.current_puzzle.height
            self.current_puzzle_column_completion = [False] * self.current_puzzle.width

            for y in range(self.current_puzzle.height):
                self.check_row_completion(y)
            for x in range(self.current_puzzle.width):
                self.check_column_completion(x)

            f.close()
        except IOError as e:
            raise e

        if self.load_puzzle_state_from:
            self.load_puzzle_state(self.load_puzzle_state_from)
            self.load_puzzle_state_from = ""


    def delete_user_created_pack(self, pack_dir):
        try:
            if not (os.path.isdir(os.path.join(self.game.core.path_user_pack_directory, pack_dir)) and os.path.exists(os.path.join(self.game.core.path_user_pack_directory, pack_dir, FILE_PACK_INFO_FILE))):
                return

            # Kill the info file
            os.remove(os.path.join(self.game.core.path_user_pack_directory, pack_dir, FILE_PACK_INFO_FILE))

            # Kill all puzzles
            cur_dir = os.getcwd()
            os.chdir(os.path.join(self.game.core.path_user_pack_directory, pack_dir))
            puzzles = glob.glob("*" + FILE_PUZZLE_EXTENSION)

            for puzzle_file in puzzles:
                if not os.path.isdir(os.path.join(self.game.core.path_user_pack_directory, pack_dir, puzzle_file)):
                    os.remove(os.path.join(self.game.core.path_user_pack_directory, pack_dir, puzzle_file))

            os.chdir(cur_dir)

            # Remove directory if it's now empty. If not just leave it, without the info file it wont be read anyway.
            if len(os.listdir(os.path.join(self.game.core.path_user_pack_directory, pack_dir))) == 0:
                os.rmdir(os.path.join(self.game.core.path_user_pack_directory, pack_dir))

            self.load_packs()
        except IOError as e:
            raise e


    def extract_pack_uuid(self, pack_dir, user_created = True):
        try:
            main_dir = self.game.core.path_user_pack_directory if user_created else self.game.core.path_game_pack_directory
            f = open(os.path.join(main_dir, pack_dir, FILE_PACK_INFO_FILE), "r")
            pack = pickle.load(f)
            uuid = pack.uuid
            f.close()
        except IOError as e:
            raise e

        return uuid


    def reset_puzzle_state(self):
        for y in range(len(self.current_puzzle_state)):
            for x in range(len(self.current_puzzle_state[y])):
                self.current_puzzle_state[y][x] = None
        

    def set_puzzle_cell(self, puzzle, x, y, value, colour = [0.0, 0.0, 1.0]):
        puzzle.cells[y][x] = (value, colour)

        
    def set_cell_colours_to_values(self, puzzle):
        for y in range(puzzle.height):
            for x in range(puzzle.width):
                if puzzle.cells[y][x][0]:
                    puzzle.cells[y][x] = (True, [0.0, 0.0, 0.0])
                else:
                    puzzle.cells[y][x] = (False, [0.0, 0.0, 1.0])
        

    def work_out_puzzle_hint_numbers(self, puzzle):
        for y in range(puzzle.height):
            puzzle.row_numbers[y] = self.work_out_single_puzzle_hint_numbers(puzzle.cells[y])
        for x in range(puzzle.width):
            puzzle.column_numbers[x] = self.work_out_single_puzzle_hint_numbers(self.get_column_cells(puzzle, x))


    def work_out_single_puzzle_hint_numbers(self, cells):
        hint_numbers = []
        current_count = 0
        for cell in cells:
            if cell[0]:
                current_count += 1
            elif current_count:
                hint_numbers.append(current_count)
                current_count = 0
        if current_count:
            hint_numbers.append(current_count)
        if len(hint_numbers) == 0:
            hint_numbers = [0]
        return tuple(hint_numbers)


    def get_column_cells(self, puzzle, col):
        cells = []
        for y in range(puzzle.height):
            cells.append(puzzle.cells[y][col])
        return cells


    def check_row_completion(self, row_index):
        found_cell_numbers = []
        current_count = 0
        
        for col, cell in enumerate(self.current_puzzle.cells[row_index]):
            if self.current_puzzle_state[row_index][col]:
                current_count += 1
            elif current_count:
                found_cell_numbers.append(current_count)
                current_count = 0
        if current_count:
            found_cell_numbers.append(current_count)

        if len(found_cell_numbers) == 0:
            found_cell_numbers = [0]

        if tuple(found_cell_numbers) == self.current_puzzle.row_numbers[row_index]:
            self.current_puzzle_row_completion[row_index] = True
        else:
            self.current_puzzle_row_completion[row_index] = False
        
        return self.current_puzzle_row_completion[row_index]

        
    def check_column_completion(self, column_index):
        found_cell_numbers = []
        current_count = 0
        column_cells = self.get_column_cells(self.current_puzzle, column_index)
        
        for row, cell in enumerate(column_cells):
            if self.current_puzzle_state[row][column_index]:
                current_count += 1
            elif current_count:
                found_cell_numbers.append(current_count)
                current_count = 0
        if current_count:
            found_cell_numbers.append(current_count)

        if len(found_cell_numbers) == 0:
            found_cell_numbers = [0]

        if tuple(found_cell_numbers) == self.current_puzzle.column_numbers[column_index]:
            self.current_puzzle_column_completion[column_index] = True
        else:
            self.current_puzzle_column_completion[column_index] = False
        
        return self.current_puzzle_column_completion[column_index]


    def is_current_puzzle_complete(self):
        if False in self.current_puzzle_row_completion or False in self.current_puzzle_column_completion:
            return False
        return True


    ############################################
    ## SAVE GAME STUFF
    ############################################


    def save_current_puzzle_state(self):
        # create save object
        save = Puzzle_save()

        # Plop save values in it
        save.pack_dir = self.current_puzzle_pack
        save.puzzle_filename = self.current_puzzle_file
        save.puzzle_state = self.current_puzzle_state
        save.timer = self.game.timer
        save.lives = self.game.lives

        # get filename we want
        save_filename = os.path.join(
            self.game.core.path_saves_user_directory if self.user_created_puzzles else self.game.core.path_saves_game_directory,
            self.current_puzzle_pack + "_" + self.current_puzzle_file + FILE_SAVES_EXTENSION
            )

        try:
            f = open(save_filename, "wb")
            pickle.dump(save, f)
            f.close()             
        except IOError as e:
            raise e



    def delete_current_puzzle_save(self):
        # get filename we want
        save_filename = os.path.join(
            self.game.core.path_saves_user_directory if self.user_created_puzzles else self.game.core.path_saves_game_directory,
            self.current_puzzle_pack + "_" + self.current_puzzle_file + FILE_SAVES_EXTENSION
            )

        if os.path.exists(save_filename):
            os.remove(save_filename)
            
        

    def load_puzzle_state(self, state_filename):
        try:
            if self.game.manager.user_created_puzzles:
                save_path = self.game.core.path_saves_user_directory
            else:
                save_path = self.game.core.path_saves_game_directory
            
            path = os.path.join(save_path, state_filename)
            f = open(path, "r")
            save = pickle.load(f)
            
            if save.pack_dir == self.current_puzzle_pack and save.puzzle_filename == self.current_puzzle_file:
                self.current_puzzle_state = save.puzzle_state
                self.game.lives = save.lives
                self.game.timer = save.timer

                for y in range(self.current_puzzle.height):
                    self.check_row_completion(y)
                for x in range(self.current_puzzle.width):
                    self.check_column_completion(x)
                
            f.close()

            os.remove(path)
        except IOError as e:
            raise e
        


    ############################################
    ## PACK MANAGEMENT
    ############################################


    def add_new_pack(self, pack_name, author, freemode):
        author = author.strip()
        pack_name = pack_name.strip()
        
        if pack_name == "":
             raise IOError("Please give your pack a name.")
        if author == "":
             raise IOError("Please supply your author name.")

        try:
            pack_directory_name = self.generate_unique_filename(self.game.core.path_user_pack_directory)
            os.mkdir(os.path.join(self.game.core.path_user_pack_directory, pack_directory_name))
        except IOError as e:
            raise e
         
        new_pack = Pack()
        new_pack.uuid = str(uuid.uuid4())
        new_pack.author_id = self.game.core.author_id
        new_pack.author_name = author
        new_pack.name = pack_name
        new_pack.freemode = freemode
        new_pack.puzzles = {}
        new_pack.order = []

        try:
            f = open(os.path.join(self.game.core.path_user_pack_directory, pack_directory_name, FILE_PACK_INFO_FILE), "wb")
            pickle.dump(new_pack, f)
            f.close()             
        except IOError as e:
            raise e

        self.load_packs()


    def edit_pack(self, pack_num, pack_name, author, freemode):
        author = author.strip()
        pack_name = pack_name.strip()
        
        if pack_name == "":
             raise IOError("Please give your pack a name.")
        if author == "":
             raise IOError("Please supply your author name.")

        self.packs[pack_num].name = pack_name
        self.packs[pack_num].author_name = author
        self.packs[pack_num].freemode = freemode

        try:
            f = open(os.path.join(self.game.core.path_user_pack_directory, self.pack_directory_list[pack_num], FILE_PACK_INFO_FILE), "wb")
            pickle.dump(self.packs[pack_num], f)
            f.close()             
        except IOError as e:
            raise e

        self.load_packs()


    def delete_pack(self, pack_num):
        dir = self.pack_directory_list[pack_num]
        
        if not (os.path.isdir(os.path.join(self.game.core.path_user_pack_directory, dir)) and os.path.exists(os.path.join(self.game.core.path_user_pack_directory, dir, FILE_PACK_INFO_FILE))):
            return

        # Kill the info file
        os.remove(os.path.join(self.game.core.path_user_pack_directory, dir, FILE_PACK_INFO_FILE))

        # Kill all puzzles
        cur_dir = os.getcwd()
        os.chdir(os.path.join(self.game.core.path_user_pack_directory, dir))
        puzzles = glob.glob("*" + FILE_PUZZLE_EXTENSION)

        for puzzle_file in puzzles:
            if not os.path.isdir(os.path.join(self.game.core.path_user_pack_directory, dir, puzzle_file)):
                os.remove(os.path.join(self.game.core.path_user_pack_directory, dir, puzzle_file))

        os.chdir(cur_dir)

        # Remove directory if it's now empty. If not just leave it, without the info file it wont be read anyway.
        if len(os.listdir(os.path.join(self.game.core.path_user_pack_directory, dir))) == 0:
            os.rmdir(os.path.join(self.game.core.path_user_pack_directory, dir))

        self.load_packs()

        
    def move_pack_puzzle_down(self, pack_directory, puzzle_filename):
        pack_num = self.pack_directory_list.index(pack_directory)
        current_index = self.packs[pack_num].order.index(puzzle_filename)
        if current_index == 0:
            return
        self.packs[pack_num].order.insert(
            current_index - 1,
            self.packs[pack_num].order.pop(current_index)
            )

        try:
            f = open(os.path.join(self.game.core.path_user_pack_directory, self.pack_directory_list[pack_num], FILE_PACK_INFO_FILE), "wb")
            pickle.dump(self.packs[pack_num], f)
            f.close()             
        except IOError as e:
            raise e

        self.load_packs()


    def move_pack_puzzle_up(self, pack_directory, puzzle_filename):
        pack_num = self.pack_directory_list.index(pack_directory)
        current_index = self.packs[pack_num].order.index(puzzle_filename)
        if current_index == len(self.packs[pack_num].order) - 1:
            return
        self.packs[pack_num].order.insert(
            current_index + 1,
            self.packs[pack_num].order.pop(current_index)
            )

        try:
            f = open(os.path.join(self.game.core.path_user_pack_directory, self.pack_directory_list[pack_num], FILE_PACK_INFO_FILE), "wb")
            pickle.dump(self.packs[pack_num], f)
            f.close()             
        except IOError as e:
            raise e

        self.load_packs()        


    def set_as_shared(self, pack_num):
        self.packs[pack_num].shared = True

        try:
            f = open(os.path.join(self.game.core.path_user_pack_directory, self.pack_directory_list[pack_num], FILE_PACK_INFO_FILE), "wb")
            pickle.dump(self.packs[pack_num], f)
            f.close()             
        except IOError as e:
            raise e

        self.load_packs()
    
        

    ############################################
    ## PUZZLE MANAGEMENT
    ############################################


    def add_new_puzzle(self, puzzle_name, pack_directory, width = 10, height = 10):
        puzzle_name = puzzle_name.strip()
        
        if puzzle_name == "":
             raise IOError("Please give your puzzle a name.")

        puzzle_filename = self.generate_unique_filename(os.path.join(self.game.core.path_user_pack_directory, pack_directory), extension = FILE_PUZZLE_EXTENSION)
        
        puzzle = Puzzle()
        puzzle.name = puzzle_name
        puzzle.width = width
        puzzle.height = height
        puzzle.cells = []
        for y in range(puzzle.height):
            puzzle.cells.append([])
            for x in range(puzzle.width):
                puzzle.cells[y].append((False, [0.0, 0.0, 1.0]))
        puzzle.row_numbers = [(0,)] * puzzle.height
        puzzle.column_numbers = [(0,)] * puzzle.width
        puzzle.background = "blue"

        try:
            f = open(os.path.join(self.game.core.path_user_pack_directory, pack_directory, puzzle_filename), "wb")
            pickle.dump(puzzle, f)
            f.close()             
        except IOError as e:
            raise e

        self.add_puzzle_to_pack(puzzle, puzzle_filename, pack_directory)


    def add_puzzle_to_pack(self, puzzle_object, puzzle_filename, pack_directory):
        try:
            f = open(os.path.join(self.game.core.path_user_pack_directory, pack_directory, FILE_PACK_INFO_FILE), "r")
            pack_object = pickle.load(f)
            f.close()
        except IOError:
            raise IOError("Can't load pack file.")

        if len(pack_object.puzzles) >= MAX_PUZZLES_PER_PACK:
            raise IOError("Can't have more than " + str(MAX_PUZZLES_PER_PACK) + " puzzles in a pack.")        

        pack_object.puzzles[puzzle_filename] = [puzzle_object.name, puzzle_object.width, puzzle_object.height]
        pack_object.order.append(puzzle_filename)
        
        try:
            f = open(os.path.join(self.game.core.path_user_pack_directory, pack_directory, FILE_PACK_INFO_FILE), "wb")
            pickle.dump(pack_object, f)
            f.close()             
        except IOError as e:
            raise e

        self.load_packs()        


    def edit_puzzle(self, pack_directory, puzzle_filename, puzzle_name):
        puzzle_name = puzzle_name.strip()
        
        if puzzle_name == "":
             raise IOError("Please give your puzzle a name.")

        try:
            f = open(os.path.join(self.game.core.path_user_pack_directory, pack_directory, puzzle_filename), "rb")
            puzzle = pickle.load(f)
            f.close()             

            puzzle.name = puzzle_name

            f = open(os.path.join(self.game.core.path_user_pack_directory, pack_directory, puzzle_filename), "wb")
            pickle.dump(puzzle, f)
            f.close()             
        except IOError as e:
            raise e

        try:
            f = open(os.path.join(self.game.core.path_user_pack_directory, pack_directory, FILE_PACK_INFO_FILE), "rb")
            pack_object = pickle.load(f)
            f.close()             

            pack_object.puzzles[puzzle_filename][0] = puzzle_name

            f = open(os.path.join(self.game.core.path_user_pack_directory, pack_directory, FILE_PACK_INFO_FILE), "wb")
            pickle.dump(pack_object, f)
            f.close()             
        except IOError as e:
            raise e

        self.load_packs()


    def delete_puzzle(self, pack_directory, puzzle_filename):
        if not (os.path.isdir(os.path.join(self.game.core.path_user_pack_directory, pack_directory)) and os.path.exists(os.path.join(self.game.core.path_user_pack_directory, pack_directory, puzzle_filename))):
            return

        # Kill the puzzle file
        os.remove(os.path.join(self.game.core.path_user_pack_directory, pack_directory, puzzle_filename))

        # Remove from pack info file
        try:
            f = open(os.path.join(self.game.core.path_user_pack_directory, pack_directory, FILE_PACK_INFO_FILE), "rb")
            pack_object = pickle.load(f)
            f.close()             

            del(pack_object.puzzles[puzzle_filename])
            pack_object.order.remove(puzzle_filename)
            
            f = open(os.path.join(self.game.core.path_user_pack_directory, pack_directory, FILE_PACK_INFO_FILE), "wb")
            pickle.dump(pack_object, f)
            f.close()             
        except IOError as e:
            raise e

        self.load_packs()


    def save_puzzle(self, pack_directory, puzzle_filename, puzzle_object):
        if not (os.path.isdir(os.path.join(self.game.core.path_user_pack_directory, pack_directory)) and os.path.exists(os.path.join(self.game.core.path_user_pack_directory, pack_directory, puzzle_filename))):
            return

        try:
            f = open(os.path.join(self.game.core.path_user_pack_directory, pack_directory, puzzle_filename), "wb")
            pickle.dump(puzzle_object, f)
            f.close()
        except IOError as e:
            raise e

        try:
            f = open(os.path.join(self.game.core.path_user_pack_directory, pack_directory, FILE_PACK_INFO_FILE), "rb")
            pack_object = pickle.load(f)
            f.close()             

            pack_object.puzzles[puzzle_filename] = [puzzle_object.name, puzzle_object.width, puzzle_object.height]

            f = open(os.path.join(self.game.core.path_user_pack_directory, pack_directory, FILE_PACK_INFO_FILE), "wb")
            pickle.dump(pack_object, f)
            f.close()             
        except IOError as e:
            raise e

        self.load_packs()


    def change_puzzle_object_size(self, puzzle, new_width, new_height):
        for y in range(new_height):
            if y >= puzzle.height: 
                puzzle.cells.append([(False, [0.0, 0.0, 1.0])] * new_width)
            for x in range(new_width):
                if x >= puzzle.width: 
                    puzzle.cells[y].append((False, [0.0, 0.0, 1.0]))
            puzzle.cells[y] = puzzle.cells[y][:new_width]
        puzzle.cells = puzzle.cells[:new_height]

        puzzle.width = new_width
        puzzle.height = new_height

        puzzle.row_numbers = [(0,)] * puzzle.height
        puzzle.column_numbers = [(0,)] * puzzle.width
        self.work_out_puzzle_hint_numbers(puzzle)            

    
    def change_current_puzzle_size(self, new_width, new_height):
        # Determine input is okay
        new_width = int(new_width)
        new_height = int(new_height)

        if new_width < MIN_PUZZLE_SIZE or new_height < MIN_PUZZLE_SIZE:
            raise Exception("Puzzles cannot be that small.")
        if new_width > MAX_PUZZLE_SIZE or new_height > MAX_PUZZLE_SIZE:
            raise Exception("Puzzles cannot be that large.")

        if new_width == self.current_puzzle.width and  new_height == self.current_puzzle.height:
            return

        for y in range(new_height):
            if y >= self.current_puzzle.height: 
                self.current_puzzle_state.append([None] * new_width)
            for x in range(new_width):
                if x >= self.current_puzzle.width: 
                    self.current_puzzle_state[y].append(None)
            self.current_puzzle_state[y] = self.current_puzzle_state[y][:new_width]
        self.current_puzzle_state = self.current_puzzle_state[:new_height]

        self.change_puzzle_object_size(self.current_puzzle, new_width, new_height)


    def change_current_puzzle_background(self, background):
        if not background in BACKGROUNDS:
            raise Exception("This background was not found.")
        self.current_puzzle.background = background
        

    def change_puzzle_size(self, pack_directory, puzzle_filename, new_width, new_height):
        # Determine input is okay
        new_width = int(new_width)
        new_height = int(new_height)

        if new_width < MIN_PUZZLE_SIZE or new_height < MIN_PUZZLE_SIZE:
            raise Exception("Puzzles cannot be that small.")
        if new_width > MAX_PUZZLE_SIZE or new_height > MAX_PUZZLE_SIZE:
            raise Exception("Puzzles cannot be that large.")
        
        try:
            # Get puzzle file
            f = open(os.path.join(self.game.core.path_user_pack_directory, pack_directory, puzzle_filename), "rb")
            puzzle = pickle.load(f)
            f.close()             

            # edit size
            if new_width == puzzle.width and  new_height == puzzle.height:
                return

            self.change_puzzle_object_size(puzzle, new_width, new_height)
            
            # dump out
            f = open(os.path.join(self.game.core.path_user_pack_directory, pack_directory, puzzle_filename), "wb")
            pickle.dump(puzzle, f)
            f.close()             
        except IOError as e:
            raise e

        try:
            # Open pack file
            f = open(os.path.join(self.game.core.path_user_pack_directory, pack_directory, FILE_PACK_INFO_FILE), "rb")
            pack_object = pickle.load(f)
            f.close()             

            # update pack puzzle info
            pack_object.puzzles[puzzle_filename][1] = new_width
            pack_object.puzzles[puzzle_filename][2] = new_height

            # Dump
            f = open(os.path.join(self.game.core.path_user_pack_directory, pack_directory, FILE_PACK_INFO_FILE), "wb")
            pickle.dump(pack_object, f)
            f.close()             
        except IOError as e:
            raise e

        self.load_packs()


    def generate_unique_filename(self, path, extension = ""):
        count = 1
        
        while True:
            filename = str(count).rjust(4, "0")            
            if not os.path.exists(os.path.join(path, filename + extension)):
                break
            count += 1

        return filename + extension
