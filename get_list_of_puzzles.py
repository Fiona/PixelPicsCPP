import argparse, glob, os, pickle, sys, uuid

class fakecore(object):
    pass
sys.modules["core"] = fakecore

sys.path.append(os.path.join(os.getcwd(), "logic"))
from puzzle import Pack


def get_names_of_puzzles_in(path):
    os.chdir(path)
    puzzle_files = glob.glob("*.puz");
    
    if len(puzzle_files) == 0:
        print "no puzzle files there"
        return
    
    for puzzle_filename in puzzle_files:
        f = open(puzzle_filename, "rb")
        puzzle = pickle.load(f)
        f.close()
        print puzzle_filename + " - " + puzzle.name + " - " + str(puzzle.width) + "x" + str(puzzle.height)

    f = open("pack.dat", "rb")
    pack = pickle.load(f)
    f.close()
    print pack.name
    print pack.uuid


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('path', metavar='P', type=str, nargs=1,
                   help='Full path to the location of the directory of puzzles to get names of')

args = parser.parse_args()
get_names_of_puzzles_in(args.path[0])
