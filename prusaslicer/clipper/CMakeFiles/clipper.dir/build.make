# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.25

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/ryan/PrusaSlicer

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/ryan/PrusaSlicer/build

# Include any dependencies generated for this target.
include src/clipper/CMakeFiles/clipper.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include src/clipper/CMakeFiles/clipper.dir/compiler_depend.make

# Include the progress variables for this target.
include src/clipper/CMakeFiles/clipper.dir/progress.make

# Include the compile flags for this target's objects.
include src/clipper/CMakeFiles/clipper.dir/flags.make

src/clipper/CMakeFiles/clipper.dir/clipper_z.cpp.o: src/clipper/CMakeFiles/clipper.dir/flags.make
src/clipper/CMakeFiles/clipper.dir/clipper_z.cpp.o: /home/ryan/PrusaSlicer/src/clipper/clipper_z.cpp
src/clipper/CMakeFiles/clipper.dir/clipper_z.cpp.o: src/clipper/CMakeFiles/clipper.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/ryan/PrusaSlicer/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object src/clipper/CMakeFiles/clipper.dir/clipper_z.cpp.o"
	cd /home/ryan/PrusaSlicer/build/src/clipper && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT src/clipper/CMakeFiles/clipper.dir/clipper_z.cpp.o -MF CMakeFiles/clipper.dir/clipper_z.cpp.o.d -o CMakeFiles/clipper.dir/clipper_z.cpp.o -c /home/ryan/PrusaSlicer/src/clipper/clipper_z.cpp

src/clipper/CMakeFiles/clipper.dir/clipper_z.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/clipper.dir/clipper_z.cpp.i"
	cd /home/ryan/PrusaSlicer/build/src/clipper && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/ryan/PrusaSlicer/src/clipper/clipper_z.cpp > CMakeFiles/clipper.dir/clipper_z.cpp.i

src/clipper/CMakeFiles/clipper.dir/clipper_z.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/clipper.dir/clipper_z.cpp.s"
	cd /home/ryan/PrusaSlicer/build/src/clipper && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/ryan/PrusaSlicer/src/clipper/clipper_z.cpp -o CMakeFiles/clipper.dir/clipper_z.cpp.s

# Object files for target clipper
clipper_OBJECTS = \
"CMakeFiles/clipper.dir/clipper_z.cpp.o"

# External object files for target clipper
clipper_EXTERNAL_OBJECTS =

src/clipper/libclipper.a: src/clipper/CMakeFiles/clipper.dir/clipper_z.cpp.o
src/clipper/libclipper.a: src/clipper/CMakeFiles/clipper.dir/build.make
src/clipper/libclipper.a: src/clipper/CMakeFiles/clipper.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/ryan/PrusaSlicer/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX static library libclipper.a"
	cd /home/ryan/PrusaSlicer/build/src/clipper && $(CMAKE_COMMAND) -P CMakeFiles/clipper.dir/cmake_clean_target.cmake
	cd /home/ryan/PrusaSlicer/build/src/clipper && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/clipper.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
src/clipper/CMakeFiles/clipper.dir/build: src/clipper/libclipper.a
.PHONY : src/clipper/CMakeFiles/clipper.dir/build

src/clipper/CMakeFiles/clipper.dir/clean:
	cd /home/ryan/PrusaSlicer/build/src/clipper && $(CMAKE_COMMAND) -P CMakeFiles/clipper.dir/cmake_clean.cmake
.PHONY : src/clipper/CMakeFiles/clipper.dir/clean

src/clipper/CMakeFiles/clipper.dir/depend:
	cd /home/ryan/PrusaSlicer/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/ryan/PrusaSlicer /home/ryan/PrusaSlicer/src/clipper /home/ryan/PrusaSlicer/build /home/ryan/PrusaSlicer/build/src/clipper /home/ryan/PrusaSlicer/build/src/clipper/CMakeFiles/clipper.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : src/clipper/CMakeFiles/clipper.dir/depend

