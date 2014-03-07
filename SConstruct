# Setup
import os, zipfile, shutil, compileall
import glob as pyglob
env = Environment()

# Tools
def walk_subdirs(path_dir):
    list = [name for name in os.listdir(path_dir) if os.path.isdir(os.path.join(path_dir, name)) and name[0] != '.']
    list.sort()
    return list


# Libraries
env.Append(CPPPATH = ['/usr/include/python2.7/'])
env.Append(LIBS = [
                'SDL', 'pthread', 'm', 'dl', 'SDL_image', 'SDL_ttf', 'SDL_mixer', 'freetype', 'bz2', 'GL', 'GLU', 'python2.7',
                #'bboost_python', 'boost_filesystem', 'boost_system'
                File('/usr/lib/libboost_python.a'), File('/usr/lib/libboost_filesystem.a'), File('/usr/lib/libboost_system.a'), File('/usr/lib/libz.a')
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
   out_dir = os.path.join('dist', 'bin')

# Build executable
object_list = env.Object(source = sources)
main_executable = env.Program(
                target = os.path.join(out_dir, 'pixelpics'),
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

   # force recompilation of python files
   compileall.compile_dir("logic")

   # get together directories and files for logic.dat
   logic_subdirs = walk_subdirs("logic")
   os.chdir("logic")
   logic_sources = pyglob.glob('*.pyc')
   for subdir in logic_subdirs:
       logic_sources += pyglob.glob(os.path.join(subdir, "*.pyc"))

   # build logic.dat
   zf = zipfile.ZipFile("../dist/logic.dat", "w")
   for x in logic_subdirs:
       zf.write(x)
   for x in logic_sources:
       zf.write(x)
   zf.close()

   os.chdir("..")

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
   print "Manually CD to 'dist' and execute '../cpld.sh bin/pixelpics libs' to collate dynamic libraries"
