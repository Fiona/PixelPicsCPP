# Setup
import sys, os, shutil
import glob as pyglob
from build_tools import walk_subdirs, create_logic_dat, clear_distribution_directory, create_distribution_directories_and_copy_libs
env = Environment()

# Figure out architecture
if sys.maxsize > 2**32:
    arch = 64
else:
    arch = 32

# Bin name
exe_name = "pixelpics"

# Libraries
env.Append(CPPPATH = ['/usr/include/python2.7/'])
env.Append(LIBS = [
                'SDL', 'pthread', 'm', 'dl', 'SDL_image', 'SDL_ttf', 'SDL_mixer', 'freetype', 'bz2', 'GL', 'GLU', 'python2.7', "z",
                #'bboost_python', 'boost_filesystem', 'boost_system'
                File('/usr/lib/libboost_python.a'), File('/usr/lib/libboost_filesystem.a'), File('/usr/lib/libboost_system.a')
                #, File('/usr/lib/libz.a')
                ]
                )

# List of sources
sources = Glob('*.cpp')

# Switch to debug
out_dir = 'release'

defines = []

debug = ARGUMENTS.get('debug', 0)
if int(debug):
    defines.append("DEBUG")
    out_dir = 'debug'
    env.Append(CCFLAGS = '-g')
else:
    env.Append(CCFLAGS = '-O')

# Output to dist directory if necessary
dist = ARGUMENTS.get('dist', 0)
if int(dist):
   if arch == 64:
       out_dir = os.path.join('dist', 'bin', 'x86_64')
   else:
       out_dir = os.path.join('dist', 'bin', 'i386')

# Demo 
demo = ARGUMENTS.get('demo', 0)
if int(demo):
   if arch == 64:
       out_dir = os.path.join('demo', 'bin', 'x86_64')
   else:
       out_dir = os.path.join('demo', 'bin', 'i386')
   defines.append("DEMO")

env.Append(CPPDEFINES=defines)

# Build executable
object_list = env.Object(source = sources)
main_executable = env.Program(
                target = os.path.join(out_dir, exe_name),
                source = object_list,
                LINKFLAGS = "-Xlinker -export-dynamic"
                )

Default(main_executable)


# Collate everything for distribution if required
if int(dist):
    clear_distribution_directory()    
    create_logic_dat()
    create_distribution_directories_and_copy_libs(arch)

    # copy all packs
    os.mkdir(os.path.join("dist", "packs"))
    pack_dirs = ["0001", "0002","0003", "0004", "0005", "0006", "0007", "0008", "0009", "0010", "last"]
    for dir in pack_dirs:
        shutil.copytree(os.path.join("packs", dir), os.path.join("dist", "packs", dir))

    # music, sfx, fonts and gfx
    for dir in ["music", "sfx", "fnt", "gfx"]:
        shutil.copytree(os.path.join(dir), os.path.join("dist", dir))

# Similar for demo as with dist with a few changes
if int(demo):
    clear_distribution_directory('demo')
    create_logic_dat('demo', skip_files = ['gui/sharing.pyc', 'gui/designer.pyc'])
    create_distribution_directories_and_copy_libs(arch, 'demo')

    # copy some packs
    os.mkdir(os.path.join("demo", "packs"))
    pack_dirs = ["0001", "0002","0003", "0004"]
    for dir in pack_dirs:
        shutil.copytree(os.path.join("packs", dir), os.path.join("demo", "packs", dir))

    # Remove numbers we don't want
    os.chdir(os.path.join("demo", "packs"))
    for _dir in ["0003", "0004"]:
        os.chdir(_dir)
        for filename in  pyglob.glob("*.puz"):
            num = filename[:filename.find(".")]
            if num.isdigit() and int(num) > 10:
                os.remove(filename)
        os.chdir("..")
    os.chdir(os.path.join("..", ".."))

    # music, sfx, fonts and gfx
    for dir in ["music", "sfx", "fnt", "gfx"]:
        shutil.copytree(os.path.join(dir), os.path.join("demo", dir))

    # remove unwanted music
    os.remove(os.path.join("demo", "music", "editor.ogg"))

    # remove unwanted sounds
    unwanted_sfx = [
        'firework.wav',
        'firework2.wav',
        'firework3.wav',
        'pipette.wav',
        'unlock.wav',
        'new_category.wav',
        'catmode-empty_square.wav',
        'catmode-failure.wav',
        'catmode-fill_square1.wav',
        'catmode-fill_square2.wav',
        'catmode-fill_square3.wav',
        'catmode-fill_square4.wav',
        'catmode-fill_square5.wav',
        'catmode-success.wav'
        ]
    for x in unwanted_sfx:
        os.remove(os.path.join("demo", "sfx", x))

    # remove unwanted graphics
    unwanted_gfx = [
        'background_designer.png',
        'background_present.png',
        'button_designer_back.png',
        'button_designer_copy.png',
        'button_designer_create.png',
        'button_designer_delete.png',
        'button_designer_edit.png',
        'button_designer_fill.png',
        'button_designer_help.png',
        'button_designer_move_down.png',
        'button_designer_move_up.png',
        'button_designer_name.png',
        'button_designer_paint.png',
        'button_designer_puzzle.png',
        'button_designer_redo.png',
        'button_designer_save.png',
        'button_designer_size.png',
        'button_designer_test.png',
        'button_designer_undo.png',
        'button_sharing_delete.png',
        'button_sharing_download.png',
        'button_sharing_next.png',
        'button_sharing_play.png',
        'button_sharing_prev.png',
        'button_sharing_tab_downloaded.png',
        'button_sharing_tab_my_puzzles.png',
        'button_sharing_tab_newest.png',
        'button_sharing_tab_top.png',
        'button_sharing_tab_top_week.png',
        'button_sharing_upload.png',
        'designer_throbber.png',
        'palette_cursor.png',
        'puzzle_cell_black_designer.png',
        'reward_star.png',
        'title_firework.png',
        'sharing_rating_stars.png',
        'verify_status.png',
        ]
    for x in unwanted_gfx:
        os.remove(os.path.join("demo", "gfx", x))
