# Setup
import os
env = Environment()

# Tools
def walk_subdirs(path_dir) :  
    list = [name for name in os.listdir(path_dir) if os.path.isdir(os.path.join(path_dir, name)) and name[0] != '.']
    list.sort()
    return list

# Libraries
env.Append(CPPPATH = ['/usr/include/python2.7/'])
env.Append(LIBS = ['SDL', 'pthread', 'm', 'dl', 'SDL_image', 'SDL_ttf', 'SDL_mixer', 'freetype', 'z', 'bz2', 'GL', 'GLU', 'python2.7', 'boost_python', 'boost_filesystem', 'boost_system'])

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

# Build executable
object_list = env.Object(source = sources)
main_executable = env.Program(target = os.path.join(out_dir, 'pixelpics'), source = object_list)

Default(main_executable)

