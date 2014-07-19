import compileall, glob, zipfile, os, shutil, sys

def walk_subdirs(path_dir):
    list = [name for name in os.listdir(path_dir) if os.path.isdir(os.path.join(path_dir, name)) and name[0] != '.']
    list.sort()
    return list

def create_logic_dat(path = 'dist', skip_files = []):
    # force recompilation of python files
    compileall.compile_dir("logic")
    # get together directories and files for logic.dat
    logic_subdirs = walk_subdirs("logic")
    os.chdir("logic")
    logic_sources = glob.glob('*.pyc')
    for subdir in logic_subdirs:
        file_list = glob.glob(os.path.join(subdir, "*.pyc")) 
        logic_sources += file_list
    for x in skip_files:
        logic_sources.remove(x)
    # build logic.dat
    zf = zipfile.ZipFile(os.path.join("..", path, "logic.dat"), "w")
    for x in logic_subdirs:
        zf.write(x)
    for x in logic_sources:
        zf.write(x)
    zf.close()

    os.chdir("..")


def clear_distribution_directory(path = 'dist'):
    # create dist dir
   if not os.path.isdir(path): os.mkdir(path)
   # destroy everything in there first
   for file in ["logic.dat", "pixelpics"]:
      if os.path.isfile(os.path.join(path, file)):
         os.remove(os.path.join(path, file))
   for dir in ["sfx", "music", "gfx", "fnt", "packs", "python27", "libs"]:
      if os.path.isdir(os.path.join(path, dir)):
         shutil.rmtree(os.path.join(path, dir))


def create_distribution_directories_and_copy_libs(arch, path = 'dist'):
    # create python library directories
    os.mkdir(os.path.join(path, "python27"))
    os.mkdir(os.path.join(path, "python27", "i386"))
    os.mkdir(os.path.join(path, "python27", "x86_64"))
    # copy standard library
    shutil.copy("python27.zip", os.path.join(path, "python27", "python27.zip"))
    # copy std library .so files
    pylib_dir = 'x86_64' if arch == 64 else 'i386'
    for item in os.listdir(os.path.join("python27", "lib-dynload")):
        shutil.copy2(os.path.join("python27", "lib-dynload", item), os.path.join(path, "python27", pylib_dir, item))
    # copy bash script, make it executable, tell user to collate libs
    shutil.copy("pixelpics.sh", os.path.join(path, "pixelpics"))
    os.system("chmod +x " + path + "/pixelpics")
    os.mkdir(os.path.join(path, "libs"))
    os.mkdir(os.path.join(path, "libs" , "i386"))
    os.mkdir(os.path.join(path, "libs" , "x86_64"))
    print "Manually CD to '" + path + "' and execute '../cpld.sh bin/" + pylib_dir + "/pixelpics libs/" + pylib_dir + "' to collate dynamic libraries"
