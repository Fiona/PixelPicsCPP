import compileall, glob, zipfile, os

def walk_subdirs(path_dir):
    list = [name for name in os.listdir(path_dir) if os.path.isdir(os.path.join(path_dir, name)) and name[0] != '.']
    list.sort()
    return list

def create_logic_dat():
    # force recompilation of python files
    compileall.compile_dir("logic")

    # get together directories and files for logic.dat
    logic_subdirs = walk_subdirs("logic")
    os.chdir("logic")
    logic_sources = glob.glob('*.pyc')
    for subdir in logic_subdirs:
        logic_sources += glob.glob(os.path.join(subdir, "*.pyc"))
    
    # build logic.dat
    zf = zipfile.ZipFile(os.path.join("..", "dist", "logic.dat"), "w")
    for x in logic_subdirs:
        zf.write(x)
    for x in logic_sources:
        zf.write(x)
    zf.close()

    os.chdir("..")
