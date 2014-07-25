import os, shutil, glob
from build_tools import walk_subdirs, create_logic_dat, clear_distribution_directory, create_distribution_directories_and_copy_libs, unwanted_sfx, unwanted_gfx

print("Clear directory 'dist'")
clear_distribution_directory('dist')

print("Create logic.dat")
create_logic_dat()

print("Plopping in executable")
shutil.copy(os.path.join("visualstudio", "Release", "pixelpics.exe"), os.path.join('dist', "PixelPics.exe"))

# copy some packs
print("Copying packs")
os.mkdir(os.path.join("dist", "packs"))
pack_dirs = ["0001", "0002","0003", "0004", "0005", "0006", "0007", "0008", "0009", "0010", "last"]
for dir in pack_dirs:
    shutil.copytree(os.path.join("packs", dir), os.path.join("dist", "packs", dir))

# music, sfx, fonts and gfx
print("Copy over music, sfx, fonts, gfx")
for dir in ["music", "sfx", "fnt", "gfx"]:
    shutil.copytree(os.path.join(dir), os.path.join("dist", dir))


