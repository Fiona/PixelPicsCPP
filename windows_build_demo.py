import os, shutil, glob
from build_tools import walk_subdirs, create_logic_dat, clear_distribution_directory, create_distribution_directories_and_copy_libs, unwanted_sfx, unwanted_gfx

print("Clear directory 'demo'")
clear_distribution_directory('demo')

print("Create logic.dat")
create_logic_dat('demo', skip_files = [os.path.join('gui','sharing.pyc'), os.path.join('gui','designer.pyc')])

print("Plopping in executable")
shutil.copy(os.path.join("visualstudio", "Demo", "pixelpics.exe"), os.path.join('demo', "PixelPics.exe"))

# copy some packs
print("Copying packs")
os.mkdir(os.path.join("demo", "packs"))
pack_dirs = ["0001", "0002","0003", "0004"]
for dir in pack_dirs:
    shutil.copytree(os.path.join("packs", dir), os.path.join("demo", "packs", dir))

# Remove numbers we don't want
print("Delete puzzles we don't want")
os.chdir(os.path.join("demo", "packs"))
for _dir in ["0003", "0004"]:
    os.chdir(_dir)
    for filename in  glob.glob("*.puz"):
        num = filename[:filename.find(".")]
        if num.isdigit() and int(num) > 10:
            os.remove(filename)
    os.chdir("..")
os.chdir(os.path.join("..", ".."))

# music, sfx, fonts and gfx
print("Copy over music, sfx, fonts, gfx")
for dir in ["music", "sfx", "fnt", "gfx"]:
    shutil.copytree(os.path.join(dir), os.path.join("demo", dir))


# remove unwanted music
print("Remove unwanted music")
os.remove(os.path.join("demo", "music", "editor.ogg"))

# remove unwanted sounds
print("Remove unwanted sounds")
for x in unwanted_sfx:
    os.remove(os.path.join("demo", "sfx", x))

    # remove unwanted graphics
print("Remove unwanted graphics")
for x in unwanted_gfx:
    os.remove(os.path.join("demo", "gfx", x))
