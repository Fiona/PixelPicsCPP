# Setup
import sys, os, shutil
import glob as pyglob
from build_tools import walk_subdirs, create_logic_dat, clear_distribution_directory, create_distribution_directories_and_copy_libs, unwanted_sfx, unwanted_gfx
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
    for x in unwanted_sfx:
        os.remove(os.path.join("demo", "sfx", x))

    # remove unwanted graphics
    for x in unwanted_gfx:
        os.remove(os.path.join("demo", "gfx", x))
