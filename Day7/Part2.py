#!/usr/bin/env python3

from __future__ import annotations
import sys
from dataclasses import dataclass, field
from typing import Union
from collections import deque

@dataclass
class FileSystem:

    @dataclass
    class Directory:
        name: str
        parent: Union[FileSystem.Directory, None]
        sub_dirs: dict[str,FileSystem.Directory] = field(default_factory=dict)
        files: dict[str,FileSystem.File] = field(default_factory=dict)

    @dataclass
    class File:
        name: str
        size: int

    # the name "/" is redundant
    root = Directory(name="/", parent=None)


# returns the first file/directory name/size terminated by \n or SPACE in the given string
# if the field is terminated by a space, return the (relative) index after the space
# index is for use with file listings from ls command
def get_field(input: str) -> tuple[str, Union[int, None]]:

    field = ''
    index = None

    for i, c in enumerate(input):
        if c == '\n':
            break
        if c == ' ':
            index = i + 1
            break
        field += c

    if len(field) < 1:
        print("No Name given. Exiting...")
        sys.exit(1)

    return (field, index)


# add the directories and files to the file system
# until a new command is found in ls_contents
# returns the (relative to ls_contents) index behind the next command
def process_ls_output(cur_dir: FileSystem.Directory, ls_outputs: list[str]) -> int:

    for index, output in enumerate(ls_outputs):

        # end of ls output
        if output[0] == '$':
            return index

        # ls command was the last command, return -1 to notify the command handler
        if output[0] == '':
            break

        # directory listing
        if output[0:4] == 'dir ':
            dir, _ = get_field(output[4:])
            if dir not in cur_dir.sub_dirs:
                cur_dir.sub_dirs[dir] = FileSystem.Directory(name=dir, parent=cur_dir)

        # file listing, if for some reason the file is updated after seeing it the first time
        # the file in the fs is still updated
        elif output[0].isnumeric():
            file_size, name_index = get_field(output)
            if name_index is None:
                print(f"The ls listing {output} contains no file name. Exiting...")
                sys.exit(1)
            if not file_size.isnumeric():
                print(f"The ls listing {output} contains an invalid file size. Exiting...")
                sys.exit(1)
            file_size = int(file_size)
            file_name, _ = get_field(output[name_index:])
            new_file = FileSystem.File(name=file_name, size=file_size)
            cur_dir.files[file_name] = new_file

        else:
            print(f"The ls listing {output} Is invalid. Exiting...")
            sys.exit(1)

    return -1


# processes the given commands and returns the resulting file system
def build_fs_from_commands(commands: list[str]) -> FileSystem:

    fs = FileSystem()
    cur_dir: FileSystem.Directory = fs.root

    i = 0
    while i < len(commands):

        if commands[i][0:2] != '$ ':
            print(f"Invalid command \"{commands[i]}\". Exiting...")
            sys.exit(1)

        # cd commands
        if commands[i][2:5] == 'cd ':

            # cd to root
            if commands[i][5:] == '/\n':
                cur_dir = fs.root

            # cd to parent
            elif commands[i][5:] == '..\n':
                if cur_dir.parent is not None:
                    cur_dir = cur_dir.parent
                else:
                    print(f"Cannot go to parent directory, current directory is root. Exiting...")
                    sys.exit(1)

            # cd to relative folder
            else:
                dir, _ = get_field(commands[i][5:])

                # cd to directory, creating if it doesn't exit
                if dir not in cur_dir.sub_dirs:
                    cur_dir.sub_dirs[dir] = FileSystem.Directory(name=dir, parent=cur_dir)
                cur_dir = cur_dir.sub_dirs[dir]

        # ls commands
        elif commands[i][2:] == 'ls\n':
            temp_i = process_ls_output(cur_dir, commands[i+1:])
            # end of commands
            if temp_i == -1:
                break
            i += temp_i

        else:
            print(f"Invalid command \"{commands[i]}\". Exiting...")
            sys.exit(1)

        i += 1

    return fs


# explore the given directory to find all sub directories with size no larger
# than 100000, and return the bounded/total sum of these directory sizes
# recursivly traverses in post order
# also returns a deque of unsorted directory sizes (for part 2)
def calculate_dir_sum(dir: FileSystem.Directory,
                      dir_sizes: Union[deque,None]=None) \
                      -> tuple[int, int, deque]:

    if dir_sizes is None:
        dir_sizes = deque()


    # sum of all directories with size less than 100000
    overall_sum = 0
    # sum of all directories and files, unbounded
    dir_sum = 0

    # get sum of sizes of sub directories
    for sub_dir in dir.sub_dirs.values():
        o, d, _ = calculate_dir_sum(sub_dir, dir_sizes)
        overall_sum += o
        dir_sum += d

    # get sum of file sizes
    for file in dir.files.values():
        dir_sum += file.size

    dir_sizes.append(dir_sum)

    if dir_sum <= 100000:
        overall_sum += dir_sum

    return (overall_sum, dir_sum, dir_sizes)


# returns the smallest directory size in the given stack that is at least as
# big as min_size
def find_min_dir_size(dir_sizes: deque, min_size) -> int:

    # default value is the total disk space of the device
    smallest_found = 70000000

    for size in dir_sizes:
        if size >= min_size and size < smallest_found:
            smallest_found = size
            # skip the rest of the stack if we found the smallest possible size
            if smallest_found == min_size:
                break

    return smallest_found


def main():

    # get filename
    if len(sys.argv) != 2:
        print("Incorrect number of inputs. Please enter a filename.")
        sys.exit(1)
    filename = sys.argv[1]

    lines: list[str]

    # read in input file as list of str lines
    try:
        with open(filename) as file:
            # the sublist index removes the always empty last line
            lines = file.readlines()
    except :
        print(f"Error trying to open {filename}. Exiting")
        sys.exit(1)

    fs = build_fs_from_commands(lines)
    answer,total_usage, dir_sizes = calculate_dir_sum(fs.root)

    print(answer)
    min_deletion_size = total_usage - 40000000
    print(find_min_dir_size(dir_sizes, min_deletion_size))


if __name__ == '__main__':
    main()
