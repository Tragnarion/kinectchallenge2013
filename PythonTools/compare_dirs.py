#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ####################################################################
#  Copyright (C) 2013 Tragnarion Studios
#  http://www.tragnarion.com
#
#  Author: Moritz Wundke
# ####################################################################
import sys, os

def walk_dir(dir):
    for f in os.listdir(dir):
        fullpath = os.path.join(dir,f)
        if os.path.isdir(fullpath) and not os.path.islink(fullpath):
            for x in walk_dir(fullpath):
                yield x
        else:
            yield fullpath

def compare_dirs(dir1, dir2):
    for file1 in walk_dir(dir1):
        file1_base = os.path.basename(file1).lower()
        for file2 in walk_dir(dir2):
            file2_base = os.path.basename(file2).lower()
            if file1_base == file2_base:
                print("Duplicated file found: %s\n - %s\n - %s"%(file1_base, file1, file2))

def main(argv):
    if len(argv) < 2:
        sys.exit('Usage: python compare_dirs.py </path/to/dir1> </path/to/dir2>')

    if not os.path.exists(argv[0]):
        sys.exit('</path/to/dir1> does not exists!')

    if not os.path.exists(argv[1]):
        sys.exit('</path/to/dir2> does not exists!')

    if argv[0].lower() == argv[1].lower():
        sys.exit('Paths provided should be different')

    compare_dirs(argv[0], argv[1])

if __name__ == '__main__':
    main(sys.argv[1:])