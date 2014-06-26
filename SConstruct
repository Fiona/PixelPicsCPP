# Setup
import sys, os, zipfile, shutil, compileall
import glob as pyglob
from build_tools import walk_subdirs, create_logic_dat
env = Environment()

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

debug = ARGUMENTS.get('debug', 0)
if int(debug):
   out_dir = 'debug'
   env.Append(CCFLAGS = '-g')
   env.Append(CPPDEFINES=['DEBUG'])
else:
   env.Append(CCFLAGS = '-O')

# Output to dist directory if necessary
dist = ARGUMENTS.get('dist', 0)
if int(dist):
   if sys.maxsize > 2**32:
       out_dir = os.path.join('dist', 'bin', 'x86_64')
   else:
       out_dir = os.path.join('dist', 'bin', 'i386')

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
   # create dist dir
   if not os.path.isdir("dist"): os.mkdir("dist")

   # destroy everything in there first
   for file in ["logic.dat", "pixelpics"]:
      if os.path.isfile(os.path.join("dist", file)):
         os.remove(os.path.join("dist", file))
   for dir in ["sfx", "music", "gfx", "fnt", "packs", "python27", "libs"]:
      if os.path.isdir(os.path.join("dist", dir)):
         shutil.rmtree(os.path.join("dist", dir))

   # Generate logic.dat file of pyc files
   create_logic_dat()

   # copy all packs
   os.mkdir(os.path.join("dist", "packs"))
   pack_dirs = ["0001", "0002","0003", "0004", "0005", "0006", "0007", "0008", "0009", "0010", "last"]
   for dir in pack_dirs:
       shutil.copytree(os.path.join("packs", dir), os.path.join("dist", "packs", dir))

   # music, sfx, fonts and gfx
   for dir in ["music", "sfx", "fnt", "gfx"]:
      shutil.copytree(os.path.join(dir), os.path.join("dist", dir))

   # copy standard library
   os.mkdir(os.path.join("dist", "python27"))
   shutil.copy("python27.zip", os.path.join("dist", "python27", "python27.zip"))

   # copy std library .so files
   for item in os.listdir(os.path.join("python27", "lib-dynload")):
       shutil.copy2(os.path.join("python27", "lib-dynload", item), os.path.join("dist", "python27", item))

   # copy bash script, make it executable, tell user to collate libs
   shutil.copy("pixelpics.sh", os.path.join("dist", "pixelpics"))
   os.system("chmod +x dist/pixelpics")
   os.mkdir(os.path.join("dist", "libs"))
   os.mkdir(os.path.join("dist", "libs" , "i386"))
   os.mkdir(os.path.join("dist", "libs" , "x86_64"))
   if sys.maxsize > 2**32:
      print "Manually CD to 'dist' and execute '../cpld.sh bin/x86_64/pixelpics libs/x86_64' to collate dynamic libraries"
   else:
      print "Manually CD to 'dist' and execute '../cpld.sh bin/i386/pixelpics libs/i386' to collate dynamic libraries"
