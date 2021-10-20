#!/usr/bin/env python
# coding=utf-8
'''
@auhor: gyl
@file: .py
@data: 2021/10/20 
@desc:
'''
# import lib

import sys
from mach_lear.fashionmnist import fashionmnist
file1=sys.argv[1]
file2=sys.argv[2]
file3 = sys.argv[3]
file4 = sys.argv[4]

if __name__ == '__main__':
	fashionmnist(file1, file2, file3, file4)

