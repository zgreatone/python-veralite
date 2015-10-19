#!/usr/bin/python
# -*- coding:utf-8 -*-

# Native modules
import sys
import os.path

test_dir = os.path.abspath(os.path.join(__file__, os.pardir))
module_dir = os.path.join(os.path.abspath(os.path.join(test_dir, os.pardir)), 'veralite')
sys.path.append(test_dir)
sys.path.append(module_dir)
