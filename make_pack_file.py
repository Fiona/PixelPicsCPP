import argparse, glob, os, pickle, sys, uuid

class fakecore(object):
    pass
sys.modules["core"] = fakecore

sys.path.append(os.path.join(os.getcwd(), "logic"))
from puzzle import Pack

AUTHOR_ID = "f2494e4b-8eff-4899-ae03-888fe9b7a94d"
AUTHOR_NAME = "Stompy Blondie"
PACK_NAME = "Puzzles"
FREEMODE = False


# ----------------------------------------



def create_pack_file_for(path):
    os.chdir(path)
    puzzle_files = sorted(glob.glob("*.puz"));
    
    if len(puzzle_files) == 0:
        print "no puzzle files there"
        return
    
    if os.path.exists("pack.dat"):
        os.rename("pack.dat", "old.pack.dat")
        print "renamed current pack.dat file to old.pack.dat"

    print "generating new pack object"
    new_pack = Pack()
    new_pack.uuid = str(uuid.uuid4())
    new_pack.author_id = AUTHOR_ID
    new_pack.author_name = AUTHOR_NAME
    new_pack.name = PACK_NAME
    new_pack.freemode = False
    new_pack.puzzles = {}
    new_pack.order = []
        
    for puzzle_filename in puzzle_files:
        print "opening puzzle - ", puzzle_filename
        f = open(puzzle_filename, "rb")
        puzzle = pickle.load(f)
        f.close()
        print "adding puzzle to pack - ", puzzle_filename
        new_pack.puzzles[puzzle_filename] = [puzzle.name, puzzle.width, puzzle.height]
        new_pack.order.append(puzzle_filename)

    print "outputting new pack file to pack.dat"
    f = open("pack.dat", "wb")
    pickle.dump(new_pack, f)
    f.close()             

    print "Done!"
    


# ----------------------------------------



parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('path', metavar='P', type=str, nargs=1,
                   help='Full path to the location of the pack to create a file for')

args = parser.parse_args()
create_pack_file_for(args.path[0])
